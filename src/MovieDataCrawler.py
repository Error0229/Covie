import requests
import bs4
import re
import json
import os
# use re to remove space and \n at the beginning and end of string also replace <br> with \n


def strfm(text):
    return re.sub(r'<br>', '\n', re.sub(r'^\s+|\s+$|\n', '', text))
# use re to get the number from string


def get_num(text):
    return re.findall(r'\d+', text)[0]


class MovieDataCrawler:

    def __init__(self, keyword):
        self.keyword = keyword
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

    def crawl_imdb(self):
        pass

    def crawl_douban(self):
        pass

    def crawl_yahoo(self):
        res = {}
        Name = self.keyword.replace(' ', '+')
        search_url = f'https://movies.yahoo.com.tw/moviesearch_result.html?keyword={Name}'
        search_res = requests.get(search_url)
        search_sp = bs4.BeautifulSoup(search_res.text, 'html.parser')
        if (search_sp.find_all("ul", {"class": "release_list mlist"}) == []):
            print(f"Can't find {self.keyword} in yahoo databse")
            return
        movie_url = search_sp.find_all("ul", {"class": "release_list mlist"})[
            0].find_all("li")[0].find_all("a")[0].get("href")
        main_page = requests.get(movie_url)
        main_sp = bs4.BeautifulSoup(main_page.text, 'html.parser')
        intro = main_sp.find_all("div", {"class": "movie_intro_info_r"})[0]

        is_movie = main_sp.find_all("div", {"class": "movie_intro_foto"})[
            0].find("div").get("class").__contains__("movie")
        res["is_movie"] = is_movie
        is_drama = main_sp.find_all("div", {"class": "movie_intro_foto"})[
            0].find("div").get("class").__contains__("drama")
        res["is_drama"] = is_drama
        res["ch_name"] = strfm(intro.find_all("h1")[0].text).replace(' ', '')
        res["en_name"] = intro.find_all("h3")[0].text
        res["hashtags"] = [strfm(tag.text) for tag in intro.find_all(
            "div", {"class": "level_name_box"})[0].find_all("a")]
        res["date"] = intro.find_all("span")[0+is_drama].text[5:]
        res["year"] = res["date"][:4]
        res["length"] = intro.find_all("span")[1+is_drama].text[5-is_drama:]
        if (intro.find_all("span")[4+is_drama].find_all("a") == []):
            res['director'] = strfm(
                strfm(intro.find_all("span")[4+is_drama].text)[3:])
        else:
            res["director"] = strfm(intro.find_all(
                "span")[4+is_drama].find_all("a")[0].text)
        res["actors"] = [strfm(name.text) for name in intro.find_all("span")[
            5+is_drama].find_all("a")]
        if (main_sp.find_all("div", {"class": "score_num"}) == []):
            res["score"] = "N/A"
        else:
            res["score"] = main_sp.find_all(
                "div", {"class": "score_num"})[0].text
        res["vote_num"] = get_num(main_sp.find_all(
            "div", {"class": "starbox2"})[0].find_all("span")[0].text)
        res["comment_url"] = main_sp.find_all("div", {"class": "btn_plus_more usercom_more gabtn"})[
            0].find_all("a")[0].get("href")
        res["intro"] = strfm(main_sp.find_all("span", {"id": "story"})[0].text)
        res["level"] = "N/A" if is_drama else intro.find_all("div")[
            0].get("class")[0][5:]
        res["poster_url"] = main_sp.find_all("div", {"class": "movie_intro_foto"})[
            0].find("img").get("src")
        self.set_name(res["ch_name"])
        self.update("yahoo", res)
        print(res)

    def to_json(self, res):
        return json.dumps(res, open(f'../data/Data_{self.title}.json', 'w'))
