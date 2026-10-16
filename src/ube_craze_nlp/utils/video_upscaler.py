"""Video upscaling utilities using FFmpeg Lanczos scaling and detail enhancement."""

import logging
import subprocess
from pathlib import Path

import imageio_ffmpeg

logger = logging.getLogger(__name__)


def upscale_video(
    input_path: Path | str,
    output_path: Path | str,
    width: int = 1080,
    height: int = 1920,
    overwrite: bool = False,
) -> bool:
    """Upscale video to target resolution (default 1080x1920) using Lanczos scaling and unsharp filter.

    Args:
        input_path: Path to source video file.
        output_path: Path to save upscaled video file.
        width: Target width in pixels (default 1080).
        height: Target height in pixels (default 1920).
        overwrite: Whether to overwrite target file if it already exists.

    Returns:
        True if upscaling completed successfully, False otherwise.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        logger.error(f"Input file does not exist: {input_path}")
        return False

    if output_path.exists() and not overwrite:
        logger.info(f"Output file already exists, skipping: {output_path}")
        return True

    output_path.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    vf_filter = (
        f"scale={width}:{height}:flags=lanczos,"
        "unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=1.0:"
        "chroma_msize_x=5:chroma_msize_y=5:chroma_amount=0.0"
    )

    cmd = [
        ffmpeg_exe,
        "-y" if overwrite else "-n",
        "-i",
        str(input_path),
        "-vf",
        vf_filter,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-c:a",
        "copy",
        str(output_path),
    ]

    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if res.returncode != 0:
            logger.error(f"FFmpeg upscaling failed for {input_path.name}: {res.stderr}")
            if output_path.exists():
                output_path.unlink()
            return False
        logger.info(
            f"Successfully upscaled {input_path.name} -> {output_path.name} ({width}x{height})"
        )
        return True
    except Exception as e:
        logger.error(f"Unexpected error during upscaling {input_path.name}: {e}")
        if output_path.exists():
            output_path.unlink()
        return False
