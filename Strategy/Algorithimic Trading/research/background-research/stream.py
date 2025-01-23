from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

from alpaca.data import CryptoDataStream

# keys are required for live data
crypto_stream = CryptoDataStream(api_key, secret_key)

async def quote_data_handler(data):
    # quote data will arrive here
    print(data)

crypto_stream.subscribe_quotes(quote_data_handler, "BTC/USD")
crypto_stream.run()