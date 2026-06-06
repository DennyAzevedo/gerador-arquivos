import { AppShell, Button, Group, Text, Title } from "@mantine/core";
import { Link, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../../features/auth/context/AuthContext";

export function MainLayout() {
  const navigate = useNavigate();
  const { user, endSession } = useAuth();

  function handleLogout(): void {
    endSession();
    navigate("/login", { replace: true });
  }

  return (
    <AppShell header={{ height: 60 }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between" wrap="nowrap">
          <Group gap="md" wrap="nowrap">
            <Title order={3} visibleFrom="sm">
              Gerador de Artigos
            </Title>
            <Title order={4} hiddenFrom="sm">
              Artigos
            </Title>
            <Group gap="xs" visibleFrom="sm">
              <Button variant="subtle" size="xs" component={Link} to="/">
                Meus artigos
              </Button>
              <Button variant="subtle" size="xs" component={Link} to="/articles/generate">
                Gerar
              </Button>
            </Group>
          </Group>
          <Group gap="sm" wrap="nowrap">
            {user && (
              <Text size="sm" c="dimmed" visibleFrom="sm" truncate maw={180}>
                {user.email}
              </Text>
            )}
            <Button variant="light" size="xs" onClick={handleLogout}>
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
