import { Alert, Button, PasswordInput, Stack, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";

import { getApiErrorMessage } from "../../../shared/lib/apiError";
import type { RegisterData } from "../domain/types";
import { useRegister } from "../hooks/useRegister";

interface RegisterFormProps {
  onSuccess: (values: RegisterData) => void;
}

const MIN_PASSWORD_LENGTH = 8;

export function RegisterForm({ onSuccess }: RegisterFormProps) {
  const registerMutation = useRegister();
  const form = useForm<RegisterData>({
    initialValues: { email: "", password: "" },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "E-mail inválido"),
      password: (value) =>
        value.length >= MIN_PASSWORD_LENGTH
          ? null
          : `A senha deve ter ao menos ${MIN_PASSWORD_LENGTH} caracteres`,
    },
  });

  function handleSubmit(values: RegisterData): void {
    registerMutation.mutate(values, { onSuccess: () => onSuccess(values) });
  }

  return (
    <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
      <Stack>
        {registerMutation.isError && (
          <Alert color="red" title="Não foi possível cadastrar">
            {getApiErrorMessage(registerMutation.error)}
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
          placeholder="Mínimo de 8 caracteres"
          withAsterisk
          {...form.getInputProps("password")}
        />
        <Button type="submit" loading={registerMutation.isPending}>
          Cadastrar
        </Button>
      </Stack>
    </form>
  );
}
