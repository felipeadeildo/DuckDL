export type Account = {
  id: number
  username: string
  password: string
  platformId: number
  extraInfos: string
  products: Node[]
  status: string

  Platform: Platform
}

export type Platform = {
  id: number
  name: string
  url: string
  version: number
}

export type Log = {
  id: number
  message: string
  logLevel: string
  dateTime: string // Assuming datetime is serialized to string
  nodeId?: number
  accountId?: number
  Node?: Node
  Account?: Account
}

export type Node = {
  id: number
  name: string
  type: string
  url?: string
  status?: string
  order?: number
  parentId?: number
  totalSize?: number
  currentSize?: number
  unit?: string
  extraInfos: string
  customName?: string
  children: Node[]
}

export type Setting = {
  id: number
  key: string
  value: string
  valueType: string
}
