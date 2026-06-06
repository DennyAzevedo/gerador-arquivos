import { Badge, Button, Card, Group, Modal, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

import type { Article } from "../domain/types";

interface ArticleCardProps {
  article: Article;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

export function ArticleCard({ article, onEdit, onDelete }: ArticleCardProps) {
  const [confirmOpened, { open, close }] = useDisclosure(false);

  const isPublished = article.status === "published";

  function handleConfirmDelete(): void {
    onDelete(article.id);
    close();
  }

  return (
    <Card withBorder padding="md" radius="md">
      <Group justify="space-between" mb="xs" wrap="nowrap">
        <Text fw={600} lineClamp={1}>
          {article.title}
        </Text>
        <Badge color={isPublished ? "green" : "gray"} variant="light">
          {isPublished ? "Publicado" : "Rascunho"}
        </Badge>
      </Group>

      <Text size="sm" c="dimmed" lineClamp={2}>
        {article.topic}
      </Text>
      <Text size="xs" c="dimmed" mt="xs">
        Criado em {new Date(article.createdAt).toLocaleString("pt-BR")}
      </Text>

      <Group mt="md" gap="xs">
        <Button size="xs" variant="light" onClick={() => onEdit(article.id)}>
          Editar
        </Button>
        <Button size="xs" variant="light" color="red" onClick={open}>
          Excluir
        </Button>
      </Group>

      <Modal opened={confirmOpened} onClose={close} title="Excluir artigo" centered>
        <Text size="sm">
          Tem certeza que deseja excluir <strong>{article.title}</strong>? Esta ação não
          pode ser desfeita.
        </Text>
        <Group justify="flex-end" mt="lg">
          <Button variant="default" onClick={close}>
            Cancelar
          </Button>
          <Button color="red" onClick={handleConfirmDelete}>
            Excluir
          </Button>
        </Group>
      </Modal>
    </Card>
  );
}
