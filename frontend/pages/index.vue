<script setup lang="ts">
import type { Account } from "~/types"

const { data: accounts } = await useAsyncData<Account[]>("accounts", () =>
  $fetch("http://localhost:8000/account")
)
</script>

<template>
  <div class="container mx-auto">
    <h1 class="text-3xl text-center my-2 animate-bounce">
      Bem vindo ao Courses Downloader
    </h1>

    <div>
      <h3 class="text-center font-bold text-xl">Contas</h3>

      <UAlert
        v-if="!accounts || accounts.length == 0"
        icon="i-heroicons-command-line"
        color="primary"
        variant="soft"
        description="Você ainda não tem contas adicionadas. Crie uma clicando no botão abaixo."
      />

      <AccountsTable v-else :accounts="accounts" />
    </div>

    <AddAccountModal />
  </div>
</template>
