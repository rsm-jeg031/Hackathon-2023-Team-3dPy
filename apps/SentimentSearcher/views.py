from django.shortcuts import render, HttpResponse
from .models import Search
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import io
import urllib, base64


# Create your views here.
def home(request):
    return render(request, "home.html")

def search_analysis(request):
    if request.method == 'POST':
        # MY SEARCH BAR 
        search_query = request.POST.get('search')

        # PLOT 1 ---------------------
        df = pd.read_csv("/Users/jesusgonzalez/Documents/Local Documents (Jesus' Mac)/Coding & Programming/Hackathon-2023-Team-3dPy/Data/Final_Vader_Time.csv")
        df['Correct_TimeStamp'] = pd.to_datetime(df['Correct_TimeStamp'], format='mixed')
        df['YearMonth'] = df['Correct_TimeStamp'].dt.to_period('M')
        vader_scores_over_time = df.groupby(['YearMonth', 'Vader_Score']).size().unstack(fill_value=0)
        vader_scores_over_time = vader_scores_over_time.reset_index()
        vader_scores_over_time['YearMonth'] = vader_scores_over_time['YearMonth'].dt.to_timestamp()
        filtered_data = vader_scores_over_time[
            (vader_scores_over_time['YearMonth'] >= '2022-10') & 
            (vader_scores_over_time['YearMonth'] <= '2024-02')]
        plt.figure(figsize=(5, 3))
        sns.lineplot(x='YearMonth', y='value', hue='Vader_Score', data=filtered_data.melt(id_vars='YearMonth'))
        plt.title('Total Vader Scores Over Time (Oct 2022 - Jan 2024)')
        plt.xlabel('Time (Year and Month)')
        plt.ylabel('Count of Comments')
        plt.xticks(rotation=45)
        plt.legend(title='Vader Score')
        plt.grid(True)
        
        # PLOT 1 BUFFER ---------------------
        buf1 = io.BytesIO()
        plt.savefig(buf1, format='png')
        buf1.seek(0)
        string1 = base64.b64encode(buf1.read())
        uri1 = urllib.parse.quote(string1)
        plt.clf()
        
        # PLOT 2 ---------------------
        df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search_query).any(), axis=1)]
        vader_scores_over_time2 = df_filtered.groupby(['YearMonth', 'Vader_Score']).size().unstack(fill_value=0)
        vader_scores_over_time2 = vader_scores_over_time2.reset_index()
        vader_scores_over_time2['YearMonth'] = vader_scores_over_time2['YearMonth'].dt.to_timestamp()
        plt.figure(figsize=(5, 3))
        sns.lineplot(x='YearMonth', y='value', hue='Vader_Score', data=vader_scores_over_time2.melt(id_vars='YearMonth'))
        plt.title(f'Sentiment for: --{search_query}--')
        plt.xlabel('Time (Year and Month)')
        plt.ylabel('Count of Comments')
        plt.xticks(rotation=45)
        plt.legend(title='Vader Score')
        plt.grid(True)
        #temp_total_comments = vader_scores_over_time2["Negative"].sum() + vader_scores_over_time2["Positive"].sum() + vader_scores_over_time2["Neutral"].sum()
        #print(f'Total comments: {temp_total_comments}')
        #print(f'Total Negative comments: {vader_scores_over_time2["Negative"].sum()}')
        #print(f'Total Positive comments: {vader_scores_over_time2["Positive"].sum()}')
        #print(f'Total Neutral comments: {vader_scores_over_time2["Neutral"].sum()}')

        # PLOT 2 BUFFER ---------------------
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        string2 = base64.b64encode(buf2.read())
        uri2 = urllib.parse.quote(string2)
        plt.clf()
        
        # PLOT 3 ---------------------
        def generate_wordcloud(sentiment, color, axs):
            comments = df_filtered[df_filtered['Vader_Score'] == sentiment]['Comment']
            comments = ' '.join(str(comment) for comment in comments)
            words = [word for word in comments.split() if word.lower() not in ENGLISH_STOP_WORDS]
            word_frequencies = {word: words.count(word) for word in set(words)}
            wordcloud = WordCloud(width=600, height=200, background_color='black', max_words=100,
                                colormap=color, random_state=42)
            wordcloud.generate_from_frequencies({word: freq for word, freq in word_frequencies.items() if len(word) > 5})
            axs.imshow(wordcloud, interpolation='bilinear')
            axs.set_title(f'{sentiment.capitalize()} Sentiment', fontsize=16)
            axs.axis('off')
        fig, axs = plt.subplots(1, 3, figsize=(14, 4))
        generate_wordcloud('Positive', 'Greens', axs[0])
        generate_wordcloud('Neutral', 'Blues', axs[1])
        generate_wordcloud('Negative', 'Reds', axs[2])
        plt.tight_layout()
        
        # PLOT 3 BUFFER ---------------------
        buf3 = io.BytesIO()
        plt.savefig(buf3, format='png')
        buf3.seek(0)
        string3 = base64.b64encode(buf3.read())
        uri3 = urllib.parse.quote(string3)        
        
        return render(request, 'search_results.html', {'data1': uri1, 'data2': uri2, 'data3': uri3})

    return render(request, 'search_results.html')
