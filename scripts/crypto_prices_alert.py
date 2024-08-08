import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def data_parsing(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    
        table = soup.find('table', class_='sc-7b3ac367-3 etbcea cmc-table')
    
        if table:
            headers = [header.text.strip() for header in table.find_all('th')]
            rows = table.find_all('tr')
    
            table_data = []
            for row in rows:
                cells = row.find_all('td')
                cell_data = [cell.text.strip() for cell in cells]
                if cell_data: 
                    table_data.append(cell_data)
            df = pd.DataFrame(table_data, columns=headers)
    return df

def dataset_processing(df):
    df = df[['Name','Price','24h %']]
    df['Name'] = df['Name'].str[-3:]
    df = df[df['Name'].isin(['BTC','ETH','BNB','XRP','TON'])]
    
    message = '<b>⚡ [CRYPTO] Prices Alert</b>\n\n'
    for index, row in df.iterrows():
        message += f"<b>{row['Name']}</b> - <code>{row['Price']}</code> (<b>{row['24h %']}</b>)\n"
    return message

def send_telegram(message, bot_token, chat_id, url_mess):
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
    response = requests.post(url_mess, data=data)

def main():
    bot_token = 'token'
    chat_id = 'chat_id'
    url_mess = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    url = 'https://coinmarketcap.com/'
    
    df = data_parsing(url)
    message = dataset_processing(df)
    send_telegram(message, bot_token, chat_id, url_mess)
    
if __name__ == "__main__":
    main()
