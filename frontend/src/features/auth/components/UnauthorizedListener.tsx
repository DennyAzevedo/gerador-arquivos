import { notifications } from "@mantine/notifications";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { registerUnauthorizedHandler } from "../../../shared/lib/unauthorizedHandler";
import { useAuth } from "../context/AuthContext";

export function UnauthorizedListener() {
  const { endSession, status } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    registerUnauthorizedHandler(() => {
      if (status !== "authenticated") {
        return;
      }

      endSession();
      notifications.show({
        title: "Sessão encerrada",
        message: "Faça login novamente para continuar.",
        color: "yellow",
      });
      navigate("/login", { replace: true });
    });

    return () => {
      registerUnauthorizedHandler(null);
    };
  }, [endSession, navigate, status]);

  return null;
}
