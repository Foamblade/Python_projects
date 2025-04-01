import sys
import requests

try:
    n = float(sys.argv[1])
except:
    sys.exit("Command-line argument is not a number")

try:
    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
    rate = r['bpi']['USD']['rate_float']
    amount = rate*n
    print(f"${amount:,.4f}")
except requests.RequestException:
    ...
