import requests
import bs4
import re
import json
# import os
# import translators as ts
import translators.server as tss
import nltk
# use re to remove space and \n at the beginning and end of string also replace <br> with \n


def strfm(text):
    # use re to remove space and \n at the beginning and middle of string also replace <br> with \n and remove space and \n at the end of string
    return re.sub(r"<br>", "\n", re.sub(r"^\s+|\s+$|\n", "", re.sub(r"\s+", " ", text)))

# use re to check the string in x hour y min format


def get_time(text):
    time = re.findall(r"\d+", text)
    if len(time) == 2:
        return int(time[0]) * 60 + int(time[1])
    else:
        return int(time[0])


# use re to get the number from string , contain "," is ok
def get_num(text):
    return re.findall(r"\d+", text)[0]
def get_num_v2(text):
    return re.findall(r'[\d,\,,\+]+',text)[0]
# def get_num_v3(text):
#     return re.findall(r'[\d,\,,\+]+ (?=Reviews)',text)[0]
# use re to test if the string is a ad year


def is_year(text):
    return re.match(r"\d{4}", text)

def get_year(text):
    return re.findall(r"\d{4}", text)[0]
class MovieDataCrawler:
    def __init__(self, keyword):
        nltk.download('omw-1.4')
        self.keyword = keyword
        # self.zh_keyword = tss.google(keyword, to_language="zh-TW")
        self.en_keyword = tss.google(keyword, to_language="en")
        self.data = {}
        self.set_name(keyword)
        self.data["website"] = ["yahoo", "imdb", "douban", "rotten_tomatoes"]
        self.data["yahoo"] = self.init_result()
        self.data["imdb"] = self.init_result()
        self.data["douban"] = self.init_result()
        self.data["rotten_tomatoes"] = self.init_result()

    def set_name(self, name):
        self.title = name
        self.data["title"] = name

    def crawl(self):
        self.crawl_yahoo()
        self.crawl_rotten_tomatoes()
        self.crawl_imdb()
        return self.data

    def update(self, website, result):
        self.data[website] = result

    def init_result(self):
        res = {}
        res["title"] = "N/A"
        res["en_name"] = "N/A"
        res["zh_name"] = "N/A"
        res["is_series"] = "N/A"
        res["length"] = "N/A"
        res["rating"] = "N/A"
        res["release_date"] = "N/A"
        res["hashtags"] = "N/A"
        res["director"] = "N/A"
        res["actors"]= "N/A"
        res["vote_num"] = "N/A"
        res["intro"] = "N/A"
        res["poster"] = "N/A"
        res["trailer"] = "N/A"
        res["website"] = "N/A"
        res["all_comments"] = []
        return res

    def crawl_rotten_tomatoes(self):
        res = {}
        Name = self.en_keyword.replace(" ", "+")
        search_url = (f"https://www.rottentomatoes.com/search?search={Name}")
        headers = {'user-agent': 'Mozilla/5.0'}
        req = requests.get(search_url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")
        all_match = soup.find("search-page-result", attrs={"type": "movie"})
        if not all_match:
            print(f"Can't find {self.keyword} in rotten tomatoes database")
            return
        all_match = all_match.find_all("search-page-media-row")
        choose = 0
        # if len(all_match) > 1:
        #     for i, pages in enumerate(all_match):
        #         print(f'{i+1}. {strfm(pages.find("a",attrs ={"slot": "title"}).text)}')
        #     choose = int(input("Choose the movie: ")) - 1
        movie_url = all_match[choose].find("a", attrs={"slot": "title"})["href"]
        res["title"] = strfm(all_match[choose].find("a", attrs={"slot": "title"}).text)
        res["website"] = movie_url
        req = requests.get(movie_url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")
        res["poster"] = soup.find("img", attrs={"class": "posterImage"})["src"]
        res["actors"] = [strfm(actor.text) for actor in soup.find_all("div", attrs={"data-qa": "cast-section"})[0].find_all("a", attrs={"data-qa": "cast-crew-item-link"})]
        res["intro"] = strfm(
            soup.find("div", attrs={"id": "movieSynopsis"}).text)
        score_container = soup.find("score-board")
        res["rating"] = score_container.attrs["tomatometerscore"]
        # if not res["rating"]:
        #     res["rating"] = "N/A"
        res["rating_count"] = get_num_v2(score_container.find_all("a")[0].text)
        res["rating_link"] = "https://www.rottentomatoes.com" + \
            score_container.find_all("a")[0]["href"]
        res["audience_rating"] = score_container.attrs["audiencescore"]
        if not res["audience_rating"]:
            res["audience_rating"] = "N/A"
        res["audience_rating_count"] = get_num_v2(score_container.find_all("a")[1].text)
        res["audience_rating_link"] = "https://www.rottentomatoes.com" + \
            score_container.find_all("a")[1]["href"]
        info_label = soup.find_all("div", attrs={"data-qa": "movie-info-item-label"})
        info_value = soup.find_all("div", attrs={"data-qa": "movie-info-item-value"})
        for index in range(len(info_label)):
            if strfm(info_label[index].text) == "Genre:":
                res["hashtags"] = [strfm(x) for x in strfm(info_value[index].text).split(",")]
            if strfm(info_label[index].text) == "Director:":
                res["director"] = strfm(info_value[index].text)
            if info_label[index].text == "Runtime:":
                # print(info_value[index].text)
                res["length"] = get_time(info_value[index].text)
            # data of theaters release date is more prior than data of streaming release date
            if info_label[index].text == "Release Date (Theaters):":
                res["date"] = strfm(info_value[index].text)
                res["year"] = get_year(res["date"].split(",")[1])
            if info_label[index].text == "Release Date (Streaming):":
                res["date"] = strfm(info_value[index].text)
                res["year"] = get_year(res["date"].split(",")[1])
        res["all_comments"] = self.crawl_rotten_tomatoes_comments(res["audience_rating_link"])
        self.update("rotten_tomatoes", res)
        # print(res)

    # def crawl_douban(self):
    #     res = {}
    #     Name = self.keyword.replace(" ", "+")
    #     search_url = (
    #         f"https://movie.douban.com/j/subject_suggest?q={Name}")
    #     search_res = requests.get(search_url)
    #     search_sp = bs4.BeautifulSoup(search_res.text, "html.parser")
    #     if search_sp.find_all("li") == []:
    #         print(f"Can't find {self.keyword} in douban database")
    #         return
    #     movie_url = (search_sp.find_all("li")[0].get("data-url"))
    #     main_page = requests.get(movie_url)
    #     main_sp = bs4.BeautifulSoup(main_page.text, "html.parser")
    #     res["title"] = main_sp.find(
    #         "span", attrs={"property": "v:itemreviewed"}).text
    #     res["origin_name"] = main_sp.find(
    #         "span", attrs={"property": "v:itemreviewed"}).text
    #     res["website"] = movie_url
    #     res["poster"] = main_sp.find("img", attrs={"rel": "v:image"}).get("src")
    #     res["intro"] = main_sp.find("span", attrs={"property": "v:summary"}).text
    #     res["director"] = main_sp.find(
    #         "a", attrs={"rel": "v:directedBy"}).text
    #     res["actors"] = [actor.text for actor in main_sp.findAll(
    #         "a", attrs={"rel": "v:starring"})[:3]]
    #     res["year"] = main_sp.find(
    #         "span", attrs={"property": "v:initialReleaseDate"}).text[:4]
    #     res["length"] = get_time(main_sp.find(
    #         "span", attrs={"property": "v:runtime"}).text)
    #     res["rating"] = main_sp.find(
    #         "strong", attrs={"property": "v:average"}).text
    #     res["vote_num"] = main_sp.find(
    #         "span", attrs={"property": "v:votes"}).text
    #     res["comment_url"] = movie_url + "comments?status=P"
    #     self.update("douban", res)
        # print(res)

    def crawl_imdb(self):
        res = {}
        Name = self.keyword.replace(" ", "+")
        search_url = (
            f"https://www.imdb.com/find?q={Name}&s=tt&ref_=fn_tt_pop")
        headers = {'user-agent': 'Mozilla/5.0',
                   'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
        req = requests.get(search_url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")

        # with open("test.html", "w", encoding="utf-8") as f:
        #     f.write(soup.prettify())
        all_match = soup.find_all(
            "a", attrs={"class": "ipc-metadata-list-summary-item__t"})
        if all_match is None:
            print(f"Can't find {self.keyword} in imdb database")
        choose = 0
        # if len(all_match) > 1:
        #     for index, data in enumerate(all_match):
        #         print(f'{index+1}. {data.text}')
        #     choose = int(input("Choose the movie: ")) - 1
        movie_url = "https://www.imdb.com" + all_match[choose]["href"].split("?")[0]

        res["title"] = all_match[choose].text
        res["website"] = movie_url
        req = requests.get(movie_url+"?ref_=ttpl_pl_tt", headers=headers).text
        main_sp = bs4.BeautifulSoup(req, "html.parser")
        try_find = main_sp.find(
            attrs={"data-testid": "hero-title-block__original-title"})
        if try_find is not None:
            res["second_name"] = try_find.text.split(":")[1]
        res["origin_name"] = main_sp.find(
            "h1", attrs={"data-testid": "hero-title-block__title"}).text
        present = main_sp.findAll(
            "ul", attrs={"data-testid": "hero-title-block__metadata"})[0].findAll("li")
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

        hashtags = [tag.text for tag in main_sp.findAll(
            "div", attrs={"class": "ipc-chip-list__scroller"})[0].findAll("span")]
        res["hashtags"] = hashtags
        res["poster"] = main_sp.findAll(
            "img", attrs={"class": "ipc-image"})[0]["src"]
        res["director"] = main_sp.find("a", attrs={
                                       "class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text
        res["actors"] = [actor.text for actor in main_sp.findAll(
            "a", attrs={"class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})[2:5]]
        res["intro"] = main_sp.find(
            "span", attrs={"class": "sc-16ede01-1 kgphFu"}).text
        if main_sp.find(attrs={"class": "sc-5766672e-1 fsIZKM"}) != None:
            # print(main_sp.find("tm-box-up-title"))
            res["release_date"] = "Coming soon"
        else:
            res["score"] = main_sp.find(
                "span", attrs={"class": "sc-7ab21ed2-1 jGRxWM"}).text
            res["vote_num"] = main_sp.find(
                "div", attrs={"class": "sc-7ab21ed2-3 dPVcnq"}).text
            res["comment_url"] = movie_url + "reviews?ref_=tt_urv"
        self.update("imdb", res)
        res["all_comments"] = self.crawl_imdb_comments(res["comment_url"])
        # print(res)

    def crawl_yahoo(self):
        res = {}
        Name = self.keyword.replace(" ", "+")

        search_url = (
            f"https://movies.yahoo.com.tw/moviesearch_result.html?keyword={Name}&type=movie&movie_type=movie")
        search_res = requests.get(search_url)
        search_sp = bs4.BeautifulSoup(search_res.text, "html.parser")
        if search_sp.find_all("div", attrs={"class": "search_num _c"})[0].find("span").text == "0":
            print(f"Can't find {self.keyword} in yahoo databse")
            return

        movie_list = search_sp.find_all("ul", attrs={"class": "release_list mlist"})[
            0].find_all("li")
        choose = 0
        # if len(movie_list) > 1:
        #     for id, movie in enumerate(movie_list):
        #         movie_name = movie.find_all("a")[1].text
        #         print(f"{id+1}. {movie_name}")
        #     choose = int(input("Choose the movie: ")) - 1
        movie_url = movie_list[choose].find_all("a")[0].get("href")
        res["title"]=strfm(movie_list[choose].find_all("a")[1].text)
        res["website"]=movie_url
        main_page = requests.get(movie_url)
        main_sp = bs4.BeautifulSoup(main_page.text, "html.parser")
        intro = main_sp.find_all("div", {"class": "movie_intro_info_r"})[0]

        is_movie = (main_sp.find_all("div", {"class": "movie_intro_foto"})[
                    0].find("div").get("class").__contains__("movie"))
        res["is_movie"] = is_movie
        is_series = (main_sp.find_all("div", {"class": "movie_intro_foto"})[
                     0].find("div").get("class").__contains__("drama"))
        res["is_series"] = is_series
        res["zh_name"] = strfm(intro.find_all("h1")[0].text).replace(" ", "")
        res["en_name"] = intro.find_all("h3")[0].text
        res["hashtags"] = [strfm(tag.text) for tag in intro.find_all(
            "div", {"class": "level_name_box"})[0].find_all("a")]
        res["date"] = intro.find_all("span")[0 + is_series].text[5:]
        res["year"] = res["date"][:4]
        res["length"] = intro.find_all(
            "span")[1 + is_series].text[5 - is_series:]
        if intro.find_all("span")[4 + is_series].find_all("a") == []:
            res["director"] = strfm(
                strfm(intro.find_all("span")[4 + is_series].text)[3:])
        else:
            res["director"] = strfm(intro.find_all(
                "span")[4 + is_series].find_all("a")[0].text)
        res["actors"] = [strfm(name.text) for name in intro.find_all("span")[
            5-is_series].find_all("a")]
        if main_sp.find_all("div", {"class": "score_num"}) == []:
            res["score"] = "N/A"
        else:
            res["score"] = main_sp.find_all(
                "div", {"class": "score_num"})[0].text
        res["vote_num"] = get_num(main_sp.find_all(
            "div", {"class": "starbox2"})[0].find_all("span")[0].text)
        res["comment_url"] = (main_sp.find_all("div", {
                              "class": "btn_plus_more usercom_more gabtn"})[0].find_all("a")[0].get("href"))
        res["intro"] = strfm(main_sp.find_all("span", {"id": "story"})[0].text)
        res["rating"] = (
            "N/A" if is_series else intro.find_all("div")[0].get("class")[0][5:])
        res["poster"] = (main_sp.find_all("div", {"class": "movie_intro_foto"})[
            0].find("img").get("src"))
        res["all_comments"] = self.crawl_yahoo_comments(res["comment_url"])
        self.update("yahoo", res)
        # print(res)

    def crawl_imdb_comments(self, url):
        res = []
        headers = {'user-agent': 'Mozilla/5.0',
                   'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
        req = requests.get(url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")
        comments = soup.find_all("div", attrs={"class": "lister-item mode-detail imdb-user-review collapsable"})

        for comment in comments:
            comment_res = {}
            text = comment.find("div", attrs={"class": "text show-more__control"}).text
            format_text = text.replace("<br>", "\n").replace("\"", "")
            helpful = comment.find("div", attrs={"class": "actions text-muted"}).text
            helpful = strfm(helpful).split(" ")
            total = int(helpful[3].replace(",", ""))
            approved = int(helpful[0].replace(",", ""))
            comment_res["text"] = format_text
            comment_res["total"] = total
            comment_res["approved"] = approved
            res.append(comment_res)
        return res

    def crawl_rotten_tomatoes_comments(self, url):
        # print(url)
        res = []
        headers = {'user-agent': 'Mozilla/5.0'}
        req = requests.get(url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")
        comments = soup.find_all("li", attrs={"class": "audience-reviews__item"})
        for comment in comments:
            comment_res = {}
            text = comment.find("p", attrs={"class": "audience-reviews__review"}).text
            format_text = text.replace("<br>", "\n").replace("\"", "")
            comment_res["text"] = format_text
            res.append(comment_res)
        return res

    def crawl_yahoo_comments(self, url):
        res = []
        headers = {'user-agent': 'Mozilla/5.0'}
        req = requests.get(url, headers=headers).text
        soup = bs4.BeautifulSoup(req, "html.parser")
        with open("test.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        if (soup.find("div", attrs={"class": "page_numbox"})) == None:
            total_page = 1
        else:
            total_page = int(soup.find("div", attrs={"class": "page_numbox"}).find_all("a")[-2].text)
        for i in range(1, min(3, total_page+1)):  # since too much comments would slow the program down
            req = requests.get(url+"?sort=update_ts&order=desc&page="+str(i), headers=headers).text
            soup = bs4.BeautifulSoup(req, "html.parser")
            comments = soup.find_all("form", id="form_good1")
            for comment in comments:
                comment_res = {}
                text = comment.find_all("span")[2].text
                format_text = text.replace("\r\n", " ")
                comment_res["text"] = format_text
                res.append(comment_res)
        return res

    def to_json(self, res):
        with open(f"data/MovieData.json", mode="w+", encoding="utf8") as f:
            json.dump(res, f, indent=4, ensure_ascii=False)
