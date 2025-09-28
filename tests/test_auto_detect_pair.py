from api.core.recognize.auto import auto_detect


def test_auto_detect_from_url_and_text():
    text = "淮安市人民政府2024年政府信息公开工作年度报告"
    result = auto_detect(text=text, url="https://www.huaian.gov.cn/report.html", title="2024年年度报告")
    assert result.region_code == "320800"
    assert result.org_name == "淮安市人民政府"
    assert result.year == 2024
    assert result.confidence >= 0.7
