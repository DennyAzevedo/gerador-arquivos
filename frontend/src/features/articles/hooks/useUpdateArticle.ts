import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { Article, UpdateArticleInput } from "../domain/types";
import { updateArticle } from "../services/articleService";
import { articleKeys } from "./articleKeys";

interface UpdateArticleVariables {
  id: string;
  input: UpdateArticleInput;
}

export function useUpdateArticle() {
  const queryClient = useQueryClient();

  return useMutation<Article, Error, UpdateArticleVariables>({
    mutationFn: ({ id, input }) => updateArticle(id, input),
    onSuccess: (article) => {
      void queryClient.invalidateQueries({ queryKey: articleKeys.all });
      void queryClient.invalidateQueries({ queryKey: articleKeys.detail(article.id) });
    },
  });
}
