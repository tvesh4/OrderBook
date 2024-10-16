import requests

class Order:
    def __init__(self, quantity, price, order_type):
        self.quantity = quantity
        self.price = price
        self.order_type = order_type 

    def __repr__(self):
        return f"{self.order_type.capitalize()} Quantity: {self.quantity}, Price: ${self.price:.2f}"

class OrderBook:
    def __init__(self):
        self.bids = []  # List of buy orders
        self.asks = []  # List of sell orders

    def add_order(self, order):
        if order.order_type == 'buy':
            self.bids.append(order)
            self.bids.sort(key=lambda x: x.price, reverse=True)  # Sort bids by price (highest first)
        else:
            self.asks.append(order)
            self.asks.sort(key=lambda x: x.price)  # Sort asks by price (lowest first)

    def execute_trades(self, wallet):
        while self.bids and self.asks:
            best_bid = self.bids[0]
            best_ask = self.asks[0]

            if best_bid.price >= best_ask.price:
                trade_quantity = min(best_bid.quantity, best_ask.quantity)
                trade_price = best_ask.price

                # Calculate profit or loss
                if best_bid.order_type == 'buy':
                    wallet['balance'] -= trade_price * trade_quantity
                else:
                    wallet['balance'] += trade_price * trade_quantity
                    
                print(f"Trade executed: Buy {trade_quantity} shares at ${trade_price:.2f}")

                # Update quantities
                best_bid.quantity -= trade_quantity
                best_ask.quantity -= trade_quantity

                # Remove orders if fully filled
                if best_bid.quantity == 0:
                    self.bids.pop(0)
                if best_ask.quantity == 0:
                    self.asks.pop(0)

                print(f"Updated Wallet Balance: ${wallet['balance']:.2f}")
            else:
                break  # No more trades can happen

    def display_order_book(self):
        print("\nOrder Book:")
        print("Bids:")
        for bid in self.bids:
            print(bid)
        
        print("Asks:")
        for ask in self.asks:
            print(ask)

def fetch_stock_price(symbol):
    api_key = '6Z63NAZRH5WRSMUQ'  
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    try:
        latest_time = list(data['Time Series (1min)'].keys())[0]
        latest_price = float(data['Time Series (1min)'][latest_time]['1. open'])
        return latest_price
    except KeyError:
        print("Error fetching data. Please check the symbol and try again.")
        return None

def main():
    order_book = OrderBook()
    wallet = {'balance': 0.0} # Initialize wallet 
    symbol = input("Enter the stock symbol (e.g., NVDA for NVIDIA): ").strip().upper()
    stock_price = fetch_stock_price(symbol)

    if stock_price is None:
        return
    
    print(f"Current {symbol} Price: ${stock_price:.2f}")

    while True:
        action = input("Do you want to place a buy or sell order? (type 'buy' or 'sell', or 'exit' to quit): ").strip().lower()
        
        if action == 'exit':
            break
        
        quantity = int(input("Enter the quantity: "))
        
        if action == 'buy':
            total_cost = stock_price * quantity
            if total_cost > wallet['balance']:
                print("Insufficient funds to complete this buy order.")
                continue
            
            order_book.add_order(Order(quantity, stock_price, 'buy'))
        
        elif action == 'sell':
            order_book.add_order(Order(quantity, stock_price, 'sell'))
        
        order_book.execute_trades(wallet)  # Execute any trades after adding the order
        order_book.display_order_book()  # Show the current state of the order book

if __name__ == "__main__":
    main()
