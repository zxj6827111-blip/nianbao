from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
DEFAULT_TEMPLATE = "report.html.j2"

env = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parents[2] / "templates")))


@dataclass
class ReportContext:
    summary: Dict[str, object]
    text_pairs: List[Dict[str, object]]
    tables: Dict[str, object]


def render_report(context: ReportContext) -> str:
    template = env.get_template(DEFAULT_TEMPLATE)
    return template.render(**context.summary, text_pairs=context.text_pairs, tables=context.tables)
