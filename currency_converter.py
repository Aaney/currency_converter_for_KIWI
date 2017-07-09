# -*- coding: utf-8 -*-

# The script is meant to be used with a specific input, taking a) amount of
# an input currency, and its currency code or symbol, or b) the amount
# of an input currecy, its code/symbol and the output currencies' codes/symbols.

# The script works in two ways:
# 1) It can be used via a CLI (Command Line Interface) in the following format:
# C:\Projects\currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
# C:\Projects\currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
# C:\Projects\currency_converter.py --amount 10.92 --input_currency £
# The input to the Command Line then looks e.g. on Windows 10 as follows:
# C:\Python\Python36\python.exe "C:\Projects\currency_converter.py" --amount 100.0 --input_currency EUR --output_currency CZK

# 2) By executing the script, local web API is activated on the address localhost:8080,
# to which the user has to add the GET request suffix, in the following format:
# /?amount=100.0&input_currency=EUR&output_currency=CZK
# /?amount=0.9&input_currency=¥&output_currency=AUD
# /?amount=10.92&input_currency=£
# The address then looks e.g. as follows:
# localhost:8080/?amount=100.0&input_currency=EUR&output_currency=CZK

# Five Python modules are used: urllib.request to get data from a website that provides
# currency rates from the European Central Bank, and json for work with the
# required output format. The library sys is used to differentiate between the usage mode,
# i.e. whether a CLI will be used, or if a web API is going to be activated (in case the CLI
# mode is used the script takes input directly from the command line, and outputs right in the
# terminal; in the other case the script is handled from a browser, and the output is displayed
# in the browser window as plain text). The http.server module is used to create a local
# server on which the web API of this script can run (in case the web API usage mode is activated by
# running the script without any parametters in the command line). The urllib.parse module is
# used in the web API mode to parse the url (e.g. localhost:8080/?amount=100.0&input_currency=EUR)
# into components, that are that are then fed to the main function, which calculates the currency
# conversion and returns a json output.

import urllib.request, json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

PORT_NUMBER = 8080
raw = []


def convert(raw):
    # This is the function doing most of the work - it takes input from either selected interface,
    # calculates the output and returns a JSON consisting of input amount, input currency, and
    # output currency or currencies and their converted amounts.


    # The variable currency_symbols consists of a dictionary created manually, with
    # information from http://www.xe.com/symbols.php and Wikipedia.
    # Edit June 12th: After uploading to Github I noticed some of the currency symbols are not
    # displayed correctly, despite working alright on my computer. Perhaps the currency symbol
    # categorization should be only limited to symbols present in most fonts, like $, €, ¥, and £.
    currency_symbols = {"$": "AUD,CAD,HKD,MXN,NZD,SGD,USD", "€": "EUR", "¥": "CNY,JPY",
                        "£": "GBP", "A$": 'AUD', "лв.": "BGN", "R$": "BRL", "Can$": "CAD", "C$": "CAD",
                        "Fr.": "CHF", "SFr.": "CHF", "元": "CNY,HKD", "RMB": "CNY", "Kč": "CZK",
                        "HK$": "HKD", "kn": "HRK", "Ft": "HUF", "Rp": "IDR", "₪": "ILS", "₹": "INR",
                        "₩": "KRW", "Mex$": "MXN", "RM": "MYR", "kr": "DKK,NOK,SEK", "NZ$": "NZD",
                        "₱": "PHP", "zł": "PLN", "lei": "RON", "₽": "RUB", "руб": "RUB", "S$": "SGD",
                        "฿": "THB", "บาท": "THB", "₺": "TRY", "TL": "TRY", "US$": "USD", "R": "ZAR"}

    input_amount = 0.0
    passing_currency_in = []
    input_currency = ""
    passing_currency_out = []
    output_currency = ""

    # The three for cycles below take the input, separate it by the given
    # keywords, and, in case the input is in currency symbols, transform
    # symbols into currency codes.
    for a, b in enumerate(raw):
        if b == "--amount":
            input_amount = float(raw[a + 1])
        if b == "--input_currency":
            passing_currency_in.append(raw[a + 1])
        if b == "--output_currency":
            passing_currency_out = raw[a + 1].split(",")

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
            output_currency += currency_symbols[symbol_out] + ","
        else:
            output_currency += symbol_out + ","

    # This if-else statement passes the currency codes obtained from the cycles above
    # to a URL which gives back currency rates.
    if len(output_currency) == 0:
        src = "http://api.fixer.io/latest?base={}".format(input_currency)
    else:
        src = "http://api.fixer.io/latest?base={}&symbols={}".format(input_currency, output_currency)

    # The following part of code gets currency rates based on the input via the
    # http://api.fixer.io API in JSON format. Afterwards another JSON is returned,
    # which contains the input amount and currency, as well as the requested
    # output currencies.
    try:
        with urllib.request.urlopen(src) as url:
            rates_from_outside_service = json.loads(url.read().decode())
        input_amount_and_currency = {"amount": input_amount, "currency": input_currency}
        output_amounts = {}
        for key, value in rates_from_outside_service["rates"].items():
            output_amounts.update({key: round(input_amount * value, 2)})
        return json.dumps({"input": input_amount_and_currency, "output": output_amounts}, sort_keys=True, indent=4)

    except urllib.error.HTTPError as e:
        # print(e.code)
        pass
    except urllib.error.URLError:
        print("Wrong URL")


class myHandler(BaseHTTPRequestHandler):
    # This class handles any incoming request from the browser
    # The structure and content of this class is based on the example1.py on
    # the following website: https://www.acmesystems.it/python_httpd BaseHTTPRequestHandler

    # Handler for the GET requests
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Send the html message
            k = parse_qs(self.path[2:])
            out = []
            for key, value in k.items():
                if key == "amount":
                    out.append("--amount")
                    out.append(value[0])
                if key == "input_currency":
                    out.append("--input_currency")
                    out.append(value[0])
                if key == "output_currency":
                    out.append("--output_currency")
                    out.append(value[0])
            self.wfile.write(convert(out).encode("utf-8"))
            print(convert(out))
            return
        except AttributeError:
            # The occurs an AttributeError several times - this takes care of it
            # not to print the error messages in the terminal (not sure at the moment how severe
            # issue this is).
            pass

if len(sys.argv) > 1:
    # Get input from the command line, in case there is any...
    raw = sys.argv[1:]
    print(convert(raw))

else:
    # ... or make a server and activate the web API - the code below is
    # based on the same source as the myHandler class above, i.e. the following
    # website: https://www.acmesystems.it/python_httpd

    try:
        # Create a web server and define the handler to manage the
        # incoming request

        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print('Started httpserver on port ', PORT_NUMBER)

        # Wait forever for incoming http requests
        server.serve_forever()
        
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()


