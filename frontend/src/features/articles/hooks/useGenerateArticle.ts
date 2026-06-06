import { useMutation } from "@tanstack/react-query";

import type { GeneratedArticle, GenerateArticleInput } from "../domain/types";
import { generateArticle } from "../services/articleService";

export function useGenerateArticle() {
  return useMutation<GeneratedArticle, Error, GenerateArticleInput>({
    mutationFn: generateArticle,
  });
}
