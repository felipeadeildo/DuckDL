import { NODE_STATUS_TRANSLATION } from "~/constants"
import type { Node, NodeStatus } from "~/types"

export const startNodeDownload = async (node: Node) => {
  const toast = useToast()
  await $fetch(`http://localhost:8000/account/start_download_product/${node.id}`, {
    method: "POST",
  })

  toast.add({
    title: "Produto adicionado para download.",
    description: `Download irá iniciar em instantes, você pode acompanhar pela aba de Processos Ativos, ou ver mais detalhes pelos LOGs`,
  })
}

export const startNodeMapping = async (node: Node) => {
  const toast = useToast()

  await $fetch(`http://localhost:8000/account/start_map_product/${node.id}`, {
    method: "POST",
  })

  toast.add({
    title: "Processo de Mapeamento Iniciado!",
    description: `Este processo pode demorar alguns minutos dependendo do tamanho do produto. Acompanhe o resultado do mapeamento pela aba de Processos Ativos, ou ver mais detalhes pelos LOGs`,
  })
}

export const getNodeStatus = (node: Node) =>
  NODE_STATUS_TRANSLATION[node.status as NodeStatus]

export const canStartMapping = (node: Node) =>
  ["stopped", "mapped", "mapping_error"].includes(node.status)

export const canStartDownload = (node: Node) =>
  ["stopped", "downloaded", "download_error", "mapped"].includes(node.status)

export const getNodeName = (node: Node) => {
  let nodeName = ""
  if (node.customName) {
    nodeName = node.customName
  } else if (node.order) {
    nodeName = `${node.order} - ${node.name}`
  } else {
    nodeName = node.name
  }

  return `${nodeName} (${node.type})`
}
