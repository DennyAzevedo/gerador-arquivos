from app.application.articles.ports.article_generator import (
    ArticleGenerationInput,
    ArticleGenerator,
    GeneratedArticle,
)


class GenerateArticleUseCase:
    """Gera o conteúdo de um artigo via IA. Não persiste nada."""

    def __init__(self, generator: ArticleGenerator) -> None:
        self._generator = generator

    async def execute(self, data: ArticleGenerationInput) -> GeneratedArticle:
        return await self._generator.generate(data)
