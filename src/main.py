"""Convert a PDF file to plain text."""


from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from io import BytesIO
from pathlib import Path

import pymupdf  # type: ignore[import-untyped]
import pytesseract  # type: ignore[import-untyped]
from PIL import Image
from pypdf import PdfReader

ENCODING = "utf-8"
OCR_LANGUAGE = "swe"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def extract_text(pdf_path: Path, *, ocr: bool = True) -> str:
    """Extract text from a PDF, using OCR when the PDF has no text layer."""
    if pdf_path.stat().st_size == 0:
        raise ValueError(f"PDF file is empty: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"--- Page {page_number} ---\n{text.strip()}".rstrip())

    extracted = "\n\n".join(pages).strip()
    # Page headers alone are not useful text, so switch to OCR when every
    # page lacks a readable text layer.
    if extracted and any(page.strip() != f"--- Page {number} ---"
                         for number, page in enumerate(pages, start=1)):
        return f"Source: {pdf_path.name}\n\n{extracted}\n"

    if not ocr:
        return f"Source: {pdf_path.name}\n\n{extracted}\n"

    return _extract_with_ocr(pdf_path)


def _extract_with_ocr(pdf_path: Path) -> str:
    """Render pages and extract text with Tesseract."""
    try:
        document = pymupdf.open(str(pdf_path))
        pages = []
        for page_number in range(1, len(document) + 1):
            page = document.load_page(page_number - 1)
            # Render at 2x resolution to give Tesseract enough detail for
            # small document text while keeping OCR processing reasonable.
            image = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
            # pytesseract accepts a PIL image, not the raw PNG bytes returned
            # by PyMuPDF.
            pil_image = Image.open(BytesIO(image.tobytes("png")))
            text = pytesseract.image_to_string(
                pil_image, lang=OCR_LANGUAGE).strip()
            pages.append(f"--- Page {page_number} ---\n{text}".rstrip())
    except pytesseract.pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "OCR requires the Tesseract executable. Install it separately "
            "(for example, with 'brew install tesseract' on macOS)."
        ) from exc
    except RuntimeError as exc:
        raise RuntimeError(f"OCR failed for '{pdf_path}': {exc}") from exc
    finally:
        if "document" in locals():
            document.close()

    return f"Source: {pdf_path.name}\n\n{chr(10).join(pages)}\n"


def _pdf_files(input_path: Path) -> tuple[Path, Path, Iterable[Path]]:
    """Return the input root, output root, and PDFs to process."""
    if not input_path.is_absolute():
        input_path = PROJECT_ROOT / input_path
    output_root = PROJECT_ROOT / "data"
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"Input file is not a PDF: {input_path}")
        return input_path.parent, output_root, (input_path,)
    if input_path.is_dir():
        return input_path, output_root, sorted(
            path for path in input_path.rglob("*")
            if path.is_file() and path.suffix.lower() == ".pdf"
        )
    raise FileNotFoundError(f"Input path does not exist: {input_path}")


def convert(input_path: Path, *, ocr: bool = True) -> int:
    """Convert one PDF or all PDFs below a directory."""
    source_root, output_root, pdfs = _pdf_files(input_path)
    pdfs = tuple(pdfs)
    if not pdfs:
        raise FileNotFoundError(f"No PDF files found under: {input_path}")

    for pdf_path in pdfs:
        # Preserve the input tree below data/ so identically named PDFs do not
        # overwrite one another when a folder is processed recursively.
        relative_path = pdf_path.relative_to(source_root).with_suffix(".txt")
        output_path = output_root / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            extract_text(pdf_path, ocr=ocr), encoding=ENCODING)
        print(f"Wrote {output_path}")
    return len(pdfs)


def main(argv: list[str] | None = None) -> int:
    """Parse command-line arguments and convert PDFs."""
    dscrpt = (
        "Convert one PDF or all PDFs below a folder into text files under "
        "data/. Defaults to resources/."
    )
    help_text = "Path to a PDF file or folder (default: resources/)."
    # Parse command-line arguments
    if argv is None:
        argv = sys.argv[1:]  # Exclude the script name from the arguments
    parser = argparse.ArgumentParser(
        description=dscrpt  # Description of the command-line tool
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=PROJECT_ROOT / "resources",
        help=help_text,
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Do not use OCR when a PDF has no extractable text",
    )
    args = parser.parse_args(argv)

    try:
        convert(args.input, ocr=not args.no_ocr)
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
