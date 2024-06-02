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
    "node_name_not_found",
    "node_start_mapping_children",
    "node_success_mapped",
    "node_start_download",
    "node_success_downloaded",
    "node_marked_as_not_be_downloaded",
    "content_already_downloaded",
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
    "node_name_not_found": (
        "error",
        "Erro eo tentar obter o nome do '{node_type}'. Será utilizado algo como '{order}. {node_type}' na nomeclatura.",
    ),
    "node_start_mapping_children": (
        "info",
        "Iniciando o mapeamento dos filhos do nó. Este processo pode demorar alguns segundos.",
    ),
    "node_success_mapped": (
        "info",
        "Mapeamento concluído com sucesso. Foram encontrados {count} {children_type}s",
    ),
    "node_start_download": (
        "info",
        "Iniciando o download. Este processo pode demorar alguns segundos (talvez minutos.)",
    ),
    "node_success_downloaded": (
        "info",
        "Download concluído com sucesso!!",
    ),
    "node_marked_as_not_be_downloaded": (
        "info",
        "Download pulado uma vez que foi marcado como 'Não baixar'.",
    ),
    "content_already_downloaded": (
        "info",
        "Conteúdo já foi baixado numa execução anterior do script.",
    ),
}


POSSIBLE_QUALITIES = Literal[
    "hd", "sd", "1080p", "720p", "480p", "360p", "240p", "144p"
]

QUALITIES_PRIORITY: Mapping[POSSIBLE_QUALITIES, int] = {
    "hd": 1,
    "sd": 3,
    "1080p": 0,
    "720p": 1,
    "480p": 2,
    "360p": 3,
    "240p": 4,
    "144p": 5,
}
