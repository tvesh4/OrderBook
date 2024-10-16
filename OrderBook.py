class Order:
    def __init__(self, quantity, price, order_type):
        self.quantity = quantity
        self.price = price
        self.order_type = order_type  # 'bid' or 'ask'

    def __repr__(self):
        return f"{self.order_type.capitalize()} Quantity: {self.quantity}, Price: ${self.price:.2f}"


class OrderBook:
    def __init__(self):
        self.bids = []  # List of bid orders
        self.asks = []  # List of ask orders

    def add_bid(self, order):
        self.bids.append(order)
        self.bids.sort(key=lambda x: x.price, reverse=True)  # Sort bids by price (highest first)

    def add_ask(self, order):
        self.asks.append(order)
        self.asks.sort(key=lambda x: x.price)  # Sort asks by price (lowest first)

    def execute_trades(self):
        while self.bids and self.asks:
            best_bid = self.bids[0]
            best_ask = self.asks[0]

            if best_bid.price >= best_ask.price:
                trade_quantity = min(best_bid.quantity, best_ask.quantity)
                trade_price = best_ask.price

                print(f"Trade executed: Buy {trade_quantity} shares at ${trade_price:.2f}")

                # Update quantities
                best_bid.quantity -= trade_quantity
                best_ask.quantity -= trade_quantity

                # Remove orders if fully filled
                if best_bid.quantity == 0:
                    self.bids.pop(0)
                if best_ask.quantity == 0:
                    self.asks.pop(0)
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


def main():
    order_book = OrderBook()

    # Initial order from Participant A
    initial_ask_price = float(input("Enter the ask price for Participant A's offer: $"))
    initial_ask_quantity = int(input("Enter the ask quantity for Participant A's offer: "))
    order_book.add_ask(Order(initial_ask_quantity, initial_ask_price, 'ask'))

    # Initial bid (no trade)
    initial_bid_price = float(input("Enter the initial bid price: $"))
    initial_bid_quantity = int(input("Enter the initial bid quantity: "))
    order_book.add_bid(Order(initial_bid_quantity, initial_bid_price, 'bid'))

    # Display initial state
    order_book.display_order_book()

    while True:
        add_order = input("\nDo you want to add another ask? (yes/no): ").strip().lower()
        if add_order == 'yes':
            ask_price = float(input("Enter the ask price: $"))
            ask_quantity = int(input("Enter the ask quantity: "))
            order_book.add_ask(Order(ask_quantity, ask_price, 'ask'))
        
        # Execute trades based on the current order book
        order_book.execute_trades()

        # Display final state of the order book
        order_book.display_order_book()

        continue_trading = input("\nDo you want to continue trading? (yes/no): ").strip().lower()
        if continue_trading != 'yes':
            break


if __name__ == "__main__":
    main()