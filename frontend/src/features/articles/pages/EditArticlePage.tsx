import { Alert, Card, Center, Loader, Stack, Title } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { useNavigate, useParams } from "react-router-dom";

import { ArticleForm, type ArticleFormValues } from "../components/ArticleForm";
import { useArticle } from "../hooks/useArticle";
import { useUpdateArticle } from "../hooks/useUpdateArticle";

export function EditArticlePage() {
  const navigate = useNavigate();
  const { articleId } = useParams<{ articleId: string }>();
  const { data: article, isLoading, isError } = useArticle(articleId);
  const updateMutation = useUpdateArticle();

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
        onError: () => {
          notifications.show({ message: "Não foi possível salvar as alterações.", color: "red" });
        },
      },
    );
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
          Não foi possível carregar o artigo.
        </Alert>
      )}

      {article && (
        <Card withBorder padding="lg" radius="md">
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
        </Card>
      )}
    </Stack>
  );
}
