from src.DataProcess import DataProcess
from src.MovieDataCrawler import MovieDataCrawler

if __name__ == '__main__':
    name = input("Enter the movie name: ")
    Crawler = MovieDataCrawler(name)
    result = Crawler.crawl()

    result = DataProcess.process(result)
    print(result)
