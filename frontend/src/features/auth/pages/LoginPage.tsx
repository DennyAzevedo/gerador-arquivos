import { Anchor, Card, Center, Stack, Text, Title } from "@mantine/core";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { LoginForm } from "../components/LoginForm";

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const locationState = location.state as { from?: string; email?: string } | null;
  const redirectTo = locationState?.from ?? "/";
  const initialEmail = locationState?.email ?? "";

  return (
    <Center mih="100vh" p="md">
      <Card withBorder w={{ base: "100%", sm: 400 }} maw={400} padding="xl" radius="md" shadow="sm">
        <Stack>
          <Title order={2} ta="center">
            Entrar
          </Title>
          <LoginForm
            initialEmail={initialEmail}
            onSuccess={() => navigate(redirectTo, { replace: true })}
          />
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
