import hashlib
import json
import os
from datetime import datetime

from app.config import UPLOAD_DIR


# Registry file
REGISTRY_DIR = os.path.join(
    os.path.dirname(UPLOAD_DIR),
    "registry"
)

REGISTRY_FILE = os.path.join(
    REGISTRY_DIR,
    "documents.json"
)


def _ensure_registry():
    """
    Make sure the registry directory and
    registry JSON file exist.
    """

    os.makedirs(
        REGISTRY_DIR,
        exist_ok=True
    )

    if not os.path.exists(REGISTRY_FILE):

        with open(
            REGISTRY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file,
                indent=4
            )


def calculate_file_hash(file_path):
    """
    Calculate SHA-256 hash of a file.

    The hash allows us to detect whether
    a document's actual content has changed.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as file:

        while True:

            data = file.read(1024 * 1024)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def load_registry():
    """
    Load the document registry.
    """

    _ensure_registry()

    with open(
        REGISTRY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_registry(registry):
    """
    Save the document registry.
    """

    _ensure_registry()

    with open(
        REGISTRY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )


def get_document(filename):
    """
    Get registry information for a filename.
    """

    registry = load_registry()

    return registry.get(
        filename
    )


def register_document(
    filename,
    file_hash,
    chunk_count=0
):
    """
    Add or update document information
    in the registry.
    """

    registry = load_registry()

    now = datetime.now().isoformat()

    existing = registry.get(
        filename
    )

    if existing:

        created_at = existing.get(
            "created_at",
            now
        )

    else:

        created_at = now

    registry[filename] = {
        "filename": filename,
        "file_hash": file_hash,
        "chunk_count": chunk_count,
        "created_at": created_at,
        "updated_at": now,
    }

    save_registry(
        registry
    )


def remove_document(filename):
    """
    Remove a document from the registry.
    """

    registry = load_registry()

    if filename in registry:

        del registry[filename]

        save_registry(
            registry
        )


def list_documents():
    """
    Return all registered documents.
    """

    registry = load_registry()

    return list(
        registry.values()
    )