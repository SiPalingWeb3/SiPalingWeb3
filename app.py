import requests
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class BitcoinPrice:
    price: float
    timestamp: datetime
    currency: str = "USD"

class BitcoinFetcher:

    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3", output_dir: str = "output"):
        self.base_url = base_url
        self.endpoint = "/simple/price"
        self.session = requests.Session()
        self.output_dir = Path(output_dir)
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _build_url(self) -> str:
        return f"{self.base_url}{self.endpoint}"

    def _build_params(self) -> Dict[str, str]:
        return {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }

    def get_price(self) -> Optional[BitcoinPrice]:
        try:
            response = self.session.get(
                self._build_url(),
                params=self._build_params(),
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            price_value = data.get('bitcoin', {}).get('usd')
            if price_value is None:
                print("Error: 'bitcoin' or 'usd' key not found in API response.")
                return None
            return BitcoinPrice(
                price=price_value,
                timestamp=datetime.now()
            )
        except requests.exceptions.RequestException as e:
            print(f"Error fetching price: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def save_price(self, price_data: Optional[BitcoinPrice]) -> bool:
        output_file = self.output_dir / "bitcoin_price.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('')
            
            if price_data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"💰 Current Bitcoin Price: ${price_data.price:,.2f}\n")
                print(f"Price saved to {output_file}")
                return True
            else:
                print("No price data to save.")
                return False
        except IOError as e:
            print(f"Error saving price to file: {e}")
            return False

def main() -> Optional[BitcoinPrice]:

    fetcher = BitcoinFetcher()
    price = fetcher.get_price()
    fetcher.save_price(price)
    return price

if __name__ == '__main__':
    main()
