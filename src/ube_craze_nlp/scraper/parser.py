"""Metadata and JSON response parser for scraped TikTok data."""

import json
import re
from datetime import UTC, datetime
from typing import Any


def extract_rehydration_data(html_content: str) -> dict[str, Any]:
    """Extract __UNIVERSAL_DATA_FOR_REHYDRATION__ JSON from page HTML."""
    try:
        match = re.search(
            r'<script\s+id="__UNIVERSAL_DATA_FOR_REHYDRATION__"\s+type="application/json">(.*?)</script>',
            html_content,
            re.DOTALL,
        )
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        print(f"Error parsing rehydration script: {e}")
    return {}


def parse_video_details(rehydration_data: dict[str, Any], url: str) -> dict[str, Any]:
    """Parse video details and stats from the rehydration data JSON structure."""
    meta = {
        "video_id": "",
        "source_url": url,
        "author": "",
        "create_time": "",
        "desc": "",
        "duration": 0,
        "play_count": 0,
        "digg_count": 0,
        "comment_count": 0,
        "share_count": 0,
        "download_count": 0,
        "play_addr": "",
    }

    try:
        # Resolve video ID from URL
        video_id_match = re.search(r"/video/(\d+)", url)
        if video_id_match:
            meta["video_id"] = video_id_match.group(1)

        # Get webapp video-detail struct
        scope = rehydration_data.get("__DEFAULT_SCOPE__", {})
        item_struct = scope.get("webapp.video-detail", {}).get("itemInfo", {}).get("itemStruct")

        if not item_struct:
            # Try alternative location in JSON
            item_struct = scope.get("videoDetail", {}).get("itemInfo", {}).get("itemStruct")

        if item_struct:
            meta["video_id"] = item_struct.get("id", meta["video_id"])
            meta["author"] = item_struct.get("author", {}).get("uniqueId", "")
            meta["desc"] = item_struct.get("desc", "")
            meta["duration"] = item_struct.get("video", {}).get("duration", 0)
            meta["play_addr"] = item_struct.get("video", {}).get("playAddr", "")

            # Create Time
            create_time_ts = int(item_struct.get("createTime", 0))
            if create_time_ts > 0:
                dt = datetime.fromtimestamp(create_time_ts, UTC)
                meta["create_time"] = dt.strftime("%Y-%m-%d %H:%M:%S")

            # Stats
            stats = item_struct.get("stats", {})
            meta["play_count"] = stats.get("playCount", 0)
            meta["digg_count"] = stats.get("diggCount", 0)
            meta["comment_count"] = stats.get("commentCount", 0)
            meta["share_count"] = stats.get("shareCount", 0)
            meta["download_count"] = stats.get("downloadCount", 0)

    except Exception as e:
        print(f"Error parsing rehydration video details: {e}")

    return meta


def parse_comments_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse comments and nested replies from a single intercepted TikTok API payload."""
    parsed_comments = []
    comments_list = payload.get("comments", [])

    if not comments_list:
        return []

    for item in comments_list:
        try:
            cid = item.get("cid", "")
            if not cid:
                continue

            text = item.get("text", "")
            likes = item.get("digg_count", 0)
            create_time_ts = int(item.get("create_time", 0))
            create_time = ""
            if create_time_ts > 0:
                dt = datetime.fromtimestamp(create_time_ts, UTC)
                create_time = dt.strftime("%Y-%m-%d %H:%M:%S")

            user = item.get("user", {})
            username = user.get("unique_id", "")
            nickname = user.get("nickname", "")

            # Top level comment fields
            reply_id = item.get("reply_id", "0")

            # Link replies to parent
            reply_to_user = ""
            reply_to_comment_id = ""

            if reply_id != "0" and reply_id != cid:
                # This is a reply
                reply_to_comment_id = reply_id
                reply_to_user = item.get("reply_to_username", "")

            parsed_comments.append(
                {
                    "comment_id": cid,
                    "username": username,
                    "nickname": nickname,
                    "text": text,
                    "likes": likes,
                    "create_time": create_time,
                    "reply_to_comment_id": reply_to_comment_id,
                    "reply_to_user": reply_to_user,
                    "is_reply": bool(reply_to_comment_id),
                }
            )

            # Check for inline reply comments (sometimes returned with the parent)
            inline_replies = item.get("reply_comment", []) or []
            for sub_item in inline_replies:
                sub_cid = sub_item.get("cid", "")
                if not sub_cid:
                    continue

                sub_text = sub_item.get("text", "")
                sub_likes = sub_item.get("digg_count", 0)
                sub_create_time_ts = int(sub_item.get("create_time", 0))
                sub_create_time = ""
                if sub_create_time_ts > 0:
                    sub_dt = datetime.fromtimestamp(sub_create_time_ts, UTC)
                    sub_create_time = sub_dt.strftime("%Y-%m-%d %H:%M:%S")

                sub_user = sub_item.get("user", {})
                sub_username = sub_user.get("unique_id", "")
                sub_nickname = sub_user.get("nickname", "")

                parsed_comments.append(
                    {
                        "comment_id": sub_cid,
                        "username": sub_username,
                        "nickname": sub_nickname,
                        "text": sub_text,
                        "likes": sub_likes,
                        "create_time": sub_create_time,
                        "reply_to_comment_id": cid,
                        "reply_to_user": username,
                        "is_reply": True,
                    }
                )

        except Exception as e:
            print(f"Error parsing individual comment item: {e}")

    return parsed_comments
