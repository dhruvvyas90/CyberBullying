from afinn import Afinn
from basicInfo import privateInfo as pr

class afinnsenti:

    def __label_sentiment(self, score):
        if score < self.neutral_threshold[0]:
            # negative sentiment
            return -1
        elif score > self.neutral_threshold[1]:
            # positive sentiment
            return 1
        else:
            # neutral sentiment
            return 0

    def get_sentiment_label(self, data, return_score=False):
        score = self.afinn.score(data)
        label = self.__label_sentiment(score)
        if return_score:
            return label, score
        else:
            return label

    def compilesentiment(self, field_no=pr.m_content, separate_sentiment_list=True):
        data = self.data
        sentiment_compilation = [] if separate_sentiment_list else None
        for idx in range(len(data)):
            datum = data[idx]
            polarity, score = self.get_sentiment_label(datum[field_no], return_score=True)
            if separate_sentiment_list:
                sentiment_compilation.append([score, polarity])
            else:
                datum.extend([score, polarity])
                data[idx] = datum
        return sentiment_compilation if separate_sentiment_list else data


    def set_neutral_threshold(self, neutral_threshold):
        self.neutral_threshold = neutral_threshold

    def set_data(self, data):
        self.data = data

    def __init__(self, data=None, neutral_threshold=[0, 2]):
        self.afinn = Afinn()
        self.set_data(data)
        self.set_neutral_threshold(neutral_threshold)