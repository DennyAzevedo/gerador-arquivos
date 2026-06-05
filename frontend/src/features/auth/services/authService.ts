import { apiClient } from "../../../shared/api/client";
import type { AuthUser, Credentials, RegisterData } from "../domain/types";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface UserResponse {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

function toAuthUser(data: UserResponse): AuthUser {
  return {
    id: data.id,
    email: data.email,
    isActive: data.is_active,
    isSuperuser: data.is_superuser,
    isVerified: data.is_verified,
  };
}

export async function login(credentials: Credentials): Promise<string> {
  const body = new URLSearchParams();
  body.append("username", credentials.email);
  body.append("password", credentials.password);

  const { data } = await apiClient.post<LoginResponse>("/auth/jwt/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data.access_token;
}

export async function register(payload: RegisterData): Promise<AuthUser> {
  const { data } = await apiClient.post<UserResponse>("/auth/register", payload);
  return toAuthUser(data);
}

export async function getCurrentUser(): Promise<AuthUser> {
  const { data } = await apiClient.get<UserResponse>("/users/me");
  return toAuthUser(data);
}
