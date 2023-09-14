import matplotlib.pyplot as plt
import streamlit as st
import helper
import seaborn as sns
import DataPreprocessor

#adding custom css
with open('style.css') as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.sidebar.title("WhatsApp Chat analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df = DataPreprocessor.preprocess(data)

    #fetching data w.r.t Users
    User_list = df['User'].unique().tolist()
    User_list.remove('group_notifications')
    User_list.sort()
    User_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis w.r.t",User_list)

    if st.sidebar.button("Show Analysis"):
        #showing stats
        num_messages,words,num_media_shared,links = helper.fetch_stats(selected_user,df)
        st.title("Top Staticstics")
        col1, col2, col3,col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Shared Media")
            st.title(num_media_shared)

        with col4:
            st.header("Shared Links")
            st.title(links)

    #timeline

        #Monthly time line
        st.title("Monthly Timeline")
        monthly_timeline = helper.monthly_timeline(selected_user,df)
        fig, ax =plt.subplots()
        ax.plot(monthly_timeline['time'], monthly_timeline['message'],color='y')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        #daily activity
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='r')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.title("Weekly activity map")
        activity_heatmap = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        plt.xticks(rotation=75)
        st.pyplot(fig)

    #finding most busy user in the group(grouo_level_analysis)

        if selected_user == 'Overall':
            st.title("Most Busy User")
            x, new_df = helper.most_busy_users(df)
            fig, ax =plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='m')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


    #WordCloud
        st.title("World Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    #most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.title("Most common Words")
        st.pyplot(fig)

    #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        if len(emoji_df) != 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f')
                st.pyplot(fig)
        else:
            st.markdown("<span style='color: red;'>This User not use any Emoji </span>", unsafe_allow_html=True)
