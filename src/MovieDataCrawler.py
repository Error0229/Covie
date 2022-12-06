import requests
import bs4
import re
import json
import os
import translators as ts
import translators.server as tss
# use re to remove space and \n at the beginning and end of string also replace <br> with \n


def strfm(text):
    return re.sub(r"<br>", "\n", re.sub(r"^\s+|\s+$|\n", "", text))

# use re to check the string in x hour y min format


def get_time(text):
    time = re.findall(r"\d+", text)
    if len(time) == 2:
        return int(time[0]) * 60 + int(time[1])
    else:
        return int(time[0])


# use re to get the number from string
def get_num(text):
    return re.findall(r"\d+", text)[0]

# use re to test if the string is a ad year


def is_year(text):
    return re.match(r"\d{4}", text)


class MovieDataCrawler:

    def __init__(self, keyword):
        self.keyword = keyword
        self.zh_keyword = tss.google(keyword, to_language="zh-TW")
        self.en_keyword = tss.google(keyword, to_language="en")
        self.data = {}
        self.data["website"] = ["yahoo", "imdb", "douban", "rotten_tomatoes"]
        self.data["yahoo"] = {}
        self.data["imdb"] = {}
        self.data["douban"] = {}
        self.data["rotten_tomatoes"] = {}

    def set_name(self, name):
        self.title = name
        self.data["title"] = name

    def crawl(self):
        self.crawl_yahoo()
        self.crawl_rotten_tomatoes()
        self.crawl_imdb()
        self.crawl_douban()

    def update(self, website, result):
        self.data[website] = result

    def crawl_rotten_tomatoes(self):
        pass

    def init_result(self):
        res = {}
        res["title"] = "N/A"
        res["en_name"] = "N/A"
        res["zh_name"] = "N/A"
        res["is_series"] = "N/A"
        res["length"] = "N/A"
        res["rating"] = "N/A"
        res["release_date"] = "N/A"
        res["genre"] = "N/A"
        res["director"] = "N/A"
        res["cast"] = "N/A"
        res["summary"] = "N/A"
        res["poster"] = "N/A"
        res["trailer"] = "N/A"
        res["website"] = "N/A"
        return res

    def crawl_imdb(self):
        res = {}
        Name = self.zh_keyword.replace(" ", "+")
        search_url = (f"https://www.imdb.com/find?q={Name}&s=tt&ref_=fn_tt_pop")
        headers = {'user-agent': 'Mozilla/5.0'}
        req = requests.get(search_url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")
        all_match = soup.find_all("a", {"class": "ipc-metadata-list-summary-item__t"})
        choose = 0
        if len(all_match) > 1:
            for index, data in enumerate(all_match):
                print(f'{index+1}. {data.text}')
            choose = int(input("Choose the movie: ")) - 1
        movie_url = "https://www.imdb.com" + all_match[choose]["href"]+"?ref_=ttpl_pl_tt"
        res["title"] = all_match[choose].text
        res["website"] = movie_url
        req = requests.get(movie_url, headers=headers).text
        main_sp = bs4.BeautifulSoup(req, "html.parser")
        res["en_name"] = main_sp.find("h1", {"class": "sc-b73cd867-0 eKrKux"}).text
        res["zh_name"] = self.zh_keyword
        present = main_sp.findAll("ul", {"data-testid": "hero-title-block__metadata"})[0].findAll("li")
        is_series = (len(present) == 4)
        res["is_series"] = is_series
        usa_movie_rating = ["G", "PG", "PG-13", "R", "NC-17"]
        for info in present:
            if "h" in info.text:
                res["length"] = get_time(info.text)
            elif info.text in usa_movie_rating:
                res["rating"] = info.text
                res["is_movie"] = True
            elif is_year(info.text):
                res["year"] = info.text[:4]

        hashtags = [tag.text for tag in main_sp.findAll("div", {"class": "ipc-chip-list__scroller"})[0].findAll("span")]
        res["hashtags"] = hashtags
        res["poster"] = main_sp.findAll("img", {"class": "ipc-image"})[0]["src"]
        res["score"] = main_sp.find("span", {"class": "sc-7ab21ed2-1 jGRxWM"}).text
        res["vote_num"] = main_sp.find("div", {"class": "sc-7ab21ed2-3 dPVcnq"}).text
        res["director"] = main_sp.find("a", {"class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text
        res["actors"] = [actor.text for actor in main_sp.findAll(
            "a", {"class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})[2:5]]
        res["comment_url"] = movie_url + "reviews?ref_=tt_urv"
        res["intro"] = main_sp.find("span", {"class": "sc-16ede01-1 kgphFu"}).text
        self.update("imdb", res)
        print(res)

    def crawl_douban(self):
        pass

    def crawl_yahoo(self):
        res = {}
        Name = self.zh_keyword.replace(" ", "+")
        search_url = (f"https://movies.yahoo.com.tw/moviesearch_result.html?keyword={Name}")
        search_res = requests.get(search_url)
        search_sp = bs4.BeautifulSoup(search_res.text, "html.parser")
        if search_sp.find_all("ul", {"class": "release_list mlist"}) == []:
            print(f"Can't find {self.keyword} in yahoo databse")
            return
        movie_url = (search_sp.find_all("ul", {"class": "release_list mlist"})[0].find_all("li")[0].find_all("a")[0].get("href"))
        main_page = requests.get(movie_url)
        main_sp = bs4.BeautifulSoup(main_page.text, "html.parser")
        intro = main_sp.find_all("div", {"class": "movie_intro_info_r"})[0]

        is_movie = (main_sp.find_all("div", {"class": "movie_intro_foto"})[0].find("div").get("class").__contains__("movie"))
        res["is_movie"] = is_movie
        is_series = (main_sp.find_all("div", {"class": "movie_intro_foto"})[0].find("div").get("class").__contains__("drama"))
        res["is_series"] = is_series
        res["zh_name"] = strfm(intro.find_all("h1")[0].text).replace(" ", "")
        res["en_name"] = intro.find_all("h3")[0].text
        res["hashtags"] = [strfm(tag.text) for tag in intro.find_all("div", {"class": "level_name_box"})[0].find_all("a")]
        res["date"] = intro.find_all("span")[0 + is_series].text[5:]
        res["year"] = res["date"][:4]
        res["length"] = intro.find_all("span")[1 + is_series].text[5 - is_series:]
        if intro.find_all("span")[4 + is_series].find_all("a") == []:
            res["director"] = strfm(strfm(intro.find_all("span")[4 + is_series].text)[3:])
        else:
            res["director"] = strfm(intro.find_all("span")[4 + is_series].find_all("a")[0].text)
        res["actors"] = [strfm(name.text) for name in intro.find_all("span")[5 + is_series].find_all("a")]
        if main_sp.find_all("div", {"class": "score_num"}) == []:
            res["score"] = "N/A"
        else:
            res["score"] = main_sp.find_all("div", {"class": "score_num"})[0].text
        res["vote_num"] = get_num(main_sp.find_all("div", {"class": "starbox2"})[0].find_all("span")[0].text)
        res["comment_url"] = (main_sp.find_all("div", {"class": "btn_plus_more usercom_more gabtn"})[0].find_all("a")[0].get("href"))
        res["intro"] = strfm(main_sp.find_all("span", {"id": "story"})[0].text)
        res["rating"] = ("N/A" if is_series else intro.find_all("div")[0].get("class")[0][5:])
        res["poster_url"] = (main_sp.find_all("div", {"class": "movie_intro_foto"})[0].find("img").get("src"))
        self.update("yahoo", res)
        print(res)

    def to_json(self, res):
        return json.dumps(res, open(f"../data/Data_{self.title}.json", "w"))
