import { ACCOUNT_STATUS_TRANSLATION } from "~/constants"
import type { Account, AccountStatus } from "~/types"

export const startListProducts = async (account: Account) => {
  const toast = useToast()
  await $fetch(`http://localhost:8000/account/${account.id}/start_list_products`, {
    method: "POST",
  })

  refreshNuxtData("accounts")

  toast.add({
    title: "Listagem de produtos iniciada",
    description: "Você pode acompanhar a listagem pelos logs.",
  })
}

export const getAccountStatus = (account: Account) =>
  ACCOUNT_STATUS_TRANSLATION[account.status as AccountStatus]

export const canListProducts = (account: Account) =>
  ["stopped", "products_listed", "error"].includes(account.status)

export const canSelectDownloadProducts = (account: Account) =>
  ["products_listed", "downloading_products"].includes(account.status)
