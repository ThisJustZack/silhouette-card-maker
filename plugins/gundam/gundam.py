from os import path
from requests import Response, get
from time import sleep

CARD_ART_URL_TEMPLATE = 'https://www.gundam-gcg.com/en/images/cards/card/{card_number}.webp'

OUTPUT_CARD_ART_FILE_TEMPLATE = '{deck_index}{card_number}{quantity_counter}.png'

def request_bandai(query: str) -> Response:
    r = get(query, headers = {'user-agent': 'silhouette-card-maker/0.1', 'accept': '*/*'})

    r.raise_for_status()
    sleep(0.15)

    return r

def fetch_card(
    index: int,
    quantity: int,
    card_number: str,
    front_img_dir: str,
):

    # Query for card info
    card_art = request_bandai(CARD_ART_URL_TEMPLATE.format(card_number=card_number)).content
    
    if card_art is not None:
        # Save image based on quantity
        for counter in range(quantity):
            image_path = path.join(front_img_dir, OUTPUT_CARD_ART_FILE_TEMPLATE.format(deck_index=str(index), card_number=card_number, quantity_counter=str(counter + 1)))

            with open(image_path, 'wb') as f:
                f.write(card_art)

def get_handle_card(
    front_img_dir: str,
):
    def configured_fetch_card(index: int, card_number: str, quantity: int = 1):
        fetch_card(
            index,
            quantity,
            card_number,
            front_img_dir
        )

    return configured_fetch_card