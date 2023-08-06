import argparse
import configparser
import os
from os import path
import re
import sys

import horkos
import horkos.errors

from horkos_doc import _definitions
from horkos_doc import _renderer

SCHEMA_FILE_RE = re.compile(r'.*\.(yaml|yml|json)$')


def _parse_config_file(config_file: str) -> dict:
    """Parse an incoming config file and extract all top level keys."""
    if not path.isfile(config_file):
        return {}
    parser = configparser.ConfigParser()
    parser.read(config_file)
    args = {
        'author': parser['default'].get('author'),
        'home_page': parser['default'].get('home_page'),
        'output': parser['default'].get('output'),
        'input': parser['default'].get('input'),
    }
    return {k: v for k, v in args.items() if v is not None}


def _parse(args: list = None) -> dict:
    """
    Parse the incoming command-line arguments as well as configuration file
    based arguments to come up with a working set of args.
    """
    parser = argparse.ArgumentParser('horkos-doc')
    defaults = {}
    parser.add_argument(
        '--config', '-c',
        help=(
            'The path to a configuration file for horkos-doc. This file can '
            'be used to override the built-in default for command-line '
            'arguments. By default this is `.horkos-doc`.'
        )
    )
    defaults['config'] = '.horkos-doc'
    parser.add_argument(
        '--author', '-a',
        help=(
            'The author of the documentation. This is used to create '
            'copyright statements within the generated documentation.'
        )
    )
    defaults['author'] = None
    parser.add_argument(
        '--home-page', '--hp',
        help=(
            'The name to use for the home page of the generated documentation.'
            ' By default this is "Horkos Doc".'
        ),
    )
    defaults['home_page'] = 'Horkos Doc'
    output_dir = path.join('.', 'build')
    parser.add_argument(
        '--output', '-o',
        help=(
            'The directory in which to store built html. By default this is '
            f'{output_dir}'
        ),
    )
    defaults['output'] = output_dir
    parser.add_argument(
        'input',
        nargs='?',
        help=(
            'A directory of schema files from which to build the html '
            'documentation. This is not required if a value is set within '
            'the given config file.'
        )
    )
    parsed = parser.parse_args(args)
    config_parsed = _parse_config_file(parsed.config or defaults['config'])

    result = defaults.copy()
    result.update({k: v for k, v in config_parsed.items() if v is not None})
    result.update({k: v for k, v in vars(parsed).items() if v is not None})
    if result.get('input') is None:
        parser.print_help(sys.stderr)
        msg = (
            '\nERROR: `input` must be specified on the command-line if '
            'not specified in the config file.'
        )
        print(msg, file=sys.stderr)
        sys.exit(1)
    return result


def _get_schema_file_paths(input_dir: str) -> list:
    """Get all of the schema files within an input directory."""
    result = []
    for root, _, files in os.walk(input_dir):
        result.extend(
            path.abspath(path.join(root, f))
            for f in files
            if SCHEMA_FILE_RE.match(f)
        )
    return result


def main(args: list = None):
    """Convert a set of horkos schema files into a static website."""
    parsed = _parse(args)
    schema_files = _get_schema_file_paths(parsed['input'])
    catalog = horkos.Catalog()
    for schema_file in schema_files:
        try:
            catalog.update(schema_file)
        except horkos.errors.SchemaValidationError:
            print(f'{schema_file} is not a valid schema file')
            sys.exit(1)
    context = _definitions.Context(
        build_dir=parsed['output'],
        home_page=parsed['home_page'],
        author=parsed['author'],
    )
    _renderer.render_catalog(catalog, context)
