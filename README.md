# PDFtoTXT-directory
Given directory and several subdirectories, convert PDFs, Word, and images into a mirrored directory txt file structure. The Program imports, typer, rich, pypdf, pymupdf, and pytesseract.

`src.file_type_detection.get_file_type(file_path)` classifies a file as `pdf`, `word`, `image`,
or `unsupported` based on its extension. Extensions are matched
case-insensitively.

`src.convert_to_text.can_convert_to_text(file_path)` uses that classification
to return `True` for supported PDF, Word, and image files, and `False` for
unsupported files.
