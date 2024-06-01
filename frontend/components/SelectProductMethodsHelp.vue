<script setup lang="ts">
const helpItems = [
  {
    label: 'O que significa selecionar para "mapeamento"?',
    icon: "i-heroicons-question-mark-circle",
    slot: "mapeamento",
  },
  {
    label: 'O que significa selecionar para "download"?',
    icon: "i-heroicons-question-mark-circle",
    slot: "download",
  },
]
</script>

<template>
  <UAccordion
    :items="helpItems"
    :ui="{
      wrapper: 'grid grid-cols-2 gap-4',
      item: { base: 'text-xs' },
    }"
    multiple
  >
    <template #download>
      Já selecionar produto para <span class="font-bold">download</span>, significa que o
      script irá descobrir o que realmente possui dentro de cada produto ao mesmo tempo em
      que faz o download sem intervenção do usuário.
    </template>

    <template #mapeamento>
      Selecionar produto para <span class="font-bold">mapeamento</span> significa que
      antes de iniciar o download em si, o script irá mapear toda a árvore do curso
      permitindo que você possa selecionar partes desejadas, renomear coisas, reordenar
      coisas, etc.
    </template>
  </UAccordion>
</template>
