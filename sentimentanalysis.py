import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Replace 'your_username' with your actual username
desktop_path = f'/Users/ahmedraza/Desktop/'

# List of input CSV files and their corresponding output CSV files
input_files = ['Reddit_Final.csv', 'metacritic_Final.csv', 'PSBlog_Final.csv', 'IGN_Final.csv']
output_files = ['Reddit_Final_with_sentiments.csv', 'metacritic_Final_with_sentiments.csv', 'PSBlog_Final_with_sentiments.csv', 'IGN_Final_with_sentiments.csv']

# Initialize the VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Initialize the TextBlob sentiment analyzer
def analyze_sentiment_textblob(text):
    analysis = TextBlob(str(text))
    sentiment_score = analysis.sentiment.polarity

    # Classify the sentiment score as positive, neutral, or negative
    if sentiment_score > 0:
        return 'Positive'
    elif sentiment_score == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Function for VADER sentiment analysis
def analyze_sentiment_vader(text):
    compound_score = vader_analyzer.polarity_scores(str(text))['compound']
    
    # Classify the compound score as positive, neutral, or negative
    if compound_score >= 0.05:
        return 'Positive'
    elif -0.05 < compound_score < 0.05:
        return 'Neutral'
    else:
        return 'Negative'

# Loop through input files
for input_file, output_file in zip(input_files, output_files):
    # Load DataFrame from the input CSV file on the desktop
    df = pd.read_csv(desktop_path + input_file)

    # Apply VADER sentiment analysis to the 'Comment' column
    df['VADER_Sentiment'] = df['Comment'].apply(analyze_sentiment_vader)

    # Apply TextBlob sentiment analysis to the 'Comment' column
    df['TextBlob_Sentiment'] = df['Comment'].apply(analyze_sentiment_textblob)

    # Save the DataFrame with sentiment analysis results to a new CSV file
    df.to_csv(desktop_path + output_file, index=False)
