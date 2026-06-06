import { apiClient } from "../../../shared/api/client";
import type {
  Article,
  ArticleStatus,
  CreateArticleInput,
  GenerateArticleInput,
  GeneratedArticle,
  UpdateArticleInput,
} from "../domain/types";

interface ArticleResponse {
  id: string;
  title: string;
  content: string;
  topic: string;
  keywords: string | null;
  tone: string | null;
  status: ArticleStatus;
  created_at: string;
  updated_at: string;
}

function toArticle(data: ArticleResponse): Article {
  return {
    id: data.id,
    title: data.title,
    content: data.content,
    topic: data.topic,
    keywords: data.keywords,
    tone: data.tone,
    status: data.status,
    createdAt: data.created_at,
    updatedAt: data.updated_at,
  };
}

export async function generateArticle(input: GenerateArticleInput): Promise<GeneratedArticle> {
  const { data } = await apiClient.post<GeneratedArticle>("/articles/generate", input);
  return data;
}

export async function listArticles(): Promise<Article[]> {
  const { data } = await apiClient.get<ArticleResponse[]>("/articles");
  return data.map(toArticle);
}

export async function getArticle(id: string): Promise<Article> {
  const { data } = await apiClient.get<ArticleResponse>(`/articles/${id}`);
  return toArticle(data);
}

export async function createArticle(input: CreateArticleInput): Promise<Article> {
  const { data } = await apiClient.post<ArticleResponse>("/articles", input);
  return toArticle(data);
}

export async function updateArticle(id: string, input: UpdateArticleInput): Promise<Article> {
  const { data } = await apiClient.put<ArticleResponse>(`/articles/${id}`, input);
  return toArticle(data);
}

export async function deleteArticle(id: string): Promise<void> {
  await apiClient.delete(`/articles/${id}`);
}
