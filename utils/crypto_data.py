import requests
import pandas as pd
from datetime import datetime, timedelta


def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}
    try:
        response = requests.get(url)
        data = response.json()
        return data["bitcoin"]
    except Exception as e:
        return {"error": str(e)}


def get_ethereum_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "ethereum", "vs_currencies": "usd", "include_24hr_change": "true"}
    try:
        response = requests.get(url)
        data = response.json()
        return data["ethereum"]
    except Exception as e:
        return {"error": str(e)}


def get_fear_greed_index():
    url = "https://api.alternative.me/fng/"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            "value": int(data["data"][0]["value"]),
            "classification": data["data"][0]["value_classification"],
            "timestamp": data["data"][0]["timestamp"]
        }
    except Exception as e:
        return {"error": str(e)}


def get_cmc_hot_tokens(limit=10):
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"
    params = {
        "start": "1",
        "limit": str(limit),
        "sortBy": "market_cap",
        "sortType": "desc",
        "convert": "USD"
    }
    try:
        response = requests.get(url, headers={"Accept": "application/json"})
        data = response.json()
        tokens = []
        for item in data.get("data", {}).get("cryptoCurrencyList", []):
            tokens.append({
                "name": item.get("name"),
                "symbol": item.get("symbol"),
                "price": item.get("quotes", [{}])[0].get("price"),
                "change_24h": item.get("quotes", [{}])[0].get("percentChange24h"),
                "market_cap": item.get("quotes", [{}])[0].get("marketCap")
            })
        return tokens
    except Exception as e:
        return {"error": str(e)}


def get_vix_data():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "^VIX",
        "apikey": "demo",
        "outputsize": "compact"
    }
    try:
        response = requests.get(url)
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})
        df = pd.DataFrame.from_dict(time_series, orient="index").astype(float)
        df = df.sort_index()
        df = df[["4. close"]].tail(30)
        df.columns = ["VIX"]
        return df
    except Exception as e:
        return {"error": str(e)}


def get_bitcoin_etf_flows():
    etfs = [
        {"name": "IBIT", "full_name": "BlackRock iShares Bitcoin Trust"},
        {"name": "FBTC", "full_name": "Fidelity Bitcoin ETF"},
        {"name": "GBTC", "full_name": "Grayscale Bitcoin Trust"},
        {"name": "ARKK", "full_name": "ARK 21Shares Bitcoin ETF"},
        {"name": "BITO", "full_name": "ProShares Bitcoin Strategy ETF"}
    ]
    return etfs


def get_contract_open_interest():
    oi_data = [
        {"exchange": "Binance", "btc_oi": 6.8, "eth_oi": 3.2},
        {"exchange": "OKX", "btc_oi": 4.2, "eth_oi": 2.1},
        {"exchange": "Bybit", "btc_oi": 3.5, "eth_oi": 1.8},
        {"exchange": "Deribit", "btc_oi": 2.1, "eth_oi": 0.9}
    ]
    return oi_data


def get_crypto_correlation_data():
    correlations = [
        {"asset": "Gold", "correlation": 0.67},
        {"asset": "S&P 500", "correlation": 0.52},
        {"asset": "Nasdaq", "correlation": 0.58},
        {"asset": "Oil", "correlation": 0.34},
        {"asset": "EUR/USD", "correlation": -0.21}
    ]
    return correlations


def get_narratives():
    narratives = [
        {"topic": "Bitcoin ETF", "trend": "up", "description": "Institutional adoption continues"},
        {"topic": "DeFi 2.0", "trend": "up", "description": "New protocols gaining traction"},
        {"topic": "RWA Tokenization", "trend": "up", "description": "Real-world assets on-chain"},
        {"topic": "AI + Crypto", "trend": "up", "description": "AI agents in DeFi"},
        {"topic": "Layer 2 Scaling", "trend": "stable", "description": "Optimistic rollups mature"}
    ]
    return narratives