import { AxiosError, type AxiosResponse, type InternalAxiosRequestConfig } from "axios";
import { describe, expect, it } from "vitest";

import { getApiErrorMessage } from "../../../src/shared/lib/apiError";

function createAxiosError(status: number, detail: unknown): AxiosError {
  const response = {
    status,
    data: { detail },
  } as AxiosResponse;
  const config = {} as InternalAxiosRequestConfig;
  return new AxiosError("Request failed", undefined, config, undefined, response);
}

describe("getApiErrorMessage", () => {
  it("traduz códigos conhecidos do backend", () => {
    const error = createAxiosError(400, "LOGIN_BAD_CREDENTIALS");
    expect(getApiErrorMessage(error)).toBe("E-mail ou senha inválidos.");
  });

  it("formata erros de validação em array", () => {
    const error = createAxiosError(422, [{ msg: "Campo obrigatório" }]);
    expect(getApiErrorMessage(error)).toBe("Campo obrigatório");
  });

  it("retorna mensagem para erro de rede", () => {
    const error = new AxiosError("Network Error");
    expect(getApiErrorMessage(error)).toBe(
      "Não foi possível conectar ao servidor. Verifique sua conexão.",
    );
  });

  it("retorna mensagens por status http", () => {
    expect(getApiErrorMessage(createAxiosError(401, null))).toBe(
      "Sessão expirada. Faça login novamente.",
    );
    expect(getApiErrorMessage(createAxiosError(404, null))).toBe("Recurso não encontrado.");
    expect(getApiErrorMessage(createAxiosError(502, null))).toBe(
      "Serviço temporariamente indisponível. Tente novamente.",
    );
  });
});
