from . import url_requests
from . import general


def ExtractChart(result: dict) -> dict:

    data = {
        "price": {},
        "dividend": {},
        "stocksplit": {}
    }

    if not "chart" in result:
        return data

    if not "result" in result["chart"]:
        return data

    if result["chart"]["result"] == None:
        return data

    if not len(result["chart"]["result"]) > 0:
        return data

    # price
    result = result["chart"]["result"][0]
    if "timestamp" in result:
        stamps = result["timestamp"]
    else:
        stamps = []
    for i in range(len(stamps)):
        stamp = int(stamps[i])
        data["price"][stamp] = {}
        data["price"][stamp]["open"] = result["indicators"]["quote"][0]["open"][i]
        data["price"][stamp]["high"] = result["indicators"]["quote"][0]["high"][i]
        data["price"][stamp]["low"] = result["indicators"]["quote"][0]["low"][i]
        data["price"][stamp]["close"] = result["indicators"]["quote"][0]["close"][i]
        if "adjclose" in result["indicators"]:
            data["price"][stamp]["adjclose"] = result["indicators"]["adjclose"][0]["adjclose"][i]
        data["price"][stamp]["volume"] = result["indicators"]["quote"][0]["volume"][i]

    # dividend
    if "events" in result and "dividends" in result["events"]:
        for stamp in result["events"]["dividends"]:
            data["dividend"][int(stamp)] = {
                "dividend": result["events"]["dividends"][stamp]["amount"]}

    # stocksplit
    if "events" in result and "splits" in result["events"]:
        for stamp in result["events"]["splits"]:
            data["stocksplit"][int(stamp)] = {
                "stocksplit": result["events"]["splits"][stamp]["splitRatio"]}

    return data


def ExtractInfo1(result: dict) -> dict:

    data = {
        "longName": None,
        "shortName": None,
        "market": None,
        "currency": None,
        "financialCurrency": None,
        "marketCap": None,
        "sharesOutstanding": None
    }

    if not "quoteResponse" in result:
        return data

    if not "result" in result["quoteResponse"]:
        return data

    if not len(result["quoteResponse"]["result"]) > 0:
        return data

    if result["quoteResponse"]["result"] == None:
        return data

    result = result["quoteResponse"]["result"][0]

    for item in data:
        if item in result:
            data[item] = result[item]

    return data


def ExtractInfo2(result: dict) -> dict:

    data = {
        "sector": None,
        "industry": None,
        "website": None
    }

    if not "quoteSummary" in result:
        return data

    if not "result" in result["quoteSummary"]:
        return data

    if result["quoteSummary"]["result"] == None:
        return data

    if not len(result["quoteSummary"]["result"]) > 0:
        return data

    if not "assetProfile" in result["quoteSummary"]["result"][0]:
        return data

    result = result["quoteSummary"]["result"][0]["assetProfile"]

    data = {
        "sector": None,
        "industry": None,
        "website": None
    }

    for item in data:
        if item in result:
            data[item] = str(result[item]).replace(
                "—", "-").replace("â€”", "-")

    return data
