import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

desktop_path = f'/Users/ahmedraza/Desktop/' # hey bro change this to a relative path when you have a sec. I also got rid of all the comments 

input_files = ['Reddit_Final.csv', 'metacritic_Final.csv', 'PSBlog_Final.csv', 'IGN_Final.csv']
output_files = ['Reddit_Final_with_sentiments.csv', 'metacritic_Final_with_sentiments.csv', 'PSBlog_Final_with_sentiments.csv', 'IGN_Final_with_sentiments.csv']

vader_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_textblob(text):
    analysis = TextBlob(str(text))
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0:
        return 'Positive'
    elif sentiment_score == 0:
        return 'Neutral'
    else:
        return 'Negative'

def analyze_sentiment_vader(text):
    compound_score = vader_analyzer.polarity_scores(str(text))['compound']
    
    if compound_score >= 0.05:
        return 'Positive'
    elif -0.05 < compound_score < 0.05:
        return 'Neutral'
    else:
        return 'Negative'

for input_file, output_file in zip(input_files, output_files):
    df = pd.read_csv(desktop_path + input_file)

    df['VADER_Sentiment'] = df['Comment'].apply(analyze_sentiment_vader)

    df['TextBlob_Sentiment'] = df['Comment'].apply(analyze_sentiment_textblob)

    df.to_csv(desktop_path + output_file, index=False)
