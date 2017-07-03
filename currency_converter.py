# The script is meant to be used with a specific input, taking a) amount of 
# an input currency, and an output currency code or symbol, or b) the amount
# of an input currecy, its code/symbol and the output currencies' codes/symbols.

# The script works in two ways:
# 1) It can be used via a CLI (Command Line Interface) in the following format:
# way/to/cnvrtr/currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
# way/to/cnvrtr/currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
# way/to/cnvrtr/currency_converter.py --amount 10.92 --input_currency £

# 2) By executing the script, an input field is activated, to which the user has to
# type the GET request, in the following format:
# GET /currency_converter?amount=100.0&input_currency=EUR&output_currency=CZK HTTP/1.1
# GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
# GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1

# Three Python libraries are used: urllib to get data from a website that provides
# currency rates from the European Central Bank, and json for work with the
# required output format. The library sys is used only to get a user input via
# the CLI.


import urllib.request, json, sys

raw = []
if len(sys.argv) > 1:
    # Get input from the command line, in case there is any...
    raw = sys.argv[1:]

else:
    # ... or get input via the input() function, in the following format:
    # GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
    try:
        get_src = input().split()
        if get_src[0]=="GET" and get_src[2]=="HTTP/1.1":
            adr = get_src[1].split("?")[1].split("&")
            aio = {}
            for i in adr:
                j = i.split("=")
                for k in j:
                    aio[j[0]] = j[1]
            for key, value in aio.items():
                raw.append("--" + key)
                raw.append(value)
    except NameError or IndexError:
        print("Incorrect input!")
    
# The variable currency_symbols consists of a dictionary created manually, with
# information from http://www.xe.com/symbols.php and Wikipedia.
# Edit June 12th: After uploading to Github I noticed some of the currency symbols are not displayed
# correctly, despite working alright on my computer. Perhaps the currency symbol
# categorization should be only limited to symbols present in most fonts, like $, €, ¥, and £.
currency_symbols = {"$":"AUD,CAD,HKD,MXN,NZD,SGD,USD", "€":"EUR", "¥":"CNY,JPY",
"£":"GBP", "A$":'AUD', "лв":"BGN", "лв.":"BGN", "R$":"BRL", "Can$":"CAD",
"C$":"CAD", "Fr.":"CHF", "SFr.":"CHF", "元":"CNY,HKD", "RMB":"CNY", "Kč":"CZK",
"kr":"DKK", "HK$":"HKD", "kn":"HRK", "Ft":"HUF", "Rp":"IDR", "₪":"ILS",
"₹":"INR", "₩":"KRW", "Mex$":"MXN", "RM":"MYR", "kr":"NOK,SEK", "NZ$":"NZD",
"₱":"PHP", "zł":"PLN", "lei":"RON", "₽":"RUB", "руб":"RUB", "S$":"SGD",
"฿":"THB", "บาท":"THB", "₺":"TRY", "TL":"TRY", "US$":"USD", "R":"ZAR"}

input_amount = 0.0
passing_currency_in = []
input_currency = ""
passing_currency_out = []
output_currency = ""


# The three for cycles below take the input, separate it by the given
# keywords, and, in case the input is in currency symbols, transform
# symbols into currency codes.
for a,b in enumerate(raw):
    if b == "--amount":
        input_amount = float(raw[a+1])
    if b == "--input_currency":
        passing_currency_in.append(raw[a+1])
    if b == "--output_currency":
        passing_currency_out = raw[a+1].split(",")

for symbol_in in passing_currency_in:
    if symbol_in in currency_symbols:
        input_currency = currency_symbols[symbol_in].split(',')[0]
        # The line above takes the the same dictionary as the output cycle
        # below - it however can pass only one currecy code to the URL,
        # which gives back currency rates, and so it takes the first relevant
        # option for the given currency symbol.
    else:
        input_currency = symbol_in
        
for symbol_out in passing_currency_out:
    if symbol_out in currency_symbols:
        output_currency += currency_symbols[symbol_out]+","
    else:
        output_currency += symbol_out + ","
        
        
# This if-else statement passes the currency codes obtained from the cycles above
# to a URL which gives back currency rates.
if len(output_currency) == 0:
    src = "http://api.fixer.io/latest?base={}".format(input_currency)
else:
    src = "http://api.fixer.io/latest?base={}&symbols={}".format(input_currency, output_currency)


# The following part of code gets currency rates based on the input via the
# http://api.fixer.io API in JSON format. Afterwards another JSON is printed,
# which contains the input amount and currency, as well as the requested
# output currencies. Return can be used instead of print() in case the output
# is meant to be further processed.
try:
    with urllib.request.urlopen(src) as url:
        rates_from_outside_service = json.loads(url.read().decode())
    # print(json.dumps(rates_from_outside_service, sort_keys=True, indent=4))
    input_amount_and_currency = {"amount": input_amount, "currency": input_currency}
    output_amounts = {}
    for key, value in rates_from_outside_service["rates"].items():
        output_amounts.update({key: round(input_amount * value, 2)})
    print(json.dumps({"input": input_amount_and_currency, "output": output_amounts}, sort_keys=True, indent=4))

except urllib.error.HTTPError as e:
    print(e.code)
except urllib.error.URLError:
    print("Wrong URL")
