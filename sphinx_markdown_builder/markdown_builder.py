from .markdown_writer import MarkdownWriter, MarkdownTranslator
from docutils.io import StringOutput
from io import open
from os import path
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import ensuredir, os_path

logger = logging.getLogger(__name__)

class MarkdownBuilder(Builder):
    name = 'markdown'
    format = 'markdown'
    epilog = __('The markdown files are in %(outdir)s.')

    allow_parallel = True
    default_translator_class = MarkdownTranslator

    current_docname = None

    def init(self):
        self.secnumbers = {}

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = path.join(self.outdir, docname + self.config.markdown_ext)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                pass

    def get_target_uri(self, docname: str, typ=None):
        # Returns the target markdown file name
        ext = self.config.markdown_target_ext
        if ext is None:
          ext = self.config.markdown_ext
        return docname + ext

    def prepare_writing(self, docnames):
        self.writer = MarkdownWriter(self)

    def write_doc(self, docname, doctree):
        self.current_docname = docname
        self.secnumbers = self.env.toc_secnumbers.get(docname, {})
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = path.join(
            self.outdir,
            os_path(docname) + self.config.markdown_ext
        )
        ensuredir(path.dirname(outfilename))
        try:
            with open(outfilename, 'w', encoding='utf-8') as f:  # type: ignore
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            logger.warning(__('error writing file %s: %s'), outfilename, err)

    def finish(self):
        pass
