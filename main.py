
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from pyparsing import col
import stanza
import numpy as np
import requests, urllib.parse, lxml
from bs4 import BeautifulSoup


#### FROM LINE 14-57 is a GOOGLE NEWS SCRAPER USE IF U WISH or just import your own data....

searchThis = "FTM" # enter topic you would like scrape via Google.

def paginate(url, previous_url=None):
        if url == previous_url: return
        headers = {
            ""
        } # INSER YOUR HEADER HERE
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')

        yield soup

        next_page_node = soup.select_one('a#pnnext')

        if next_page_node is None: return

        next_page_url = urllib.parse.urljoin('https://www.google.com/', next_page_node['href'])
        yield from paginate(next_page_url)
data = []
def scrape():
        pages = paginate(f"https://www.google.com/search?hl=en-US&q={searchThis}&tbm=nws")
        for soup in pages:
            print(f'Current page: {int(soup.select_one(".YyVfkd").text)}\n')

            for result in soup.select('.WlydOe'):
                title = result.select_one('.nDgy9d').text
                link = result['href']
                source = result.select_one('.NUnG9d span').text
                snippet = result.select_one('.GI74Re.nDgy9d').text
                date_published = result.select_one('.ZE0LJd span').text
                print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')
                data.append((title, link, snippet, source, date_published))
                dataray = np.asarray(data)
                df = pd.DataFrame(dataray)
                df.columns = ['title', 'link', 'snippet', 'source', 'date']
                df.to_csv(fr'C:\Users\Owner\Desktop\news_scrapR\crp00.csv')

scrape()


dataray = np.asarray(data)
df = pd.DataFrame(dataray)
df.columns = ['title', 'link', 'snippet', 'source', 'date']
print(df)

# INSERT CSV or use scraper ABOVE
#df = pd.read_csv(fr"CVXnews.csv") 

### PIPELINE STARTS
data = df['title'].to_list()
print(data)
stanza.download(lang='en', processors='tokenize,sentiment')
nlp = stanza.Pipeline(lang='en', package=None, processors='tokenize ,sentiment', tokenize_batch_size=64, tokenize_no_ssplit=True, batch_size=500)
bruh = nlp(data)
resultt = []
for i, sentence in enumerate(bruh.sentences):
    results = (sentence.sentiment)
    resultt.append(results)

pd3 = pd.DataFrame(resultt, columns=['results'])
def labelR(score):
    if score == 0:
        return 'Bear'
    elif score == 2:
        return 'Bull'
    else:
        return 'eh'
pd3['sentiMENT'] = pd3['results'].apply(labelR)
pd3['headlines'] = df['title']
print(pd3)

plt.title('BTC News Analysis')
barlist = pd3['results'].value_counts().plot(kind='bar', color=['blue', 'green', 'red'])
plt.xlabel('Sentiments')
plt.ylabel('Count')
plt.show()




    

    


  









