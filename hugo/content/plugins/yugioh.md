---
title: 'Yu-Gi-Oh!'
weight: 5
---

This plugin reads a decklist, fetches card art from [ygoprodeck](https://ygoprodeck.com/card-database), and puts them in the proper `game/` directories.

This plugin supports the following decklist formats: `ydk`, `ydke`. To learn more, see [here](#formats).

## Basic Instructions

Navigate to the root directory as plugins are not meant to be run in the plugins directory.

If you're on macOS or Linux, open **Terminal**. If you're on Windows, open **PowerShell**.

Create and start your virtual Python environment and install Python dependencies if you have not done so already. See [here]({{% ref "../docs/create/#basic-usage" %}}) for more information.

Put your decklist into a text file in `game/decklist`. In this example, the filename is `deck.ydk` and the decklist format is YDK (`ydk`).

Run the script.

```sh
python plugins/yugioh/fetch.py game/decklist/deck.ydk ydk
```

Now you can create the PDF using [`create_pdf.py`]({{% ref "../docs/create" %}}). You should use `--card_size japanese` for the correct card size.

## CLI Options

```
Usage: fetch.py [OPTIONS] DECK_PATH {ydke|ydk}

Options:
  --help  Show this message and exit.
```

## Formats

### `ydk`

YDK is the file format used by [ygoprodeck](https://ygoprodeck.com/) and edopro.

```
#main
91073013
92895501
92895501
92895501
9091064
9091064
9091064
91025875
92248362
#extra
90448279
90303227
61374414
64276752
!side
27204311
27204311
82385847
```

### `ydke`

YDKE is a compressed version of YDK that allows decks to be easily imported or exported into YGO Omega, edopro, or [ygoprodeck](https://ygoprodeck.com/) via copy/paste. It begins with `ydke://` followed by a long string.

```
ydke://CDfpAQg36QGBAyEEgQMhBOcqwwXnKsMFSIA/AUiAPwFIgD8B/s84AJuTywGbk8sBm5PLATUHgwI1B4MCNQeDAv2JnAX9iZwF/YmcBdcanwGglAQCE0dlADm+EgQ5vhIE/fqRBYv9YwAQLRoCEC0aAhAtGgIeN4IBPqRxAf4KgAQiSJkAIkiZACJImQBL8mcCS/JnAkvyZwIkQTwBNlmlBQ==!tGFNAfmCDgQUh7AFmBskA45gkQMm1FgAQvNMAGlM5gWNJ5gDSw97ATI1VQLERCEFqRp+AMoavwGS+pQA!reIKAq3iCgKt4goCRK0EBUStBAVErQQF+9wUAUO+3QBDvt0AtYgRALWIEQC1iBEAkvrlAWaDAgCc4b0A!
```

You can also use YDKE directly in the command line. Note the single quotes around the YDKE.

```sh
python plugins/yugioh/fetch.py 'ydke://...' ydke
```