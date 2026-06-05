import { AppShell, Group, Title } from "@mantine/core";
import { Outlet } from "react-router-dom";

export function MainLayout() {
  return (
    <AppShell header={{ height: 60 }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md">
          <Title order={3}>Gerador de Artigos</Title>
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
