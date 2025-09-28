from api.core.diff.text import split_sentences


def test_boilerplate_removed():
    text = "根据《中华人民共和国政府信息公开条例》……\n本机关加强公开。"
    sentences = split_sentences(text)
    assert sentences == ["本机关加强公开。"]
