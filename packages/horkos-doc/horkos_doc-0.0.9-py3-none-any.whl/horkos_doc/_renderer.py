import datetime
import json
from os import path
import typing
import urllib.parse

import bleach
import bs4
import horkos
import jinja2
import markdown
import yaml

from horkos_doc import _definitions
from horkos_doc import _site_generator

PACKAGE_DIR = path.dirname(path.realpath(__file__))
RESOURCE_DIR = path.join(PACKAGE_DIR, 'resources')


def first_paragraph(value: str) -> str:
    """Extract the first paragraph from a markdown string."""
    rendered = render_markdown(value)
    soup = bs4.BeautifulSoup(rendered, features="html.parser")
    return str(soup.find('p'))


def shorten(value: typing.Any) -> str:
    """
    Attempt to render the given value, shorten it if it is more
    than 20 characters.
    """
    result = json.dumps(value)
    if len(result) < 20:
        return result
    return f'{result[:16]}...'


def render_markdown(value: str) -> str:
    """Render the given markdown."""
    result = markdown.markdown(value, extensions=['fenced_code'])
    allowed = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
        'ol', 'strong', 'ul', 'p', 'pre'
    ]
    return bleach.clean(result, tags=allowed)


def yamilify_field(field: horkos.Field) -> str:
    """Convert a field to yaml."""
    return yaml.dump({
        'required': field.required,
        'nullable': field.nullable,
        'checks': [
            c.name if not c.args else {'name': c.name, 'args': c.args}
            for c in field.checks
        ],
        'labels': field.labels,
        'derived': field.derived,
    }, sort_keys=False)


def yamilify(value: typing.Any) -> str:
    """Convert anything to yaml."""
    return yaml.dump(value, sort_keys=False)


def _add_schema_files(
        gen: _site_generator.SiteGenerator,
        catalog: horkos.Catalog,
        context: _definitions.Context,
):
    schemas = sorted(catalog.schemas, key=lambda s: s.name)
    for i, schema in enumerate(schemas):
        bottom = max(i - 15, 0)
        top = bottom + 30
        if top > len(schemas):
            top = len(schemas)
            bottom = max(top - 30, 0)
        neighbors = schemas[bottom:top]
        cleaned = schema.name.replace(' ', '-').replace('/', '-')
        page_path = f'schemas/{cleaned}.html'
        gen.add_page(
            f'schemas/{schema.name}',
            page_path,
            'dataset.html',
            {
                'schema': schema,
                'context': context,
                'links': [
                    {
                        'to': f'schemas/{s.name}',
                        'text': s.name,
                        'bold': s.name == schema.name,
                    }
                    for s in neighbors
                ],
            },
        )

def _add_index_list(
        gen: _site_generator.SiteGenerator,
        catalog: horkos.Catalog,
        context: _definitions.Context,
):
    """Render a listing of all schemas in the catalog."""
    schemas = sorted(catalog.schemas, key=lambda s: s.name)
    gen.add_page(
        'index',
        'index.html',
        'listing.html',
        {'schemas': schemas, 'context': context}
    )


def _add_static_files(gen: _site_generator.SiteGenerator):
    gen.add_page('static/style', 'static/style.css', 'style.css')
    gen.add_page(
        'static/expand_script', 'static/expand_script.js', 'expand_script.js'
    )


def _add_search(
        gen: _site_generator.SiteGenerator,
        catalog: horkos.Catalog,
        context: _definitions.Context,
):
    gen.add_page('search', 'search.html', 'search.html')
    results = []
    for schema in catalog.schemas:
        base_url = gen.relative_url('search', f'schemas/{schema.name}')
        results.append({
            'title': [schema.name],
            'text': schema.description,
            'html': first_paragraph(schema.description),
            'link': base_url,
        })
        for field in schema.fields:
            results.append({
                'title': [schema.name, field.name],
                'text': field.description,
                'html': first_paragraph(field.description),
                'link': f'{base_url}#{urllib.parse.quote(field.name)}',
            })
    size = 100
    chunks = [results[i:i+size] for i in range(0, len(results), size)]
    search_indices = []
    for i, chunk in enumerate(chunks):
        gen.add_page(
            f'search-resources/{i}',
            f'search-resources/{i}.json',
            'raw_json.json',
            {'body': json.dumps(chunk)},
        )
        search_indices.append(
            gen.relative_url('search', f'search-resources/{i}')
        )
    # Add it again to use new args
    gen.add_page(
        'search', 'search.html', 'search.html',
        {'indices': json.dumps(search_indices), 'context': context}
    )


def render_catalog(
        catalog: horkos.Catalog,
        context: _definitions.Context = None,
):
    """Render the given catalog into the dest_path directory."""
    context = context or _definitions.Context()
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('horkos_doc', 'templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    env.filters['shorten'] = shorten
    env.filters['markdown'] = render_markdown
    env.filters['field_to_yaml'] = yamilify_field
    env.filters['to_yaml'] = yamilify
    env.filters['first_paragraph'] = first_paragraph
    env.globals['now'] = datetime.datetime.utcnow
    gen = _site_generator.SiteGenerator(env)
    _add_schema_files(gen, catalog, context)
    _add_static_files(gen)
    _add_index_list(gen, catalog, context)
    _add_search(gen, catalog, context)
    gen.render(context.build_dir)
