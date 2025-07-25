import re

def convert_pine_to_python(pine_script: str) -> str:
    """Convert Pine Script to Python trading strategy"""
    
    # Extract strategy name
    strategy_name_match = re.search(r'strategy\("([^"]+)"', pine_script)
    strategy_name = strategy_name_match.group(1) if strategy_name_match else "Trading Strategy"
    
    # Extract inputs
    inputs = {}
    input_matches = re.findall(r'(\w+)\s*=\s*input\.int\((\d+),\s*title="([^"]+)"\)', pine_script)
    for var_name, default_val, title in input_matches:
        inputs[var_name] = {'default': int(default_val), 'title': title}
    
    # Generate Python code
    python_code = f'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

class {strategy_name.replace(" ", "").replace("+", "")}:
    def __init__(self, data: pd.DataFrame):
        """
        {strategy_name}
        
        Parameters:
        data (pd.DataFrame): OHLCV data with columns ['open', 'high', 'low', 'close', 'volume']
        """
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        
    def calculate_indicators(self'''
    
    # Add input parameters to function signature
    param_list = []
    for var_name, info in inputs.items():
        param_list.append(f"{var_name}: int = {info['default']}")
    
    if param_list:
        python_code += ", " + ", ".join(param_list)
    
    python_code += '''):
        """Calculate technical indicators"""
        '''
    
    # Add indicator calculations
    if 'ta.ema' in pine_script:
        python_code += '''
        # EMA calculation
        self.data['ema'] = self.data['close'].ewm(span=emaLength).mean()'''
    
    if 'ta.sma' in pine_script:
        python_code += '''
        # SMA calculation  
        self.data['sma'] = self.data['close'].rolling(window=smaLength).mean()'''
        
    if 'ta.rsi' in pine_script:
        python_code += '''
        # RSI calculation
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsiLength).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsiLength).mean()
        rs = gain / loss
        self.data['rsi'] = 100 - (100 / (1 + rs))'''
    
    if 'ta.macd' in pine_script:
        python_code += '''
        # MACD calculation
        ema12 = self.data['close'].ewm(span=12).mean()
        ema26 = self.data['close'].ewm(span=26).mean()
        self.data['macd'] = ema12 - ema26
        self.data['macd_signal'] = self.data['macd'].ewm(span=9).mean()
        self.data['macd_histogram'] = self.data['macd'] - self.data['macd_signal']'''
    
    python_code += '''
        
    def generate_signals(self):
        """Generate buy/sell signals based on strategy logic"""'''
    
    # Buy/Sell logic (example)
    if 'crossover(rsi, 30)' in pine_script and 'close > ema' in pine_script:
        python_code += '''
        # Buy condition: RSI crosses above 30 AND close > EMA
        rsi_crossover = (self.data['rsi'] > 30) & (self.data['rsi'].shift(1) <= 30)
        buy_condition = rsi_crossover & (self.data['close'] > self.data['ema'])'''
    
    if 'crossunder(rsi, 70)' in pine_script and 'close < ema' in pine_script:
        python_code += '''
        # Sell condition: RSI crosses below 70 AND close < EMA  
        rsi_crossunder = (self.data['rsi'] < 70) & (self.data['rsi'].shift(1) >= 70)
        sell_condition = rsi_crossunder & (self.data['close'] < self.data['ema'])'''
    
    python_code += '''
        
        self.signals['buy'] = buy_condition
        self.signals['sell'] = sell_condition
        
        return self.signals
    
    def backtest(self, initial_capital: float = 10000) -> dict:
        """Simple backtest implementation"""
        capital = initial_capital
        position = 0
        trades = []
        
        for i, (date, row) in enumerate(self.signals.iterrows()):
            current_price = self.data.loc[date, 'close']
            
            if row['buy'] and position == 0:
                position = capital / current_price
                capital = 0
                trades.append({
                    'date': date, 'action': 'BUY', 'price': current_price, 'shares': position
                })
                
            elif row['sell'] and position > 0:
                capital = position * current_price
                trades.append({
                    'date': date, 'action': 'SELL', 'price': current_price, 'shares': position
                })
                position = 0
        
        if position > 0:
            final_price = self.data['close'].iloc[-1]
            capital = position * final_price
            
        return {
            'final_value': capital,
            'total_return': (capital - initial_capital) / initial_capital * 100,
            'total_trades': len(trades),
            'trades': trades
        }
'''
    
    return python_code
