import pytest


@pytest.fixture
def mock_rehydration_data():
    return {
        "__DEFAULT_SCOPE__": {
            "webapp.video-detail": {
                "itemInfo": {
                    "itemStruct": {
                        "id": "738291038",
                        "author": {"uniqueId": "filipinofoodie"},
                        "desc": "Traditional ube halaya recipe #ube #filipinofood",
                        "createTime": 1719736800,
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


@pytest.fixture
def mock_comments_payload():
    return {
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
