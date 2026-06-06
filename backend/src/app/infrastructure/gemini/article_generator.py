import json
import logging

from google import genai
from google.genai import types
from pydantic import BaseModel

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


class _ArticleOutput(BaseModel):
    title: str
    content: str


class GeminiArticleGenerator(ArticleGenerator):
    """Adapter que isola o SDK do Gemini atrás da porta ArticleGenerator."""

    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model

    async def generate(self, data: ArticleGenerationInput) -> GeneratedArticle:
        prompt = f"{SYSTEM_PROMPT}\n\n{self._build_prompt(data)}"
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=_ArticleOutput,
                ),
            )
        except Exception as exc:
            logger.exception("Gemini generation request failed")
            raise ArticleGenerationError("Falha ao gerar o artigo via Gemini") from exc

        if isinstance(response.parsed, _ArticleOutput):
            return GeneratedArticle(
                title=response.parsed.title,
                content=response.parsed.content,
            )

        raw_content = response.text or ""
        try:
            payload = json.loads(raw_content)
            return GeneratedArticle(title=payload["title"], content=payload["content"])
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.error("Unexpected Gemini response format: %s", raw_content[:500])
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
