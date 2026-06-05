import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import {
  clearAccessToken,
  getAccessToken,
  setAccessToken,
} from "../../../shared/lib/authStorage";
import type { AuthUser } from "../domain/types";
import { getCurrentUser } from "../services/authService";

type AuthStatus = "loading" | "authenticated" | "unauthenticated";

interface AuthContextValue {
  user: AuthUser | null;
  status: AuthStatus;
  startSession: (token: string) => Promise<AuthUser>;
  endSession: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [status, setStatus] = useState<AuthStatus>("loading");

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      setStatus("unauthenticated");
      return;
    }

    getCurrentUser()
      .then((currentUser) => {
        setUser(currentUser);
        setStatus("authenticated");
      })
      .catch(() => {
        clearAccessToken();
        setStatus("unauthenticated");
      });
  }, []);

  async function startSession(token: string): Promise<AuthUser> {
    setAccessToken(token);
    const currentUser = await getCurrentUser();
    setUser(currentUser);
    setStatus("authenticated");
    return currentUser;
  }

  function endSession(): void {
    clearAccessToken();
    setUser(null);
    setStatus("unauthenticated");
  }

  return (
    <AuthContext.Provider value={{ user, status, startSession, endSession }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider");
  }
  return context;
}
