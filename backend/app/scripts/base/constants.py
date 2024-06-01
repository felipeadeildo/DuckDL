from typing import Literal, Mapping, Tuple

LOG_LEVELS = Literal["debug", "info", "warning", "error"]

MESSAGE_KEYS = Literal[
    "login_success",
    "login_error",
    "account_status_block_product_list",
    "account_products_deleted",
    "account_start_listing_products",
    "account_products_listed_success",
    "node_status_block_download",
    "node_class_not_found",
]

MESSAGE_CONTENTS: Mapping[MESSAGE_KEYS, Tuple[LOG_LEVELS, str]] = {
    "login_success": ("info", "Login efetuado com sucesso!"),
    "login_error": ("error", "Falha ao fazer login, verifique as credenciais."),
    "account_status_block_product_list": (
        "error",
        "Atualmente a conta encontra-se no estado {status} que impede a listagem de produtos.",
    ),
    "account_products_deleted": (
        "info",
        "Produtos removidos para iniciar nova listagem de produtos.",
    ),
    "account_start_listing_products": (
        "info",
        "Iniciando listagem de produtos. Este processo pode demorar alguns segundos",
    ),
    "account_products_listed_success": (
        "info",
        "Produtos listados com sucesso. Quantidade de produtos encontrados: {count}",
    ),
    "node_status_block_download": (
        "error",
        "Atualmente o nó encontra-se no estado {status} que impede o download.",
    ),
    "node_class_not_found": (
        "error",
        "Classe do nó não encontrada. Verifique se o nó foi adicionado corretamente. Chave: {key}",
    ),
}
