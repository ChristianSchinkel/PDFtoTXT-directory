# PDFtoTXT-directory

Place PDF files in `resources/`, including any nested folders, and run:

```bash
./app.py
```

Each PDF is converted to a `.txt` file in `data/` with the same relative
folder structure. For example, `resources/contracts/a.pdf` becomes
`data/contracts/a.txt`.

An explicit PDF or directory can also be supplied:

```bash
./app.py resources/contracts
```

`src.file_type_detection.get_file_type(file_path)` classifies a file as `pdf`, `word`, `image`,
or `unsupported` based on its extension. Extensions are matched
case-insensitively.

`src.convert_to_text.can_convert_to_text(file_path)` uses that classification
to return `True` for supported PDF, Word, and image files, and `False` for
unsupported files.

`src.converter.convert_file_to_text(file_path)` converts a supported file and
returns its extracted text. PDF conversion uses `pypdf`, DOCX conversion uses
`python-docx`, and image conversion uses `pillow` and `pytesseract`.
