"""Unit tests for the TikTok scraper parser module."""

from ube_craze_nlp.scraper.parser import (
    extract_rehydration_data,
    parse_comments_payload,
    parse_video_details,
)


def test_extract_rehydration_data():
    """Test extracting JSON from rehydration script tag."""
    mock_html = """
    <html>
        <body>
            <script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">
                {
                    "__DEFAULT_SCOPE__": {
                        "webapp.video-detail": {
                            "itemInfo": {
                                "itemStruct": {
                                    "id": "12345"
                                }
                            }
                        }
                    }
                }
            </script>
        </body>
    </html>
    """
    data = extract_rehydration_data(mock_html)
    assert data != {}
    assert (
        data.get("__DEFAULT_SCOPE__", {})
        .get("webapp.video-detail", {})
        .get("itemInfo", {})
        .get("itemStruct", {})
        .get("id")
        == "12345"
    )


def test_parse_video_details():
    """Test parsing video details from rehydration data dict."""
    mock_rehydration = {
        "__DEFAULT_SCOPE__": {
            "webapp.video-detail": {
                "itemInfo": {
                    "itemStruct": {
                        "id": "738291038",
                        "author": {"uniqueId": "filipinofoodie"},
                        "desc": "Traditional ube halaya recipe #ube #filipinofood",
                        "createTime": 1719736800,  # 2024-06-30 UTC
                        "video": {
                            "duration": 60,
                            "playAddr": "https://example.com/video.mp4",
                        },
                        "stats": {
                            "playCount": 150000,
                            "diggCount": 23000,
                            "commentCount": 420,
                            "shareCount": 1200,
                            "downloadCount": 350,
                        },
                    }
                }
            }
        }
    }
    url = "https://www.tiktok.com/@filipinofoodie/video/738291038"
    details = parse_video_details(mock_rehydration, url)

    assert details["video_id"] == "738291038"
    assert details["author"] == "filipinofoodie"
    assert details["desc"] == "Traditional ube halaya recipe #ube #filipinofood"
    assert details["duration"] == 60
    assert details["play_addr"] == "https://example.com/video.mp4"
    assert details["play_count"] == 150000
    assert details["digg_count"] == 23000
    assert details["comment_count"] == 420
    assert details["share_count"] == 1200
    assert details["download_count"] == 350
    assert details["create_time"] == "2024-06-30 08:40:00"  # 1719736800 epoch in UTC


def test_parse_comments_payload():
    """Test parsing comments JSON payload with nested reply structures."""
    mock_payload = {
        "comments": [
            {
                "cid": "c001",
                "text": "This is a top-level comment",
                "digg_count": 85,
                "create_time": 1719737000,
                "user": {"unique_id": "commenter1", "nickname": "Commenter One"},
                "reply_comment": [
                    {
                        "cid": "c001_r01",
                        "text": "First reply to commenter1",
                        "digg_count": 10,
                        "create_time": 1719737100,
                        "user": {"unique_id": "replier1", "nickname": "Replier One"},
                    }
                ],
            },
            {
                "cid": "c002",
                "text": "Another top-level comment",
                "digg_count": 140,
                "create_time": 1719737200,
                "user": {"unique_id": "commenter2", "nickname": "Commenter Two"},
                "reply_id": "0",
            },
        ]
    }

    parsed = parse_comments_payload(mock_payload)

    # Total comments: 2 top-level + 1 reply = 3 comments
    assert len(parsed) == 3

    # Verify first comment
    assert parsed[0]["comment_id"] == "c001"
    assert parsed[0]["text"] == "This is a top-level comment"
    assert parsed[0]["username"] == "commenter1"
    assert parsed[0]["likes"] == 85
    assert not parsed[0]["is_reply"]

    # Verify nested reply
    assert parsed[1]["comment_id"] == "c001_r01"
    assert parsed[1]["text"] == "First reply to commenter1"
    assert parsed[1]["username"] == "replier1"
    assert parsed[1]["likes"] == 10
    assert parsed[1]["is_reply"]
    assert parsed[1]["reply_to_comment_id"] == "c001"
    assert parsed[1]["reply_to_user"] == "commenter1"

    # Verify second top-level comment
    assert parsed[2]["comment_id"] == "c002"
    assert parsed[2]["text"] == "Another top-level comment"
    assert parsed[2]["username"] == "commenter2"
    assert not parsed[2]["is_reply"]
