class ArticleGenerationError(Exception):
    """Levantada quando a geração de artigo via provedor de IA falha."""


class WordPressPublishError(Exception):
    """Levantada quando a publicação no WordPress falha."""
