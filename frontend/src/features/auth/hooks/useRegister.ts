import { useMutation } from "@tanstack/react-query";

import type { AuthUser, RegisterData } from "../domain/types";
import { register } from "../services/authService";

export function useRegister() {
  return useMutation<AuthUser, Error, RegisterData>({
    mutationFn: register,
  });
}
