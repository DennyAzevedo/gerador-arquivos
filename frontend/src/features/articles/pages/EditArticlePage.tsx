import { Alert, Button, Card, Center, Group, Loader, Stack, Title } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { useNavigate, useParams } from "react-router-dom";

import { getApiErrorMessage } from "../../../shared/lib/apiError";
import { ArticleForm, type ArticleFormValues } from "../components/ArticleForm";
import { useArticle } from "../hooks/useArticle";
import { usePublishToWordPress } from "../hooks/usePublishToWordPress";
import { useUpdateArticle } from "../hooks/useUpdateArticle";

export function EditArticlePage() {
  const navigate = useNavigate();
  const { articleId } = useParams<{ articleId: string }>();
  const { data: article, isLoading, isError, error } = useArticle(articleId);
  const updateMutation = useUpdateArticle();
  const publishMutation = usePublishToWordPress();

  function handleSave(values: ArticleFormValues): void {
    if (!articleId) {
      return;
    }
    updateMutation.mutate(
      {
        id: articleId,
        input: {
          title: values.title,
          content: values.content,
          status: values.status,
        },
      },
      {
        onSuccess: () => {
          notifications.show({ title: "Alterações salvas", message: "Artigo atualizado.", color: "green" });
          navigate("/");
        },
        onError: (mutationError) => {
          notifications.show({
            message: getApiErrorMessage(mutationError, "Não foi possível salvar as alterações."),
            color: "red",
          });
        },
      },
    );
  }

  function handlePublishWordPress(): void {
    if (!articleId) {
      return;
    }
    publishMutation.mutate(articleId, {
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
      <Title order={2}>Editar artigo</Title>

      {isLoading && (
        <Center py="xl">
          <Loader />
        </Center>
      )}

      {isError && (
        <Alert color="red" title="Erro ao carregar">
          {getApiErrorMessage(error, "Não foi possível carregar o artigo.")}
        </Alert>
      )}

      {article && (
        <Card withBorder padding="lg" radius="md">
          <Stack gap="md">
            <Group justify="flex-end">
              <Button
                variant="light"
                color="blue"
                loading={publishMutation.isPending}
                onClick={handlePublishWordPress}
              >
                Publicar no WordPress
              </Button>
            </Group>
            <ArticleForm
              initialValues={{
                title: article.title,
                content: article.content,
                status: article.status,
              }}
              submitLabel="Salvar alterações"
              isSubmitting={updateMutation.isPending}
              onSubmit={handleSave}
              onCancel={() => navigate("/")}
            />
          </Stack>
        </Card>
      )}
    </Stack>
  );
}
