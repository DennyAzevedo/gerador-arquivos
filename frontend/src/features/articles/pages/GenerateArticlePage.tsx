import { Card, Stack, Text, Title } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { ArticleForm, type ArticleFormValues } from "../components/ArticleForm";
import { GenerateArticleForm } from "../components/GenerateArticleForm";
import type { GeneratedArticle, GenerateArticleInput } from "../domain/types";
import { useCreateArticle } from "../hooks/useCreateArticle";

export function GenerateArticlePage() {
  const navigate = useNavigate();
  const createMutation = useCreateArticle();
  const [generated, setGenerated] = useState<GeneratedArticle | null>(null);
  const [sourceInput, setSourceInput] = useState<GenerateArticleInput | null>(null);

  function handleGenerated(result: GeneratedArticle, input: GenerateArticleInput): void {
    setGenerated(result);
    setSourceInput(input);
  }

  function handleSave(values: ArticleFormValues): void {
    if (!sourceInput) {
      return;
    }
    createMutation.mutate(
      {
        title: values.title,
        content: values.content,
        topic: sourceInput.topic,
        keywords: sourceInput.keywords ?? null,
        tone: sourceInput.tone ?? null,
        status: values.status,
      },
      {
        onSuccess: () => {
          notifications.show({ title: "Artigo salvo", message: "Seu artigo foi salvo.", color: "green" });
          navigate("/");
        },
        onError: () => {
          notifications.show({ message: "Não foi possível salvar o artigo.", color: "red" });
        },
      },
    );
  }

  return (
    <Stack>
      <Title order={2}>Gerar artigo</Title>

      <Card withBorder padding="lg" radius="md">
        <GenerateArticleForm onGenerated={handleGenerated} />
      </Card>

      {generated && (
        <Card withBorder padding="lg" radius="md">
          <Stack>
            <div>
              <Title order={3}>Revisar e salvar</Title>
              <Text size="sm" c="dimmed">
                Edite o conteúdo gerado antes de salvar.
              </Text>
            </div>
            <ArticleForm
              initialValues={{
                title: generated.title,
                content: generated.content,
                status: "draft",
              }}
              submitLabel="Salvar artigo"
              isSubmitting={createMutation.isPending}
              onSubmit={handleSave}
              onCancel={() => navigate("/")}
            />
          </Stack>
        </Card>
      )}
    </Stack>
  );
}
