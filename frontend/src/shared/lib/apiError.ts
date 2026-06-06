import { AxiosError } from "axios";

const KNOWN_MESSAGES: Record<string, string> = {
  LOGIN_BAD_CREDENTIALS: "E-mail ou senha inválidos.",
  LOGIN_USER_NOT_VERIFIED: "Usuário não verificado.",
  REGISTER_USER_ALREADY_EXISTS: "Já existe uma conta com este e-mail.",
  REGISTER_INVALID_PASSWORD: "A senha não atende aos requisitos mínimos.",
};

function formatValidationDetail(detail: unknown): string | null {
  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => {
        if (typeof item === "object" && item !== null && "msg" in item) {
          return String((item as { msg: string }).msg);
        }
        return null;
      })
      .filter((message): message is string => message !== null);
    return messages.length > 0 ? messages.join(" ") : null;
  }

  if (typeof detail === "object" && detail !== null && "msg" in detail) {
    return String((detail as { msg: string }).msg);
  }

  return null;
}

export function getApiErrorMessage(
  error: unknown,
  fallback = "Ocorreu um erro. Tente novamente.",
): string {
  if (!(error instanceof AxiosError)) {
    return fallback;
  }

  if (!error.response) {
    return "Não foi possível conectar ao servidor. Verifique sua conexão.";
  }

  const { status, data } = error.response;
  const detail = data?.detail;

  if (typeof detail === "string") {
    return KNOWN_MESSAGES[detail] ?? detail;
  }

  const validationMessage = formatValidationDetail(detail);
  if (validationMessage) {
    return validationMessage;
  }

  if (status === 401) {
    return "Sessão expirada. Faça login novamente.";
  }
  if (status === 404) {
    return "Recurso não encontrado.";
  }
  if (status === 502) {
    return "Serviço temporariamente indisponível. Tente novamente.";
  }

  return fallback;
}
