<script setup lang="ts">
import type { Log } from "~/types"

useHead({ title: "LOGs" })

const page = ref(1)
const perPage = ref(10)

type LogsPagination = {
  data: Log[]
  total: number
}

const defaultValue = { data: [], total: 0 }

const { data: logsData, refresh: fetchLogs } = useAsyncData<LogsPagination>("logs", () =>
  $fetch("http://localhost:8000/log", {
    params: { page: page.value, per_page: perPage.value },
  })
)

let timeoutId: ReturnType<typeof setTimeout>

const autoRefresh = () => {
  timeoutId = setTimeout(async () => {
    await fetchLogs()
    autoRefresh()
  }, 10000)
}

autoRefresh()

onBeforeUnmount(() => {
  clearTimeout(timeoutId)
})

const columns = [
  {
    key: "message",
    label: "Mensagem",
  },
  {
    key: "logLevel",
    label: "Nível",
  },
  {
    key: "dateTime",
    label: "Data e Hora",
  },
  {
    key: "node",
    label: "Entidade",
  },
  {
    key: "account",
    label: "Conta",
  },
]
</script>

<template>
  <UTable
    :rows="(logsData || defaultValue).data"
    :columns="columns"
    :ui="{
      th: {
        base: 'text-center',
      },
      td: {
        base: 'text-center',
        padding: 'p-3',
        color: 'text-gray-500 dark:text-gray-400',
        font: '',
        size: 'text-xs',
      },
    }"
  >
    <template #node-data="{ row }">
      <span>{{ row.Node ? `${row.Node.name} (v${row.Node.type})` : "-" }}</span>
    </template>

    <template #account-data="{ row }">
      <span class="text-xs">
        {{ row.Account ? `${row.Account.username} (${row.Account.Platform.name})` : "-" }}
      </span>
    </template>

    <template #dateTime-data="{ row }">
      <span class="text-xs">
        {{ row.dateTime ? new Date(row.dateTime).toLocaleString() : "-" }}
      </span>
    </template>
  </UTable>
  <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
    <UPagination
      v-model="page"
      :page-count="perPage"
      :total="logsData ? logsData.total : defaultValue.total"
    />
  </div>
</template>
