import { Anchor, Card, Center, Stack, Text, Title } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { Link, useNavigate } from "react-router-dom";

import { RegisterForm } from "../components/RegisterForm";

export function RegisterPage() {
  const navigate = useNavigate();

  function handleSuccess(): void {
    notifications.show({
      title: "Cadastro realizado",
      message: "Sua conta foi criada. Faça login para continuar.",
      color: "green",
    });
    navigate("/login");
  }

  return (
    <Center mih="100vh" p="md">
      <Card withBorder w={400} padding="xl" radius="md" shadow="sm">
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
