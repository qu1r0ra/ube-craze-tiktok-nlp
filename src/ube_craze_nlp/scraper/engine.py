"""TikTok Scraper Engine using Playwright with Network Interception."""

import asyncio
import json
import logging
import random
import re
from pathlib import Path
from typing import Any

import requests
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from ube_craze_nlp.scraper.parser import (
    extract_rehydration_data,
    parse_comments_payload,
    parse_video_details,
)
from ube_craze_nlp.utils.paths import LINKS_FILE, RAW_DATA_DIR, ensure_dirs

logger = logging.getLogger(__name__)


class TikTokScraperEngine:
    MAX_SCROLL_ATTEMPTS = 80
    STUCK_THRESHOLD = 15
    MAX_REPLY_PASSES = 10
    TARGET_COMMENTS_CAP = 100
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self, headless: bool = False, delay_range: tuple[float, float] = (1.5, 3.5)):
        self.headless = headless
        self.delay_range = delay_range
        ensure_dirs()

    async def random_sleep(
        self, min_sec: float | None = None, max_sec: float | None = None
    ) -> None:
        """Sleep for a random duration to mimic human behavior."""
        low = min_sec if min_sec is not None else self.delay_range[0]
        high = max_sec if max_sec is not None else self.delay_range[1]
        time_to_sleep = random.uniform(low, high)
        await asyncio.sleep(time_to_sleep)

    def _download_sync(
        self, play_url: str, save_path: Path, cookies: dict[str, str], user_agent: str
    ) -> bool:
        """Download MP4 video stream synchronously using Playwright session headers and cookies."""
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
            logger.warning(f"Video download failed: HTTP Status {response.status_code}")
        except requests.RequestException as e:
            logger.warning(f"Warning: Error downloading video: {e}")
        return False

    async def download_video(
        self, play_url: str, save_path: Path, cookies: dict[str, str], user_agent: str
    ) -> bool:
        """Download MP4 video stream using Playwright session headers and cookies."""
        return await asyncio.to_thread(
            self._download_sync, play_url, save_path, cookies, user_agent
        )

    async def _launch_context(self, p):
        browser = await p.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--window-size=1280,720",
            ],
        )
        context = await browser.new_context(
            user_agent=self.DEFAULT_USER_AGENT,
            viewport={"width": 1280, "height": 720},
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        return browser, context, page

    async def _click_comments_tab(self, page):
        from playwright.async_api import Error as PlaywrightError

        try:
            comments_tab = await page.evaluate(
                """
                () => {
                    const span = Array.from(document.querySelectorAll('span'))
                        .find(el => el.textContent.trim().toLowerCase() === 'comments');
                    if (span) {
                        const button = span.closest('button');
                        if (button) {
                            button.click();
                            return true;
                        }
                    }
                    return false;
                }
                """
            )
            if comments_tab:
                logger.info("Clicked Comments tab button to load comments section.")
                await self.random_sleep(2.0, 3.5)
            else:
                logger.info("Comments tab button not found (comments might be loaded directly).")
        except PlaywrightError as e:
            logger.error(f"Error clicking Comments tab: {e}")

    async def _scroll_for_comments(self, page, target, unique_cids):
        stuck_count = 0
        last_comment_len = 0

        for _attempt in range(self.MAX_SCROLL_ATTEMPTS):
            current_top_level = len(unique_cids)
            logger.info(f"   Collected top-level comments: {current_top_level}/{target}")

            if current_top_level >= target and target > 0:
                logger.info("   Target count of top-level comments reached.")
                break

            await page.evaluate(
                """
                () => {
                    const selectors = [
                        '[data-e2e="comment-list"]',
                        'div[class*="CommentMain"]',
                        'div[class*="DivCommentMain"]',
                        'div[class*="CommentListContainer"]',
                        'div[class*="DivCommentListContainer"]'
                    ];
                    let container = null;
                    for (const sel of selectors) {
                        const el = document.querySelector(sel);
                        if (el) {
                            const style = window.getComputedStyle(el);
                            const scrollY = style.overflowY;
                            const isScrollable = el.scrollHeight > el.clientHeight &&
                                (scrollY === 'auto' || scrollY === 'scroll');
                            if (isScrollable) {
                                container = el;
                                break;
                            }
                        }
                    }
                    if (!container) {
                        for (const sel of selectors) {
                            const el = document.querySelector(sel);
                            if (el) { container = el; break; }
                        }
                    }
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    } else {
                        window.scrollTo(0, document.body.scrollHeight);
                    }
                }
            """
            )

            await self.random_sleep(1.5, 3.0)

            if len(unique_cids) == last_comment_len:
                stuck_count += 1
                if stuck_count >= self.STUCK_THRESHOLD:
                    logger.info("   Scraped all available comments (reached end of feed).")
                    break
            else:
                stuck_count = 0

            last_comment_len = len(unique_cids)

    async def _expand_reply_threads(self, page):
        for pass_idx in range(self.MAX_REPLY_PASSES):
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
            logger.info(f"   Pass {pass_idx + 1}: Clicked {clicked} reply expand buttons.")
            if clicked == 0:
                break
            await self.random_sleep(2.0, 3.5)

    def _save_scrape_artifacts(
        self, video_folder: Path, payloads: list[dict[str, Any]], meta: dict[str, Any]
    ):
        video_folder.mkdir(parents=True, exist_ok=True)
        raw_payloads_path = video_folder / "comments_raw.json"
        with open(raw_payloads_path, "w", encoding="utf-8") as f:
            json.dump(payloads, f, indent=2, ensure_ascii=False)
        metadata_path = video_folder / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    async def scrape_video(self, url: str) -> dict[str, Any]:
        """Scrape a single TikTok video metadata, comments, and replies."""
        logger.info(f"\nInitiating scrape for URL: {url}")

        video_id = ""
        video_id_match = re.search(r"/video/(\d+)", url)
        if video_id_match:
            video_id = video_id_match.group(1)

        if not video_id:
            logger.error("Error: Invalid TikTok Video URL (could not extract Video ID).")
            return {"status": "failed", "error": "Invalid URL"}

        intercepted_comment_payloads: list[dict[str, Any]] = []
        unique_cids: set[str] = set()

        async with async_playwright() as p:
            browser, context, page = await self._launch_context(p)

            async def handle_response(response):
                if "/api/comment/list/" in response.url:
                    try:
                        content_type = response.headers.get("content-type", "")
                        if "application/json" in content_type:
                            data = await response.json()
                            intercepted_comment_payloads.append(data)
                            parsed = parse_comments_payload(data)
                            for c in parsed:
                                if not c["is_reply"]:
                                    unique_cids.add(c["comment_id"])
                    except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                        logger.debug("Skipping malformed payload: %s", e)

            page.on("response", handle_response)

            from playwright.async_api import Error as PlaywrightError

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            except PlaywrightError as e:
                logger.warning(f"Page navigation warning (timeout/incomplete): {e}")

            await self.random_sleep(3, 5)

            await self._click_comments_tab(page)

            html_content = await page.content()
            rehydration_data = extract_rehydration_data(html_content)
            video_meta = parse_video_details(rehydration_data, url)

            author = video_meta.get("author") or "unknown"
            logger.info(f"Video Author: @{author}")
            logger.info(f"Expected Comment Count: {video_meta.get('comment_count', 0)}")

            logger.info("Loading comments...")
            target_comments = min(
                self.TARGET_COMMENTS_CAP, video_meta.get("comment_count", self.TARGET_COMMENTS_CAP)
            )
            await self._scroll_for_comments(page, target_comments, unique_cids)

            logger.info("Expanding replies (View replies)...")
            await self._expand_reply_threads(page)

            playwright_cookies = await context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in playwright_cookies}

            video_folder = RAW_DATA_DIR / f"{author}_{video_id}"
            self._save_scrape_artifacts(video_folder, intercepted_comment_payloads, video_meta)

            play_addr = video_meta.get("play_addr")
            video_downloaded = False
            if play_addr:
                logger.info("Downloading video MP4...")
                mp4_path = video_folder / f"{video_id}.mp4"
                video_downloaded = await self.download_video(
                    play_addr, mp4_path, cookie_dict, self.DEFAULT_USER_AGENT
                )
                if video_downloaded:
                    logger.info(f"   Saved MP4: {mp4_path}")

            await context.close()
            await browser.close()

        logger.info(f"Completed scraping for video {video_id}!")
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
        logger.warning(f"Warning: {LINKS_FILE} not found. Creating empty file...")
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
        logger.error("Error: No URLs found in links.txt. Add URLs and try again.")
        return

    logger.info(f"Loaded {len(urls)} URLs from links.txt.")
    engine = TikTokScraperEngine(headless=True)

    for i, url in enumerate(urls, 1):
        logger.info(f"\n--- Progress: [{i}/{len(urls)}] ---")
        try:
            result = await engine.scrape_video(url)
            logger.info(f"Result: {result}")
            # Dynamic sleep between videos to prevent IP banning
            await engine.random_sleep(5.0, 10.0)
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
