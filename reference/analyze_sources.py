from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SLIDES_DIR = ROOT / "fall2025-slides"
TEXTBOOK = next(ROOT.glob("Abraham*.pdf"))

GENERIC_LINES = {
    "DATABASE SYSTEMS (FALL 2025)",
    "DATABASESYSTEMS",
    "15-445/645 FALL 2025",
    "PROF. ANDY PAVLO",
    "DATABASE SYSTEMS",
    "ADMINISTRIVIA",
    "LAST CLASS",
    "TODAY'S AGENDA",
    "TODAY'S AGENDA",
    "COURSE OUTLINE",
}

STOP_WORDS = {
    "database",
    "databases",
    "systems",
    "system",
    "fall",
    "lecture",
    "class",
    "will",
    "this",
    "that",
    "with",
    "from",
    "have",
    "more",
    "page",
    "pages",
    "table",
    "data",
    "query",
    "queries",
    "using",
    "based",
    "example",
    "examples",
    "operator",
    "operators",
    "record",
    "records",
}


def clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).replace("’", "'")


def significant(line: str) -> bool:
    if not line or line in GENERIC_LINES:
        return False
    if re.fullmatch(r"[0-9\s]+", line):
        return False
    if line.startswith("https://"):
        return False
    administrative = (
        "Project #",
        "Homework #",
        "Office Hours",
        "Mid-Term",
        "Recitation",
        "due Sunday",
        "CMU-DB",
        "WaitList",
    )
    return not any(marker in line for marker in administrative)


def slide_summary(path: Path) -> tuple[int, list[str], list[str], list[str]]:
    reader = PdfReader(str(path))
    headings: list[str] = []
    agenda: list[str] = []
    words: Counter[str] = Counter()

    for page in reader.pages:
        text = page.extract_text() or ""
        lines = [clean_line(line) for line in text.splitlines()]
        for index, line in enumerate(lines):
            if line.upper() in {"TODAY'S AGENDA", "TODAY'S AGENDA"}:
                for agenda_line in lines[index + 1 : index + 10]:
                    if significant(agenda_line) and agenda_line not in agenda:
                        agenda.append(agenda_line)
        for line in lines:
            if significant(line):
                if len(line) <= 80 and (
                    line.isupper()
                    or line.istitle()
                    or re.match(r"^[A-Z0-9][A-Za-z0-9 +\-/&().,#]+$", line)
                ):
                    if line not in headings:
                        headings.append(line)
                for word in re.findall(r"[A-Za-z][A-Za-z0-9_+-]{3,}", line.lower()):
                    if word not in STOP_WORDS:
                        words[word] += 1

    keywords = [word for word, _ in words.most_common(24)]
    return len(reader.pages), agenda[:16], headings[:55], keywords


def print_textbook_outline() -> None:
    reader = PdfReader(str(TEXTBOOK))
    labels = reader.page_labels

    def walk(items, level: int = 0) -> None:
        for item in items:
            if isinstance(item, list):
                walk(item, level + 1)
                continue
            try:
                page_index = reader.get_destination_page_number(item)
                label = labels[page_index]
                print(f"{'  ' * level}{page_index + 1:>4} / label {label:>4}: {item.title}")
            except Exception as exc:
                print(f"{'  ' * level}????: {item!r} ({exc})")

    walk(reader.outline)


def main() -> None:
    print(f"Textbook: {TEXTBOOK.name}")
    print_textbook_outline()
    print("\nSlides:")
    for slide in sorted(SLIDES_DIR.glob("*.pdf")):
        page_count, agenda, headings, keywords = slide_summary(slide)
        print(f"\n{slide.name} ({page_count} slide pages)")
        if agenda:
            print("  Agenda: " + "; ".join(agenda))
        print("  Headings: " + "; ".join(headings))
        print("  Keywords: " + ", ".join(keywords))


if __name__ == "__main__":
    main()
