from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Document:
    id: int
    title: str
    year: Optional[int]
    region_code: Optional[str]
    org_name: Optional[str]
    source_url: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Section:
    id: int
    doc_id: int
    sec_key: str
    raw: str


@dataclass
class Table:
    id: int
    section_id: int
    table_key: str


@dataclass
class Cell:
    id: int
    table_id: int
    path_key: str
    value_raw: str


class Database:
    def __init__(self) -> None:
        self.documents: Dict[int, Document] = {}
        self.sections: Dict[int, Section] = {}
        self.tables: Dict[int, Table] = {}
        self.cells: Dict[int, Cell] = {}
        self.doc_counter = 1
        self.section_counter = 1
        self.table_counter = 1
        self.cell_counter = 1

    def create_document(
        self,
        *,
        title: str,
        year: Optional[int],
        region_code: Optional[str],
        org_name: Optional[str],
        source_url: str,
    ) -> Document:
        doc = Document(
            id=self.doc_counter,
            title=title,
            year=year,
            region_code=region_code,
            org_name=org_name,
            source_url=source_url,
        )
        self.documents[self.doc_counter] = doc
        self.doc_counter += 1
        return doc

    def create_section(self, doc_id: int, sec_key: str, raw: str) -> Section:
        section = Section(id=self.section_counter, doc_id=doc_id, sec_key=sec_key, raw=raw)
        self.sections[self.section_counter] = section
        self.section_counter += 1
        return section

    def create_table(self, section_id: int, table_key: str) -> Table:
        table = Table(id=self.table_counter, section_id=section_id, table_key=table_key)
        self.tables[self.table_counter] = table
        self.table_counter += 1
        return table

    def create_cell(self, table_id: int, path_key: str, value_raw: str) -> Cell:
        cell = Cell(id=self.cell_counter, table_id=table_id, path_key=path_key, value_raw=value_raw)
        self.cells[self.cell_counter] = cell
        self.cell_counter += 1
        return cell

    def get_document(self, doc_id: int) -> Optional[Document]:
        return self.documents.get(doc_id)

    def list_sections(self, doc_id: int) -> List[Section]:
        return [section for section in self.sections.values() if section.doc_id == doc_id]

    def get_section(self, doc_id: int, sec_key: str) -> Optional[Section]:
        for section in self.sections.values():
            if section.doc_id == doc_id and section.sec_key == sec_key:
                return section
        return None

    def get_table_by_section(self, section_id: int) -> Optional[Table]:
        for table in self.tables.values():
            if table.section_id == section_id:
                return table
        return None

    def list_cells(self, table_id: int) -> List[Cell]:
        return [cell for cell in self.cells.values() if cell.table_id == table_id]


DATABASE = Database()
