<script setup lang="ts">
import type { Account } from "~/types"

defineProps<{
  account: Account
}>()
</script>

<template>
  <div class="space-x-2">
    <UTooltip
      :text="
        !canListProducts(account)
          ? `Atualmente está ${getStatus(account)}`
          : 'Listar Produtos da Conta'
      "
    >
      <UButton
        icon="i-heroicons-arrow-path"
        @click="startListProducts(account)"
        :disabled="!canListProducts(account)"
      />
    </UTooltip>

    <UTooltip text="Remover Conta">
      <UButton icon="i-heroicons-trash" variant="outline" color="red" />
    </UTooltip>

    <AccountSelectProductModal :account="account" />
  </div>
</template>
