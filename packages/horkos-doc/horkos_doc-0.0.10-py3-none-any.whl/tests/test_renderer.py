import os
from os import path
import tempfile

import horkos
import horkos_doc
from horkos_doc import _renderer

MY_DIR = path.dirname(__file__)
RESOURCE_DIR = path.join(MY_DIR, 'resources')
SCHEMAS_DIR = path.join(RESOURCE_DIR, 'schemas')


def create_test_catalog() -> horkos.Catalog:
    """Create a generic catalog."""
    return horkos.Catalog(
        path.join(SCHEMAS_DIR, f) for f in os.listdir(SCHEMAS_DIR)
    )


def test_render_catalog_without_error():
    """Should be able to render a catalog without error"""
    catalog = create_test_catalog()
    with tempfile.TemporaryDirectory() as tmpdirname:
        context = horkos_doc.Context(build_dir=tmpdirname)
        _renderer.render_catalog(catalog, context)
