# TD Ameritrade API Key
# Get one for free at https://developer.tdameritrade.com/
API_KEY = ""

# Ticker of the stock you want spreads of, no $ needed
SYMBOL = ""

# Price where you want the strike to break even
TARGET_PRICE = 0

# Price where you do not expect the stock to exceed
UPPER_LIMIT = 0

# CONFIDENCE INTERVAL - HOW MUCH CAN IT DEVIATE FROM TARGET PRICE AND UPPER LIMIT
# Recommended - at least 8-10%
CI = 0.1

# TIMEFRAME - Over 1/2 year?
TIMEFRAME_LONG = True
