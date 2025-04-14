import pandas as pd
import requests
from datetime import datetime
import time

# Load location and category data
locations_df = pd.read_csv("blinkit_locations.csv")
categories_df = pd.read_csv("blinkit_categories.csv")

# Define headers for all requests
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "access_token": "null",
    "app_client": "consumer_web",
    "app_version": "1010101010",
    "auth_key": "c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477",
    "content-type": "application/json",
    "device_id": "f439bb9f-2c96-4e0e-a5ae-d2bf97bfe0dc",
    "dnt": "1",
    "lat": "28.6217627",
    "lon": "77.0558233",
    "origin": "https://blinkit.com",
    "platform": "desktop_web",
    "priority": "u=1, i",
    "referer": "https://blinkit.com/cn/chips-crisps/cid/1237/940",
    "rn_bundle_version": "1009003012",
    "sec-ch-ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "session_uuid": "600540e8-889a-4fbd-b5f5-ca50d0bba27c",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "web_app_version": "1008010016",
    "x-age-consent-granted": "true"
}

# Function to fetch product data from listing_widgets API
def fetch_products_via_widgets(l0_cat, l1_cat):
    url = f"https://blinkit.com/v1/layout/listing_widgets?l0_cat={l0_cat}&l1_cat={l1_cat}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            widgets = response.json().get("widgets", [])
            for widget in widgets:
                data = widget.get("data", {})
                if "products" in data:
                    return data["products"]
        return []
    except Exception as e:
        print(f"❌ Error for category {l1_cat}: {e}")
        return []

# Function to map raw product data to your schema
def parse_product(product, location, cat_row):
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "l1_category": cat_row["l1_category"],
        "l1_category_id": cat_row["l1_category_id"],
        "l2_category": cat_row["l2_category"],
        "l2_category_id": cat_row["l2_category_id"],
        "store_id": f"{location['latitude']}_{location['longitude']}",
        "variant_id": product.get("id"),
        "variant_name": product.get("display_name"),
        "group_id": product.get("group_id"),
        "selling_price": product.get("price"),
        "mrp": product.get("mrp"),
        "in_stock": product.get("in_stock"),
        "inventory": product.get("inventory", {}).get("quantity") if product.get("inventory") else None,
        "is_sponsored": product.get("is_sponsored", False),
        "image_url": product.get("image_url"),
        "brand_id": product.get("brand_id"),
        "brand": product.get("brand_name")
    }

# Main execution loop
def main():
    all_data = []

    for _, loc in locations_df.iterrows():
        for _, cat in categories_df.iterrows():
            print(f"🔍 Scraping: {cat['l2_category']} @ {loc['latitude']}, {loc['longitude']}")
            products = fetch_products_via_widgets(cat['l1_category_id'], cat['l2_category_id'])
            for p in products:
                all_data.append(parse_product(p, loc, cat))
            time.sleep(1)  # Respectful delay

    # Save results to CSV
    df = pd.DataFrame(all_data)
    df.to_csv("blinkit_scraping_output.csv", index=False)
    print("✅ Scraping complete. Output saved to 'blinkit_scraping_output.csv'.")

if __name__ == "__main__":
    main()
