import { Alert, Button, PasswordInput, Stack, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";

import { getApiErrorMessage } from "../../../shared/lib/apiError";
import type { Credentials } from "../domain/types";
import { useLogin } from "../hooks/useLogin";

interface LoginFormProps {
  initialEmail?: string;
  onSuccess: () => void;
}

export function LoginForm({ initialEmail = "", onSuccess }: LoginFormProps) {
  const loginMutation = useLogin();
  const form = useForm<Credentials>({
    initialValues: { email: initialEmail, password: "" },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "E-mail inválido"),
      password: (value) => (value.length > 0 ? null : "Informe a senha"),
    },
  });

  function handleSubmit(values: Credentials): void {
    loginMutation.mutate(values, { onSuccess });
  }

  return (
    <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
      <Stack>
        {loginMutation.isError && (
          <Alert color="red" title="Não foi possível entrar">
            {getApiErrorMessage(loginMutation.error)}
          </Alert>
        )}
        <TextInput
          label="E-mail"
          placeholder="voce@exemplo.com"
          withAsterisk
          {...form.getInputProps("email")}
        />
        <PasswordInput
          label="Senha"
          placeholder="Sua senha"
          withAsterisk
          {...form.getInputProps("password")}
        />
        <Button type="submit" loading={loginMutation.isPending}>
          Entrar
        </Button>
      </Stack>
    </form>
  );
}
