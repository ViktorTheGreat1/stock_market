import os
import csv
import yfinance as yf

# -------------------------------
# Setup save file (cross-platform)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where script runs
SAVE_FILE = os.path.join(BASE_DIR, "game_progress.csv")

total = 1000   # starting money
stocks = {}    # owned stocks
lookups = []   # list of company lookups

# -------------------------------
# Save / Load Functions
# -------------------------------
def create_save_file():
    """Create a new save file with headers if it doesn't exist"""
    with open(SAVE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TotalDollars", "Stocks", "Lookups"])
        writer.writerow([total, stocks, lookups])
    print("Created new save file ✅")

def load_progress():
    """Load progress from file into memory"""
    global total, stocks, lookups
    if not os.path.exists(SAVE_FILE):
        create_save_file()
    else:
        with open(SAVE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            row = next(reader)  # only one row of data
            total = float(row["TotalDollars"])
            stocks = eval(row["Stocks"]) if row["Stocks"] else {}
            lookups = eval(row["Lookups"]) if row["Lookups"] else []
        print("Loaded save file ✅")

def save_progress():
    """Save current progress to file"""
    with open(SAVE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TotalDollars", "Stocks", "Lookups"])
        writer.writerow([total, stocks, lookups])
    print("Progress saved ✅")

# -------------------------------
# Game Functions
# -------------------------------
def symbol_lookup():
    company_input = input("What company's symbol do you want? ").lower().strip()
    lookups.append(company_input)
    stock = yf.Ticker(company_input.upper())
    try:
        info = stock.info
        symbol = info.get("symbol", company_input.upper())
        print(f"Found symbol: {symbol}")
    except Exception:
        print("Could not find symbol.")

def stock_check():
    symbol = input("Enter stock symbol: ").upper()
    stock = yf.Ticker(symbol)

    timeperiod = input("Period? days/months/years ").lower()
    many = input(f"How many {timeperiod}? ")

    if timeperiod == "days":
        per = "d"
    elif timeperiod == "months":
        per = "mo"
    elif timeperiod == "years":
        per = "y"
    else:
        print("Not valid.")
        return

    hist = stock.history(period=f"{many}{per}", interval="1d")
    if hist.empty:
        print("No data.")
        return

    print(hist['Close'])
    hist['Change'] = hist['Close'].diff()
    print("\nDaily changes:")
    print(hist['Change'].fillna(0))

def buysell_stock():
    global total
    do = input("Will you buy or sell stock? ").lower()
    stock = input("Which symbol? ").upper()
    amount = int(input("How many shares? "))

    ticker = yf.Ticker(stock)
    try:
        price = ticker.fast_info["last_price"]
    except Exception:
        print("Could not fetch price.")
        return

    if do == "buy":
        cost = price * amount
        if total >= cost:
            total -= cost
            stocks[stock] = stocks.get(stock, 0) + amount
            print(f"Bought {amount} {stock} at {price}, total left: {total}")
        else:
            print("Not enough money.")
    elif do == "sell":
        if stock in stocks and stocks[stock] >= amount:
            total += price * amount
            stocks[stock] -= amount
            if stocks[stock] == 0:
                stocks.pop(stock)
            print(f"Sold {amount} {stock} at {price}, total: {total}")
        else:
            print("You don’t own enough shares.")

# -------------------------------
# Main Loop
# -------------------------------
def main():
    load_progress()

    wanna = "0"
    while wanna != "5":
        print(f"\nWhat do you want to do?        Total: {total}")
        wanna = input("1. Look up company symbol\n2. Check stocks\n3. View lookups/shares\n4. Buy/Sell stock\n5. Quit\n ").strip()

        if wanna == "1":
            symbol_lookup()
        elif wanna == "2":
            stock_check()
        elif wanna == "3":
            print("Lookups:", lookups)
            print("Stocks:", stocks)
        elif wanna == "4":
            buysell_stock()
        elif wanna == "5":
            save_progress()
            print("Goodbye 👋")
            break
        else:
            print("Not valid.")

if __name__ == "__main__":
    main()
