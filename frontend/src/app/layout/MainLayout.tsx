import { AppShell, Button, Group, Text, Title } from "@mantine/core";
import { Outlet } from "react-router-dom";

import { useAuth } from "../../features/auth/context/AuthContext";

export function MainLayout() {
  const { user, endSession } = useAuth();

  return (
    <AppShell header={{ height: 60 }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Title order={3}>Gerador de Artigos</Title>
          <Group gap="sm">
            {user && (
              <Text size="sm" c="dimmed">
                {user.email}
              </Text>
            )}
            <Button variant="light" size="xs" onClick={endSession}>
              Sair
            </Button>
          </Group>
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
