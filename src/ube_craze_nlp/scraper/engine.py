"""TikTok Scraper Engine using Playwright with Network Interception."""

import asyncio
import json
import random
import re
from pathlib import Path
from typing import Any

import requests
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

from ube_craze_nlp.scraper.parser import (
    extract_rehydration_data,
    parse_comments_payload,
    parse_video_details,
)
from ube_craze_nlp.utils.paths import LINKS_FILE, RAW_DATA_DIR, ensure_dirs


class TikTokScraperEngine:
    def __init__(self, headless: bool = False, delay_range: tuple = (1.5, 3.5)):
        self.headless = headless
        self.delay_range = delay_range
        ensure_dirs()

    def random_sleep(self, min_sec: float = None, max_sec: float = None):
        """Sleep for a random duration to mimic human behavior."""
        low = min_sec if min_sec is not None else self.delay_range[0]
        high = max_sec if max_sec is not None else self.delay_range[1]
        time_to_sleep = random.uniform(low, high)
        return asyncio.sleep(time_to_sleep)

    async def download_video(
        self, play_url: str, save_path: Path, cookies: dict[str, str], user_agent: str
    ) -> bool:
        """Download MP4 video stream using Playwright session headers and cookies."""
        if not play_url:
            return False
        try:
            session = requests.Session()
            session.headers.update(
                {
                    "User-Agent": user_agent,
                    "Referer": "https://www.tiktok.com/",
                    "Accept-Encoding": "identity",
                }
            )
            for name, value in cookies.items():
                session.cookies.set(name, value, domain=".tiktok.com")

            response = session.get(play_url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                return True
            else:
                print(f"⚠️ Video download failed: HTTP Status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error downloading video: {e}")
        return False

    async def scrape_video(self, url: str) -> dict[str, Any]:
        """Scrape a single TikTok video metadata, comments, and replies."""
        print(f"\n🚀 Initiating scrape for URL: {url}")

        video_id = ""
        video_id_match = re.search(r"/video/(\d+)", url)
        if video_id_match:
            video_id = video_id_match.group(1)

        if not video_id:
            print("❌ Invalid TikTok Video URL (could not extract Video ID).")
            return {"status": "failed", "error": "Invalid URL"}

        # Store intercepted comment API payloads
        intercepted_comment_payloads: list[dict[str, Any]] = []
        unique_cids: set[str] = set()

        async with async_playwright() as p:
            # Launch Chromium browser with stealth settings
            browser = await p.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--window-size=1280,720",
                ],
            )

            # Create context with custom user agent
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            context = await browser.new_context(
                user_agent=user_agent,
                viewport={"width": 1280, "height": 720},
            )

            page = await context.new_page()
            await stealth_async(page)

            # Network Interception handler
            async def handle_response(response):
                if "/api/comment/list/" in response.url:
                    try:
                        content_type = response.headers.get("content-type", "")
                        if "application/json" in content_type:
                            data = await response.json()
                            intercepted_comment_payloads.append(data)

                            # Track unique top-level comments to determine when to stop scrolling
                            parsed = parse_comments_payload(data)
                            for c in parsed:
                                if not c["is_reply"]:
                                    unique_cids.add(c["comment_id"])
                    except Exception:
                        # Fail silently for parsing errors on incomplete payloads
                        pass

            page.on("response", handle_response)

            # Navigate to TikTok video
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print(f"⚠️ Page navigation warning (timeout/incomplete): {e}")

            await self.random_sleep(3, 5)

            # Parse video details from page rehydration script
            html_content = await page.content()
            rehydration_data = extract_rehydration_data(html_content)
            video_meta = parse_video_details(rehydration_data, url)

            # Resolve author name
            author = video_meta.get("author") or "unknown"
            print(f"🎥 Video Author: @{author}")
            print(f"💬 Expected Comment Count: {video_meta.get('comment_count', 0)}")

            # Scrape top-level comments by scrolling
            print("⏳ Loading comments...")
            stuck_count = 0
            last_comment_len = 0
            max_scroll_attempts = 80  # Safety net limit

            # Target 100 comments (or less if the video doesn't have that many)
            target_comments = min(100, video_meta.get("comment_count", 100))

            for attempt in range(max_scroll_attempts):
                # Count current unique top-level comments
                current_top_level = len(
                    [
                        c
                        for payload in intercepted_comment_payloads
                        for c in parse_comments_payload(payload)
                        if not c["is_reply"]
                    ]
                )

                print(f"   Collected top-level comments: {current_top_level}/{target_comments}")

                if current_top_level >= target_comments and target_comments > 0:
                    print("   ✅ Target count of top-level comments reached.")
                    break

                # Scroll comment container or body
                await page.evaluate(
                    """
                    const container = document.querySelector('[data-e2e="comment-list"]') ||
                                      document.querySelector(
                                          'div[class*="CommentListContainer"]'
                                      ) ||
                                      document.querySelector(
                                          'div[class*="DivCommentListContainer"]'
                                      );
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    } else {
                        window.scrollTo(0, document.body.scrollHeight);
                    }
                """
                )

                await self.random_sleep(1.5, 3.0)

                # Check if stuck
                if len(unique_cids) == last_comment_len:
                    stuck_count += 1
                    if stuck_count >= 15:
                        print("   ✅ Scraped all available comments (reached end of feed).")
                        break
                else:
                    stuck_count = 0

                last_comment_len = len(unique_cids)

            # Expand reply threads
            print("🔄 Expanding replies (View replies)...")
            # We run this in a loop to click the reply buttons multiple times as they appear
            max_reply_passes = 10
            for pass_idx in range(max_reply_passes):
                clicked = await page.evaluate(
                    """
                    () => {
                        let buttons = Array.from(document.querySelectorAll('div, p, span, button'))
                            .filter(el => {
                                const text = el.innerText || el.textContent || '';
                                return text.trim().toLowerCase().match(
                                    /^(view\\s+\\d+\\s+replies|view\\s+replies|view\\s+more\\s+replies|view\\s+more)$/i
                                );
                            });
                        buttons.forEach(btn => {
                            btn.scrollIntoView({block: "center", behavior: "instant"});
                            btn.click();
                        });
                        return buttons.length;
                    }
                """
                )
                print(f"   Pass {pass_idx + 1}: Clicked {clicked} reply expand buttons.")
                if clicked == 0:
                    break
                await self.random_sleep(2.0, 3.5)

            # Get cookies and user-agent for downloading video MP4
            playwright_cookies = await context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in playwright_cookies}

            # Setup directory structure
            video_folder = RAW_DATA_DIR / f"{author}_{video_id}"
            video_folder.mkdir(parents=True, exist_ok=True)

            # Save raw intercepted payloads
            raw_payloads_path = video_folder / "comments_raw.json"
            with open(raw_payloads_path, "w", encoding="utf-8") as f:
                json.dump(intercepted_comment_payloads, f, indent=2, ensure_ascii=False)

            # Save parsed metadata
            metadata_path = video_folder / "metadata.json"
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(video_meta, f, indent=2, ensure_ascii=False)

            # Download MP4 Video file
            play_addr = video_meta.get("play_addr")
            video_downloaded = False
            if play_addr:
                print("⬇️ Downloading video MP4...")
                mp4_path = video_folder / f"{video_id}.mp4"
                video_downloaded = await self.download_video(
                    play_addr, mp4_path, cookie_dict, user_agent
                )
                if video_downloaded:
                    print(f"   ✅ Saved MP4: {mp4_path}")

            # Shutdown browser
            await context.close()
            await browser.close()

        print(f"🎉 Completed scraping for video {video_id}!")
        return {
            "status": "success",
            "video_id": video_id,
            "author": author,
            "comments_count": len(unique_cids),
            "video_downloaded": video_downloaded,
            "folder": str(video_folder),
        }


def read_video_urls() -> list[str]:
    """Read target TikTok URLs from links.txt file."""
    urls = []
    if not LINKS_FILE.exists():
        print(f"⚠️ {LINKS_FILE} not found. Creating empty file...")
        with open(LINKS_FILE, "w") as f:
            f.write("# Paste TikTok URLs here\n")
        return []

    with open(LINKS_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


async def main():
    """Main execution block to scrape all links."""
    urls = read_video_urls()
    if not urls:
        print("❌ No URLs found in links.txt. Add URLs and try again.")
        return

    print(f"📋 Loaded {len(urls)} URLs from links.txt.")
    engine = TikTokScraperEngine(headless=False)

    for i, url in enumerate(urls, 1):
        print(f"\n--- Progress: [{i}/{len(urls)}] ---")
        try:
            result = await engine.scrape_video(url)
            print(f"Result: {result}")
            # Dynamic sleep between videos to prevent IP banning
            await engine.random_sleep(5.0, 10.0)
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
