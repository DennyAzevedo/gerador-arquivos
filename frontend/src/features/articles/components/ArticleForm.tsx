import { Button, Group, Select, Stack, Textarea, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";

import type { ArticleStatus } from "../domain/types";

export interface ArticleFormValues {
  title: string;
  content: string;
  status: ArticleStatus;
}

interface ArticleFormProps {
  initialValues: ArticleFormValues;
  submitLabel: string;
  isSubmitting: boolean;
  showStatus?: boolean;
  onSubmit: (values: ArticleFormValues) => void;
  onCancel?: () => void;
}

const STATUS_OPTIONS = [
  { value: "draft", label: "Rascunho" },
  { value: "published", label: "Publicado" },
];

export function ArticleForm({
  initialValues,
  submitLabel,
  isSubmitting,
  showStatus = true,
  onSubmit,
  onCancel,
}: ArticleFormProps) {
  const form = useForm<ArticleFormValues>({
    initialValues,
    validate: {
      title: (value) => (value.trim().length > 0 ? null : "Informe um título"),
      content: (value) => (value.trim().length > 0 ? null : "O conteúdo não pode ficar vazio"),
    },
  });

  return (
    <form onSubmit={form.onSubmit(onSubmit)} noValidate>
      <Stack>
        <TextInput label="Título" withAsterisk {...form.getInputProps("title")} />
        <Textarea
          label="Conteúdo (Markdown)"
          autosize
          minRows={10}
          maxRows={24}
          withAsterisk
          {...form.getInputProps("content")}
        />
        {showStatus && (
          <Select
            label="Status"
            data={STATUS_OPTIONS}
            allowDeselect={false}
            {...form.getInputProps("status")}
          />
        )}
        <Group justify="flex-end">
          {onCancel && (
            <Button variant="default" onClick={onCancel} type="button">
              Cancelar
            </Button>
          )}
          <Button type="submit" loading={isSubmitting}>
            {submitLabel}
          </Button>
        </Group>
      </Stack>
    </form>
  );
}
