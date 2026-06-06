import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { Article, CreateArticleInput } from "../domain/types";
import { createArticle } from "../services/articleService";
import { articleKeys } from "./articleKeys";

export function useCreateArticle() {
  const queryClient = useQueryClient();

  return useMutation<Article, Error, CreateArticleInput>({
    mutationFn: createArticle,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: articleKeys.all });
    },
  });
}
