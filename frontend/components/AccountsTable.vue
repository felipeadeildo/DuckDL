<script setup lang="ts">
import type { Account } from "~/types"
import { getStatus } from "~/utils/account"

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
  { key: "status", label: "Estado", class: "text-center" },
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

    <template #status-data="{ row }">
      {{ getStatus(row) }}
    </template>

    <template #actions-data="{ row }">
      <AccountActions :account="row" />
    </template>
  </UTable>
</template>
