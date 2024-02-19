import requests

def get_btc_exchange_rate(currency="EUR"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
    response = requests.get(url).json()
    return response["bitcoin"][currency.lower()]

def get_mempool_fees():
    url = "https://mempool.space/api/v1/fees/recommended"
    response = requests.get(url).json()
    return response

def calculate_net_btc_and_satoshis(amount_in_fiat, money_changer_fee_percentage, currency="EUR"):
    exchange_rate = get_btc_exchange_rate(currency)
    fees = get_mempool_fees()
    mining_fee_sats_per_byte = fees['fastestFee']
    # Assuming a transaction size, adjust as necessary
    mining_fee_btc = (mining_fee_sats_per_byte * 250) / 1e8  # Convert satoshis to BTC
    ln_opening_fee_btc = mining_fee_btc  # Assuming same fee for opening LN channel
    
    net_fiat_after_fee = amount_in_fiat - (amount_in_fiat * money_changer_fee_percentage / 100)
    btc_before_network_fees = net_fiat_after_fee / exchange_rate
    net_btc = btc_before_network_fees - (mining_fee_btc + ln_opening_fee_btc)
    net_satoshi = net_btc * 1e8  # Convert net BTC to satoshis
    
    return net_btc, net_satoshi

# User input
try:
    amount_in_fiat = float(input("Za koľko chceš kúpiť BTC ? (napr. 500 EUR): ")) #Enter the amount in fiat currency (e.g., 500 EUR)
    money_changer_fee_percentage = float(input("Aký poplatok si pýta vekslák ? (napr. 3%): ")) #Enter the money changer (vekslák) fee percentage (e.g., 3%)
except ValueError:
    print("Invalid input. Please enter a numerical value.")
else:
    net_btc, net_satoshi = calculate_net_btc_and_satoshis(amount_in_fiat, money_changer_fee_percentage)
    print(f"Na LN peňaženke by ti malo pristáť {net_btc:.8f} BTC resp. {net_satoshi:.0f} satoshis") #Net BTC or Satoshis after all fees
