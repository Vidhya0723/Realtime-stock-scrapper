import csv
import requests
from bs4 import BeautifulSoup
import yfinance as yf
class Stock:
    def __init__(self, company, price, change):
        self.company = company
        self.price = price
        self.change = change

def scrape_stock_data(ticker):
    stocks = []

    for t in ticker:


        ticker = yf.Ticker(t)
    
    # Get the live price
        live_price = ticker.history(period='1d')['Close'][-1]

        print("Live Price",live_price)
        url = f"https://finance.yahoo.com/quote/{t}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        with open(f"{t}_page.html", "w", encoding="utf-8") as html_file:
            html_file.write(str(soup))
        stock_info_div = soup.find('div', {'id': 'quote-header-info'})
        if stock_info_div:
            fin_streamer = stock_info_div.select_one("div:nth-of-type(3) div:nth-of-type(1) div fin-streamer:nth-of-type(1)").get_text()
            print("fin",fin_streamer)
        stock = Stock(
            company=soup.select_one("h1").get_text(),
            price=soup.select_one("[data-field='regularMarketPrice']").get_text(),
            change=soup.select_one("[data-field='regularMarketChangePercent']").get_text()
        )

        stocks.append(stock)

    return stocks

def save_to_csv(stocks, filename='stocks.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ["company", "price", "change"]
        writer.writerow(headers)

        for stock in stocks:
            row = [stock.company, stock.price, stock.change]
            writer.writerow(row)

if __name__ == "__main__":
    ticker = [
        "TATAMOTORS.NS",
    ]

    stocks = scrape_stock_data(ticker)
    print(stocks[0].price)
    # save_to_csv(stocks)
    print("Data scraped and saved to stocks.csv")