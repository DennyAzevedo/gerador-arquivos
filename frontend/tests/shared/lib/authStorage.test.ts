import { describe, expect, it, beforeEach } from "vitest";

import {
  clearAccessToken,
  getAccessToken,
  setAccessToken,
} from "../../../src/shared/lib/authStorage";

describe("authStorage", () => {
  beforeEach(() => {
    clearAccessToken();
  });

  it("persiste e recupera o token", () => {
    setAccessToken("token-teste");
    expect(getAccessToken()).toBe("token-teste");
  });

  it("remove o token ao limpar", () => {
    setAccessToken("token-teste");
    clearAccessToken();
    expect(getAccessToken()).toBeNull();
  });
});
