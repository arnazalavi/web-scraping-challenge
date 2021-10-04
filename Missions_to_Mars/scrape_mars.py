from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
#
def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_list = {}

# This is a news data

    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all('div', class_='content_title')[1].text
    news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    # Create a mars dict

    mars_list['latest_news_title']=news_title
    mars_list['news_paragraph'] =news_paragraph
    
# This is Mars Image data

    jpl_img_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_img_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    img_results = soup.find("img", class_='headerimage').get('src')
    #print(img_results)

    final_image_url = jpl_img_url + str(img_results)
    mars_list['featured_Image'] = final_image_url

    #This is Mars Hemisphers data
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)
    links = browser.find_by_css('a.product-item img')
    Hemispheres = []
    for index in range(len(links)):
        Hemisphere = {}
        browser.find_by_css('a.product-item img')[index].click()
        element = browser.links.find_by_text('Sample').first
    #print(element)
    #print(element['href'])
        Hemisphere['img_url'] = element['href']
        #print(browser.find_by_css('h2.title').text)
        Hemisphere['title'] = browser.find_by_css('h2.title').text
        Hemispheres.append(Hemisphere)
        browser.back()

    mars_list["Hemispher_links"] = Hemispheres

    # This is a Mars Fact data
    mars_fact_url = "https://space-facts.com/mars/"
    tables = pd.read_html(mars_fact_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ["Name","Value"]
    mars_facts_df= mars_facts_df.set_index("Name")
    mars_fact_html_table = mars_facts_df.to_html()
    mars_fact_html_table.replace('\n','')
    #print(mars_fact_html_table)
    # get rid of index
    # Move on the side
    mars_list['mars_fact_table'] = str(mars_fact_html_table)



    #browser.back()

    #Hemispheres
    # Quit the browser
    browser.quit()

    return mars_list
