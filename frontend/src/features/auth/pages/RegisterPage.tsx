import { Anchor, Card, Center, Stack, Text, Title } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { Link, useNavigate } from "react-router-dom";

import { RegisterForm } from "../components/RegisterForm";
import type { RegisterData } from "../domain/types";
import { useLogin } from "../hooks/useLogin";

export function RegisterPage() {
  const navigate = useNavigate();
  const loginMutation = useLogin();

  function handleSuccess(values: RegisterData): void {
    loginMutation.mutate(
      { email: values.email, password: values.password },
      {
        onSuccess: () => {
          notifications.show({
            title: "Conta criada",
            message: "Bem-vindo! Você já está autenticado.",
            color: "green",
          });
          navigate("/", { replace: true });
        },
        onError: () => {
          notifications.show({
            title: "Cadastro realizado",
            message: "Sua conta foi criada. Faça login para continuar.",
            color: "green",
          });
          navigate("/login", { state: { email: values.email } });
        },
      },
    );
  }

  return (
    <Center mih="100vh" p="md">
      <Card withBorder w={{ base: "100%", sm: 400 }} maw={400} padding="xl" radius="md" shadow="sm">
        <Stack>
          <Title order={2} ta="center">
            Criar conta
          </Title>
          <RegisterForm onSuccess={handleSuccess} />
          <Text size="sm" ta="center" c="dimmed">
            Já tem conta?{" "}
            <Anchor component={Link} to="/login">
              Entrar
            </Anchor>
          </Text>
        </Stack>
      </Card>
    </Center>
  );
}
