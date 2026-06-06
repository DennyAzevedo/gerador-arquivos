import axios from "axios";

import { getAccessToken } from "../lib/authStorage";
import { notifyUnauthorized } from "../lib/unauthorizedHandler";

const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const AUTH_PATHS_WITHOUT_LOGOUT = ["/auth/jwt/login", "/auth/register"];

export const apiClient = axios.create({ baseURL });

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const requestUrl = error.config?.url ?? "";
    const isAuthRequest = AUTH_PATHS_WITHOUT_LOGOUT.some((path) => requestUrl.includes(path));

    if (error.response?.status === 401 && !isAuthRequest) {
      notifyUnauthorized();
    }

    return Promise.reject(error);
  },
);
