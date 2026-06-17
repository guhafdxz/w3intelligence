import os
from typing import Dict, Optional
from openai import OpenAI

try:
    import streamlit as st
    ZZZ_API_KEY = st.secrets.get("ZZZ_API_KEY") or os.getenv("ZZZ_API_KEY")
except:
    ZZZ_API_KEY = os.getenv("ZZZ_API_KEY")

client = OpenAI(
    api_key=ZZZ_API_KEY,
    base_url="https://api.zhizengzeng.com/v1"
)


def get_real_time_data_summary():
    try:
        from .crypto_data import get_bitcoin_price, get_ethereum_price, get_fear_greed_index, get_cmc_hot_tokens
        from .tradfi_data import get_rwa_stats, get_rwa_categories, get_top_rwa_assets
        
        data_parts = []
        
        fng = get_fear_greed_index()
        hot_tokens = get_cmc_hot_tokens(5)
        
        btc_price, btc_change = 0, 0
        eth_price, eth_change = 0, 0
        for token in hot_tokens:
            if token.get('symbol') == 'BTC':
                btc_price = token.get('price', 0)
                btc_change = token.get('change_24h', 0)
            elif token.get('symbol') == 'ETH':
                eth_price = token.get('price', 0)
                eth_change = token.get('change_24h', 0)
        
        crypto_part = f"""
**Cryptocurrency Data (2026):**

- Bitcoin: ${btc_price:,.0f} ({btc_change:.2f}%)
- Ethereum: ${eth_price:,.0f} ({eth_change:.2f}%)
- Fear & Greed Index: {fng.get('value', 0)} ({fng.get('classification', 'N/A')})

Top Tokens:
"""
        for token in hot_tokens[:5]:
            crypto_part += f"- {token.get('symbol', '')}: ${token.get('price', 0):,.2f} ({token.get('change_24h', 0):.2f}%)\n"
        data_parts.append(crypto_part)
        
        stats = get_rwa_stats()
        categories = get_rwa_categories()
        top_assets = get_top_rwa_assets(5)
        
        cats_summary = "\n".join([f"- {cat['name']}: ${cat['total_value']/1000:.2f}B" for cat in categories])
        assets_summary = "\n".join([f"- {a['symbol']}: {a['value_str']} ({a['change_24h']})" for a in top_assets])
        
        rwa_part = f"""
**RWA Market Data (2026):**

- Distributed Value: {stats.get('distributed_value', 'N/A')}
- Represented Value: {stats.get('represented_value', 'N/A')}
- Total Asset Holders: {stats.get('total_holders', 'N/A')}

Category Breakdown:
{cats_summary}

Top Assets:
{assets_summary}
"""
        data_parts.append(rwa_part)
        
        prediction_part = """
**Prediction Markets (2026):**

Active Topics:
- Bitcoin Price > $100K by Dec 2026 (Polymarket)
- Spot Ethereum ETF Approval (Polymarket)
- US Presidential Election (Polymarket)

Top Platforms: Polymarket, Metaculus, Manifold, PredictIt
"""
        data_parts.append(prediction_part)
        
        return "\n".join(data_parts)
    except Exception as e:
        return f"Data fetch error: {str(e)}"


def analyze_prediction_topic(material: str) -> Dict:
    knowledge_prompt = ""
    try:
        from .topic_data import get_knowledge_prompt, is_knowledge_loaded
        if is_knowledge_loaded():
            knowledge_prompt = get_knowledge_prompt()
    except:
        pass
    
    system_prompt = f"""
    You are a Web3 prediction market analyst AI. Your task is to analyze prediction materials and evaluate:
    
    1. Sensitivity level: How sensitive/controversial is this topic?
       - LOW: General market trends, publicly available information
       - MEDIUM: Somewhat sensitive, may involve specific companies or individuals
       - HIGH: Highly sensitive, involves illegal activities, privacy concerns, or highly controversial topics
    
    2. Prediction market eligibility: Whether this topic can be listed on prediction markets
       - YES: Suitable for prediction markets
       - NO: Not suitable due to legal, ethical, or practical reasons
    
    3. Risk assessment: Potential risks of listing this topic
    
    4. Suggestion: Recommendations for handling this topic
    
    {knowledge_prompt}
    
    Provide your analysis in JSON format with the following structure:
    {{
        "sensitivity_level": "LOW/MEDIUM/HIGH",
        "sensitivity_reason": "Explanation of sensitivity level",
        "market_eligibility": "YES/NO",
        "eligibility_reason": "Explanation of eligibility",
        "risk_assessment": "Risk description",
        "suggestion": "Handling recommendation"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze the following prediction material:\n\n{material}"}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}


def chat_with_agent(message: str, history: Optional[list] = None) -> str:
    real_time_data = get_real_time_data_summary()
    
    system_prompt = f"""
    You are a Web3 intelligence assistant. You specialize in:
    - Cryptocurrency market analysis
    - Traditional finance (TradFi) insights
    - RWA (Real World Assets) trends
    - Prediction markets
    - Blockchain technology
    
    Current Market Data (2026):
    {real_time_data}
    
    Use the current data above when answering questions. Provide insightful, accurate, and actionable responses.
    """

    messages = [{"role": "system", "content": system_prompt}]
    
    if history:
        for msg in history:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})
    
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"