import { Alert, Button, Stack, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";

import { getApiErrorMessage } from "../../../shared/lib/apiError";
import type { GeneratedArticle, GenerateArticleInput } from "../domain/types";
import { useGenerateArticle } from "../hooks/useGenerateArticle";

interface GenerateArticleFormProps {
  onGenerated: (result: GeneratedArticle, input: GenerateArticleInput) => void;
}

export function GenerateArticleForm({ onGenerated }: GenerateArticleFormProps) {
  const generateMutation = useGenerateArticle();
  const form = useForm<GenerateArticleInput>({
    initialValues: { topic: "", keywords: "", tone: "" },
    validate: {
      topic: (value) =>
        value.trim().length >= 3 ? null : "Descreva o tema com ao menos 3 caracteres",
    },
  });

  function handleSubmit(values: GenerateArticleInput): void {
    const input: GenerateArticleInput = {
      topic: values.topic.trim(),
      keywords: values.keywords?.trim() || undefined,
      tone: values.tone?.trim() || undefined,
    };
    generateMutation.mutate(input, {
      onSuccess: (result) => onGenerated(result, input),
    });
  }

  return (
    <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
      <Stack>
        {generateMutation.isError && (
          <Alert color="red" title="Falha na geração">
            {getApiErrorMessage(generateMutation.error)}
          </Alert>
        )}
        <TextInput
          label="Tema"
          placeholder="Ex.: como cultivar suculentas em apartamento"
          withAsterisk
          {...form.getInputProps("topic")}
        />
        <TextInput
          label="Palavras-chave (opcional)"
          placeholder="Ex.: suculentas, jardinagem, apartamento"
          {...form.getInputProps("keywords")}
        />
        <TextInput
          label="Tom (opcional)"
          placeholder="Ex.: informal e didático"
          {...form.getInputProps("tone")}
        />
        <Button type="submit" loading={generateMutation.isPending}>
          Gerar artigo
        </Button>
      </Stack>
    </form>
  );
}
