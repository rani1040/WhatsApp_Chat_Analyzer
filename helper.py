from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import emoji


def fetch_stat(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Total number of Messages
    nu_of_messages = df['User'].shape[0]

    # Total number of words in messages
    word = []
    for i in df['Message']:
        word.extend(i.split())

    # number of media file shared
    media_file_shared = df[df['Message'] == ' <Media omitted>\n'].shape[0]

    return nu_of_messages,len(word),media_file_shared


def fetch_most_busy(df):
    X = df['User'].value_counts().head()
    per_df = round(df['User'].value_counts().sort_values(ascending=False)/len(df) * 100, 2).reset_index().rename(
        columns={'index': 'User_Name', 'User': 'Percent'})

    return X,per_df


def most_frequent_word(selected_user,df):
    f = open("hinghlish.txt")
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != ' <Media omitted>\n']

    words = []

    for i in temp['Message']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def create_wordcloud(selected_user,df):
    f = open("hinghlish.txt")
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != ' <Media omitted>\n']

    def remove_sw(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return "".join(word)

    we = WordCloud(background_color='white',
                   height=600,
                   width=600)
    temp['Message'] = temp['Message'].apply(remove_sw)
    df_wc = we.generate(temp['Message'].str.cat(sep=" "))
    return df_wc


# emoji analysis
def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['User']==selected_user]

    emojis = []

    for message in df['Message']:
        for i in message.split():
            if len(emoji.distinct_emoji_list(i)) > 0:
                emojis.append(emoji.distinct_emoji_list(i))

    list_of_emjoi = []
    for i in emojis:
        for j in i:
            list_of_emjoi.append(j)

    emoji_df = pd.DataFrame(Counter(list_of_emjoi).most_common(len(Counter(list_of_emjoi))))

    return emoji_df

# time line
def timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    df['Month_Number'] = df['date'].dt.month
    timeline = df.groupby(['Year', 'Month_Number', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + " " + str(timeline['Year'][i]))
    timeline['time'] = time

    return timeline

#daily timeline
def dailytime(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    dailytime_df = df.groupby(['date']).count()['Message'].reset_index()
    return dailytime_df

# week activity map
def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    new_df=df['day_name'].value_counts().reset_index()
    return new_df

def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    new_df=df['Month'].value_counts().reset_index()
    return new_df

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    p = df.pivot_table(index='day_name', columns='btw_time', values='Message', aggfunc='count').fillna(0)
    return p












