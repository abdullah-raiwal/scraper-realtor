import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_real_estate(city):
    base_url = "https://www.realtor.com/realestateandhomes-search/"
    page_number = 1

    data_list = []

    while page_number < 10:
        search_url = f"{base_url}{city}/pg-{page_number}"

        response = requests.get(search_url, headers={
            'authority': 'www.google.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        })

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")
            properties = soup.find(
                'section', class_='PropertiesList_propertiesContainer__HTNbx PropertiesList_listViewGrid__U_BlK')

            if not properties:
                break

            for property in properties:
                title_element = property.find(
                    'span', class_='BrokerTitle_titleText__Y8pb0')
                price_element = property.find(
                    'div', class_='Pricestyles__StyledPrice-rui__btk3ge-0 bvgLFe card-price')
                url_element = property.find(
                    'a', class_='LinkComponent_anchor__0C2xC')

                title = title_element.text.strip() if title_element else ''
                price = price_element.text.strip() if price_element else ''
                url = url_element.get('href') if url_element else ''

                if title and price and url:
                    
                    data_list.append({
                        'Title': title,
                        'Price': price,
                        'URL'  : 'www.realtor.com' + url
                    })
                    print(f"INFO : SCRAPPED FOR {title}")

            page_number += 1
        else:
            print(f"Failed to retrieve data from {
                  search_url}. Status code: {response.status_code}")
            break

    if data_list:
        df = pd.DataFrame(data_list)
        df.to_csv(f'{city}_real_estate_data.csv', index=False)
    else:
        print("No data found.")


city_to_search = input("Enter the city to scrape data: ").lower().replace(' ', '-')
scrape_real_estate(city_to_search)
