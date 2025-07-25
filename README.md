# 🧠 Pine Script to Python Strategy Converter

Convert your TradingView Pine Script strategies into Python code with one click.  
Ideal for quants, traders, and developers who want to backtest or build bots in Python.

## 🚀 Live App

🔗 [Try the app on Streamlit Cloud](https://your-streamlit-url.streamlit.app)

## 📌 Features

✅ Paste your Pine Script  
✅ Instantly converts to Python class format  
✅ Download ready-to-run Python code  
✅ Built-in RSI + EMA sample strategy

## 🧪 Sample Pine Script

```pinescript
//@version=5
strategy("RSI + EMA Strategy", overlay=true)
emaLength = input.int(50)
rsiLength = input.int(14)
ema = ta.ema(close, emaLength)
rsi = ta.rsi(close, rsiLength)
buy = crossover(rsi, 30) and close > ema
sell = crossunder(rsi, 70) and close < ema
strategy.entry("Buy", strategy.long, when=buy)
strategy.close("Buy", when=sell)
```

## 🛠 How It Works
Uses Streamlit for UI

Python code is generated with structured Strategy class

Output follows best practices for backtesting in pandas

## 📁 Repo Structure
pine-to-python/
├── app.py              # Streamlit UI
├── pine_to_python.py   # Converter logic
├── requirements.txt
└── README.md

## 🧠 About the Author
I'm a data analyst / quant freelancer with experience in:

Trading strategy development

Python, Pine Script, Streamlit

Financial data backtesting

Quantitative research

👨‍💻 Connect on Upwork(https://www.upwork.com/freelancers/~017089a43e1d63a351?mp_source=share)

