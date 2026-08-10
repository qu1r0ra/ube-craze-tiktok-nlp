"""Build the upload-ready Google Drive editor-guide package."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs" / "docs" / "cluster_samples.md"
PACKAGE = ROOT / "outputs" / "editor guide"

CLUSTERS = {
    "01_appreciation": {
        "title": "Appreciation and empathy",
        "source_cluster": 2,
        "keywords": ["love seeing", "love ube", "try ube", "culture", "labor of love"],
    },
    "02_pronunciation": {
        "title": "Pronunciation as respect",
        "source_cluster": 0,
        "keywords": ["pronounced u-be", "pronounced oo-be", "pronounced ube", "pronounce", "ask them"],
    },
    "03_ube_vs_taro": {
        "title": "Ube versus taro",
        "source_cluster": 5,
        "keywords": ["taro and ube", "not taro", "same taste", "vanilla", "different"],
    },
    "04_oob_backlash": {
        "title": "Oob backlash and memes",
        "source_cluster": 3,
        "keywords": ["oob", "wtf", "calling", "pronounced", "ears"],
    },
    "05_matcha_fication": {
        "title": "Matcha-fication anxiety",
        "source_cluster": 4,
        "keywords": ["matcha", "gentrif", "shortage", "business", "corporate"],
    },
    "06_agriculture_and_economy": {
        "title": "Agriculture and economic consequences",
        "source_cluster": 1,
        "keywords": ["farmers", "agriculture", "expensive", "government", "supply", "middle"],
    },
    "07_botanical_accuracy": {
        "title": "Botanical and technical accuracy",
        "source_cluster": 6,
        "keywords": ["purple yam", "sweet potato", "dioscorea", "yam", "botanical", "ube is"],
    },
}

DIVISION_COMMENTS = {
    "01_research_overview": {
        "title": "Research overview: the comment landscape",
        "must": [
            "i love seeing people enjoy mu cultrure's food",
            "We promise we did not invent Ube. Just making sure she gets the spotlight she deserves!",
            "Before this trendy wave, I already loved Ube",
            "I would love to try Ube from a Filipino place!",
            "There goes my culture",
        ],
        "support": [
            "Ube halaya is a labor of love",
            "I love Ube I am from California",
            "I have never tried Ube before! I would really love to try it!",
            "I hope the Philippines will be able to protect our Ube.",
            "All good honestly. No harm done. Let us do a quick Google search in future times.",
        ],
    },
    "02_sentiment": {
        "title": "Sentiment: mixed, not simply celebratory",
        "must": [
            "i love seeing people enjoy mu cultrure's food",
            "The Government should invest more in our agriculture",
            "It was just nice to look at but the sugar level was through the roof.",
            "I hope the Philippines will be able to protect our Ube.",
            "All good honestly. No harm done. Let us do a quick Google search in future times.",
        ],
        "support": [
            "Ube cake is SOOO good",
            "Real ube has its own taste, usually the one you taste has mixed with sweet potato",
            "I love Ube everything",
            "It makes me sad how much we are deteriorating as a country.",
            "Beautiful! Thank you",
        ],
    },
    "04_synthesis": {
        "title": "Synthesis: appreciation with responsibility",
        "must": [
            "We promise we did not invent Ube. Just making sure she gets the spotlight she deserves!",
            "It is pronounced OO-Beh. I hope it can be pronounced properly. But thank you for saying it is from the Philippines!",
            "Taro and Ube are different yam roots",
            "The Government should invest more in our agriculture",
            "we might have a shortage of ube if it truly gets popular similar to matcha",
        ],
        "support": [
            "Ube is a Filipino term which translates to yam in English.",
            "Before this trendy wave, I already loved Ube",
            "There goes my culture",
            "Everywhere always got taro but not ube",
            "One day, we hope everyone will know that ube comes from the Philippines and that it is a purple yam.",
        ],
    },
}


def ascii_text(value: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"(?i)fcking", "f***ing", value)
    value = re.sub(r"(?i)\bshit\b", "s***", value)
    value = re.sub(r"(?i)\bwtf\b", "w**", value)
    return value


def parse_source_comments() -> dict[int, list[str]]:
    text = SOURCE.read_text(encoding="utf-8")
    sections = re.split(r"^## Cluster (\d+) - .*?$", text, flags=re.MULTILINE)
    clusters: dict[int, list[str]] = {}
    for index in range(1, len(sections), 2):
        cluster_number = int(sections[index])
        body = sections[index + 1]
        comments = []
        for match in re.finditer(r"^\s*>\s*(.+?)\s*$", body, flags=re.MULTILINE):
            value = match.group(1).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            value = ascii_text(value)
            if value and value not in comments:
                comments.append(value)
        clusters[cluster_number] = comments
    return clusters


def choose_comments(comments: list[str], keywords: list[str]) -> tuple[list[str], list[str]]:
    scored = []
    for position, comment in enumerate(comments):
        lowered = comment.lower()
        score = sum(lowered.count(keyword) for keyword in keywords)
        score += max(0, 10 - position) / 100
        scored.append((score, position, comment))
    ranked = [comment for _, _, comment in sorted(scored, key=lambda item: (-item[0], item[1]))]
    selected = []
    for comment in ranked:
        if comment not in selected:
            selected.append(comment)
        if len(selected) == 10:
            break
    while len(selected) < 10:
        selected.append("Additional sampled comment available in the cluster source PDF.")
    return selected[:5], selected[5:10]


def make_pdf(path: Path, title: str, comments: list[str], label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#3F245E"),
        spaceAfter=8,
    )
    note_style = ParagraphStyle(
        "GuideNote",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#5A5360"),
        spaceAfter=10,
    )
    comment_style = ParagraphStyle(
        "GuideComment",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1F1728"),
    )
    footer_style = ParagraphStyle(
        "GuideFooter",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#6D6674"),
    )
    story = [
        Paragraph(ascii_text(title), title_style),
        Paragraph(
            ascii_text(
                f"{label}: choose one primary comment first, then add supporting comments only if the narration has room. "
                "Text is lightly normalized for readability; usernames and profile details are intentionally omitted."
            ),
            note_style,
        ),
    ]
    rows = []
    for number, comment in enumerate(comments, start=1):
        rows.append([
            Paragraph(f"<b>{number}</b>", comment_style),
            Paragraph(ascii_text(f'"{comment}"'), comment_style),
        ])
    table = Table(rows, colWidths=[0.42 * inch, 6.65 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F0FA")),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#C7B4D8")),
                ("INNERGRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#DCCFE6")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.extend([table, Spacer(1, 10)])
    story.append(
        Paragraph(
            "Editor note: crop or blur usernames and profile photos. Keep this comment bank nearby while assembling the layered 9:16 sequence.",
            footer_style,
        )
    )
    document = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.45 * inch,
        title=ascii_text(title),
    )
    document.build(story)


def copy_chart(source: Path, destination: Path, missing: list[str]) -> None:
    if source.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    else:
        missing.append(str(source.relative_to(ROOT)))


def main() -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    source_clusters = parse_source_comments()
    missing: list[str] = []

    for division, data in DIVISION_COMMENTS.items():
        folder = PACKAGE / division
        make_pdf(folder / "must_show.pdf", data["title"], data["must"], "Must show")
        make_pdf(folder / "supporting.pdf", data["title"], data["support"], "Supporting options")

    for folder_name, data in CLUSTERS.items():
        cluster_number = data["source_cluster"]
        must, support = choose_comments(source_clusters.get(cluster_number, []), data["keywords"])
        folder = PACKAGE / "03_topic_clusters" / folder_name
        make_pdf(folder / "must_show.pdf", data["title"], must, "Must show")
        make_pdf(folder / "supporting.pdf", data["title"], support, "Supporting options")

    chart_map = {
        "outputs/plots/sentiment_distribution.png": "02_sentiment/sentiment_distribution.png",
        "outputs/clusters/topic_clusters_wordclouds_sentiment.png": "03_topic_clusters/00_cluster_map.png",
        "outputs/clusters/cluster_sentiment_stacked.png": "03_topic_clusters/00_cluster_sentiment.png",
        "outputs/plots/word_frequency_bigrams.png": "03_topic_clusters/00_word_frequency_bigrams.png",
        "outputs/plots/reply_sentiment_heatmap.png": "02_sentiment/reply_sentiment_heatmap.png",
    }
    for source_name, destination_name in chart_map.items():
        copy_chart(ROOT / source_name, PACKAGE / destination_name, missing)

    manifest = PACKAGE / "README.md"
    lines = [
        "# Editor guide upload package",
        "",
        "Upload this folder to the Google Drive path `GEWORLD Ube Craze/editor guide`.",
        "The video script uses the same relative paths beginning with `editor guide/`.",
        "",
        "Each comment PDF contains five primary or five supporting options. Use one primary comment first, then add supporting comments as time allows.",
        "Usernames and profile details are omitted from the prepared text so the editor can crop or blur them in any source screenshot.",
        "",
        "## Included chart copies",
        "",
    ]
    for source_name, destination_name in chart_map.items():
        if source_name not in missing:
            lines.append(f"- `{destination_name}`")
    if missing:
        lines.extend(["", "## Missing source files", ""])
        lines.extend(f"- `{item}`" for item in missing)
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Built editor guide package at {PACKAGE}")
    print(f"Generated {len(list(PACKAGE.rglob('*.pdf')))} PDFs")
    if missing:
        print("Missing chart sources:")
        for item in missing:
            print(f"- {item}")


if __name__ == "__main__":
    main()
