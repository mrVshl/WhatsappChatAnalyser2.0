from urlextract import URLExtract
extract =URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User']==selected_user]

    #Fetching the numbers of messages
    num_messages = df.shape[0]

    #fetching the total number of words
    words = []
    for messages in df['message']:
        words.extend(messages.split())

    #fetching number of media messages
    num_media_shared = df[df['message']=='<Media omitted>\n'].shape[0]

    #fetching number of link shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_shared,len(links)

def most_busy_users(df):
    x = df['User'].value_counts().head()
    new_df = round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','User':'percent'})
    return x, new_df

def create_wordcloud(selected_user,df):
    f1 = open('stop_hinglish.txt', 'r')
    stop_words = f1.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width= 500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


#most common words
def most_common_words(selected_user,df):
    f1 = open('stop_hinglish.txt', 'r')
    stop_words = f1.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

#emoji
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

#monthly timeline function

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month', 'month_num']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time

    return timeline


#daily timeline function

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

#weekly activity analysis

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    weekly_timeline = df['day_name'].value_counts()
    return weekly_timeline

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def activity_heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_heatmap

#function for Datapreprocessor file

def convertDateTimeFormat(date):
    from datetime import datetime
    dates = []
    for time_str in date:
        am_pm_mapping = {'am': 'AM', 'pm': 'PM'}
        date_part, time_part = time_str.split(', ')
        parsed_time = datetime.strptime(time_part, '%I:%M %p - ')
        formatted_time = parsed_time.strftime('%H:%M')
        if len(date_part) > 8:
            year = date_part[-2:]
            result = f'{date_part[:-4]}{year}, {formatted_time} - '
            dates.append(result)
            
        else:
            result = f'{date_part}, {formatted_time} - '
            dates.append(result)
    return dates