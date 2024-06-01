import type { AccountStatus, NodeStatus } from "./types"

export const ACCOUNT_STATUS_TRANSLATION: Record<AccountStatus, string> = {
  stopped: "Parada",
  error: "Erro",
  listing_products: "Listando produtos",
  products_listed: "Produtos listados",
  downloading_products: "Baixando produtos",
}

export const NODE_STATUS_TRANSLATION: Record<NodeStatus, string> = {
  stopped: "Parado",
  downloading: "Baixando",
  downloaded: "Baixado",
  download_error: "Erro no Download",
  mapping: "Mapeando",
  mapped: "Mapeado",
  mapping_error: "Erro no Mapeamento",
}
