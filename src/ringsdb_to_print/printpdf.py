import os
import re
import tempfile

import requests
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def fetch_deck_json(deck_url):
    # Extract deck id from URL
    match = re.search(r"/decklist/view/(\d+)/", deck_url)
    if not match:
        raise ValueError("Invalid RingsDB deck URL")
    deck_id = match.group(1)
    api_url = f"https://ringsdb.com/api/public/decklist/{deck_id}"
    resp = requests.get(api_url)
    resp.raise_for_status()
    return resp.json()


def fetch_card_image_to_file(card_code, folder):
    url = f"https://ringsdb.com/bundles/cards/{card_code}.png"
    resp = requests.get(url)
    resp.raise_for_status()
    img = Image.open(BytesIO(resp.content))
    img_path = os.path.join(folder, f"{card_code}.png")
    img.save(img_path)
    return img_path


def generate_pdf_from_ringsdb(deck_url, output_path="output.pdf"):
    deck = fetch_deck_json(deck_url)
    cards = []
    for card_code, quantity in deck["slots"].items():
        for _ in range(quantity):
            cards.append(card_code)
    card_w, card_h = 63.5 * mm, 88 * mm
    cards_per_page = 8
    cols, _ = 4, 2

    with tempfile.TemporaryDirectory() as tempdir:
        img_paths = []
        for code in cards:
            img_path = fetch_card_image_to_file(code, tempdir)
            img_paths.append(img_path)

        c = canvas.Canvas(output_path, pagesize=landscape(A4))
        block_w = cols * card_w
        block_h = 2 * card_h
        x_offset = int(round((c._pagesize[0] - block_w) / 2))
        y_offset = int(round((c._pagesize[1] - block_h) / 2))
        for i in range(0, len(img_paths), cards_per_page):
            batch = img_paths[i : i + cards_per_page]
            for idx, img_path in enumerate(batch):
                col = idx % cols
                row = idx // cols
                x = x_offset + int(round(col * card_w))
                y = y_offset + int(round((1 - row) * card_h))
                c.drawImage(
                    img_path,
                    x,
                    y,
                    card_w,
                    card_h,
                    preserveAspectRatio=False,
                    anchor="nw",
                )
            c.showPage()
        c.save()
    print(f"PDF saved to {output_path}")
