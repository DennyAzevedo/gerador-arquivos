import { useMutation } from "@tanstack/react-query";

import { useAuth } from "../context/AuthContext";
import type { AuthUser, Credentials } from "../domain/types";
import { login } from "../services/authService";

export function useLogin() {
  const { startSession } = useAuth();

  return useMutation<AuthUser, Error, Credentials>({
    mutationFn: async (credentials) => {
      const token = await login(credentials);
      return startSession(token);
    },
  });
}
