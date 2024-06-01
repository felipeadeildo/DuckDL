import type { AccountStatus } from "./types"

export const ACCOUNT_STATUS_TRANSLATION: Record<AccountStatus, string> = {
  stopped: "Parada",
  error: "Erro",
  listing_products: "Listando produtos",
  products_listed: "Produtos listados",
  downloading_products: "Baixando produtos",
}
