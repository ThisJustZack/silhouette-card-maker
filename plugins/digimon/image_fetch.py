from os import path
from requests import Response, get
from time import sleep

CARD_ART_URL_TEMPLATE = 'https://world.digimoncard.com/images/cardlist/card/{card_number}.png'

def request_digimon(query: str) -> Response:
    r = get(query, headers = {'user-agent': 'silhouette-card-maker/0.1', 'accept': '*/*'})

    r.raise_for_status()
    sleep(0.15)
    
    return r

def fetch_card_art(index: int, card_number: str, quantity: int, front_img_dir: str):

    card_art = request_digimon(CARD_ART_URL_TEMPLATE.format(card_number=card_number)).content
    
    if card_art is not None:
        # Save image based on quantity
        for counter in range(quantity):
            image_path = path.join(front_img_dir, f'{index}{card_number}_{counter + 1}.jpg')

            with open(image_path, 'wb') as f:
                f.write(card_art)

            print(f'{image_path}')

            
def get_handle_card(
    front_img_dir: str
):
    def configured_fetch_card(index: int, card_number: str, quantity: int):
        fetch_card_art(
            index,
            card_number,
            quantity,
            front_img_dir
        )

    return configured_fetch_card