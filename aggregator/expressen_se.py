import requests
from bs4 import BeautifulSoup
import helpers
import json


def scrape_story(url):
    page = requests.get(url, headers={"User-Agent": helpers.chrome_user_agent})

    soup = BeautifulSoup(page.content, 'html.parser')

    article = {"url": url, "fetched_at": helpers.get_timestamp()}
    full_text = ""

    try:
        title = '\n'.join([p.get_text() for p in soup.find(
            class_="article__header").find_all('h1')]).replace("\xa0", "")
        article["title"] = title
        full_text += title + "\n"
    except:
        pass

    try:
        location = soup.find("a", href=lambda href: href and "/tagg/location" in href).get_text()
        article["location"] = location
    except:
        pass

    try:
        preamble = '\n'.join([p.get_text() for p in soup.find(
            class_="article__preamble").find_all('p')]).replace("\xa0", "")

        if preamble.startswith("Premium"):
            return None

        article["preamble"] = preamble
        full_text += preamble + "\n"
    except:
        pass

    try:
        body = '\n'.join([p.get_text() for p in soup.find(
            class_="article__body-text").find_all('p')]).replace("\xa0", "")
        article["body"] = body
        full_text += body + "\n"
    except:
        pass

    try:
        time = soup.find("time")["datetime"]
        article["published_at"] = time
    except:
        pass

    article["full_text"] = full_text

    # ensure that article has some content
    if len(full_text) < 1:
        return None

    return article


def scrape():
    url = "https://www.expressen.se/nyhetsdygnet/"

    # chrome user agent
    page = requests.get(url, headers={"User-Agent": helpers.chrome_user_agent})
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all articles
    list_elements = soup.find_all(class_="list-page__item")

    news_links = []

    for element in list_elements:
        href = element.find('a')['href']
        if "expressen.se" not in href:
            href = "https://www.expressen.se" + href
        if "premium" in href:
            continue
        if "/tv/" in href:
            continue
        news_links.append(href)

    articles = []

    for link in news_links:
        try:
            article = scrape_story(link)
            if article is not None:
                articles.append(article)
        except:
            pass

    return articles


if __name__ == '__main__':
    print(json.dumps(scrape_story("https://www.expressen.se/tv/nyheter/polisanmals-efter-skamtet-kommer-aka-in-/")))
    # print(json.dumps(scrape()))
