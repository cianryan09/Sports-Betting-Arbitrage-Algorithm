# Import libraries
import betfairlightweight
from betfairlightweight import filters
import betfairlightweight.endpoints
import pandas as pd
import numpy as np
import os
import datetime
import json
import requests

# Change this certs path to wherever you're storing your certificates
certs_path = "C:\\Users\\Cian\\Desktop\\Personal\\Betfair\\"

# Change these login details to your own
my_username = "brickwall3031"
my_password = "Hotspur123!"
my_app_key = "Y7EhzfhOmfOK6RcG"

trading = betfairlightweight.APIClient(username=my_username,
                                       password=my_password,
                                       app_key=my_app_key,
                                       certs=certs_path)

trading.login_interactive()

trading.historic.read_timeout = 100

account = betfairlightweight.endpoints.Account(trading)

funds = account.get_account_funds(wallet='UK', session=requests.Session(), lightweight=True)['availableToBetBalance']
print(funds)