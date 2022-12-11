import helper
import streamlit as st
import  Preprocess
import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud

st.sidebar.title("WhatsApp Chat Analyzer ")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")



    # displaying dataframe
    df = Preprocess.preprocessing(data)

    # fetching number of user
    user_list = df['User'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis Wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        total_msg,total_word,total_shared = helper.fetch_stat(selected_user,df)
        st.title("Top Statistics")
        c1,c2,c3,c4=st.columns(4)

        with c1:
            st.header("Total Messages ")
            st.title(total_msg)

        with c2 :
            st.header("Total Words ")
            st.title(total_word)

        with c3:
            st.header("Media Shared ")
            st.title(total_shared)

        with c4:
            st.header("Linked Shared")

    # showing monthly timeline
    st.title("Monthly TimeLine ")
    timeline = helper.timeline(selected_user,df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['Message'],color ='pink')
    plt.xlabel("month with year")
    plt.ylabel("number of messages")
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline

    st.title("Daily Timeline")
    daily_df = helper.dailytime(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(daily_df['date'],daily_df['Message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)



    if selected_user == 'Overall':

        st. title("Active Users ")
        X,per_df = helper.fetch_most_busy(df)
        col1,col2 = st.columns(2)

        with col1:
            st.header("Contributor ")
            fig, ax = plt.subplots()
            ax.bar(X.index, X.values,color='violet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Percentage of Each Contributor ")
            st.dataframe(per_df)




    # wordcloud
    st.title("WordCloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most frquent words used in between chat
    most_common_df = helper.most_frequent_word(selected_user, df)
    st.title("Most Frequent Words ")
    fig, ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    # st.dataframe(emoji_df)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)

   # DAY activity map

    st.title("Activity Map")
    col1,col2 =st.columns(2)



    with col1:
        st.header("Daily")
        w_df = helper.week_activity(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(w_df['index'],w_df['day_name'],color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    # Monthly Activity MAp

    with col2:
        m_df = helper.month_activity(selected_user, df)
        st.header("Monthly ")
        fig, ax = plt.subplots()
        ax.bar(m_df['index'], m_df['Month'],color='pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    st.title("Weekly Activity HeatMap")
    pivot = helper.activity_heatmap(selected_user,df)
    fig,ax =plt.subplots()
    ax =sns.heatmap(pivot)
    st.pyplot(fig)








