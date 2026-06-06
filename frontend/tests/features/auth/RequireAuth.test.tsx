import { Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { RequireAuth } from "../../../src/features/auth/components/RequireAuth";
import { renderWithProviders } from "../../test-utils";

vi.mock("../../../src/features/auth/context/AuthContext", () => ({
  useAuth: vi.fn(),
}));

import { useAuth } from "../../../src/features/auth/context/AuthContext";

describe("RequireAuth", () => {
  it("redireciona para login quando não autenticado", () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      status: "unauthenticated",
      startSession: vi.fn(),
      endSession: vi.fn(),
    });

    const { getByText } = renderWithProviders(
      <Routes>
        <Route element={<RequireAuth />}>
          <Route path="/articles/generate" element={<div>Protegido</div>} />
        </Route>
        <Route path="/login" element={<div>Página de login</div>} />
      </Routes>,
      { route: "/articles/generate" },
    );
    expect(getByText("Página de login")).toBeInTheDocument();
  });

  it("renderiza rota protegida quando autenticado", () => {
    vi.mocked(useAuth).mockReturnValue({
      user: {
        id: "1",
        email: "user@exemplo.com",
        isActive: true,
        isSuperuser: false,
        isVerified: false,
      },
      status: "authenticated",
      startSession: vi.fn(),
      endSession: vi.fn(),
    });

    const { getByText } = renderWithProviders(
      <Routes>
        <Route element={<RequireAuth />}>
          <Route path="/" element={<div>Conteúdo protegido</div>} />
        </Route>
      </Routes>,
      { route: "/" },
    );
    expect(getByText("Conteúdo protegido")).toBeInTheDocument();
  });
});
