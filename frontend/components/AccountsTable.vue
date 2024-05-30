<script setup lang="ts">
import type { Account } from "~/types"

defineProps<{
  accounts: Account[]
}>()

const columns = [
  {
    key: "username",
    label: "Login",
    sortable: true,
    class: "text-center",
  },
  {
    key: "password",
    label: "Senha",
    class: "text-center",
  },
  {
    key: "Platform",
    label: "Plataforma",
    sortable: true,
    class: "text-center",
  },
  {
    key: "actions",
    label: "Ações",
    class: "text-center",
  },
]
</script>

<template>
  <UTable :rows="accounts" :columns="columns" class="text-center">
    <template #Platform-data="{ row }">
      {{ `${row.Platform.name} - ${row.Platform.url} (v${row.Platform.version})` }}
    </template>

    <template #actions-data="{ row }">
      <div class="space-x-2">
        <UButton icon="i-heroicons-magnifying-glass">Mapear Produtos</UButton>
        <UButton icon="i-heroicons-trash" variant="outline" color="red">Excluir</UButton>
      </div>
    </template>
  </UTable>
</template>
