from sys import path
from pathlib import Path
from click import command, argument, Choice
from asyncio import run

# Add plugin directory to path to allow imports when run as a script
path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from plugins.netrunner.application.NetrunnerPlugin import NetrunnerDeckFormats, NetrunnerPlugin

@command()
@argument('deck_path')
@argument('format', type=Choice([t.value for t in NetrunnerDeckFormats], case_sensitive=False))
def cli(deck_path: str, format: NetrunnerDeckFormats):
    if not Path(deck_path).exists():
        print(f'{deck_path} is not a valid file.')
        return
    
    plugin = NetrunnerPlugin(NetrunnerDeckFormats(format))
    
    run(plugin.run(deck_path))

if __name__ == '__main__':
    cli()