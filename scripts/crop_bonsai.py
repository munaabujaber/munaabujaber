"""Crop the transparent canvas around every frame of the bonsai growth GIF."""

from pathlib import Path
import sys

from PIL import Image, ImageSequence


def crop_bonsai(source_path: Path, output_path: Path) -> None:
    with Image.open(source_path) as source:
        frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(source)]
        durations = [frame.info.get("duration", 100) for frame in ImageSequence.Iterator(source)]
        loop = source.info.get("loop", 0)

    bounds = [frame.getchannel("A").getbbox() for frame in frames]
    bounds = [box for box in bounds if box is not None]
    if not bounds:
        raise ValueError("Bonsai GIF contains no visible pixels")

    padding = 8
    box = (
        max(0, min(bound[0] for bound in bounds) - padding),
        max(0, min(bound[1] for bound in bounds) - padding),
        min(frames[0].width, max(bound[2] for bound in bounds) + padding),
        min(frames[0].height, max(bound[3] for bound in bounds) + padding),
    )
    cropped = [frame.crop(box) for frame in frames]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cropped[0].save(
        output_path,
        save_all=True,
        append_images=cropped[1:],
        duration=durations,
        loop=loop,
        disposal=2,
    )


if __name__ == "__main__":
    crop_bonsai(Path(sys.argv[1]), Path(sys.argv[2]))
