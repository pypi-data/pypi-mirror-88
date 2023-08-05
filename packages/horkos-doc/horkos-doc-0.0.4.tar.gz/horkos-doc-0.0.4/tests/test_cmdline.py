import os
from os import path
import tempfile

import horkos
import pytest

import horkos_doc
from horkos_doc import _cmdline

MY_DIR = path.dirname(__file__)
RESOURCE_DIR = path.join(MY_DIR, 'resources')
SCHEMAS_DIR = path.join(RESOURCE_DIR, 'schemas')
CONFIG_FILE = path.join(RESOURCE_DIR, 'horkos-doc.config')


def test_render_catalog_happy_path():
    """Should be able to generate html from yaml files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        _cmdline.main(['-c', CONFIG_FILE, '-o', tmpdirname, SCHEMAS_DIR])

        generated_root = os.listdir(tmpdirname)
        schemas_html = os.listdir(path.join(tmpdirname, 'schemas'))

    assert 'index.html' in generated_root
    assert len(schemas_html) > 2


def test_render_catalog_without_config():
    """Should be able to generate html from yaml files without config."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        _cmdline.main(['-o', tmpdirname, SCHEMAS_DIR])

        generated_root = os.listdir(tmpdirname)
        schemas_html = os.listdir(path.join(tmpdirname, 'schemas'))

    assert 'index.html' in generated_root
    assert len(schemas_html) > 2


def test_render_catalog_fails_without_input_arg():
    """Should exit if `input` is omitted."""
    with pytest.raises(SystemExit):
        with tempfile.TemporaryDirectory() as tmpdirname:
            _cmdline.main(['-o', tmpdirname])


def test_render_catalog_fails_without_valid_schema():
    """Should exit if a parsed schema is bad."""
    schema_dir = path.join(RESOURCE_DIR, 'erant-schemas')
    with pytest.raises(SystemExit):
        with tempfile.TemporaryDirectory() as tmpdirname:
            _cmdline.main(['-o', tmpdirname, schema_dir])
