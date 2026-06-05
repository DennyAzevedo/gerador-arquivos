from uuid import UUID


class ArticleNotFoundError(Exception):
    """Levantada quando um artigo não existe ou não pertence ao usuário."""

    def __init__(self, article_id: UUID) -> None:
        super().__init__(f"Article {article_id} not found")
        self.article_id = article_id
