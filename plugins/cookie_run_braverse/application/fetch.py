from sys import path
from pathlib import Path
from click import command, argument, Choice
from asyncio import run

# Add plugin directory to path to allow imports when run as a script
path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from plugins.cookie_run_braverse.application.CookieRunPlugin import CookieRunDeckFormats, CookieRunPlugin

@command()
@argument('deck_path')
@argument('format', type=Choice([t.value for t in CookieRunDeckFormats], case_sensitive=False))
def cli(deck_path: str, format: CookieRunDeckFormats):
    is_deck_a_file: bool = Path(deck_path).exists()

    plugin = CookieRunPlugin(CookieRunDeckFormats(format))

    if not plugin.is_inline_format and not is_deck_a_file:
        print(f'{deck_path} is not a valid file.')
        return   
    
    run(plugin.run(deck_path))

if __name__ == '__main__':
    cli()