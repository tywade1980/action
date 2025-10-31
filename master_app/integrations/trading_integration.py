"""
Trading Floor Integration
Wraps the trading floor system for use in the master application
"""

import sys
from pathlib import Path

# Add trading floor to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "3_trading_floor"))

from traders import Trader
from accounts import Account
from trading_floor import names, lastnames, model_names


class TradingIntegration:
    """
    Integration wrapper for the Trading Floor system
    """
    
    def __init__(self):
        self.traders = {}
        self._initialize_traders()
    
    def _initialize_traders(self):
        """Initialize all traders"""
        for name, lastname, model_name in zip(names, lastnames, model_names):
            self.traders[name] = Trader(name, lastname, model_name)
    
    def get_trader(self, name: str) -> Trader:
        """Get a trader by name"""
        return self.traders.get(name)
    
    def get_account(self, name: str) -> Account:
        """Get an account by trader name"""
        return Account.get(name)
    
    def get_all_traders(self) -> list:
        """Get list of all trader names"""
        return list(self.traders.keys())
    
    async def execute_trade(self, trader_name: str):
        """Execute a trading cycle for a specific trader"""
        trader = self.get_trader(trader_name)
        if not trader:
            raise ValueError(f"Trader {trader_name} not found")
        
        await trader.run()
        return {"trader": trader_name, "status": "completed"}
    
    def get_portfolio_summary(self, trader_name: str) -> dict:
        """Get portfolio summary for a trader"""
        account = self.get_account(trader_name)
        if not account:
            return None
        
        portfolio_value = account.calculate_portfolio_value()
        pnl = account.calculate_profit_loss(portfolio_value)
        
        return {
            "name": account.name,
            "balance": account.balance,
            "holdings": account.holdings,
            "portfolio_value": portfolio_value,
            "profit_loss": pnl,
            "strategy": account.strategy,
            "transaction_count": len(account.transactions)
        }
    
    def get_all_portfolios(self) -> dict:
        """Get portfolio summaries for all traders"""
        portfolios = {}
        for name in self.get_all_traders():
            portfolios[name] = self.get_portfolio_summary(name)
        return portfolios
    
    def get_system_info(self) -> dict:
        """Get information about the trading system"""
        return {
            "name": "Trading Floor",
            "description": "Multi-trader AI portfolio management system",
            "capabilities": [
                "Autonomous trading decisions",
                "Portfolio management and tracking",
                "Real-time market data integration",
                "Strategy-based trading",
                "Performance analytics",
                "Knowledge graph for market intelligence"
            ],
            "traders": [
                {
                    "name": name,
                    "lastname": lastname,
                    "model": model,
                    "strategy": self.get_account(name).strategy if self.get_account(name) else "Not set"
                }
                for name, lastname, model in zip(names, lastnames, model_names)
            ],
            "features": [
                "SQLite database for persistence",
                "MCP servers for tool integration",
                "Gradio dashboard for monitoring",
                "Multi-model support (GPT, DeepSeek, Gemini, Grok)"
            ]
        }
