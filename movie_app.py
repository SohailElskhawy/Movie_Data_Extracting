from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)


def main():
    driver.get('https://www.imdb.com/search/title/?groups=top_1000')

    master_list = []
    m = 1
    while m != 20:
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        movie_descrip = soup.find_all("div",class_='lister-item mode-advanced')
        
        for i in movie_descrip:
            my_dict = {}
            try:
                movie_name = i.h3.a.text
                movie_about = (i.find_all("p",class_='text-muted')[1].text)
                movie_info = i.find_all("p",class_='text-muted')[0].text.strip().split("\n|\n")
                movie_age = movie_info[0]
                movie_min = movie_info[1]
                movie_genre = movie_info[2].strip()
                movie_rate = i.find("strong").text
                movie_cast = i.find("p",class_="").text.strip().split("|")
                movie_directors = movie_cast[0]
                movie_actors = movie_cast[1]
                my_dict["Movie Name"] = movie_name
                my_dict["Movie Description"] = movie_about
                my_dict["Movie Age Rate"] = movie_age
                my_dict["Movie Duration"] = movie_min
                my_dict['Movie Genres'] = movie_genre
                my_dict["Movie Directors"] = movie_directors.split(":")[1].strip().rstrip().lstrip()
                my_dict["Movie Stars"] = movie_actors.replace("Stars:","").strip().rstrip().lstrip()
                my_dict["Movie Rate"] = movie_rate
            except:
                continue
            master_list.append(my_dict)
        
        m += 1
        next_butn = driver.find_element(By.CLASS_NAME, "lister-page-next")
        next_butn.click()
        driver.implicitly_wait(6)
    
    
    import pandas as pd
    
    dataframe = pd.DataFrame(master_list)
    dataframe.to_csv("sample_output.csv",index=False)



main()
driver.close()