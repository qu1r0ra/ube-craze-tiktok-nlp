"""Batch script to upscale all raw TikTok videos to 1080p HD (1080x1920)."""

import logging
import sys
from pathlib import Path

from ube_craze_nlp.utils import upscale_video
from ube_craze_nlp.utils.paths import VIDS_1080P_DIR, VIDS_DIR, ensure_dirs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Upscale all MP4 videos in VIDS_DIR to 1080x1920 in VIDS_1080P_DIR."""
    ensure_dirs()

    if not VIDS_DIR.exists():
        logger.error(f"Input video directory does not exist: {VIDS_DIR}")
        sys.exit(1)

    video_files = sorted(list(VIDS_DIR.glob("*.mp4")))
    total_count = len(video_files)

    if total_count == 0:
        logger.warning(f"No MP4 video files found in {VIDS_DIR}")
        return

    logger.info(f"Starting batch 1080p upscaling for {total_count} videos...")
    logger.info(f"Source: {VIDS_DIR}")
    logger.info(f"Target: {VIDS_1080P_DIR}")

    successful = 0
    skipped = 0
    failed = 0

    for idx, video_path in enumerate(video_files, 1):
        output_path = VIDS_1080P_DIR / video_path.name
        if output_path.exists():
            logger.info(f"[{idx}/{total_count}] Skipped existing: {video_path.name}")
            skipped += 1
            continue

        logger.info(f"[{idx}/{total_count}] Upscaling: {video_path.name}")
        success = upscale_video(
            input_path=video_path,
            output_path=output_path,
            width=1080,
            height=1920,
            overwrite=False,
        )

        if success:
            successful += 1
        else:
            failed += 1

    logger.info("=" * 60)
    logger.info("Batch upscaling execution completed!")
    logger.info(
        f"Total: {total_count} | New Upscaled: {successful} | Skipped: {skipped} | Failed: {failed}"
    )
    logger.info("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
