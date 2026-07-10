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


def test_extract_rehydration_data_no_script():
    """Test extracting JSON when script tag is missing."""
    mock_html = "<html><body><h1>No data here</h1></body></html>"
    data = extract_rehydration_data(mock_html)
    assert data == {}


def test_parse_video_details(mock_rehydration_data):
    """Test parsing video details from rehydration data dict."""
    url = "https://www.tiktok.com/@filipinofoodie/video/738291038"
    details = parse_video_details(mock_rehydration_data, url)

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
    assert details["create_time"] == "2024-06-30 08:40:00"


def test_parse_video_details_missing_scope():
    """Test parsing video details when __DEFAULT_SCOPE__ is empty."""
    url = "https://www.tiktok.com/@filipinofoodie/video/738291038"
    details = parse_video_details({}, url)
    assert details["video_id"] == "738291038"
    assert details["author"] == ""
    assert details["desc"] == ""
    assert details["create_time"] == ""


def test_parse_comments_payload(mock_comments_payload):
    """Test parsing comments JSON payload with nested reply structures."""
    parsed = parse_comments_payload(mock_comments_payload)

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


def test_parse_comments_payload_empty():
    """Test parsing comments when payload is empty."""
    assert parse_comments_payload({}) == []
    assert parse_comments_payload({"comments": []}) == []
