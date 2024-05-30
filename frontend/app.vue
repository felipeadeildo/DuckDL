<script setup lang="ts">
useHead({
  titleTemplate(title) {
    return title ? `${title} | CoursesDownloader` : "CoursesDownloader"
  },
})
</script>

<template>
  <HorizontalNavBar />

  <ClientOnly>
    <Suspense>
      <NuxtPage />
    </Suspense>
  </ClientOnly>
</template>
