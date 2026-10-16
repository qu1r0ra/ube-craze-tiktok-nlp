"""Metadata and JSON response parser for scraped TikTok data."""

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


def _deep_get(d: dict, *keys, default=None):
    for key in keys[:-1]:
        if not isinstance(d, dict):
            return default
        d = d.get(key, {})
    if not isinstance(d, dict):
        return default
    return d.get(keys[-1], default)


def _format_timestamp(epoch: int) -> str:
    if epoch > 0:
        dt = datetime.fromtimestamp(epoch, UTC)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return ""


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
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        logger.error(f"Error parsing rehydration script: {e}")
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
        item_struct = _deep_get(scope, "webapp.video-detail", "itemInfo", "itemStruct")

        if not item_struct:
            # Try alternative location in JSON
            item_struct = _deep_get(scope, "videoDetail", "itemInfo", "itemStruct")

        if item_struct:
            meta["video_id"] = item_struct.get("id", meta["video_id"])
            meta["author"] = item_struct.get("author", {}).get("uniqueId", "")
            meta["desc"] = item_struct.get("desc", "")
            meta["duration"] = item_struct.get("video", {}).get("duration", 0)

            # Extract highest bitrate/resolution HD 1080p stream from bitrateInfo or downloadAddr
            video_data = item_struct.get("video", {})
            best_play_addr = ""

            bitrate_info = video_data.get("bitrateInfo", [])
            if isinstance(bitrate_info, list) and bitrate_info:
                # Sort streams by Bitrate and resolution descending
                sorted_streams = sorted(
                    bitrate_info,
                    key=lambda s: (
                        s.get("Bitrate", 0) if isinstance(s, dict) else 0,
                        (
                            (s.get("Width", 0) or 0) * (s.get("Height", 0) or 0)
                            if isinstance(s, dict)
                            else 0
                        ),
                    ),
                    reverse=True,
                )
                for stream in sorted_streams:
                    if isinstance(stream, dict):
                        play_addr_obj = stream.get("PlayAddr", {})
                        if isinstance(play_addr_obj, dict):
                            url_list = play_addr_obj.get("UrlList", [])
                            if url_list and isinstance(url_list, list) and url_list[0]:
                                best_play_addr = url_list[0]
                                break
                        elif isinstance(play_addr_obj, str) and play_addr_obj:
                            best_play_addr = play_addr_obj
                            break

            if not best_play_addr:
                best_play_addr = video_data.get("downloadAddr", "") or video_data.get(
                    "playAddr", ""
                )

            meta["play_addr"] = best_play_addr

            # Create Time
            create_time_ts = int(item_struct.get("createTime", 0))
            meta["create_time"] = _format_timestamp(create_time_ts)

            # Stats
            stats = item_struct.get("stats", {})
            meta["play_count"] = stats.get("playCount", 0)
            meta["digg_count"] = stats.get("diggCount", 0)
            meta["comment_count"] = stats.get("commentCount", 0)
            meta["share_count"] = stats.get("shareCount", 0)
            meta["download_count"] = stats.get("downloadCount", 0)

    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        logger.error(f"Error parsing rehydration video details: {e}")

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
            create_time = _format_timestamp(create_time_ts)

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
                sub_create_time = _format_timestamp(sub_create_time_ts)

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

        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing individual comment item: {e}")

    return parsed_comments
