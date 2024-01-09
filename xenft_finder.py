from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pytz
from prettytable import PrettyTable
from math import log2

# Configurable options
ETH_TO_USD = True  # Set to False to use a fixed value
XEN_TO_USD = True  # Set to False to use a fixed value
ETH_USD_FIXED = 2300  # Used if ETH_TO_USD is False
XEN_USD_FIXED = 0.00000038  # Used if XEN_TO_USD is False
XEN_GLOBAL_RANK = 19_960_000 # This value should roughly represent XEN's Global Rank (find it here: https://xen.pub/index-xen-eth.php)
TERM_MIN = 100
VMU_MIN = 10
SORT_BY = "ratio"  # Options: "xen_per_usd", "price_per_vmu_usd", "ratio"
CLASS_VALUES = ["Rare++++++","Limited+++","Epic++++++","Xunicorn++","Legendary+","Exotic++++","Sapphire++","Aquamarine","Topaz+++++","Emerald+++","Amethyst++","Opal++++++","Xenturion+"]
MATURITY_YEARS = ["2024", "2025", "2026"]

# Convert CLASS_VALUES and MATURITY_YEARS to JSON strings
class_values_json = json.dumps(CLASS_VALUES)
maturity_years_json = json.dumps(MATURITY_YEARS)

def get_crypto_value(crypto_id, vs_currency):
    cg = CoinGeckoAPI()
    price = cg.get_price(ids=[crypto_id], vs_currencies=vs_currency)
    return price[crypto_id][vs_currency]

# Fetch current ETH and XEN to USD rates
eth_to_usd = get_crypto_value('ethereum', 'usd') if ETH_TO_USD else ETH_USD_FIXED
xen_to_usd = get_crypto_value('xen-crypto', 'usd') if XEN_TO_USD else XEN_USD_FIXED


# Convert CLASS_VALUES and MATURITY_YEARS to a JSON string for the 'filters' parameter
filters_dict = {
    "traits": [
        {"type": "Class", "values": CLASS_VALUES},
        {"type": "Maturity Year", "values": MATURITY_YEARS}
    ]
}
filters_json = json.dumps(filters_dict)

# Construct the URL
url = f'https://core-api.prod.blur.io/v1/collections/0x0a252663dbcc0b073063d6420a40319e438cfa59/tokens?filters={filters_json}'

# Set up and navigate to the URL
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# Process the JSON response
json_text = driver.find_element(by="xpath", value="/html/body/pre").text
data = json.loads(json_text)
driver.quit()

# Check if 'tokens' key exists in the response
if "tokens" not in data:
    print("Error: 'tokens' key not found in the response. Here is the response data:")
    print(data)
    exit()

# Process tokens
tokens_data = []
now_utc = datetime.now(pytz.utc)
for token in data["tokens"]:
    term = token["traits"].get("Term")
    if term and term.isdigit():
        term = int(term)
        if term > TERM_MIN:
            price_info = token.get("price")
            if price_info and float(price_info["amount"]) > 0:
                maturity_date_str = token["traits"].get("Maturity DateTime")
                days_remaining = None

                if maturity_date_str:
                    maturity_date = datetime.strptime(maturity_date_str, "%b %d, %Y %H:%M %Z")
                    maturity_date = maturity_date.replace(tzinfo=pytz.utc)
                    days_remaining = (maturity_date - now_utc).days

                    if days_remaining > 0:
                        price_amount = float(price_info["amount"])
                        vmus = int(token["traits"].get("VMUs", 0))
                        amp = int(token["traits"].get("AMP", 0))
                        cRank = int(token["traits"].get("cRank", 0))
                        xen = round(vmus * (log2(XEN_GLOBAL_RANK - cRank) * term * amp))
                        xenft_class = token["traits"].get("Class", "Unknown").strip()

                        if vmus > VMU_MIN:
                            price_per_vmu = price_amount / vmus
                            price_per_vmu_usd = price_per_vmu * eth_to_usd
                            xen_per_usd = round(xen / (price_amount * eth_to_usd)) if price_amount * eth_to_usd != 0 else 0
                            xen_in_usd = xen * xen_to_usd
                            ratio = xen_in_usd / (price_amount * eth_to_usd) if price_amount * eth_to_usd != 0 else 0

                            tokens_data.append({
                                "token_id": token['tokenId'],
                                "ratio": ratio,
                                "amp": amp,
                                "cRank": cRank,
                                "xen": xen,
                                "xen_in_usd": xen_in_usd,
                                "xen_per_usd": xen_per_usd,
                                "maturity_date": maturity_date_str,
                                "formatted_maturity_date": maturity_date.strftime("%a %d %b %Y"),
                                "term": term,
                                "days_remaining": days_remaining,
                                "price_eth": price_amount,
                                "price_usd": price_amount * eth_to_usd,
                                "vmus": vmus,
                                "price_per_vmu_eth": price_per_vmu,
                                "price_per_vmu_usd": price_per_vmu_usd,
                                "xenft_class": xenft_class,
                            })

# Sort the tokens
sort_order = True if SORT_BY in ["xen_per_usd", "ratio"] else False
sorted_tokens = sorted(tokens_data, key=lambda x: x[SORT_BY], reverse=sort_order)

# Create and populate a PrettyTable
table = PrettyTable()
table.field_names = ["Token", "XENFT Type", "Maturity", "Term", "Term Left", "VMUs", "AMP", "cRank", "Xen", "Xen/USD", "Ratio", "Price", "Price/VMU", "URL"]
for token in sorted_tokens:
    token_url = f"https://blur.io/asset/0x0a252663dbcc0b073063d6420a40319e438cfa59/{token['token_id']}"
    price_info = f"{token['price_eth']} ETH (${token['price_usd']:.2f})"
    price_per_vmu_info = f"{token['price_per_vmu_eth']:.6f} ETH (${token['price_per_vmu_usd']:.2f})"
    ratio = token['ratio']
    xen_formatted = f"{token['xen']:,} (${token['xen_in_usd']:,.2f})"
    xen_per_usd_formatted = f"{token['xen_per_usd']:,}"

    table.add_row([
        token['token_id'],
        token['xenft_class'],
        token['formatted_maturity_date'],
        token['term'],
        token['days_remaining'],
        token['vmus'],
        token['amp'],
        token['cRank'],
        xen_formatted,
        xen_per_usd_formatted,
        f"{ratio:.2f}",
        price_info,
        price_per_vmu_info,
        token_url
    ])

# Print the table
print(table)
