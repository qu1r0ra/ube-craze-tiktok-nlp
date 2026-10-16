"""Generate a public teaching example from invented material only."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = (
    "Synthetic example A: I would like to learn how this dessert is prepared.",
    "Synthetic example B: Please explain the difference between the ingredients.",
    "Synthetic example C: I disagree with that description of the dish.",
)


def main():
    destination = ROOT / "examples" / "synthetic-comments.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Synthetic teaching examples",
        "",
        "Entirely invented examples, not observed, anonymized, or paraphrased comments.",
        "They have no connection to historical sentiment percentages or cluster findings.",
        "",
        *(f"- {example}" for example in EXAMPLES),
        "",
    ]
    destination.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote synthetic examples to %s", destination)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
