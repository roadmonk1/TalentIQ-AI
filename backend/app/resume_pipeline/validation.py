import hashlib
import logging
from .config import MAX_FILE_SIZE_BYTES

logger = logging.getLogger('app.resume_pipeline.validation')

# Simple in-memory duplicate cache (for demo). In prod, use DB.
_seen_hashes = set()


def compute_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


def validate_upload(filename: str, file_bytes: bytes):
    """Validate file size, basic format, duplicates, and simple scanned/encrypted detection.

    Returns: (valid: bool, reason: str or None, meta: dict)
    """
    if not filename:
        return False, 'missing_filename', {}

    if len(file_bytes) == 0:
        return False, 'empty_file', {}

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return False, 'file_too_large', {}

    h = compute_hash(file_bytes)
    if h in _seen_hashes:
        return False, 'duplicate_file', {'hash': h}

    # Basic file signature checks
    meta = {}
    if filename.lower().endswith('.pdf'):
        # check PDF header
        if not file_bytes.startswith(b'%PDF'):
            return False, 'invalid_pdf', {}
    elif filename.lower().endswith('.docx'):
        # docx is a zip file; check PK header
        if not file_bytes.startswith(b'PK'):
            return False, 'invalid_docx', {}
    else:
        return False, 'unsupported_format', {}

    # simple scanned detection heuristic: if few ASCII letters after extraction stage (handled by parser)
    # here just accept and let parser detect scanned PDFs

    # mark seen
    _seen_hashes.add(h)
    meta['hash'] = h
    return True, None, meta
