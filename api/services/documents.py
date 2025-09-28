from __future__ import annotations

from typing import Dict

from ..core.parsers.simple import ParsedDocument, parse_text_document
from ..core.recognize.auto import auto_detect
from ..models.datastore import DATABASE, Document


class DocumentService:
    def ingest_text(self, *, text: str, title: str = "", url: str = "") -> Dict[str, object]:
        parsed = parse_text_document(text)
        auto = auto_detect(text, url=url, title=title)
        document = DATABASE.create_document(
            title=title,
            year=auto.year,
            region_code=auto.region_code,
            org_name=auto.org_name,
            source_url=url,
        )
        self._store_sections(document, parsed)
        return {
            "doc_id": document.id,
            "auto": {
                "region_code": auto.region_code,
                "org_name": auto.org_name,
                "year": auto.year,
                "confidence": auto.confidence,
            },
        }

    def _store_sections(self, document: Document, parsed: ParsedDocument) -> None:
        for sec_key, content in parsed.sections.items():
            section = DATABASE.create_section(document.id, sec_key, content)
            if sec_key in parsed.tables and parsed.tables[sec_key]:
                table = DATABASE.create_table(section.id, sec_key)
                for key, value in sorted(parsed.tables[sec_key].items()):
                    DATABASE.create_cell(table.id, key, value)
