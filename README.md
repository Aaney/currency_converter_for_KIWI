# currency_converter_for_KIWI
Currency converter task for KIWI.com - June/July 2017

Author: Anestis Karasaridis

Assignment link: https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c

Changelog:

Edit July 11th: Just found out about the built-in sys.argparse function... I've been sort of inventing the wheel on this with sys.argv... Well, the script would have worked the same if argparse was used, which might have helped with troubleshooting too, but basically the current code does the same (the arguments that are used here aren't predefined, as they would have been in the case of argparse usage).

Edit July 9th: The web API sort of works fine on Python 3.6 - the first issue was that previously the output to the web browser wasn't encoded to utf-8, which led to the code not working via this interface. The second issue at the moment were numerous AttributeError messages in the terminal when using the web API - solved via a lousy except-pass statement. Also the web API output looks nicer now - instead of text/html its type is now application/json.

Edit July 8th: Added a more or less working web API (using the accessible via the localhost after running the script) - still testing it though (it doesn't output a "pretty" json as the CLI, just an unindented string). The CLI works still the same (OK).

Edit June 12th: After uploading to Github I noticed some of the currency symbols are not displayed correctly, despite working alright on my computer. Perhaps the currency symbol categorization should be only limited to symbols present in most fonts, like $, €, ¥, and £.
