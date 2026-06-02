from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "reference"
TEXTBOOK = next(ROOT.glob("Abraham*.pdf"))
SCHEDULE_URL = "https://15445.courses.cs.cmu.edu/fall2025/schedule.html"


@dataclass(frozen=True)
class PageRange:
    start: int
    end: int
    sections: str


@dataclass(frozen=True)
class LectureReference:
    lecture: int
    slide_file: str
    title: str
    slide_focus: str
    reading_basis: str
    ranges: tuple[PageRange, ...]
    note: str = ""

    @property
    def output_name(self) -> str:
        return f"Lecture{self.lecture:02d}-Reference-Textbook.pdf"


LECTURES: tuple[LectureReference, ...] = (
    LectureReference(
        1,
        "01-relationalmodel.pdf",
        "Relational Model & Algebra",
        "DBMS background, relational model, relational algebra, and alternative data models.",
        "CMU schedule: Chapters 1-2; slide agenda adds alternative data model context.",
        (
            PageRange(30, 59, "Chapter 1 Introduction"),
            PageRange(66, 88, "Chapter 2 Introduction to the Relational Model"),
            PageRange(394, 410, "Chapter 8.1-8.2 semi-structured/object data models"),
        ),
    ),
    LectureReference(
        2,
        "02-modernsql.pdf",
        "Modern SQL",
        "Aggregations, grouping, nested queries, lateral joins, CTEs, and window functions.",
        "CMU schedule: Chapters 3-5.",
        (PageRange(94, 260, "Chapters 3-5 SQL, intermediate SQL, and advanced SQL"),),
    ),
    LectureReference(
        3,
        "03-storage1.pdf",
        "Database Storage I",
        "Storage hierarchy, file storage, page layout, and tuple layout.",
        "CMU schedule: Chapter 12.1-12.4, 13.2-13.3.",
        (
            PageRange(588, 598, "Chapter 12.1-12.4 physical storage media"),
            PageRange(617, 630, "Chapter 13.2-13.3 file organization and records"),
        ),
    ),
    LectureReference(
        4,
        "04-bufferpool.pdf",
        "Memory Management",
        "Buffer pool organization, metadata, replacement, disk scheduling, and optimizations.",
        "CMU schedule: Chapter 13.2-13.5.",
        (PageRange(617, 639, "Chapter 13.2-13.5 file organization, records, and database buffer"),),
    ),
    LectureReference(
        5,
        "05-storage2.pdf",
        "Database Storage II",
        "Buffer pool optimizations, tuple-oriented storage, index-organized storage, and log-structured storage.",
        "CMU schedule: Chapter 14.8.1, 24.2; slide recap adds tuple/page storage context.",
        (
            PageRange(617, 630, "Chapter 13.2-13.3 tuple-oriented file and record organization"),
            PageRange(663, 678, "Chapter 14.3 B+-Tree index files / index-organized storage context"),
            PageRange(694, 698, "Chapter 14.8 write-optimized index structures"),
            PageRange(1205, 1210, "Chapter 24.2 log-structured merge tree and variants"),
        ),
    ),
    LectureReference(
        6,
        "06-storage3.pdf",
        "Storage Models & Compression",
        "OLTP/OLAP workloads, row vs. column storage models, and compression.",
        "CMU schedule: Chapter 11.2, 13.6; slide agenda adds OLAP and compression context.",
        (
            PageRange(550, 568, "Chapter 11.2-11.3 data warehousing and OLAP"),
            PageRange(640, 643, "Chapter 13.6 column-oriented storage"),
            PageRange(699, 700, "Chapter 14.9 bitmap indices as compression/filtering-adjacent storage"),
        ),
    ),
    LectureReference(
        7,
        "07-hashtables.pdf",
        "Hash Tables",
        "Hash functions, static hashing, and dynamic hashing schemes.",
        "CMU schedule: Chapter 14.5, 24.5.",
        (
            PageRange(687, 689, "Chapter 14.5 hash indices"),
            PageRange(1219, 1231, "Chapter 24.5 hash indices"),
        ),
    ),
    LectureReference(
        8,
        "08-indexes1.pdf",
        "Indexes & Filters I",
        "B+-Tree overview, design choices, insertion/deletion, and optimizations.",
        "CMU schedule: Chapter 14.1-14.4.",
        (PageRange(652, 686, "Chapter 14.1-14.4 indexing basics, ordered indices, B+-Trees, and B+-Tree extensions"),),
    ),
    LectureReference(
        9,
        "09-indexes2.pdf",
        "Indexes & Filters II",
        "Bloom filters, skip lists, tries/radix trees, inverted indexes, vector indexes, and covering indexes.",
        "CMU schedule: Chapter 14.1-14.4, 24.1; slide topics add textual and spatial/index variants.",
        (
            PageRange(411, 415, "Chapter 8.3 textual data and inverted-index context"),
            PageRange(652, 686, "Chapter 14.1-14.4 indexing basics and B+-Tree context"),
            PageRange(1204, 1204, "Chapter 24.1 Bloom filter"),
            PageRange(1211, 1218, "Chapter 24.3-24.4 bitmap and spatial indexing variants"),
        ),
        "The textbook has limited direct coverage of skip lists, radix trees, and modern vector indexes.",
    ),
    LectureReference(
        10,
        "10-indexconcurrency.pdf",
        "Index Concurrency Control",
        "Latches, hash table latching, B+-Tree latch crabbing/coupling, and leaf scans.",
        "CMU schedule: Chapter 18.10.2; B+-Tree structure pages included for context.",
        (
            PageRange(663, 686, "Chapter 14.3-14.4 B+-Tree structures and extensions"),
            PageRange(914, 919, "Chapter 18.10.2-18.10.3 concurrency in index structures and latch-free structures"),
        ),
    ),
    LectureReference(
        11,
        "11-sorting.pdf",
        "Sorting & Aggregation Algorithms",
        "Top-N heap sort, external merge sort, and aggregation algorithms.",
        "CMU schedule: Chapter 15.4-15.5; slide agenda adds aggregations from 15.6.",
        (PageRange(730, 752, "Chapter 15.4-15.6 sorting, join operation, and other operations including aggregation"),),
    ),
    LectureReference(
        12,
        "12-joins.pdf",
        "Join Algorithms",
        "Nested-loop joins, sort-merge join, hash join, and join cost analysis.",
        "CMU schedule: Chapter 15.4-15.6.",
        (PageRange(730, 752, "Chapter 15.4-15.6 sorting and join/other query operations"),),
    ),
    LectureReference(
        13,
        "13-queryexecution1.pdf",
        "Query Execution I",
        "Processing models, access methods, modification queries, and expression evaluation.",
        "CMU schedule: Chapter 15.1-15.3, 15.7.",
        (
            PageRange(718, 729, "Chapter 15.1-15.3 query processing overview, cost, and selection"),
            PageRange(753, 759, "Chapter 15.7 evaluation of expressions"),
        ),
    ),
    LectureReference(
        14,
        "14-queryexecution2.pdf",
        "Query Execution II",
        "Process models, execution parallelism, and I/O parallelism.",
        "CMU schedule: Chapter 22; slide agenda adds process-model context from architectures.",
        (
            PageRange(990, 1018, "Chapter 20.1-20.6 database-system architectures and parallel/distributed systems"),
            PageRange(1068, 1117, "Chapter 22 parallel and distributed query processing"),
        ),
    ),
    LectureReference(
        15,
        "15-optimization1.pdf",
        "Query Planning & Optimization I",
        "Transformations, heuristic/rule-based optimization, and cost-based optimization.",
        "CMU schedule: Chapter 16.",
        (PageRange(772, 817, "Chapter 16 query optimization"),),
    ),
    LectureReference(
        16,
        "16-optimization2.pdf",
        "Query Planning & Optimization II",
        "Optimizer search algorithms, data statistics, cardinality estimation, and cost models.",
        "CMU schedule: Chapter 16.",
        (PageRange(772, 817, "Chapter 16 query optimization"),),
    ),
    LectureReference(
        17,
        "17-concurrencycontrol.pdf",
        "Concurrency Control Theory",
        "ACID, schedules, conflict/view serializability, and isolation.",
        "Slide content maps to textbook Chapter 17 Transactions; CMU schedule lists Chapter 18 in the current course page.",
        (PageRange(828, 859, "Chapter 17 transactions, isolation, serializability, and isolation levels"),),
    ),
    LectureReference(
        18,
        "18-twophaselocking.pdf",
        "Two-Phase Locking",
        "Lock types, two-phase locking, deadlock detection/prevention, and hierarchical locking.",
        "CMU schedule: Chapter 18.1-18.3, 18.9.",
        (
            PageRange(864, 885, "Chapter 18.1-18.3 lock-based protocols, deadlock, and multiple granularity"),
            PageRange(909, 911, "Chapter 18.9 weak levels of consistency in practice"),
        ),
    ),
    LectureReference(
        19,
        "19-timestampordering.pdf",
        "Timestamp Ordering",
        "Timestamp ordering, optimistic/validation-based concurrency control, phantom reads, and isolation levels.",
        "CMU schedule: Chapter 18.5-18.6; slide agenda adds phantom/isolation context.",
        (
            PageRange(850, 854, "Chapter 17.8-17.9 isolation levels and implementation"),
            PageRange(886, 897, "Chapter 18.4-18.6 predicate reads, timestamp-based, and validation-based protocols"),
        ),
    ),
    LectureReference(
        20,
        "20-multiversioning.pdf",
        "Multi-Version Concurrency Control",
        "MVCC, snapshot isolation, write skew, version storage, and garbage collection.",
        "CMU schedule: Chapter 18.7-18.8.",
        (PageRange(898, 908, "Chapter 18.7-18.8 multiversion schemes and snapshot isolation"),),
    ),
    LectureReference(
        21,
        "21-logging.pdf",
        "Database Logging",
        "Buffer pool policies, shadow paging, WAL, logging schemes, and checkpoints.",
        "CMU schedule: Chapter 19.1-19.8.",
        (PageRange(936, 969, "Chapter 19.1-19.8 recovery system, logging, buffer management, and logical undo"),),
    ),
    LectureReference(
        22,
        "22-recovery.pdf",
        "Database Recovery",
        "LSNs, commit/abort handling, fuzzy checkpointing, and ARIES recovery.",
        "CMU schedule: Chapter 19.1-19.9.",
        (PageRange(936, 975, "Chapter 19.1-19.9 recovery system and ARIES"),),
    ),
    LectureReference(
        23,
        "23-distributed1.pdf",
        "Distributed Database Systems I",
        "System architectures, partitioning, replication, and distributed concurrency control.",
        "CMU schedule: Chapter 20.4-20.5, 21, 23.1-23.4.",
        (
            PageRange(999, 1017, "Chapter 20.4-20.5 parallel and distributed systems"),
            PageRange(1032, 1061, "Chapter 21 parallel and distributed storage"),
            PageRange(1127, 1157, "Chapter 23.1-23.4 distributed transactions, commit protocols, concurrency, and replication"),
        ),
    ),
    LectureReference(
        24,
        "24-distributed2.pdf",
        "Distributed Database Systems II",
        "Atomic commit, consistency issues, distributed joins, distributed query processing, and shuffle.",
        "CMU schedule: Chapter 20.7, 22.9; slide agenda adds commit, consensus, and distributed join context.",
        (
            PageRange(1019, 1023, "Chapter 20.7 cloud-based services"),
            PageRange(1070, 1089, "Chapter 22.2-22.5 parallel sort/join and parallel plan evaluation"),
            PageRange(1105, 1114, "Chapter 22.9 distributed query processing"),
            PageRange(1127, 1139, "Chapter 23.1-23.2 distributed transactions and commit protocols"),
            PageRange(1162, 1190, "Chapter 23.6-23.8 weak consistency, coordinator selection, and consensus"),
        ),
    ),
    LectureReference(
        25,
        "25-potpourri.pdf",
        "Final Review + Systems Potpourri",
        "Final review plus advanced DBMS speed-run: vectorized execution, cloud OLAP systems, shuffle, storage engines, and tuning.",
        "No CMU schedule reading listed; selected closest textbook sections from prior and advanced chapters.",
        (
            PageRange(550, 568, "Chapter 11.2-11.3 data warehousing and OLAP"),
            PageRange(640, 643, "Chapter 13.6 column-oriented storage"),
            PageRange(760, 762, "Chapter 15.8 query processing in memory"),
            PageRange(1019, 1023, "Chapter 20.7 cloud-based services"),
            PageRange(1081, 1114, "Chapter 22.5-22.9 parallel/distributed query plans and distributed query processing"),
            PageRange(1204, 1214, "Chapter 24.1-24.3 Bloom filters, LSM variants, and bitmap indices"),
            PageRange(1239, 1262, "Chapter 25.1-25.2 performance tuning and benchmarks"),
        ),
        "This lecture is partly a course review and partly modern-system case studies, so the textbook match is intentionally selective.",
    ),
)


def iter_pages(ranges: Iterable[PageRange]) -> Iterable[int]:
    for page_range in ranges:
        if page_range.start > page_range.end:
            raise ValueError(f"Invalid page range: {page_range}")
        yield from range(page_range.start, page_range.end + 1)


def range_label(reader: PdfReader, page_range: PageRange) -> str:
    start_label = reader.page_labels[page_range.start - 1]
    end_label = reader.page_labels[page_range.end - 1]
    if page_range.start == page_range.end:
        return f"PDF p. {page_range.start} / book p. {start_label}"
    return f"PDF pp. {page_range.start}-{page_range.end} / book pp. {start_label}-{end_label}"


def build_pdf(reader: PdfReader, lecture: LectureReference) -> None:
    writer = PdfWriter()
    seen = set()
    for page_num in iter_pages(lecture.ranges):
        if page_num in seen:
            continue
        seen.add(page_num)
        writer.add_page(reader.pages[page_num - 1])

    writer.add_metadata(
        {
            "/Title": f"Lecture {lecture.lecture:02d} Reference Textbook Pages",
            "/Subject": lecture.title,
            "/Source": TEXTBOOK.name,
        }
    )
    output_path = REFERENCE_DIR / lecture.output_name
    with output_path.open("wb") as output:
        writer.write(output)


def write_map_files(reader: PdfReader) -> None:
    map_payload = []
    for lecture in LECTURES:
        map_payload.append(
            {
                "lecture": lecture.lecture,
                "slide_file": lecture.slide_file,
                "title": lecture.title,
                "output_pdf": lecture.output_name,
                "slide_focus": lecture.slide_focus,
                "reading_basis": lecture.reading_basis,
                "note": lecture.note,
                "ranges": [
                    {
                        "pdf_pages": [page_range.start, page_range.end],
                        "book_pages": [
                            reader.page_labels[page_range.start - 1],
                            reader.page_labels[page_range.end - 1],
                        ],
                        "sections": page_range.sections,
                    }
                    for page_range in lecture.ranges
                ],
            }
        )

    json_path = REFERENCE_DIR / "reference_map.json"
    json_path.write_text(
        json.dumps(
            {
                "generated_on": date.today().isoformat(),
                "textbook_pdf": TEXTBOOK.name,
                "course_schedule_source": SCHEDULE_URL,
                "lectures": map_payload,
            },
            indent=2,
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Reference Textbook Page Packs",
        "",
        f"Generated from `{TEXTBOOK.name}`.",
        "",
        f"Primary mapping source: CMU 15-445/645 Fall 2025 schedule readings ({SCHEDULE_URL}).",
        "I also checked the slide agendas/topics and added nearby textbook sections when the schedule reading was too narrow.",
        "",
        "`PDF pages` are the physical page numbers used for extraction. `Book pages` are the textbook's printed page labels.",
        "",
        "| Lecture | Slide | Output PDF | Textbook pages | Basis / focus |",
        "| --- | --- | --- | --- | --- |",
    ]
    for lecture in LECTURES:
        page_bits = "<br>".join(
            f"{range_label(reader, page_range)}: {page_range.sections}"
            for page_range in lecture.ranges
        )
        basis = lecture.reading_basis
        if lecture.note:
            basis += f" Note: {lecture.note}"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{lecture.lecture:02d} {lecture.title}",
                    lecture.slide_file,
                    lecture.output_name,
                    page_bits,
                    basis,
                ]
            )
            + " |"
        )

    (REFERENCE_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REFERENCE_DIR.mkdir(exist_ok=True)
    reader = PdfReader(str(TEXTBOOK))
    for lecture in LECTURES:
        build_pdf(reader, lecture)
    write_map_files(reader)
    print(f"Created {len(LECTURES)} reference PDFs in {REFERENCE_DIR}")


if __name__ == "__main__":
    main()
