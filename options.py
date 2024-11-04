from bs4 import BeautifulSoup
import requests
import time


def fetch_prices():
    try:
        html_text = requests.get("https://groww.in/options/nifty").text
        soup = BeautifulSoup(html_text, "lxml")

        chain = soup.find(
            "div",
            class_="SpotPrice_spotPriceText__6G_Na pos-abs center-align absolute-center contentInversePrimary bodySmallHeavy",
        ).span.text

        print("Current Index Price:", chain)

        strike_price = soup.find_all("span", class_="opr84AbsoluteCentre")

        last_call = None

        for strike in strike_price:
            strike_text = strike.text.replace(",", "").split(".")[0]

            if float(strike_text) < float(chain.replace(",", "")):
                call_prices = soup.find(
                    "a", href=f"/options/nifty/NIFTY24N07{strike_text}CE"
                ).text
                last_call = call_prices.split()[-1]

        if last_call is not None:
            print("Last Call Price:", last_call)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    while True:
        fetch_prices()
        time_wait = 10
        print(f"Waiting for {time_wait} seconds...")
        print(" ")
        time.sleep(time_wait)
