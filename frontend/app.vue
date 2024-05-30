<script setup lang="ts">
useHead({
  titleTemplate(title) {
    return title ? `${title} - CoursesDownloader` : "CoursesDownloader"
  },
})

const links = [
  {
    label: "Home",
    avatar: {
      src: "/favicon.ico",
      size: "sm" as const,
    },
    to: "/",
  },
  {
    label: "Downloads Ativos",
    icon: "i-heroicons-arrow-down-tray",
    to: "/downloads",
  },
  {
    label: "LOGs",
    icon: "i-heroicons-clipboard-document",
    to: "/logs",
  },
  {
    label: "Settings",
    icon: "i-heroicons-cog-6-tooth",
    to: "/settings",
  },
]
</script>

<template>
  <UHorizontalNavigation
    :links="links"
    class="border-b border-gray-200 dark:border-gray-800 justify-center"
  />

  <NuxtPage />
</template>
