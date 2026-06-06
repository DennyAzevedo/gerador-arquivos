export const articleKeys = {
  all: ["articles"] as const,
  detail: (id: string) => ["articles", id] as const,
};
