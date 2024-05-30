<script setup lang="ts">
import type { FormSubmitEvent } from "#ui/types"
import { z } from "zod"
import type { Platform } from "~/types"

const emit = defineEmits(["close"])

const schema = z.object({
  username: z.string({ required_error: "O nome de usuário é obrigatório" }),
  password: z.string({ required_error: "A senha é obrigatória" }),
  platformId: z.number({ required_error: "A plataforma é obrigatória" }),
})

type Schema = z.output<typeof schema>

const state = reactive({
  username: undefined,
  password: undefined,
  platformId: undefined,
})

const { data: platforms = [] } = await useFetch<Platform[]>(
  "http://localhost:8000/platform"
)

const onSubmit = async (event: FormSubmitEvent<Schema>) => {
  const res = await $fetch("http://localhost:8000/account", {
    method: "POST",
    body: event.data,
    headers: {
      "Content-Type": "application/json",
    },
  })

  refreshNuxtData("accounts")
  // TODO: show success toast or erro when add account
  emit("close")
}
</script>

<template>
  <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
    <UFormGroup label="Usuário" name="username">
      <UInput v-model="state.username" />
    </UFormGroup>

    <UFormGroup label="Senha" name="password">
      <UInput v-model="state.password" type="password" />
    </UFormGroup>

    <UFormGroup label="Plataforma" name="platformId">
      <USelectMenu
        label="Plataforma"
        name="platformId"
        :options="
          (platforms || []).map((platform) => ({
            label: `${platform.name} - ${platform.url} (v${platform.version})`,
            value: platform.id,
          }))
        "
        v-model="state.platformId"
        value-attribute="value"
      />
    </UFormGroup>

    <UButton type="submit" icon="i-heroicons-plus-circle-solid">Adicionar</UButton>
  </UForm>
</template>
