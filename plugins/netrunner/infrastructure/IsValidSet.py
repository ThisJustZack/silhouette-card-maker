from re import sub

from plugins.abstraction_base.infrastructure.WebRequest import perform_web_request

NETRUNNERDB_SET_URL_TEMPLATE = 'https://api-preview.netrunnerdb.com/api/v3/public/card_sets/{SET_NAME}'

async def is_valid_set(set_name: str) -> bool:
    # Attempt to query for set info
    sanitized = sub(r'[^A-Za-z0-9 ]+', '', set_name)
    slugified = sub(r' ', '_', sanitized).lower()

    # Web requests can fail with a None response
    request = await perform_web_request(NETRUNNERDB_SET_URL_TEMPLATE.format(SET_NAME=slugified))

    if request is not None:
        return True
    else:
        return False
