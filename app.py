import streamlit as st
from converter import convert_pine_to_python

def main():
    st.set_page_config(page_title="Pine Script → Python Converter", layout="wide")
    
    st.title("📈 Pine Script → Python Converter")
    st.markdown("Convert TradingView Pine Script strategies into Python strategy classes with backtesting logic.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Pine Script Input")
        default_code = """//@version=5
strategy("RSI + EMA Strategy", overlay=true)
emaLength = input.int(50, title="EMA Length")
rsiLength = input.int(14, title="RSI Length")
ema = ta.ema(close, emaLength)
rsi = ta.rsi(close, rsiLength)
buy = crossover(rsi, 30) and close > ema
sell = crossunder(rsi, 70) and close < ema
plot(ema, color=color.orange, title="EMA")
strategy.entry("Buy", strategy.long, when=buy)
strategy.close("Buy", when=sell)"""
        
        pine_code = st.text_area("Paste your Pine Script code below:", value=default_code, height=350)
        convert = st.button("🚀 Convert to Python")
    
    with col2:
        st.subheader("🐍 Python Output")
        
        if convert and pine_code.strip():
            with st.spinner("Converting..."):
                python_code = convert_pine_to_python(pine_code)
                st.code(python_code, language='python')
                st.download_button("📥 Download Python File", python_code, "strategy.py", "text/plain")

if __name__ == "__main__":
    main()
