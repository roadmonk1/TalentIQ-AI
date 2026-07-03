import logging

logger = logging.getLogger('app.resume_pipeline.docx_parser')


def extract_text_from_docx_bytes(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes using python-docx if available.
    Returns extracted text (possibly empty) and raises on fatal errors.
    """
    try:
        from docx import Document
        import io
    except Exception:
        logger.warning('python-docx not available; returning empty text')
        return ''

    try:
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs]
        return '\n'.join(paragraphs)
    except Exception:
        logger.exception('DOCX parsing failed')
        return ''
