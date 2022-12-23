from src.DataProcess import DataProcess
from src.MovieDataCrawler import MovieDataCrawler
import sys
if __name__ == '__main__':
    # name = input("Enter the movie name: ")
    name = " ".join(sys.argv[1:])
    Crawler = MovieDataCrawler(name)
    result = Crawler.crawl()
    result = DataProcess.process(result)
    Crawler.to_json(result)
    # print(result)
