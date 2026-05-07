
import pytest

@pytest.mark.parametrize("diff_text", [None, ""])
def test_is_boilerplate_heavy_null(diff_text):
    analyzer = AIAnalyzer()
    with pytest.raises(NullPointerException):
        analyzer._is_boilerplate_heavy(diff_text)
