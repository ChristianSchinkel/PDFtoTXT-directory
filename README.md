# PDFtoTXT-directory
Given directory and several subdirectories, convert PDFs, Word, and images into a mirrored directory txt file structure. The Program imports, typer, rich, pypdf, pymupdf, and pytesseract.

`src.main.get_file_type(file_path)` classifies a file as `pdf`, `word`, `image`,
or `unsupported` based on its extension. Extensions are matched
case-insensitively.
