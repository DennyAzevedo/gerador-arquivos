import { useQuery } from "@tanstack/react-query";

import { getArticle } from "../services/articleService";
import { articleKeys } from "./articleKeys";

export function useArticle(id: string | undefined) {
  return useQuery({
    queryKey: articleKeys.detail(id ?? ""),
    queryFn: () => getArticle(id as string),
    enabled: Boolean(id),
  });
}
