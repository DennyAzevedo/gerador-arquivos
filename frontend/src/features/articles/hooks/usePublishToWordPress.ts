import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { WordPressPublishResult } from "../domain/types";
import { publishArticleToWordPress } from "../services/articleService";
import { articleKeys } from "./articleKeys";

export function usePublishToWordPress() {
  const queryClient = useQueryClient();

  return useMutation<WordPressPublishResult, Error, string>({
    mutationFn: publishArticleToWordPress,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: articleKeys.all });
    },
  });
}
