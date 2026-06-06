import { describe, expect, it, vi } from "vitest";

import { LoginForm } from "../../../src/features/auth/components/LoginForm";
import { renderWithProviders } from "../../test-utils";

vi.mock("../../../src/features/auth/hooks/useLogin", () => ({
  useLogin: () => ({
    mutate: vi.fn(),
    isPending: false,
    isError: false,
    error: null,
  }),
}));

describe("LoginForm", () => {
  it("exibe validação quando campos estão vazios", async () => {
    const { getByRole, findByText } = renderWithProviders(<LoginForm onSuccess={vi.fn()} />);
    getByRole("button", { name: "Entrar" }).click();
    expect(await findByText("E-mail inválido")).toBeInTheDocument();
    expect(await findByText("Informe a senha")).toBeInTheDocument();
  });
});
