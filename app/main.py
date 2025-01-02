from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    print(f"Sentiment Analysis: {sentiment}")

if __name__ == "__main__":
    analyze_sentiment("I love programming in Python!")
