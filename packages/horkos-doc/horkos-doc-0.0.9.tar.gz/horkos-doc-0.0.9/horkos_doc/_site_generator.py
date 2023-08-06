import os
from os import path
import urllib.parse

import jinja2


class SiteGenerator:
    """class for aggregating site pages and rendering them to html."""

    def __init__(self, environment: jinja2.Environment):
        self._pages = {}
        self.environment = environment
        self.environment.filters['relative_url'] = self._get_path_for

    @jinja2.contextfilter
    def _get_path_for(
            self, context: jinja2.runtime.Context, page_name: str
    ) -> str:
        """
        Get the relative path from the page being rendered within the context
        to the given page_name.
        """
        return self.relative_url(context['_rendering_page_name'], page_name)


    def relative_url(self, source_page: str, dest_page: str) -> str:
        source_page = self._pages[source_page]
        dest_page = self._pages[dest_page]
        source_path = list(source_page['page_path'].split('/'))[:-1]
        dest_path = list(dest_page['page_path'].split('/'))

        diverge_at = 0
        for i, pair in enumerate(zip(source_path, dest_path)):
            diverge_at = i
            if pair[0] != pair[1]:
                break
        escaped = [urllib.parse.quote(s) for s in dest_path[diverge_at:]]
        back_up = len(source_path) - diverge_at
        return '/'.join(['..'] * back_up + escaped)


    def add_page(
            self,
            page_name: str,
            page_path: str,
            template_name: str,
            template_args: dict = None,
    ):
        args = dict(template_args or {})
        args['_rendering_page_name'] = page_name
        self._pages[page_name] = {
            'page_name': page_name,
            'page_path': page_path,
            'template_name': template_name,
            'template_args': args
        }

    def render(self, build_dir: str):
        for page in self._pages.values():
            template = self.environment.get_template(page['template_name'])
            rendered = template.render(
                **page['template_args'],
            )
            write_path = path.join(build_dir, page['page_path'])
            dirname = path.dirname(write_path)
            if not path.exists(dirname):
                os.makedirs(dirname)
            with open(write_path, 'w') as f:
                f.write(rendered)
