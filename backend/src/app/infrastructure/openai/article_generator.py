import json
import logging

from openai import AsyncOpenAI

from app.application.articles.exceptions import ArticleGenerationError
from app.application.articles.ports.article_generator import (
    ArticleGenerationInput,
    ArticleGenerator,
    GeneratedArticle,
)
from app.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Você é um redator especialista em conteúdo para blogs WordPress. "
    "Escreva artigos claros, bem estruturados e otimizados para SEO, em português do Brasil. "
    "Responda SEMPRE em JSON válido com exatamente as chaves 'title' (string) e "
    "'content' (string em Markdown)."
)


class OpenAIArticleGenerator(ArticleGenerator):
    """Adapter que isola o SDK da OpenAI atrás da porta ArticleGenerator."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    async def generate(self, data: ArticleGenerationInput) -> GeneratedArticle:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": self._build_prompt(data)},
                ],
                response_format={"type": "json_object"},
            )
        except Exception as exc:
            logger.exception("OpenAI generation request failed")
            raise ArticleGenerationError("Falha ao gerar o artigo via OpenAI") from exc

        raw_content = response.choices[0].message.content or ""
        try:
            payload = json.loads(raw_content)
            return GeneratedArticle(title=payload["title"], content=payload["content"])
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.error("Unexpected OpenAI response format: %s", raw_content[:500])
            raise ArticleGenerationError("Resposta inválida do provedor de IA") from exc

    @staticmethod
    def _build_prompt(data: ArticleGenerationInput) -> str:
        parts = [f"Escreva um artigo de blog sobre: {data.topic}."]
        if data.keywords:
            parts.append(f"Palavras-chave para SEO: {data.keywords}.")
        if data.tone:
            parts.append(f"Tom de escrita: {data.tone}.")
        parts.append(
            "O campo 'content' deve estar em Markdown, com introdução, subtítulos e conclusão."
        )
        return " ".join(parts)
