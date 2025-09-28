from pathlib import Path

from api.services.documents import DocumentService
from api.services.compare import CompareService

def read_sample(name: str) -> str:
    return (Path(__file__).resolve().parents[1] / 'api' / 'data' / 'samples' / name).read_text(encoding='utf-8')


def test_ingest_and_compare_flow():
    document_service = DocumentService()
    compare_service = CompareService()

    resp_left = document_service.ingest_text(text=read_sample('sample_2023.txt'), title='2023年政府信息公开工作年度报告')
    resp_right = document_service.ingest_text(text=read_sample('sample_2024.txt'), title='2024年政府信息公开工作年度报告')

    result = compare_service.compare(resp_left['doc_id'], resp_right['doc_id'])
    assert 'summary' in result
    assert result['summary']['text_reuse'] >= 0.0
    assert 'tables' in result
