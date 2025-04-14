# BlinkIt Category Scraping

This project scrapes subcategory product data from BlinkIt’s public API based on given latitude/longitude and category IDs.

## 📋 Input Files
- `blinkit_locations.csv` — list of coordinates
- `blinkit_categories.csv` — category and subcategory IDs

## 📤 Output
- `blinkit_scraping_output.csv` — full dataset with fields:
  - date, l1_category, l2_category, variant_id, group_id, price, etc.

## ▶️ How to Run

```bash
# activate your virtual env
source env/Scripts/activate

# install dependencies
pip install -r requirements.txt

# run the script
python blinkit_scraper.py
# blinkit-scraper
