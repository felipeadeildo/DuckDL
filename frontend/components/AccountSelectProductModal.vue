<script setup lang="ts">
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

const fetchData = async (clean: boolean = false) => {
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
    const currentNodes = clean ? [] : data.value?.nodes || []
    data.value = {
      nodes: [...currentNodes, ...result.nodes],
      total: result.total,
    }
  } catch (error) {
    console.error(error)
  } finally {
    pending.value = false
  }
}

watch([isOpen, page], () => fetchData(), { deep: true })

watch(
  query,
  debounce(() => fetchData(true), 500)
)
</script>

<template>
  <UTooltip
    :text="
      canSelectDownloadProducts(account)
        ? 'Selecionar Cursos para Download'
        : `Atualmente está ${getAccountStatus(account)}`
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

      <div v-if="pending && !data" class="flex justify-center items-center gap-3 my-4">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin" />
        <span class="font-bold text-lg">Carregando produtos...</span>
      </div>

      <UInput
        v-model="query"
        icon="i-heroicons-magnifying-glass-20-solid"
        size="sm"
        color="white"
        class="mx-48"
        :trailing="false"
        placeholder="Pesquisar produto por nome..."
      />

      <div
        class="grid grid-cols-2 gap-2 overflow-y-auto max-h-[80vh] mt-4 border-2 border-gray-700 rounded-lg"
      >
        <UCard v-for="product in data?.nodes" :key="product.id">
          <template #header>
            <div class="flex gap-2 items-center justify-between">
              <h1 class="font-medium">
                {{ product.name }}
                <UBadge color="blue">{{ getNodeStatus(product) }}</UBadge>
              </h1>

              <UButton
                v-if="product.url"
                :to="product.url"
                icon="i-heroicons-arrow-top-right-on-square"
              />
            </div>
          </template>

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton
                variant="outline"
                color="blue"
                icon="i-heroicons-arrow-down-on-square"
                @click="startNodeDownload(product)"
                :disabled="!canStartDownload(product)"
              >
                Baixar
              </UButton>
              <UButton
                variant="outline"
                color="green"
                icon="i-heroicons-document-magnifying-glass"
                @click="!canStartMapping(product)"
              >
                Mapear
              </UButton>
            </div>
          </template>
        </UCard>

        <div
          class="col-span-2 flex justify-center my-3"
          v-if="data && data.total > data.nodes.length"
        >
          <UButton icon="i-heroicons-arrow-path" @click="page++" :loading="pending">
            Carregar mais
          </UButton>
        </div>
      </div>
    </div>
  </UModal>
</template>
