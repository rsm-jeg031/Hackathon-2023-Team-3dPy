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
        search_query = request.POST.get('search')

        df = pd.read_csv("/Users/jesusgonzalez/Documents/Local Documents (Jesus' Mac)/Coding & Programming/Hackathon-2023-Team-3dPy/Data/Final_Vader_Time.csv")
        df['Correct_TimeStamp'] = pd.to_datetime(df['Correct_TimeStamp'], format='mixed')
        df['YearMonth'] = df['Correct_TimeStamp'].dt.to_period('M')
        vader_scores_over_time = df.groupby(['YearMonth', 'Vader_Score']).size().unstack(fill_value=0)
        vader_scores_over_time = vader_scores_over_time.reset_index()
        vader_scores_over_time['YearMonth'] = vader_scores_over_time['YearMonth'].dt.to_timestamp()
        filtered_data = vader_scores_over_time[
            (vader_scores_over_time['YearMonth'] >= '2022-10') & 
            (vader_scores_over_time['YearMonth'] <= '2024-02')]
        
        plt.figure(figsize=(6, 4))
        sns.lineplot(x='YearMonth', y='value', hue='Vader_Score', data=filtered_data.melt(id_vars='YearMonth'))
        plt.title('Vader Scores Over Time (Oct 2022 - Jan 2024)')
        plt.xlabel('Time (Year and Month)')
        plt.ylabel('Count of Comments')
        plt.xticks(rotation=45)
        plt.legend(title='Vader Score')
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return render(request, 'search_results.html', {'data': uri})

    return render(request, 'search_results.html')
