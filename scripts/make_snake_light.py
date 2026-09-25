"""Make a light-theme copy of the generated contribution snake SVG."""

import argparse
import re
from pathlib import Path


# The action's green theme uses a dark contribution palette. Recolor the
# generated SVG, including its animation keyframes, for a light background.
LIGHT_COLORS = {
    "#161b22": "#ebedf0",  # empty tiles
    "#0e4429": "#9be9a8",
    "#006d32": "#40c463",
    "#26a641": "#30a14e",
    "#39d353": "#216e39",
    "#8affc1": "#1a7f37",  # near the snake's head
    "#b7ffd0": "#0e4429",  # snake head
    "#7d8590": "#57606a",  # labels
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    svg = args.source.read_text(encoding="utf-8")
    colors = set(re.findall(r"#[0-9a-fA-F]{6}\b", svg))
    unknown = colors - LIGHT_COLORS.keys()
    if unknown:
        parser.error(f"unexpected snake colors: {', '.join(sorted(unknown))}")

    light_svg = re.sub(
        r"#[0-9a-fA-F]{6}\b",
        lambda match: LIGHT_COLORS[match.group()],
        svg,
    )
    args.destination.write_text(light_svg, encoding="utf-8")


if __name__ == "__main__":
    main()
