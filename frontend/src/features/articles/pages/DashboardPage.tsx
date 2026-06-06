import { Alert, Button, Center, Group, Loader, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { useNavigate } from "react-router-dom";

import { getApiErrorMessage } from "../../../shared/lib/apiError";
import { ArticleCard } from "../components/ArticleCard";
import { useArticles } from "../hooks/useArticles";
import { useDeleteArticle } from "../hooks/useDeleteArticle";
import { usePublishToWordPress } from "../hooks/usePublishToWordPress";

export function DashboardPage() {
  const navigate = useNavigate();
  const { data: articles, isLoading, isError, error } = useArticles();
  const deleteMutation = useDeleteArticle();
  const publishMutation = usePublishToWordPress();

  function handleDelete(id: string): void {
    deleteMutation.mutate(id, {
      onSuccess: () => {
        notifications.show({ message: "Artigo excluído.", color: "green" });
      },
      onError: (error) => {
        notifications.show({
          message: getApiErrorMessage(error, "Não foi possível excluir o artigo."),
          color: "red",
        });
      },
    });
  }

  function handlePublishWordPress(id: string): void {
    publishMutation.mutate(id, {
      onSuccess: (result) => {
        notifications.show({
          title: result.mocked ? "Envio simulado" : "Publicado no WordPress",
          message: result.message,
          color: "green",
        });
      },
      onError: (publishError) => {
        notifications.show({
          title: "Falha na publicação",
          message: getApiErrorMessage(publishError, "Não foi possível publicar no WordPress."),
          color: "red",
        });
      },
    });
  }

  return (
    <Stack>
      <Group justify="space-between" align="flex-start" wrap="wrap" gap="sm">
        <Title order={2}>Meus artigos</Title>
        <Button onClick={() => navigate("/articles/generate")}>Gerar artigo</Button>
      </Group>

      {isLoading && (
        <Center py="xl">
          <Loader />
        </Center>
      )}

      {isError && (
        <Alert color="red" title="Erro ao carregar">
          {getApiErrorMessage(error, "Não foi possível carregar seus artigos. Tente novamente mais tarde.")}
        </Alert>
      )}

      {articles && articles.length === 0 && (
        <Center py="xl">
          <Stack align="center" gap="xs">
            <Text c="dimmed">Você ainda não tem artigos.</Text>
            <Button variant="light" onClick={() => navigate("/articles/generate")}>
              Gerar meu primeiro artigo
            </Button>
          </Stack>
        </Center>
      )}

      {articles && articles.length > 0 && (
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }}>
          {articles.map((article) => (
            <ArticleCard
              key={article.id}
              article={article}
              onEdit={(id) => navigate(`/articles/${id}/edit`)}
              onDelete={handleDelete}
              onPublishWordPress={handlePublishWordPress}
              isPublishing={publishMutation.isPending && publishMutation.variables === article.id}
            />
          ))}
        </SimpleGrid>
      )}
    </Stack>
  );
}
