import { describe, expect, it, vi } from "vitest";

import { DashboardPage } from "../../../src/features/articles/pages/DashboardPage";
import { renderWithProviders } from "../../test-utils";

vi.mock("../../../src/features/articles/hooks/useArticles", () => ({
  useArticles: vi.fn(),
}));

vi.mock("../../../src/features/articles/hooks/useDeleteArticle", () => ({
  useDeleteArticle: () => ({
    mutate: vi.fn(),
    isPending: false,
  }),
}));

import { useArticles } from "../../../src/features/articles/hooks/useArticles";

describe("DashboardPage", () => {
  it("exibe estado de carregamento", () => {
    vi.mocked(useArticles).mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
      error: null,
    } as ReturnType<typeof useArticles>);

    const { getByText } = renderWithProviders(<DashboardPage />);
    expect(getByText("Meus artigos")).toBeInTheDocument();
  });

  it("exibe estado vazio com CTA", () => {
    vi.mocked(useArticles).mockReturnValue({
      data: [],
      isLoading: false,
      isError: false,
      error: null,
    } as ReturnType<typeof useArticles>);

    const { getByText } = renderWithProviders(<DashboardPage />);
    expect(getByText("Você ainda não tem artigos.")).toBeInTheDocument();
    expect(getByText("Gerar meu primeiro artigo")).toBeInTheDocument();
  });

  it("exibe erro ao falhar carregamento", () => {
    vi.mocked(useArticles).mockReturnValue({
      data: undefined,
      isLoading: false,
      isError: true,
      error: new Error("falha"),
    } as ReturnType<typeof useArticles>);

    const { getByText } = renderWithProviders(<DashboardPage />);
    expect(getByText("Erro ao carregar")).toBeInTheDocument();
  });
});
