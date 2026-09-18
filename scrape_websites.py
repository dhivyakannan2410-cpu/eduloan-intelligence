import requests
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re

class EducationLoanScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.results = {}
        
    def clean_rate(self, text):
        if not text:
            return None
        matches = re.findall(r'(\d+\.?\d*)', text)
        if matches:
            return float(matches[0])
        return None
    
    def scrape_axis_bank(self):
        print('📊 Scraping Axis Bank...')
        try:
            url = 'https://www.axisbank.com/education-loan'
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rate_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'\d+\.?\d*\s*%'))
            rates = []
            for elem in rate_elements[:5]:
                text = elem.get_text().strip()
                rate = self.clean_rate(text)
                if rate and 1 <= rate <= 20:
                    rates.append(rate)
            if rates:
                avg_rate = round(sum(rates) / len(rates), 2)
                return {
                    'bank': 'Axis Bank',
                    'interest_rate': avg_rate,
                    'rates_found': rates,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'Axis Bank Website'
                }
            else:
                return {
                    'bank': 'Axis Bank',
                    'interest_rate': 8.50,
                    'rates_found': [8.50],
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'Axis Bank (Default)'
                }
        except Exception as e:
            print(f'⚠️ Axis Bank scrape warning: {e}')
            return {
                'bank': 'Axis Bank',
                'interest_rate': 8.50,
                'rates_found': [8.50],
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Axis Bank (Default)'
            }
    
    def scrape_bob(self):
        print('📊 Scraping Bank of Baroda...')
        try:
            url = 'https://www.bankofbaroda.in/personal-banking/loans/education-loan'
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rate_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'\d+\.?\d*\s*%'))
            rates = []
            for elem in rate_elements[:5]:
                text = elem.get_text().strip()
                rate = self.clean_rate(text)
                if rate and 1 <= rate <= 20:
                    rates.append(rate)
            if rates:
                avg_rate = round(sum(rates) / len(rates), 2)
                return {
                    'bank': 'Bank of Baroda',
                    'interest_rate': avg_rate,
                    'rates_found': rates,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'BOB Website'
                }
            else:
                return {
                    'bank': 'Bank of Baroda',
                    'interest_rate': 6.85,
                    'rates_found': [6.85],
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'BOB (Default)'
                }
        except Exception as e:
            print(f'⚠️ BOB scrape warning: {e}')
            return {
                'bank': 'Bank of Baroda',
                'interest_rate': 6.85,
                'rates_found': [6.85],
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'BOB (Default)'
            }
    
    def scrape_hdfc(self):
        print('📊 Scraping HDFC Bank...')
        try:
            url = 'https://www.hdfc.com/education-loan'
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rate_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'\d+\.?\d*\s*%'))
            rates = []
            for elem in rate_elements[:5]:
                text = elem.get_text().strip()
                rate = self.clean_rate(text)
                if rate and 1 <= rate <= 20:
                    rates.append(rate)
            if rates:
                avg_rate = round(sum(rates) / len(rates), 2)
                return {
                    'bank': 'HDFC Bank',
                    'interest_rate': avg_rate,
                    'rates_found': rates,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'HDFC Website'
                }
            else:
                return {
                    'bank': 'HDFC Bank',
                    'interest_rate': 7.55,
                    'rates_found': [7.55],
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'HDFC (Default)'
                }
        except Exception as e:
            print(f'⚠️ HDFC scrape warning: {e}')
            return {
                'bank': 'HDFC Bank',
                'interest_rate': 7.55,
                'rates_found': [7.55],
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'HDFC (Default)'
            }
    
    def scrape_icici(self):
        print('📊 Scraping ICICI Bank...')
        try:
            url = 'https://www.icicibank.com/personal-banking/loans/education-loan'
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rate_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'\d+\.?\d*\s*%'))
            rates = []
            for elem in rate_elements[:5]:
                text = elem.get_text().strip()
                rate = self.clean_rate(text)
                if rate and 1 <= rate <= 20:
                    rates.append(rate)
            if rates:
                avg_rate = round(sum(rates) / len(rates), 2)
                return {
                    'bank': 'ICICI Bank',
                    'interest_rate': avg_rate,
                    'rates_found': rates,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'ICICI Website'
                }
            else:
                return {
                    'bank': 'ICICI Bank',
                    'interest_rate': 8.58,
                    'rates_found': [8.58],
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'ICICI (Default)'
                }
        except Exception as e:
            print(f'⚠️ ICICI scrape warning: {e}')
            return {
                'bank': 'ICICI Bank',
                'interest_rate': 8.58,
                'rates_found': [8.58],
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'ICICI (Default)'
            }
    
    def scrape_sbi(self):
        print('📊 Scraping SBI...')
        try:
            url = 'https://sbi.co.in/web/personal-banking/loans/education-loans'
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rate_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'\d+\.?\d*\s*%'))
            rates = []
            for elem in rate_elements[:5]:
                text = elem.get_text().strip()
                rate = self.clean_rate(text)
                if rate and 1 <= rate <= 20:
                    rates.append(rate)
            if rates:
                avg_rate = round(sum(rates) / len(rates), 2)
                return {
                    'bank': 'SBI',
                    'interest_rate': avg_rate,
                    'rates_found': rates,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'SBI Website'
                }
            else:
                return {
                    'bank': 'SBI',
                    'interest_rate': 8.00,
                    'rates_found': [8.00],
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'SBI (Default)'
                }
        except Exception as e:
            print(f'⚠️ SBI scrape warning: {e}')
            return {
                'bank': 'SBI',
                'interest_rate': 8.00,
                'rates_found': [8.00],
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'SBI (Default)'
            }
    
    def scrape_all(self):
        print('\n' + '='*60)
        print('🕷️  STARTING WEB SCRAPER')
        print('='*60)
        print(f'🕐 Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        
        banks = [
            ('axis', self.scrape_axis_bank),
            ('bob', self.scrape_bob),
            ('hdfc', self.scrape_hdfc),
            ('icici', self.scrape_icici),
            ('sbi', self.scrape_sbi)
        ]
        
        for name, scraper in banks:
            data = scraper()
            self.results[name] = data
            print(f'   ✅ {name.upper()} rate: {data.get("interest_rate", "N/A")}%')
            time.sleep(2)
        
        print('\n💾 Saving data...')
        for name, data in self.results.items():
            filename = f'{name}_education_rates.json'
            try:
                with open(filename, 'r') as f:
                    existing = json.load(f)
                    if isinstance(existing, list):
                        data['scraped_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        existing.append(data)
                        with open(filename, 'w') as f:
                            json.dump(existing, f, indent=2)
                    else:
                        existing.update(data)
                        with open(filename, 'w') as f:
                            json.dump(existing, f, indent=2)
            except FileNotFoundError:
                data['scraped_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
            print(f'   ✅ Saved {filename}')
        
        print('\n' + '='*60)
        print('✅ SCRAPING COMPLETE!')
        print('='*60)
        print(f'🕐 Completed at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('\n📊 Summary:')
        for name, data in self.results.items():
            print(f'   • {name.upper()}: {data.get("interest_rate", "N/A")}%')
        print('='*60)
        return self.results

def main():
    scraper = EducationLoanScraper()
    results = scraper.scrape_all()
    return results

if __name__ == '__main__':
    main()
