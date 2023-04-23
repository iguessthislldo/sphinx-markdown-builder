from .markdown_builder import MarkdownBuilder

def setup(app):
    app.add_builder(MarkdownBuilder)
    app.add_config_value('markdown_ext', '.md', 'env')
    app.add_config_value('markdown_http_base', '', 'env')
    app.add_config_value('markdown_target_ext', None, 'env')
