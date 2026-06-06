import { Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { RequireGuest } from "../../../src/features/auth/components/RequireGuest";
import { renderWithProviders } from "../../test-utils";

vi.mock("../../../src/features/auth/context/AuthContext", () => ({
  useAuth: vi.fn(),
}));

import { useAuth } from "../../../src/features/auth/context/AuthContext";

describe("RequireGuest", () => {
  it("redireciona usuário autenticado para a home", () => {
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
        <Route element={<RequireGuest />}>
          <Route path="/login" element={<div>Página de login</div>} />
        </Route>
        <Route path="/" element={<div>Home</div>} />
      </Routes>,
      { route: "/login" },
    );
    expect(getByText("Home")).toBeInTheDocument();
  });
});
