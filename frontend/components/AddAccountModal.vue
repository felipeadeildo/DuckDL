<script setup lang="ts">
const isOpen = ref(false)
</script>

<template>
  <div>
    <UButton
      icon="i-heroicons-plus-circle-solid"
      size="sm"
      color="primary"
      variant="solid"
      label="Adicionar Conta"
      :trailing="false"
      class="absolute bottom-4 right-4"
      @click="isOpen = true"
    />

    <UModal v-model="isOpen">
      <div class="p-4">
        <h3 class="text-2xl my-2 text-center">Adicionar Conta</h3>
        <AddAccountForm @close="isOpen = false" />
      </div>
    </UModal>
  </div>
</template>
