# Riftbound Plugin

This plugin reads a decklist, fetches the card image from either [Piltover Archive](https://piltoverarchive.com/) or [Riftmana](https://riftmana.com/), and puts the card images into the proper `game/` directories.

This plugin supports many decklist formats such as `tts` and `piltover_archive`. To learn more, see [here](#formats).

## Basic Instructions

Navigate to the [root directory](../..) as plugins are not meant to be run in the [plugin directory](.).

If you're on macOS or Linux, open **Terminal**. If you're on Windows, open **PowerShell**.

Create and start your virtual Python environment and install Python dependencies if you have not done so already. See [here](../../README.md#basic-usage) for more information.

Put your decklist into a text file in [game/decklist](../game/decklist/). In this example, the filename is `deck.txt` and the decklist format is Tabletop Simulator (`tts`).

Run the script.

```sh
python plugins/riftbound/application/fetch.py game/decklist/deck.txt tts
```

Now you can create the PDF using [`create_pdf.py`](../../README.md#create_pdfpy).

## CLI Options

```
Usage: fetch.py [OPTIONS] DECK_PATH {piltover_archive|tts}

Options:
  --source [piltover_archive|riftmana]
                                  The desired image source.  [default:
                                  piltover_archive]
  --help                          Show this message and exit.
```

## Formats

### `piltover_archive`

[Piltover Archive](https://piltoverarchive.com) format.

```
1 Viktor, Herald of the Arcane

1 Viktor, Leader

3 Seal of Unity
3 Stupefy
3 Hidden Blade
3 Siphon Power
3 Soaring Scout
3 Cull the Weak
3 Watchful Sentry
3 Faithful Manufactor
3 Vanguard Captain
3 Cruel Patron
3 Machine Evangel
3 Grand Strategem
3 Harnessed Dragon

1 Targon's Peak
1 Trifarian War Camp
1 Obelisk of Power

12 Order Rune
```

### `tts`

Tabletop Simulator format.

```
OGN-265-1 OGN-246-1 OGN-245-1 OGN-245-1 OGN-245-1 OGN-095-1 OGN-095-1 OGN-095-1 OGN-213-1 OGN-213-1 OGN-213-1 OGN-266-1 OGN-266-1 OGN-266-1 OGN-216-1 OGN-216-1 OGN-216-1 OGN-209-1 OGN-209-1 OGN-209-1 OGN-096-1 OGN-096-1 OGN-096-1 OGN-211-1 OGN-211-1 OGN-211-1 OGN-218-1 OGN-218-1 OGN-218-1 OGN-208-1 OGN-208-1 OGN-208-1 OGN-239-1 OGN-239-1 OGN-239-1 OGN-233-1 OGN-233-1 OGN-233-1 OGN-234-1 OGN-234-1 OGN-234-1 OGN-289-1 OGN-294-1 OGN-284-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1 OGN-214-1
```