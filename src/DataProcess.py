import json
import text2emotion as te
import cnsenti as cs
# import translators.server as tss
# from deep_translator import GoogleTranslator


class DataProcess:

    def __init__(self, data):
        self.data = data

    senti = cs.Sentiment(pos='data/pos_words.txt', neg='data/neg_words.txt', merge=True, encoding='utf-8')

    @staticmethod
    def process(data):
        
        data["imdb"]["NLP Score"] = DataProcess.process_comments_en(data["imdb"]["all_comments"])
        data["rotten_tomatoes"]["NLP Score"] = DataProcess.process_comments_en(data["rotten_tomatoes"]["all_comments"])
        data["yahoo"]["NLP Score"] = DataProcess.process_comments_zh(data["yahoo"]["all_comments"])

        return data

    @staticmethod
    def process_comments_en(comments):
        if len(comments) == 0:
            return 0
        total_score = 0.0
        for comment in comments:
            text_en = comment["text"]
            # text_en = ""
            # i = 0
            # while i * 4500 < len(comment["text"]):
            #     text_en += GoogleTranslator(source='auto', target='en').translate(text=comment["text"][i*4500:(i+1)*4500])
            #     i += 1
            emotion = te.get_emotion(text_en)
            approved = comment.get("approved", 5)
            total = comment.get("total", 10)
            factor = 0.7
            if total != 0:
                factor = approved/total
            score = (emotion["Happy"]-emotion["Angry"]+emotion["Surprise"])*factor
            score = 1 if score > 1 else score
            score = -1 if score < -1 else score
            total_score += score
        return total_score/len(comments)

    @staticmethod
    def process_comments_zh(comments):
        if len(comments) == 0:
            return 0
        total = 0.0
        for comment in comments:
            text_zhCN = comment["text"]
            # text_zhCN = ""
            # i = 0
            # while i * 4500 < len(comment["text"]):
            #     text_zhCN += GoogleTranslator(source='auto', target='zh-CN').translate(text=comment["text"][i*4500:(i+1)*4500])
            #     i += 1
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
        with open('data/data.json', 'w') as f:
            json.dump(data, f, indent=4)
