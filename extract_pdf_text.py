from pathlib import Path
import subprocess
import importlib.util

PDFS = [
    "AI trafiklys for SAMF.pdf",
    "AI trafiklys for humanioria.pdf",
    "AI trafiklys for mat-naturfag.pdf",
]


def extract_with_pypdf(pdf_path: str) -> str:
    if importlib.util.find_spec("pypdf") is None:
        return ""
    try:
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n\n".join(pages)
    except Exception:
        return ""


def extract_with_textutil(pdf_path: str) -> str:
    try:
        proc = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", pdf_path],
            capture_output=True,
            check=False,
        )
        return proc.stdout.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def main() -> None:
    for pdf in PDFS:
        text = extract_with_pypdf(pdf)
        if not text.strip():
            text = extract_with_textutil(pdf)
        output_file = Path(pdf).with_suffix(".extracted.txt")
        output_file.write_text(text, encoding="utf-8")
        print(f"WROTE {output_file} chars={len(text)}")


if __name__ == "__main__":
    main()
