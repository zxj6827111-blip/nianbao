from api.core.diff.text import split_sentences
from api.core.facts.numbers import align_facts, extract_facts


def test_extract_and_align_numeric_facts():
    left_sentences = split_sentences("召开新闻发布会10场，发布信息200条。")
    right_sentences = split_sentences("召开新闻发布会12场，发布信息260条。")
    left_facts = extract_facts("sec_1", left_sentences)
    right_facts = extract_facts("sec_1", right_sentences)
    aligned = align_facts(left_facts, right_facts)
    assert "sec_1/召开新闻发布会" in aligned
    assert aligned["sec_1/召开新闻发布会"]["left"].value != aligned["sec_1/召开新闻发布会"]["right"].value
