#!/usr/bin/env python3
# coding: utf-8

"""Generate publications.md plus a local CCF matching audit report."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from dataclasses import dataclass
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path


CCF_URL = "https://ccf.atom.im/"
AUTHOR_TO_HIGHLIGHT = "Zhiquan Lai"
KEEP_RANKS = {"A", "B"}
DEFAULT_CACHE_NAME = "ccf_atom_cache.json"
DEFAULT_REPORT_NAME = "publications_ccf_match_report.md"
VENUE_TYPE_CONF = "conference"
VENUE_TYPE_JOURNAL = "journal"
WHITESPACE_RE = re.compile(r"\s+")
NON_MAIN_CONF_MARKERS = (
    "workshop",
    "workshops",
    "poster abstract",
    "phd forum",
    "doctoral consortium",
    "demo",
    "companion",
    "extended abstract",
)
CCF_CONF_TYPE_ALIASES = {
    VENUE_TYPE_CONF,
    "会议",
    "浼氳",
    "æµ¼æ°³î†…",
}
CCF_JOURNAL_TYPE_ALIASES = {
    VENUE_TYPE_JOURNAL,
    "期刊",
    "鏈熷垔",
    "éˆç†·åž”",
}
CCF_ABBR_ALIASES = {
    "fcsc": "fcs",
    "chinaf": "scis",
    "pkdd": "ecmlpkdd",
}
CCF_VENUE_TEXT_ALIASES = {
    "frontierscomputsci": "fcs",
    "sciencechinainformationsciences": "scis",
    "scichinainfsci": "scis",
    "ecmlpkdd": "ecmlpkdd",
}


@dataclass
class CCFVenue:
    abbr: str
    name: str
    rank: str
    venue_type: str


@dataclass
class MatchResult:
    venue: CCFVenue | None
    method: str
    raw_venue: str
    candidate_abbrs: list[str]


@dataclass
class AuditRecord:
    venue_type: str
    year: str
    title: str
    bib_id: str
    raw_venue: str
    decision: str
    matched_abbr: str
    matched_name: str
    matched_rank: str
    match_method: str
    candidate_abbrs: str


class TableRowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._in_row = False
        self._in_cell = False
        self._current_row: list[str] = []
        self._current_cell: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "tr":
            self._in_row = True
            self._current_row = []
        elif tag in {"td", "th"} and self._in_row:
            self._in_cell = True
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._in_cell:
            self._current_row.append(normalize_space("".join(self._current_cell)))
            self._current_cell = []
            self._in_cell = False
        elif tag == "tr" and self._in_row:
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = []
            self._in_row = False


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Generate _pages/publications.md and a local CCF audit report."
    )
    parser.add_argument(
        "bib_file",
        nargs="?",
        default=str(script_dir / "4279.bib"),
        help="Path to the BibTeX file.",
    )
    parser.add_argument(
        "--output",
        default=str(script_dir.parent / "_pages" / "publications.md"),
        help="Output markdown path for the website page.",
    )
    parser.add_argument(
        "--report",
        default=str(script_dir / DEFAULT_REPORT_NAME),
        help="Output markdown path for the local CCF audit report.",
    )
    parser.add_argument(
        "--cache",
        default=str(script_dir / DEFAULT_CACHE_NAME),
        help="Local cache file for parsed CCF venue data.",
    )
    parser.add_argument(
        "--refresh-ccf",
        action="store_true",
        help="Refresh the CCF cache from ccf.atom.im before generating outputs.",
    )
    return parser.parse_args()


def normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def clean_bib_text(text: str) -> str:
    text = text.replace(r"{\_}", "_")
    text = text.replace(r"\_", "_")
    text = text.replace(r"{\&}", "&")
    text = text.replace(r"\&", "&")
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace("\\", "")
    text = text.replace("~", " ")
    return normalize_space(text)


def normalize_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", clean_bib_text(text).lower())


def normalize_ccf_venue_type(value: str) -> str | None:
    value = normalize_space(value)
    if not value:
        return None
    if value in CCF_CONF_TYPE_ALIASES:
        return VENUE_TYPE_CONF
    if value in CCF_JOURNAL_TYPE_ALIASES:
        return VENUE_TYPE_JOURNAL

    lowered = value.lower()
    if "conference" in lowered or "conf" in lowered:
        return VENUE_TYPE_CONF
    if "journal" in lowered:
        return VENUE_TYPE_JOURNAL
    return None


def split_entries(text: str) -> list[str]:
    entries = []
    index = 0

    while True:
        at_index = text.find("@", index)
        if at_index == -1:
            break

        brace_index = text.find("{", at_index)
        if brace_index == -1:
            break

        depth = 0
        end_index = None
        for i in range(brace_index, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end_index = i
                    break

        if end_index is None:
            break

        entries.append(text[at_index : end_index + 1])
        index = end_index + 1

    return entries


def parse_braced_value(text: str, start: int) -> tuple[str, int]:
    depth = 0
    chars = []

    for index in range(start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
            if depth > 1:
                chars.append(char)
        elif char == "}":
            depth -= 1
            if depth == 0:
                return "".join(chars), index + 1
            chars.append(char)
        else:
            chars.append(char)

    raise ValueError("Unbalanced braces in BibTeX value.")


def parse_quoted_value(text: str, start: int) -> tuple[str, int]:
    chars = []
    escaped = False

    for index in range(start + 1, len(text)):
        char = text[index]
        if escaped:
            chars.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            chars.append(char)
            continue
        if char == '"':
            return "".join(chars), index + 1
        chars.append(char)

    raise ValueError("Unbalanced quotes in BibTeX value.")


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    index = 0

    while index < len(body):
        while index < len(body) and body[index] in " \t\r\n,":
            index += 1
        if index >= len(body):
            break

        key_start = index
        while index < len(body) and body[index] not in "=\r\n":
            index += 1
        key = body[key_start:index].strip().lower()

        while index < len(body) and body[index] in " \t\r\n=":
            index += 1
        if index >= len(body):
            break

        if body[index] == "{":
            value, index = parse_braced_value(body, index)
        elif body[index] == '"':
            value, index = parse_quoted_value(body, index)
        else:
            value_start = index
            while index < len(body) and body[index] not in ",\r\n":
                index += 1
            value = body[value_start:index].strip()

        fields[key] = value.strip()

        while index < len(body) and body[index] in " \t\r\n,":
            index += 1

    return fields


def parse_entry(entry_text: str) -> dict[str, object]:
    match = re.match(r"@(?P<entry_type>\w+)\s*\{\s*(?P<bib_id>[^,]+),", entry_text, re.S)
    if not match:
        raise ValueError("Invalid BibTeX entry.")

    body = entry_text[match.end() : -1].strip()
    return {
        "entry_type": match.group("entry_type").lower(),
        "bib_id": match.group("bib_id").strip(),
        "fields": parse_fields(body),
    }


def fetch_ccf_html() -> str:
    request = urllib.request.Request(CCF_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_ccf_venues(html_text: str) -> list[CCFVenue]:
    parser = TableRowParser()
    parser.feed(html_text)

    venues: list[CCFVenue] = []
    for row in parser.rows:
        if len(row) < 6:
            continue

        rank = row[3].strip().upper()
        venue_type = normalize_ccf_venue_type(row[4])
        if rank not in {"A", "B", "C"} or venue_type is None:
            continue

        venues.append(
            CCFVenue(
                abbr=row[1].strip(),
                name=row[2].strip(),
                rank=rank,
                venue_type=venue_type,
            )
        )

    return venues


def save_ccf_cache(cache_path: Path, venues: list[CCFVenue]) -> None:
    cache_path.write_text(
        json.dumps([venue.__dict__ for venue in venues], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_ccf_cache(cache_path: Path) -> list[CCFVenue]:
    data = json.loads(cache_path.read_text(encoding="utf-8"))
    venues: list[CCFVenue] = []
    cache_needs_rewrite = False

    for item in data:
        venue_type = normalize_ccf_venue_type(str(item.get("venue_type", "")))
        if venue_type is None:
            continue
        if venue_type != item.get("venue_type"):
            cache_needs_rewrite = True

        venues.append(
            CCFVenue(
                abbr=str(item.get("abbr", "")),
                name=str(item.get("name", "")),
                rank=str(item.get("rank", "")).upper(),
                venue_type=venue_type,
            )
        )

    if cache_needs_rewrite:
        save_ccf_cache(cache_path, venues)

    return venues


def get_ccf_venues(cache_path: Path, refresh: bool) -> list[CCFVenue]:
    if cache_path.exists() and not refresh:
        return load_ccf_cache(cache_path)

    venues = parse_ccf_venues(fetch_ccf_html())
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    save_ccf_cache(cache_path, venues)
    return venues


def classify_entry(bib_id: str) -> str | None:
    if bib_id.startswith("DBLP:conf/"):
        return VENUE_TYPE_CONF
    if bib_id.startswith("DBLP:journals/"):
        return VENUE_TYPE_JOURNAL
    return None


def get_entry_venue_text(entry: dict[str, object]) -> str:
    fields = entry["fields"]  # type: ignore[assignment]
    venue_type = classify_entry(entry["bib_id"])  # type: ignore[index]
    if venue_type == VENUE_TYPE_CONF:
        return clean_bib_text(fields.get("booktitle", ""))
    if venue_type == VENUE_TYPE_JOURNAL:
        return clean_bib_text(fields.get("journal", ""))
    return ""


def is_main_published_entry(entry: dict[str, object]) -> bool:
    venue_type = classify_entry(entry["bib_id"])  # type: ignore[index]
    fields = entry["fields"]  # type: ignore[assignment]

    if venue_type == VENUE_TYPE_JOURNAL:
        journal = clean_bib_text(fields.get("journal", ""))
        return bool(journal) and normalize_key(journal) != "corr"

    if venue_type == VENUE_TYPE_CONF:
        combined = " ".join(
            [
                clean_bib_text(fields.get("booktitle", "")),
                clean_bib_text(fields.get("title", "")),
            ]
        ).lower()
        return not any(marker in combined for marker in NON_MAIN_CONF_MARKERS)

    return False


def get_non_main_reason(entry: dict[str, object]) -> str:
    venue_type = classify_entry(entry["bib_id"])  # type: ignore[index]
    fields = entry["fields"]  # type: ignore[assignment]

    if venue_type == VENUE_TYPE_JOURNAL:
        journal = clean_bib_text(fields.get("journal", ""))
        if not journal:
            return "missing journal field"
        if normalize_key(journal) == "corr":
            return "preprint venue (CoRR)"
        return "journal excluded by publication filter"

    if venue_type == VENUE_TYPE_CONF:
        combined = " ".join(
            [
                clean_bib_text(fields.get("booktitle", "")),
                clean_bib_text(fields.get("title", "")),
            ]
        ).lower()
        for marker in NON_MAIN_CONF_MARKERS:
            if marker in combined:
                return f"auxiliary conference publication ({marker})"
        if not clean_bib_text(fields.get("booktitle", "")):
            return "missing booktitle field"
        return "conference excluded by publication filter"

    return "unsupported entry type"


def extract_venue_code(bib_id: str) -> str:
    parts = bib_id.split("/")
    return parts[1] if len(parts) >= 2 else ""


def extract_candidate_abbrs(entry: dict[str, object], ccf_abbr_keys: set[str]) -> list[str]:
    fields = entry["fields"]  # type: ignore[assignment]
    candidates = []

    venue_code = normalize_key(extract_venue_code(entry["bib_id"]))  # type: ignore[index]
    if venue_code:
        candidates.append(venue_code)
        alias = CCF_ABBR_ALIASES.get(venue_code)
        if alias and alias in ccf_abbr_keys and alias not in candidates:
            candidates.append(alias)

    venue_text = clean_bib_text(fields.get("booktitle") or fields.get("journal") or "")
    text_patterns = re.findall(r"\b[A-Za-z0-9]+(?:[-/ ][A-Za-z0-9]+)*\b", venue_text)
    for pattern in text_patterns:
        key = normalize_key(pattern)
        if key and key in ccf_abbr_keys and key not in candidates:
            candidates.append(key)
        alias = CCF_ABBR_ALIASES.get(key)
        if alias and alias in ccf_abbr_keys and alias not in candidates:
            candidates.append(alias)

    normalized_venue_text = normalize_key(venue_text)
    for key, alias in CCF_VENUE_TEXT_ALIASES.items():
        if key in normalized_venue_text and alias in ccf_abbr_keys and alias not in candidates:
            candidates.append(alias)

    if "ipdps" in normalize_key(venue_text) and "ipdps" not in candidates:
        candidates.append("ipdps")

    return candidates


def simplify_conf_venue(venue_text: str) -> str:
    venue_text = clean_bib_text(venue_text)
    venue_text = re.sub(r",\s*[A-Z][A-Za-z0-9\- ]*\s+\d{4}.*$", "", venue_text)
    venue_text = re.sub(r",\s*\d{4}.*$", "", venue_text)
    venue_text = re.sub(r"\s+-\s+.*$", "", venue_text)
    return normalize_space(venue_text)


def choose_best_name_match(venue_text: str, candidates: list[CCFVenue]) -> CCFVenue | None:
    normalized_venue = normalize_key(venue_text)
    if not normalized_venue:
        return None

    best_match = None
    best_score = 0.0
    for candidate in candidates:
        normalized_name = normalize_key(candidate.name)
        if not normalized_name:
            continue
        if normalized_name in normalized_venue or normalized_venue in normalized_name:
            score = 1.0
        else:
            score = SequenceMatcher(None, normalized_venue, normalized_name).ratio()

        if score > best_score:
            best_score = score
            best_match = candidate

    return best_match if best_score >= 0.86 else None


def match_ccf_venue(entry: dict[str, object], venues: list[CCFVenue]) -> MatchResult:
    venue_type = classify_entry(entry["bib_id"])  # type: ignore[index]
    raw_venue = get_entry_venue_text(entry)
    if venue_type is None:
        return MatchResult(None, "unsupported-entry-type", raw_venue, [])

    filtered = [venue for venue in venues if venue.venue_type == venue_type]
    abbr_map: dict[str, list[CCFVenue]] = {}
    for venue in filtered:
        key = normalize_key(venue.abbr)
        if key:
            abbr_map.setdefault(key, []).append(venue)

    candidate_abbrs = extract_candidate_abbrs(entry, set(abbr_map.keys()))
    for candidate in candidate_abbrs:
        if candidate in abbr_map:
            ranked = sorted(abbr_map[candidate], key=lambda item: item.rank)
            return MatchResult(ranked[0], f"abbr:{candidate}", raw_venue, candidate_abbrs)

    venue_text = raw_venue if venue_type == VENUE_TYPE_JOURNAL else simplify_conf_venue(raw_venue)
    venue = choose_best_name_match(venue_text, filtered)
    method = "name-similarity" if venue is not None else "unmatched"
    return MatchResult(venue, method, raw_venue, candidate_abbrs)


def split_authors(author_field: str) -> list[str]:
    authors = [clean_bib_text(part) for part in re.split(r"\s+and\s+", author_field)]
    return [author for author in authors if author]


def highlight_author(name: str) -> str:
    return f"**{name}**" if normalize_key(name) == normalize_key(AUTHOR_TO_HIGHLIGHT) else name


def build_paper_link(fields: dict[str, str]) -> str:
    if fields.get("url"):
        return fields["url"].strip()
    if fields.get("doi"):
        return f"https://doi.org/{fields['doi'].strip()}"
    return ""


def format_entry(entry: dict[str, object], ccf_venue: CCFVenue) -> str:
    fields = entry["fields"]  # type: ignore[assignment]
    authors = ", ".join(highlight_author(author) for author in split_authors(fields.get("author", "")))
    title = clean_bib_text(fields.get("title", ""))
    year = clean_bib_text(fields.get("year", ""))
    paper_link = build_paper_link(fields)

    if ccf_venue.venue_type == VENUE_TYPE_CONF:
        venue_display = ccf_venue.abbr or simplify_conf_venue(fields.get("booktitle", ""))
        venue_segment = f"{venue_display} {year}".strip()
    else:
        venue_display = clean_bib_text(fields.get("journal", "")) or ccf_venue.abbr or ccf_venue.name
        venue_segment = f"{venue_display} ({year})".strip()

    line = " ".join(
        part
        for part in [
            "-",
            authors + "." if authors else "",
            f"\"{title}.\"" if title else "",
            venue_segment,
            f"(**CCF {ccf_venue.rank}**).",
        ]
        if part
    )
    if paper_link:
        line += f" [[Paper]]({paper_link})"
    return line


def entry_sort_key(entry: dict[str, object]) -> tuple[int, str]:
    fields = entry["fields"]  # type: ignore[assignment]
    try:
        year_value = int(clean_bib_text(fields.get("year", "0")))
    except ValueError:
        year_value = 0
    return (-year_value, clean_bib_text(fields.get("title", "")).lower())


def render_section(title: str, entries: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    if not entries:
        lines.append("- None yet.")
        lines.append("")
        return lines

    lines.extend(entries)
    lines.append("")
    return lines


def build_audit_record(
    entry: dict[str, object],
    decision: str,
    match_result: MatchResult | None = None,
) -> AuditRecord:
    fields = entry["fields"]  # type: ignore[assignment]
    venue_type = classify_entry(entry["bib_id"])  # type: ignore[index]
    matched = match_result.venue if match_result is not None else None
    return AuditRecord(
        venue_type=venue_type or "unknown",
        year=clean_bib_text(fields.get("year", "")),
        title=clean_bib_text(fields.get("title", "")),
        bib_id=str(entry["bib_id"]),
        raw_venue=(match_result.raw_venue if match_result is not None else get_entry_venue_text(entry)),
        decision=decision,
        matched_abbr=matched.abbr if matched is not None else "",
        matched_name=matched.name if matched is not None else "",
        matched_rank=matched.rank if matched is not None else "",
        match_method=match_result.method if match_result is not None else "",
        candidate_abbrs=", ".join(match_result.candidate_abbrs) if match_result is not None else "",
    )


def audit_sort_key(record: AuditRecord) -> tuple[int, str]:
    try:
        year_value = int(record.year)
    except ValueError:
        year_value = 0
    return (-year_value, record.title.lower())


def render_audit_item(record: AuditRecord) -> list[str]:
    lines = [
        f"- [{record.venue_type}] {record.year} | {record.title}",
        f"  bib_id: `{record.bib_id}`",
    ]

    if record.raw_venue:
        lines.append(f"  raw venue: `{record.raw_venue}`")

    if record.matched_abbr or record.matched_name:
        lines.append(
            f"  matched CCF: `{record.matched_abbr}` | {record.matched_name} | "
            f"rank `{record.matched_rank}` via `{record.match_method}`"
        )
    else:
        lines.append(f"  matched CCF: none ({record.match_method or 'no-match'})")

    if record.candidate_abbrs:
        lines.append(f"  extracted candidates: `{record.candidate_abbrs}`")

    lines.append(f"  decision: {record.decision}")
    return lines


def render_audit_section(title: str, records: list[AuditRecord]) -> list[str]:
    lines = [f"## {title}", ""]
    if not records:
        lines.append("- None")
        lines.append("")
        return lines

    for record in sorted(records, key=audit_sort_key):
        lines.extend(render_audit_item(record))
    lines.append("")
    return lines


def generate_report(
    report_path: Path,
    bib_path: Path,
    records_by_section: dict[str, list[AuditRecord]],
) -> None:
    lines = [
        "# CCF Match Report",
        "",
        f"Source bib: `{bib_path.name}`",
        "",
        "## Summary",
        "",
        f"- Included in publications page: {len(records_by_section['included'])}",
        f"- Excluded as non-main / preprint: {len(records_by_section['filtered_non_main'])}",
        f"- Excluded because matched venue is not CCF A/B: {len(records_by_section['filtered_rank'])}",
        f"- Excluded because no CCF venue match was found: {len(records_by_section['unmatched'])}",
        f"- Excluded because bib_id could not be classified: {len(records_by_section['unsupported'])}",
        "",
    ]

    lines.extend(render_audit_section("Included In Publications Page", records_by_section["included"]))
    lines.extend(render_audit_section("Excluded: Non-main / Preprint", records_by_section["filtered_non_main"]))
    lines.extend(render_audit_section("Excluded: Matched Venue But Not CCF A/B", records_by_section["filtered_rank"]))
    lines.extend(render_audit_section("Excluded: No CCF Match", records_by_section["unmatched"]))
    lines.extend(render_audit_section("Excluded: Unsupported bib_id", records_by_section["unsupported"]))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def generate_outputs(
    bib_path: Path,
    output_path: Path,
    report_path: Path,
    cache_path: Path,
    refresh_ccf: bool,
) -> None:
    entries = [parse_entry(entry_text) for entry_text in split_entries(bib_path.read_text(encoding="utf-8"))]
    ccf_venues = get_ccf_venues(cache_path, refresh_ccf)

    selected_conferences: list[tuple[dict[str, object], str]] = []
    selected_journals: list[tuple[dict[str, object], str]] = []
    records_by_section: dict[str, list[AuditRecord]] = {
        "included": [],
        "filtered_non_main": [],
        "filtered_rank": [],
        "unmatched": [],
        "unsupported": [],
    }

    for entry in entries:
        venue_type = classify_entry(entry["bib_id"])  # type: ignore[index]
        if venue_type is None:
            records_by_section["unsupported"].append(
                build_audit_record(entry, "unsupported bib_id prefix")
            )
            continue

        if not is_main_published_entry(entry):
            records_by_section["filtered_non_main"].append(
                build_audit_record(entry, get_non_main_reason(entry))
            )
            continue

        match_result = match_ccf_venue(entry, ccf_venues)
        if match_result.venue is None:
            records_by_section["unmatched"].append(
                build_audit_record(entry, "no CCF venue match found", match_result)
            )
            continue

        if match_result.venue.rank not in KEEP_RANKS:
            records_by_section["filtered_rank"].append(
                build_audit_record(
                    entry,
                    f"matched CCF {match_result.venue.rank}, not kept",
                    match_result,
                )
            )
            continue

        line = format_entry(entry, match_result.venue)
        if venue_type == VENUE_TYPE_CONF:
            selected_conferences.append((entry, line))
        else:
            selected_journals.append((entry, line))

        records_by_section["included"].append(
            build_audit_record(
                entry,
                f"included as CCF {match_result.venue.rank}",
                match_result,
            )
        )

    selected_conferences.sort(key=lambda item: entry_sort_key(item[0]))
    selected_journals.sort(key=lambda item: entry_sort_key(item[0]))

    lines = [
        "---",
        'layout: archive',
        'title: "Publications"',
        "permalink: /publications/",
        "author_profile: true",
        "---",
        "",
        "{% include base_path %}",
        "",
        f"<!-- Generated from markdown_generator/{bib_path.name}. CCF labels sourced from https://ccf.atom.im/ -->",
        "",
    ]

    lines.extend(render_section("Selected Conference Papers", [line for _, line in selected_conferences]))
    lines.extend(render_section("Selected Journal Papers", [line for _, line in selected_journals]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    generate_report(report_path, bib_path, records_by_section)


def main() -> int:
    args = parse_args()
    generate_outputs(
        bib_path=Path(args.bib_file).resolve(),
        output_path=Path(args.output).resolve(),
        report_path=Path(args.report).resolve(),
        cache_path=Path(args.cache).resolve(),
        refresh_ccf=args.refresh_ccf,
    )
    print(f"Generated {Path(args.output).resolve()}")
    print(f"Generated {Path(args.report).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
