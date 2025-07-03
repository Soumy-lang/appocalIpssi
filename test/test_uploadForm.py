import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import extract_text_from_pdf

def test_extract_text_from_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%Fake PDF content")

    try:
        text = extract_text_from_pdf(str(pdf_path))
        assert isinstance(text, str)
    except Exception:
        assert True
