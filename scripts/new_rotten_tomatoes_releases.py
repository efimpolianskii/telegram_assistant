import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")

def data_parsing(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        blocks = soup.find_all('div', class_='flex-container')
        releases = []
        for i in blocks:
            title = i.find('span', class_='p--small').text.strip()
            date = i.find('span', class_='smaller').text.strip()
            audience_score = i.find('rt-text', {'slot': 'audienceScore'})
            audience_score_text = audience_score.text.strip() if audience_score else "N/A"
            critics_score = i.find('rt-text', {'slot': 'criticsScore'})
            critics_score_text = critics_score.text.strip() if critics_score else "N/A"
            releases.append({
                'title': title,
                'date':date,
                'audience_score':audience_score_text,
                'critics_score':critics_score_text})
    else:
        releases = None 
    return releases

def extract_date(text):
    return pd.to_datetime(text.replace('Streaming ', ''), format='%b %d, %Y').strftime('%b %d')
        
def dataset_processing(releases):
    df = pd.DataFrame(releases)
    df['date'] = df['date'].apply(extract_date)
    df = df[df['date']==(datetime.today() - timedelta(days=1)).strftime('%b %d')]
    df.replace('', pd.NA, inplace=True)
    df.fillna('❓', inplace=True)
    return df

def message_generation(df):
    message='<b>⚡ [MOVIES] New Releases</b>\n\n'
    for index, row in df.head(10).iterrows():
        message+=f"[{row['date']}] - <code>{row['title']}</code> (AUD:{row['audience_score']} | CRT:{row['critics_score']})\n"
    return message

def send_telegram(message, bot_token, chat_id, url_mess):
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
    response = requests.post(url_mess, data=data)

def main():
    bot_token = 'token'
    chat_id = 'chat_id'
    url_mess = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    url = 'https://www.rottentomatoes.com/browse/movies_at_home/sort:newest'
    
    releases = data_parsing(url)
    df = dataset_processing(releases)
    message = message_generation(df)
    send_telegram(message, bot_token, chat_id, url_mess)
    
if __name__ == "__main__":
    main()
