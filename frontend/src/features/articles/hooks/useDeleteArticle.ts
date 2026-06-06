import { useMutation, useQueryClient } from "@tanstack/react-query";

import { deleteArticle } from "../services/articleService";
import { articleKeys } from "./articleKeys";

export function useDeleteArticle() {
  const queryClient = useQueryClient();

  return useMutation<void, Error, string>({
    mutationFn: deleteArticle,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: articleKeys.all });
    },
  });
}
