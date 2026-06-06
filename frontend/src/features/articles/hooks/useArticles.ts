import { useQuery } from "@tanstack/react-query";

import { listArticles } from "../services/articleService";
import { articleKeys } from "./articleKeys";

export function useArticles() {
  return useQuery({
    queryKey: articleKeys.all,
    queryFn: listArticles,
  });
}
