export type ArticleStatus = "draft" | "published";

export interface Article {
  id: string;
  title: string;
  content: string;
  topic: string;
  keywords: string | null;
  tone: string | null;
  status: ArticleStatus;
  createdAt: string;
  updatedAt: string;
}

export interface GenerateArticleInput {
  topic: string;
  keywords?: string;
  tone?: string;
}

export interface GeneratedArticle {
  title: string;
  content: string;
}

export interface CreateArticleInput {
  title: string;
  content: string;
  topic: string;
  keywords?: string | null;
  tone?: string | null;
  status?: ArticleStatus;
}

export interface UpdateArticleInput {
  title?: string;
  content?: string;
  keywords?: string | null;
  tone?: string | null;
  status?: ArticleStatus;
}
