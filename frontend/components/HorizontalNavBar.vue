<script setup lang="ts">
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
    label: "Configurações",
    icon: "i-heroicons-cog-6-tooth",
    to: "/settings",
  },
  {
    label: "LOGs",
    icon: "i-heroicons-clipboard-document",
    to: "/logs",
  },
]
</script>

<template>
  <UHorizontalNavigation
    :links="links"
    class="border-b border-gray-200 dark:border-gray-800 justify-center"
  />
</template>
