import os


def resolve_test_database_url() -> str:
    explicit = os.getenv("TEST_DATABASE_URL")
    if explicit:
        return explicit

    base_url = os.getenv("DATABASE_URL")
    if base_url:
        if "gerador_artigos_test" in base_url:
            return base_url
        if "gerador_artigos" in base_url:
            return base_url.replace("gerador_artigos", "gerador_artigos_test", 1)

    return (
        "postgresql+asyncpg://denny:M%40109G6Gustav@localhost:5432/gerador_artigos_test"
    )
