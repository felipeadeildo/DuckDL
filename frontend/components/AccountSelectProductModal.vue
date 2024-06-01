<script setup lang="ts">
import { ref, watch } from "vue"
import type { Account, Node } from "~/types"

const { account } = defineProps<{
  account: Account
}>()
const isOpen = ref(false)
const page = ref(1)
const query = ref("")

type NodesPagination = {
  nodes: Node[]
  total: number
}

const data = ref<NodesPagination | null>(null)
const pending = ref(false)

const fetchData = async () => {
  if (!isOpen.value) return
  pending.value = true
  try {
    const result = await $fetch<NodesPagination>(
      `http://localhost:8000/account/${account.id}/products`,
      {
        params: {
          page: page.value,
          per_page: 20,
          query: query.value,
        },
      }
    )
    data.value = result
  } catch (error) {
    console.error(error)
  } finally {
    pending.value = false
  }
}

watch([isOpen, page], fetchData, { deep: true })

watch(query, debounce(fetchData, 300))
</script>

<template>
  <UTooltip
    :text="
      canSelectDownloadProducts(account)
        ? 'Selecionar Cursos para Download'
        : `Atualmente está ${getStatus(account)}`
    "
  >
    <UButton
      icon="i-heroicons-check-circle"
      variant="soft"
      color="green"
      @click="isOpen = true"
      :disabled="!canSelectDownloadProducts(account)"
    />
  </UTooltip>

  <UModal v-model="isOpen" class="max-w-4xl w-full" fullscreen>
    <div class="p-4">
      <UButton
        color="gray"
        variant="ghost"
        icon="i-heroicons-x-mark-20-solid"
        class="absolute top-4 right-4"
        @click="isOpen = false"
      />
      <h1 class="text-xl text-center">Selecionar Produtos para Download ou Mapeamento</h1>

      <SelectProductMethodsHelp />

      <div v-if="pending" class="flex justify-center items-center gap-3 my-4">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin" />
        <span class="font-bold text-lg">Carregando produtos...</span>
      </div>

      <div class="grid grid-cols-2 gap-2">
        <UInput
          v-model="query"
          icon="i-heroicons-magnifying-glass-20-solid"
          size="sm"
          color="white"
          class="col-span-2 mx-48"
          :trailing="false"
          placeholder="Pesquisar produto por nome..."
        />

        <UCard v-for="product in data?.nodes" :key="product.id">
          <template #header>
            <div class="flex gap-2 items-center justify-between">
              <h1 class="font-medium">{{ product.name }}</h1>

              <UButton
                v-if="product.url"
                :to="product.url"
                icon="i-heroicons-arrow-top-right-on-square"
              />
            </div>
          </template>

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton variant="outline" color="blue">Marcar para download</UButton>
              <UButton variant="outline">Marcar para mapeamento</UButton>
            </div>
          </template>
        </UCard>
      </div>
    </div>
  </UModal>
</template>
