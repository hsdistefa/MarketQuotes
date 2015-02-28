import urllib.request
import json

# This URL returns all stock tickers in JSON format
TICKER_URL = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.industry%20where%20id%20in%20%28select%20industry.id%20from%20yahoo.finance.sectors%29&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'

OUTPUT_FILE = 'symbols.txt'

class TickerDownloader:
    def get_symbols(self):
        self.download_url()
        self.parse()

    def download_url(self, url=TICKER_URL):
        request = urllib.request.Request(TICKER_URL)
        response = urllib.request.urlopen(request)
        encoding = response.info().get_param('charset', 'utf8')
        # Load JSON
        self._json = json.loads(
            response.read().decode(encoding))['query']['results']['industry']

    def parse(self):
        with open(OUTPUT_FILE, 'w+') as outfile:
            # Parse symbols from JSON
            for i in range(len(self._json)):
                try:
                    num_companies = len(self._json[i]['company'])
                except:
                    print('format error')
                    continue
                for j in range(num_companies):
                    try:
                        outfile.write(
                            self._json[i]['company'][j]['symbol'] + '\n')
                    except:
                        print('format error')


if __name__ == '__main__':
    TickerDownloader().get_symbols()
