from typing import Protocol
from click import Group

class FetchPlugin(Protocol):
    def register_fetch(self, fetch_group: Group) -> None:
        """Attach one or more `fetch` subcommands to the group."""
