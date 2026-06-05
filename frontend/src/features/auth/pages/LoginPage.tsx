import { Anchor, Card, Center, Stack, Text, Title } from "@mantine/core";
import { Link, useNavigate } from "react-router-dom";

import { LoginForm } from "../components/LoginForm";

export function LoginPage() {
  const navigate = useNavigate();

  return (
    <Center mih="100vh" p="md">
      <Card withBorder w={400} padding="xl" radius="md" shadow="sm">
        <Stack>
          <Title order={2} ta="center">
            Entrar
          </Title>
          <LoginForm onSuccess={() => navigate("/")} />
          <Text size="sm" ta="center" c="dimmed">
            Não tem conta?{" "}
            <Anchor component={Link} to="/register">
              Cadastre-se
            </Anchor>
          </Text>
        </Stack>
      </Card>
    </Center>
  );
}
