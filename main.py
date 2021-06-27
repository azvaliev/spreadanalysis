from urllib.request import urlopen
import json
import pprint

APIKEY = "PRXEUA8NGTONOWLNLGAOCCSLGKUKN41H"
SYMBOL = "PLTR"
# Price where you want the strike to break even
TARGET_PRICE = 25
# Price where you do not expect the stock to exceed
UPPER_LIMIT = 30
# INTERVAL - Rounded to nearest 0.5
SPREAD = UPPER_LIMIT - TARGET_PRICE
if int(UPPER_LIMIT - TARGET_PRICE) != SPREAD:
    INTERVAL = round((SPREAD) * 2) / 2
else:
    INTERVAL = SPREAD
# CONFIDENCE INTERVAL - HOW MUCH CAN IT DEVIATE FROM TARGET PRICE AND UPPER LIMIT
CI = 0.2
# TIMEFRAME - Over 1/2 year?
TIMEFRAME_LONG = True


def sort_chain(data,target_price,upper_limit):
    # Sorted by two cheapest, two least risk
    # Set it to some ridiculous number so there is something to reference for first iteration
    value_spread = {
            "Cost": 1000000000.0,
            "Buy Call": 1000000000.0
        }

    value_spread_2 = {
            "Cost": 1000000000,
            "Buy Call": 1000000000.0
        }
    max_profit_spread = {
            "Max Profit": 0
        }
    max_profit_spread_2 = {
            "Max Profit": 0
        }
    for x in range(0, len(data)):
        if TIMEFRAME_LONG:
            if data[x]["daysToExp"] >= 200:
                for y in range(0, len(data[x]["optionStrategyList"])):
                    strike = str(data[x]["optionStrategyList"][y]["strategyStrike"])
                    strike = strike.split("/")
                    if float(strike[1]) > TARGET_PRICE * (1+(CI/2)):
                        if float(strike[0]) >= (target_price * (1 - CI)) and float(strike[1]) <= (upper_limit * (1 + CI)):
                            strategy_cost = float(data[x]["optionStrategyList"][y]["strategyAsk"])
                            if float(strike[0]) + strategy_cost < (target_price * (1 + (CI / 2))):
                                # For Extracting Expiration Date
                                s = data[x]["optionStrategyList"][y]["primaryLeg"]["description"].find(SYMBOL) + len(SYMBOL) + 1
                                if float(strike[0]) == int(float(strike[0])):
                                    t = data[x]["optionStrategyList"][y]["primaryLeg"]["description"].find(" " + str(int(float(strike[0]))) + " Call")
                                else:
                                    t = data[x]["optionStrategyList"][y]["primaryLeg"]["description"].find(
                                        " " + str(int(float(strike[0]))) + " ")
                                try:
                                    if value_spread["Cost"] + value_spread["Buy Call"] > strategy_cost + data[x]["optionStrategyList"][y]["primaryLeg"]["strikePrice"]:
                                        if value_spread["Cost"] + value_spread["Buy Call"] > value_spread_2["Cost"] + value_spread_2["Buy Call"]:
                                            value_spread_2 = value_spread
                                        value_spread = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Safe1"
                                        }
                                    elif value_spread["Cost"] + value_spread_2["Buy Call"] > strategy_cost + data[x]["optionStrategyList"][y]["primaryLeg"]["strikePrice"]:
                                        value_spread_2 = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Safe2"
                                        }
                                    if float(strike[1]) - float(strike[0]) - strategy_cost > max_profit_spread["Max Profit"]:
                                        if max_profit_spread["Max Profit"] > max_profit_spread_2["Max Profit"]:
                                            max_profit_spread_2 = max_profit_spread
                                        max_profit_spread = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Profit1"
                                        }
                                    elif float(strike[1]) - float(strike[0]) - strategy_cost > max_profit_spread_2["Max Profit"]:
                                        max_profit_spread_2 = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Profit2"
                                        }
                                except ZeroDivisionError:
                                    pass
        else:
            if data[x]["daysToExp"] < 365:
                for y in range(0, len(data[x]["optionStrategyList"])):
                    strike = str(data[x]["optionStrategyList"][y]["strategyStrike"])
                    strike = strike.split("/")
                    if float(strike[1]) > TARGET_PRICE * (1 + (CI / 2)):
                        if float(strike[0]) >= (target_price * (1 - CI)) and float(strike[1]) <= (
                                upper_limit * (1 + CI)):
                            strategy_cost = float(data[x]["optionStrategyList"][y]["strategyAsk"])
                            if float(strike[0]) + strategy_cost < (target_price * (1 + (CI / 2))):
                                # For Extracting Expiration Date
                                s = data[x]["optionStrategyList"][y]["primaryLeg"]["description"].find(SYMBOL) + len(
                                    SYMBOL) + 1
                                if float(strike[0]) == int(float(strike[0])):
                                    t = data[x]["optionStrategyList"][y]["primaryLeg"]["description"].find(
                                        " " + str(int(float(strike[0]))) + " Call")
                                else:
                                    t = data[x]["optionStrategyList"][y]["primaryLeg"]["description"].find(
                                        " " + str(int(float(strike[0]))) + " ")
                                try:
                                    if value_spread["Cost"] + value_spread["Buy Call"] > strategy_cost + \
                                            data[x]["optionStrategyList"][y]["primaryLeg"]["strikePrice"]:
                                        if value_spread["Cost"] + value_spread["Buy Call"] > value_spread_2["Cost"] + \
                                                value_spread_2["Buy Call"]:
                                            value_spread_2 = value_spread
                                        value_spread = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][
                                                       s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Safe1"
                                        }
                                    elif value_spread["Cost"] + value_spread_2["Buy Call"] > strategy_cost + \
                                            data[x]["optionStrategyList"][y]["primaryLeg"]["strikePrice"]:
                                        value_spread_2 = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][
                                                       s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Safe2"
                                        }
                                    if float(strike[1]) - float(strike[0]) - strategy_cost > max_profit_spread[
                                        "Max Profit"]:
                                        if max_profit_spread["Max Profit"] > max_profit_spread_2["Max Profit"]:
                                            max_profit_spread_2 = max_profit_spread
                                        max_profit_spread = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][
                                                       s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Profit1"
                                        }
                                    elif float(strike[1]) - float(strike[0]) - strategy_cost > max_profit_spread_2[
                                        "Max Profit"]:
                                        max_profit_spread_2 = {
                                            "Buy Call": float(strike[0]),
                                            "Sell Call": float(strike[1]),
                                            "Cost": strategy_cost,
                                            "Break Even": float(strike[0]) + strategy_cost,
                                            "Max Profit": round(float(strike[1]) - strategy_cost - float(strike[0]), 2),
                                            "Expires": data[x]["optionStrategyList"][y]["primaryLeg"]["description"][
                                                       s:t],
                                            "ROI": round((float(strike[1]) - float(strike[0])) / strategy_cost, 1),
                                            "Strategy": "Profit2"
                                        }
                                except ZeroDivisionError:
                                    pass

    return value_spread,value_spread_2,max_profit_spread,max_profit_spread_2


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


DATA_INITIAL = get_jsonparsed_data(
    "https://api.tdameritrade.com/v1/marketdata/chains?apikey=" + APIKEY + "&symbol=" + SYMBOL + "&contractType=CALL&strikeCount=128&strategy=VERTICAL"
                                                                                                 "&interval=" + str(INTERVAL))
DATA_INITIAL = DATA_INITIAL["monthlyStrategyList"]

golden_strat = {
    "ROI": 0
}

CHAIN_INITIAL = sort_chain(DATA_INITIAL, TARGET_PRICE, UPPER_LIMIT)

value_strat = CHAIN_INITIAL[0], CHAIN_INITIAL[1]


for strat in range(2,3):
    if golden_strat["ROI"] < CHAIN_INITIAL[strat]["Max Profit"]/CHAIN_INITIAL[strat]["Cost"]:
        golden_strat = CHAIN_INITIAL[strat]
        golden_strat["ROI"] = round(INTERVAL/CHAIN_INITIAL[strat]["Cost"], 1)

if TARGET_PRICE < 50:
    WIDE_INTERVAL = INTERVAL + 5
    WIDE_TARGET_PRICE = TARGET_PRICE - 2.5
    WIDE_UPPER_LIMIT = UPPER_LIMIT + 2.5
else:
    WIDE_INTERVAL = INTERVAL * 1.05
    WIDE_INTERVAL = round(WIDE_INTERVAL/2.5) * 2.5
    WIDE_TARGET_PRICE = TARGET_PRICE * 0.975
    WIDE_TARGET_PRICE = round(WIDE_TARGET_PRICE/2.5) * 2.5
    WIDE_UPPER_LIMIT = UPPER_LIMIT * 1.025
    WIDE_UPPER_LIMIT = round(WIDE_UPPER_LIMIT/2.5) * 2.5

DATA_WIDER = get_jsonparsed_data(
    "https://api.tdameritrade.com/v1/marketdata/chains?apikey=" + APIKEY + "&symbol=" + SYMBOL + "&contractType=CALL&strikeCount=128&strategy=VERTICAL"
                                                                                                 "&interval=" + str(WIDE_INTERVAL))
DATA_WIDER = DATA_WIDER["monthlyStrategyList"]
wide = sort_chain(DATA_WIDER, WIDE_TARGET_PRICE, WIDE_UPPER_LIMIT)
for spread in wide:
    try:
        if spread["Max Profit"]/spread["Cost"] > golden_strat["ROI"]:
            golden_strat = spread
            golden_strat["ROI"] = round(WIDE_INTERVAL/spread["Cost"], 1)
    except KeyError:
        pass

print("Best ROI\n" + str(golden_strat))
print("Safest\n" + str(value_strat[0]) + "\n" + str(value_strat[1]))

