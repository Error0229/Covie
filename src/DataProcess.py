import json
import text2emotion as te
import cnsenti as cs
import translators.server as tss
from deep_translator import GoogleTranslator

class DataProcess:

    def __init__(self, data):
        self.data = data

    senti = cs.Sentiment(pos='data/pos_words.txt', neg='data/neg_words.txt', merge=True, encoding='utf-8')

    @staticmethod
    def process(data):

        data["imdb"]["NLP Score"] = DataProcess.process_comments_all(data["imdb"]["all_comments"])
        data["rotten_tomatoes"]["NLP Score"] = DataProcess.process_comments_all(data["rotten_tomatoes"]["all_comments"])
        data["yahoo"]["NLP Score"] = DataProcess.process_comments_all(data["yahoo"]["all_comments"])
        # data["douban"]["NLP Score"] = DataProcess.process_comments_zh(data["douban"]["all_comments"])
        return data

    @staticmethod
    def process_comments_en(comments):
        if len(comments) == 0:
            return 0
        total = 0.0
        for comment in comments:
            text_en = ""
            if len(comment["text"]) > 4500 :
                i = 0
                while 4500 + i* 4500 < len(comment["text"]):
                    text_en += GoogleTranslator(source='auto', target='en').translate(text=comment["text"][i*4500:(i+1)*4500])
                    i += 1
            # text_en =  GoogleTranslator(source='auto', target='en').translate(text=comment["text"])
            emotion = te.get_emotion(text_en)
            approved = comment.get("approved", 0.7)
            total = comment.get("total", 1)
            if total != 0:
                factor = approved/total
            score = (2*emotion["Happy"]-2*emotion["Angry"]+0.5*emotion["Surprise"]-0.5*emotion["Sad"]-0.5*emotion["Fear"])*factor
            score = 1 if score > 1 else score
            score = -1 if score < -1 else score
            total += score
        return total/len(comments)

    @staticmethod
    def process_comments_zh(comments):
        if len(comments) == 0:
            return 0
        total = 0.0
        for comment in comments:
            text_zhCN = ""
            if len(comment["text"]) > 4500 :
                i = 0
                while 4500 + i* 4500 < len(comment["text"]):
                    text_zhCN += GoogleTranslator(source='auto', target='zh-CN').translate(text=comment["text"][i*4500:(i+1)*4500])
                    i += 1
            # text_zhCN = GoogleTranslator(source='auto', target='zh-CN').translate(text=comment["text"])
            emotion = DataProcess.senti.sentiment_calculate(text_zhCN)
            neg = emotion["neg"]
            pos = emotion["pos"]
            neg = 1 if neg == 0 else neg
            pos = 1 if pos == 0 else pos
            score = (pos-neg)/(pos+neg)
            total += score
        return total/len(comments)

    @staticmethod
    def process_comments_all(comments):
        en_score = DataProcess.process_comments_en(comments)
        zh_score = DataProcess.process_comments_zh(comments)
        return {"en_score": en_score, "zh_score": zh_score, "all_score": (0.8*en_score+zh_score)/1.8}

    @staticmethod
    def to_json(data):  # save data to json file
        with open('/data/data.json', 'w') as f:
            json.dump(data, f, indent=4)
