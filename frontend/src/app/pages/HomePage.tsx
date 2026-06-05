import { Stack, Text, Title } from "@mantine/core";

export function HomePage() {
  return (
    <Stack>
      <Title order={1}>Bem-vindo</Title>
      <Text c="dimmed">
        Gerador de artigos para WordPress com IA. A autenticação e a geração de
        artigos serão habilitadas nas próximas etapas.
      </Text>
    </Stack>
  );
}
