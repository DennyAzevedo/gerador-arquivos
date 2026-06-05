import { AxiosError } from "axios";

const KNOWN_MESSAGES: Record<string, string> = {
  LOGIN_BAD_CREDENTIALS: "E-mail ou senha inválidos.",
  LOGIN_USER_NOT_VERIFIED: "Usuário não verificado.",
  REGISTER_USER_ALREADY_EXISTS: "Já existe uma conta com este e-mail.",
};

export function getApiErrorMessage(
  error: unknown,
  fallback = "Ocorreu um erro. Tente novamente.",
): string {
  if (error instanceof AxiosError) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string") {
      return KNOWN_MESSAGES[detail] ?? detail;
    }
  }
  return fallback;
}
