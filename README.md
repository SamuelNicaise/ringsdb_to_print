# ringsdb_to_print

Generate a printable PDF from a RingsDB deck

## Installation

```bash
conda create -n ringsdb_to_print python=3.10
conda activate ringsdb_to_print
git clone --shared https://github.com/SamuelNicaise/ringsdb_to_print.git
cd ringsdb_to_print
pip install -e . 
```

## Usage example

```bash
python -m ringsdb_to_print printpdf -u "https://ringsdb.com/decklist/view/6936/caldara-2-0-1.0 -o deck.pdf"
```

This will create `deck.pdf` containing all card images in the deck, sized 63.5x88mm.
