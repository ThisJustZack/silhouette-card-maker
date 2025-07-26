# Grand Archive Plugin

This plugin reads a decklist, fetches the card image from the [Grand Archive website](https://gatcg.com), and puts the card images into the proper `game/` directories.

This plugin currently supports the ``Cockatrice/Omnidex`` format.

## Instructions

Navigate to the [root directory](../..), as the plugins are not meant to be run in the [plugin directory](.).

Open a terminal on your device in the root directory.

> [!NOTE]
> On Windows, this would be the ``PowerShell`` application, unless you use another terminal of your choice.
>
> On MacOS or Linux, this would be the ``Terminal`` application, unless you use another terminal of your choice.

Create and start your Python virtual environment in the terminal.
```bash
.\venv\Scripts\Activate.ps1
```

> [!WARNING]
> If this fails on Windows due to authorization policy issues, then run the following command to get around it.
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

Then install the Python dependencies in the Python virtual environment using the following command.
```bash
pip install -r requirements.txt  
```

Put your decklist into a text file within the [decklist directory/folder](../../game/decklist).

Now, you are ready to run the program to generate the images for the deck using the following command.
```bash
python plugins/grand_archive/fetch.py game/decklist/deck.txt cockatrice
```

And finally, you can generate the [PDF files](../../README.md#create_pdfpy) for the deck to print so that you can play at the table!

## CLI Options

There are currently no additional options to run with the program, however they can be added on for any scenario that you may come across.