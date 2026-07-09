from typing import Optional

def get_id_for_scm(name: str, title: Optional[str]):
    return name if title == '' else f'{name}, {title}'