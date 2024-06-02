<script setup lang="ts">
useHead({
  titleTemplate(title) {
    return title ? `${title} | DuckDL` : "DuckDL"
  },
})
</script>

<template>
  <HorizontalNavBar />

  <ClientOnly>
    <Suspense>
      <NuxtPage />
    </Suspense>
    <UNotifications />
  </ClientOnly>
</template>
