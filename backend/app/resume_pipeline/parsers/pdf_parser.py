import logging

logger = logging.getLogger('app.resume_pipeline.pdf_parser')


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Try to extract text deterministically from PDF bytes using pdfplumber if available.
    Returns extracted text (possibly empty) and raises on fatal errors.
    """
    try:
        import pdfplumber
    except Exception:
        logger.warning('pdfplumber not available; returning empty text')
        return ''

    try:
        import io
        txt = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                try:
                    page_text = page.extract_text() or ''
                except Exception:
                    page_text = ''
                txt.append(page_text)
        return '\n'.join(txt)
    except Exception as exc:
        logger.exception('PDF parsing failed')
        return ''
