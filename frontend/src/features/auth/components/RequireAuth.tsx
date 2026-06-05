import { Center, Loader } from "@mantine/core";
import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export function RequireAuth() {
  const { status } = useAuth();

  if (status === "loading") {
    return (
      <Center h="100vh">
        <Loader />
      </Center>
    );
  }

  if (status === "unauthenticated") {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
