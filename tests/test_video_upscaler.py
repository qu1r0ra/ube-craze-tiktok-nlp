"""Unit tests for video upscaler module."""

from pathlib import Path

import cv2
import numpy as np
from ube_craze_nlp.utils.video_upscaler import upscale_video


def test_upscale_video(tmp_path: Path):
    """Test video upscaling function on a synthetic test video."""
    input_path = tmp_path / "test_input.mp4"
    output_path = tmp_path / "test_output.mp4"

    # Create a synthetic 100x200 video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(input_path), fourcc, 10.0, (100, 200))
    for _ in range(5):
        frame = np.zeros((200, 100, 3), dtype=np.uint8)
        writer.write(frame)
    writer.release()

    assert input_path.exists()

    # Run upscaler
    success = upscale_video(
        input_path=input_path,
        output_path=output_path,
        width=1080,
        height=1920,
        overwrite=True,
    )

    assert success is True
    assert output_path.exists()

    # Verify output resolution
    cap = cv2.VideoCapture(str(output_path))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    assert width == 1080
    assert height == 1920
