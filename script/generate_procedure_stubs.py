"""
Generate per-procedure stub files from a KNX spec.

Two input modes:

  - ``--spec FILE [--prefix NM_]`` — point at a raw KNX spec txt (pdftotext
    output) and let the script find every ``<section> <Name>`` heading.
    Recommended; no external tooling needed.

  - ``--extract FILE`` — feed a hand-curated extract with one block per
    procedure in the documented format. Useful when the LLM has already
    produced a clean per-section breakdown::

         ---
         **PROCEDURE: <SpecName>**
         **SECTION: §X.Y[.Z]**
         **PDF_PAGE: <page or range>**
         **INPUTS:** <verbatim inputs/parameters line, optional>

         **PROSE:** | **PSEUDOCODE:**
         <verbatim spec text, indented to taste — preserved verbatim>
         END_PROSE | END_PSEUDOCODE
         ---

Examples::

    # Bulk-stub every NM_* procedure straight from the spec.
    python script/generate_procedure_stubs.py \\
        --spec "docs/03_05_02 Management Procedures v02.01.02 AS.txt" \\
        --prefix NM_ \\
        --family nm

    # Re-run from a curated extract.
    python script/generate_procedure_stubs.py \\
        --extract /tmp/nm_extracts.txt \\
        --family nm --force

Stubs land under ``xknx/management/procedures/<family>/`` and matching
skip-marked test files land under
``test/management_tests/procedures/<family>/``. Existing files are skipped
by default (idempotent re-runs); pass ``--force`` to overwrite.

The function inside each stub raises ``NotImplementedError`` with a spec
citation. Implementers replace the body and un-skip the test file.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys


@dataclass(frozen=True)
class FamilyConfig:
    """Where a family's source + test files live, and how to name them."""

    src_dir: Path
    test_dir: Path
    spec_doc: str  # e.g. "03.05.02"
    filename_prefix: str  # "nm_" / "dm_" / ...; empty for Configuration


REPO_ROOT = Path(__file__).resolve().parent.parent

FAMILIES: dict[str, FamilyConfig] = {
    "nm": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/nm",
        test_dir=REPO_ROOT / "test/management_tests/procedures/nm",
        spec_doc="03.05.02",
        filename_prefix="nm_",
    ),
    "dm": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/dm",
        test_dir=REPO_ROOT / "test/management_tests/procedures/dm",
        spec_doc="03.05.02",
        filename_prefix="dm_",
    ),
    "dmp": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/dmp",
        test_dir=REPO_ROOT / "test/management_tests/procedures/dmp",
        spec_doc="03.05.02",
        filename_prefix="dmp_",
    ),
    "ftp": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/ftp",
        test_dir=REPO_ROOT / "test/management_tests/procedures/ftp",
        spec_doc="03.05.02",
        filename_prefix="ftp_",
    ),
    "configuration/common": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/configuration/common",
        test_dir=REPO_ROOT / "test/management_tests/procedures/configuration/common",
        spec_doc="03.05.03",
        filename_prefix="",
    ),
    "configuration/s_mode": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/configuration/s_mode",
        test_dir=REPO_ROOT / "test/management_tests/procedures/configuration/s_mode",
        spec_doc="03.05.03",
        filename_prefix="",
    ),
    "configuration/e_mode": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/configuration/e_mode",
        test_dir=REPO_ROOT / "test/management_tests/procedures/configuration/e_mode",
        spec_doc="03.05.03",
        filename_prefix="",
    ),
    "configuration/pb_mode": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/configuration/pb_mode",
        test_dir=REPO_ROOT / "test/management_tests/procedures/configuration/pb_mode",
        spec_doc="03.05.03",
        filename_prefix="",
    ),
    "configuration/ctrl_mode": FamilyConfig(
        src_dir=REPO_ROOT / "xknx/management/procedures/configuration/ctrl_mode",
        test_dir=REPO_ROOT / "test/management_tests/procedures/configuration/ctrl_mode",
        spec_doc="03.05.03",
        filename_prefix="",
    ),
}


@dataclass(frozen=True)
class ProcedureExtract:
    """One procedure parsed out of the extract file."""

    proc_name: str  # spec name, e.g. "NM_DomainAddress_Read"
    section: str  # e.g. "§2.7"
    page: str  # e.g. "18" or "18-19"
    inputs: str
    body_kind: str  # "PSEUDOCODE", "PROSE", or "NOTE"
    body: str


PROCEDURE_RE = re.compile(r"\*\*PROCEDURE:\s*(\S+?)\*\*")
SECTION_RE = re.compile(r"\*\*SECTION:\s*(§\S+)\*\*")
PAGE_RE = re.compile(r"\*\*PDF_PAGE:\s*([^*]+?)\*\*")
INPUTS_RE = re.compile(r"\*\*INPUTS:\*\*\s*([^\n]+)")
BODY_RE = re.compile(r"\*\*(PROSE|PSEUDOCODE):\*\*\s*\n(.*?)\nEND_\1", re.DOTALL)

# Spec-text extraction patterns (pdftotext -layout output of KNX standards).
# Matches ANY section header in the spec (e.g. `3 Device Management
# Procedures`, `2.23.5.1 Procedure`, `2.14.1.2.2 NM_DomainAddress_Scan2`).
# Both single-digit (`3 ...`) and multi-level (`2.14.1.2.2 ...`) numbers
# are accepted because EVERY heading must mark a body boundary, otherwise
# §2.24's body would bleed into §3's prose when no §3.x heading carries
# an underscored name yet (e.g. §3 Introduction).
SPEC_ANY_HEADER_RE = re.compile(
    r"^[ \t\f]*(?P<num>\d+(?:\.\d+)*)[ \t]+"
    r"(?:Procedure:[ \t]+)?"
    # Tab/space-separated words only — \s would eat the trailing newline
    # and pull the body line into the captured name.
    r"(?P<name>[A-Z][A-Za-z0-9_]*(?:[ \t]+[A-Za-z0-9_]+)*)[ \t]*$",
    re.MULTILINE,
)
# KNX procedure names always contain at least one underscore and no
# whitespace. We use this to decide which headers turn into stubs.
_PROCEDURE_NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+$")
SPEC_PAGE_RE = re.compile(r"page\s+(\d+)\s+of\s+\d+", re.IGNORECASE)
# Matches PDF page-break leftovers — copyright lines and the running
# "KNX Standard <chapter> <section>" header line that follows. Both lines
# typically appear indented to the centre of the page, so we allow leading
# whitespace.
SPEC_FOOTER_RE = re.compile(
    r"^[ \t\f]*(?:©\s+Copyright|KNX Standard\b).*$", re.MULTILINE
)
SPEC_BLANK_RUN_RE = re.compile(r"\n{3,}")


def parse_extract(extract_text: str) -> list[ProcedureExtract]:
    """Split the extract text into per-procedure blocks."""
    chunks = [c.strip() for c in extract_text.split("\n---\n") if c.strip()]
    results: list[ProcedureExtract] = []
    for chunk in chunks:
        m_proc = PROCEDURE_RE.search(chunk)
        m_sec = SECTION_RE.search(chunk)
        m_page = PAGE_RE.search(chunk)
        if not (m_proc and m_sec and m_page):
            continue
        m_in = INPUTS_RE.search(chunk)
        m_body = BODY_RE.search(chunk)
        results.append(
            ProcedureExtract(
                proc_name=m_proc.group(1),
                section=m_sec.group(1),
                page=m_page.group(1).strip(),
                inputs=m_in.group(1).strip() if m_in else "",
                body_kind=m_body.group(1) if m_body else "NOTE",
                body=m_body.group(2).strip() if m_body else "[spec text unavailable]",
            )
        )
    return results


def extract_from_spec(
    spec_text: str, prefix_filter: str | None = None
) -> list[ProcedureExtract]:
    """
    Walk a KNX spec txt (pdftotext output) and emit one ProcedureExtract per section.

    Each section heading like ``2.7  NM_DomainAddress_Read`` becomes one
    ProcedureExtract carrying the verbatim text from after that heading up to
    the next section heading, minus copyright / page-header footer lines.

    ``prefix_filter`` (e.g. ``"NM_"``) restricts emission to procedures whose
    name starts with the given prefix. Pass ``None`` to capture every match.
    """
    matches = list(SPEC_ANY_HEADER_RE.finditer(spec_text))
    extracts: list[ProcedureExtract] = []
    for i, match in enumerate(matches):
        proc_name = match.group("name").strip()
        # Skip headers that aren't named procedures (no underscore, contains
        # spaces, etc.). They still act as body boundaries above.
        if not _PROCEDURE_NAME_RE.match(proc_name):
            continue
        if prefix_filter and not proc_name.startswith(prefix_filter):
            continue
        section_num = match.group("num")
        body_start = match.end()
        # Extend body through every descendant sub-section (e.g. §2.23.5
        # NM_Coupler_Scan_LocalSubnetwork has §2.23.5.1 Procedure,
        # §2.23.5.2 Management Server support, etc. that all belong to it).
        # Stop at the first sibling or higher-level heading.
        section_prefix = section_num + "."
        body_end = len(spec_text)
        for j in range(i + 1, len(matches)):
            next_num = matches[j].group("num")
            if not next_num.startswith(section_prefix):
                body_end = matches[j].start()
                break
        body_text = spec_text[body_start:body_end]
        body_text = SPEC_FOOTER_RE.sub("", body_text)
        body_text = SPEC_BLANK_RUN_RE.sub("\n\n", body_text).strip()
        page = ""
        prefix_text = spec_text[:body_start]
        page_matches = list(SPEC_PAGE_RE.finditer(prefix_text))
        if page_matches:
            page = page_matches[-1].group(1)
        extracts.append(
            ProcedureExtract(
                proc_name=proc_name,
                section=f"§{section_num}",
                page=page,
                inputs="(see body)",
                body_kind="VERBATIM",
                body=body_text or "[spec text unavailable]",
            )
        )
    return extracts


def to_snake_case(spec_name: str) -> str:
    """``NM_DomainAddress_Read`` -> ``nm_domain_address_read``."""
    # camelCase / PascalCase to snake_case
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", spec_name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = s.lower().replace("__", "_")
    return s


def filename_for(proc_name: str, family: FamilyConfig) -> str:
    """Derive the on-disk module name from the spec procedure name."""
    snake = to_snake_case(proc_name)
    # If the snake_case name already starts with the family prefix, don't double it.
    if family.filename_prefix and snake.startswith(family.filename_prefix):
        return f"{snake}.py"
    return f"{family.filename_prefix}{snake}.py"


def indent_docstring(body: str, indent: str = "    ") -> str:
    """Indent each line and escape embedded triple quotes for safe docstring use."""
    safe = body.replace('"""', '\\"\\"\\"')
    return "\n".join(
        f"{indent}{line}".rstrip() if line.strip() else "" for line in safe.splitlines()
    )


SRC_TEMPLATE = '''\
"""
{proc} — KNX {spec} {section} (PDF p. {page}).

{verbatim_marker} (verbatim from spec):

{body_indented}

Inputs (from spec):
    {inputs}
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def {fname}(xknx: XKNX) -> None:
    """{proc} — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "{proc} (KNX {spec} {section}) — implementation pending"
    )
'''

TEST_TEMPLATE = '''\
"""Tests for {fname} — KNX {spec} {section} {proc}."""

import pytest

{import_block}

{pytestmark_block}


async def test_{fname}_placeholder() -> None:
    """Placeholder for {section} {proc} scenarios. Add real cases when impl lands."""
    _ = {fname}  # silence unused-import for the skipped test
'''


def render_src(
    extract: ProcedureExtract, fname_stem: str, family: FamilyConfig
) -> str:
    """Produce the source file contents for one stub."""
    verbatim_marker = (
        "Spec pseudocode" if extract.body_kind == "PSEUDOCODE" else "Spec text"
    )
    return SRC_TEMPLATE.format(
        proc=extract.proc_name,
        spec=family.spec_doc,
        section=extract.section,
        page=extract.page,
        verbatim_marker=verbatim_marker,
        body_indented=indent_docstring(extract.body),
        inputs=extract.inputs or "(none specified in spec)",
        fname=fname_stem,
    )


def render_test(
    extract: ProcedureExtract,
    fname_stem: str,
    family_key: str,
    family: FamilyConfig,
) -> str:
    """Produce the test file contents for one stub.

    Pre-wraps the ``pytestmark`` and import lines when they would exceed ruff's
    default line length (88 chars) so that re-running the script + ``ruff
    format`` is a no-op against committed content.
    """
    module_path = family_key.replace("/", ".")
    pytestmark_oneline = (
        f'pytestmark = pytest.mark.skip(reason="{fname_stem} — implementation pending")'
    )
    import_oneline = (
        f"from xknx.management.procedures.{module_path}.{fname_stem} import {fname_stem}"
    )
    pytestmark_block = (
        f'pytestmark = pytest.mark.skip(reason="{fname_stem} — implementation pending")'
        if len(pytestmark_oneline) <= 88
        else 'pytestmark = pytest.mark.skip(\n'
        f'    reason="{fname_stem} — implementation pending"\n'
        ')'
    )
    import_block = (
        f"from xknx.management.procedures.{module_path}.{fname_stem} import {fname_stem}"
        if len(import_oneline) <= 88
        else (
            f"from xknx.management.procedures.{module_path}.{fname_stem} import (\n"
            f"    {fname_stem},\n"
            ")"
        )
    )
    return TEST_TEMPLATE.format(
        fname=fname_stem,
        spec=family.spec_doc,
        section=extract.section,
        proc=extract.proc_name,
        import_block=import_block,
        pytestmark_block=pytestmark_block,
    )


def generate(
    family_key: str,
    *,
    extract_path: Path | None = None,
    spec_path: Path | None = None,
    prefix_filter: str | None = None,
    force: bool = False,
) -> tuple[int, int]:
    """
    Write stubs + tests for every procedure parsed from the source.

    Pass either:

      - ``extract_path``: a hand-curated extract file in the documented format.
      - ``spec_path``: a raw KNX spec txt (pdftotext output) plus an optional
        ``prefix_filter`` (e.g. ``"NM_"``).

    By default existing files are skipped (idempotent re-runs are no-ops).
    With ``force=True`` existing files are overwritten — useful when iterating
    on the template and verifying via ``git diff`` that the script reproduces
    committed content faithfully.

    Returns ``(written, skipped)`` counts.
    """
    if family_key not in FAMILIES:
        raise SystemExit(
            f"Unknown family {family_key!r}; choose from: {sorted(FAMILIES)}"
        )
    if (extract_path is None) == (spec_path is None):
        raise SystemExit("Pass exactly one of extract_path / spec_path")
    family = FAMILIES[family_key]
    if not family.src_dir.is_dir():
        raise SystemExit(f"Source directory {family.src_dir} does not exist")
    if not family.test_dir.is_dir():
        family.test_dir.mkdir(parents=True, exist_ok=True)

    if extract_path is not None:
        procedures = parse_extract(extract_path.read_text())
        source_desc = str(extract_path)
    else:
        assert spec_path is not None
        procedures = extract_from_spec(spec_path.read_text(), prefix_filter)
        source_desc = (
            f"{spec_path} (prefix={prefix_filter})" if prefix_filter else str(spec_path)
        )
    print(f"Parsed {len(procedures)} procedures from {source_desc}")

    written_paths: list[Path] = []

    written = 0
    skipped = 0
    for extract in procedures:
        fname_stem = filename_for(extract.proc_name, family).removesuffix(".py")
        src_path = family.src_dir / f"{fname_stem}.py"
        test_path = family.test_dir / f"test_{fname_stem}.py"
        if src_path.exists() and not force:
            print(f"  SKIP exists: {src_path.relative_to(REPO_ROOT)}")
            skipped += 1
            continue
        already_existed = src_path.exists()
        if already_existed and _is_implemented(src_path):
            # The src has a real implementation (no NotImplementedError
            # sentinel). Only refresh the module docstring; leave the body
            # alone and never touch the test file.
            new_doc = _extract_module_docstring(
                render_src(extract, fname_stem, family)
            )
            existing = src_path.read_text()
            existing_doc = _extract_module_docstring(existing)
            src_path.write_text(existing.replace(existing_doc, new_doc, 1))
            print(f"  REFRESHED docstring: {src_path.relative_to(REPO_ROOT)}")
            written += 1
            continue
        src_path.write_text(render_src(extract, fname_stem, family))
        test_path.write_text(render_test(extract, fname_stem, family_key, family))
        verb = "OVERWROTE" if already_existed else "WROTE"
        print(f"  {verb}: {src_path.relative_to(REPO_ROOT)} + test")
        written += 1
    return written, skipped


_DOCSTRING_RE = re.compile(r'^"""(?:.|\n)*?"""\n', re.MULTILINE)


def _extract_module_docstring(text: str) -> str:
    """Return the leading module docstring (including both triple-quote delimiters)."""
    m = _DOCSTRING_RE.match(text)
    if not m:
        raise SystemExit("no leading module docstring found")
    return m.group(0)


def _is_implemented(src_path: Path) -> bool:
    """A stub raises NotImplementedError; anything else is a real implementation."""
    try:
        text = src_path.read_text()
    except OSError:
        return False
    return "raise NotImplementedError" not in text


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--extract",
        type=Path,
        help="Path to a hand-curated extract file (see module docstring for format).",
    )
    source.add_argument(
        "--spec",
        type=Path,
        help="Path to a raw KNX spec txt (pdftotext output); the script will parse "
        "section headings directly.",
    )
    parser.add_argument(
        "--prefix",
        default=None,
        help='Restrict --spec to procedures whose name starts with this prefix '
        '(e.g. "NM_", "DMP_"). Ignored with --extract.',
    )
    parser.add_argument(
        "--family",
        required=True,
        choices=sorted(FAMILIES),
        help="Procedure family. Picks src/test directories and filename prefix.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files instead of skipping them.",
    )
    args = parser.parse_args(argv)

    written, skipped = generate(
        args.family,
        extract_path=args.extract,
        spec_path=args.spec,
        prefix_filter=args.prefix,
        force=args.force,
    )
    print(f"Done. Written: {written}. Skipped (already exist): {skipped}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
