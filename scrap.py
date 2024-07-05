import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
import time

def Page_100_movie(pages = 100):

    headers = {
        'Accept-Language': 'en-US,en;q=0.5'
    }
    time.sleep(5)


    page_1 = []
    base_url = "https://www.themoviedb.org"

    for item in range(1,101):
        url = f"{base_url}/movie?page={item}"
            
        response = requests.get(url, headers=headers)
        source = response.text
        soup_data = BeautifulSoup(source, 'html.parser')

        first_div = soup_data.find_all('div', class_="card style_1")


    # url = "https://www.themoviedb.org/movie?page=1"
    # This the main url of page from where we find all data of movie 


    # print(movie_url)   This is link where we find inner data of movie

        for first_all_data in first_div:
            movie_name_div = first_all_data.find('a')
            movie_name = movie_name_div['title']  if movie_name_div else 'Not Available'

            release_date = first_all_data.find('p', class_='').text.strip()
            
            review_div = first_all_data.find('div', class_="user_score_chart")
            review = review_div['data-percent'] if review_div else 'Not Available'
            

            # This line where we access the anchor tag find paticular movie url
            Inner_link_data = first_all_data.find('a', href=True)
            # Here i combined the  inner page link with particular movie link 
            movie_url = base_url + Inner_link_data['href']
            
            movie_detail_response = requests.get(movie_url, headers=headers)
            movie_detail_soup = BeautifulSoup(movie_detail_response.text, 'html.parser')
            
            duration_span = movie_detail_soup.find('span', class_='runtime')
            duration = duration_span.text.strip() if duration_span else 'Not Available'
            
            genre_span = movie_detail_soup.find('span', class_='genres')
            genre_all = genre_span.find_all('a')  if genre_span else [] 
            genre_data = [item.get_text() for item in genre_all]
            
            
            # director =  movie_detail_soup.find_all('li', class_='profile')
            # for item in director:

            #     All_P_tag = item.find('p', class_='character')
            #     if All_P_tag.text.strip() == 'Director' or 'Director,Screenplay' or 'Director, Story' or 'Director, Writer':

            #     # if All_P_tag and (All_P_tag.text.strip() in ['Director', 'Director,Screenplay', 'Director, Story']):
                
                    
            #             director_All_data = item.find('a').text.strip()
                    
            # # print(director_data)


            
            
            director_all_li = movie_detail_soup.find_all('li', class_='profile')
            
            for section in director_all_li:
                All_p_tag = section.find('p', class_='character')
                if All_p_tag  and ('Director' in All_p_tag .text.strip()):
                    director_name_tag = section.find('a')
                    if director_name_tag:
                        director_name = director_name_tag.text.strip()
            
                    

            
            first_div_product = {
                'movie_name': movie_name,
                'release_date': release_date,
                'review': review,
                'duration': duration,
                'genre': genre_data,
                'director': director_name
            }
            
            page_1.append(first_div_product)


    product_df = pd.DataFrame(page_1)
    # print(product_df)
    product_df.to_excel('All_data_page_100.xlsx')
    return product_df

product_df = Page_100_movie()
print(product_df)
