import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('35__welcome_survey_cleaned.csv', sep=";")

st.title('Ankieta powitalna')

def draw_pie_chart(names, values, title):
    fig = px.pie(names=names, values=values, title=title)
    fig.update_layout(title=dict(x=0.4, xanchor='center'))
    st.plotly_chart(fig)

def sort_column_values(category_name, category, xlabel, title):
    category_name = category.value_counts().reset_index()
    if len(category_name) > 0:
        category_name.columns = [xlabel, 'Count']
        category_name = category_name.sort_values(by='Count', ascending=False)
        draw_pie_chart(category_name[xlabel], category_name['Count'], title)
    else:
        st.error('Nie znaleziono rekordów spełniających podane filtry')
        
    
def sort_sum_columns_values(sums_columns_name, sums_columns_array, xlabel, title):
    sums_columns_name = sums_columns_array.sum().sort_values(ascending=False).reset_index()
    sums_columns_name.columns = ['Name', 'Count']
    if sums_columns_name['Count'].sum() > 0:
        draw_pie_chart(xlabel, sums_columns_name['Count'], title)
    else:
        st.error('Nie znaleziono rekordów spełniających podane filtry')  
    

with st.sidebar:
    gender_filter = st.radio('Wybierz płeć', ['Wszyscy', 'Kobiety', 'Mężczyźni'], index=None)
    age_filter = st.multiselect('Wybierz przedział wiekowy', df['age'].unique(), placeholder='Wybierz jedną lub więcej opcji')
    industry_filter = st.multiselect('Wybierz branżę', df['industry'].dropna().sort_values().unique(), placeholder='Wybierz jedną lub więcej opcji')
    edu_level_filter = st.multiselect('Wybierz poziom wykształcenia', df['edu_level'].unique(), placeholder='Wybierz jedną lub więcej opcji')


if gender_filter == 'Kobiety':
    df = df[df['gender'] == 1]
elif gender_filter == 'Mężczyźni':
    df = df[df['gender'] == 0]

if age_filter:
    df = df[df['age'].isin(age_filter)]

if edu_level_filter:
    df = df[df['edu_level'].isin(edu_level_filter)]

if industry_filter:
    df = df[df['industry'].isin(industry_filter)]

if len(df) == 0:
    st.error("Nie znaleziono rekordów spełniających podane filtry")
else:
    c0, c1, c2 = st.columns(3)
    with c0:
        st.metric('Liczba ankietowanych', len(df))

    with c1:
        st.metric('Liczba kobiet', len(df[df['gender'] == 1]))

    with c2:
        st.metric('Liczba mężczyzn', len(df[df['gender'] == 0]))


    st.header('Losowe wiersze')
    value_main = min(10, len(df))
    number_rows_main = st.number_input('Wybierz liczbę losowych wierszy do pokazania', min_value=0, max_value=len(df), value=value_main, step=1, label_visibility="visible")

    if number_rows_main == 1:
        st.subheader(f'{number_rows_main} losowy wiersz')
    elif (1 < number_rows_main < 5):
        st.subheader(f'{number_rows_main} losowe wiersze')
    elif number_rows_main >= 5 or number_rows_main == 0:
        st.subheader(f'{number_rows_main} losowych wierszy')

    st.dataframe(
        df.sample(number_rows_main),
        use_container_width=True,
        hide_index=True
    )


    st.header('Wiek ankietowanych')
    df_age = df['age'].map({
        '<18': ' <18',
        '18-24': '18-24',
        '25-34': '25-34',
        '35-44': '35-44',
        '45-54': '45-54',
        '55-64': '55-64',
        '>=65': '>=65'
    })
    df_age_sorted = df_age.sort_values()
    fig=px.histogram(df_age_sorted, x='age', nbins=30, title='Rozkład wieku ankietowanych')
    fig.update_layout(xaxis_title='Wiek', yaxis_title='Częstość', title=dict(x=0.55, y=0.85, xanchor='center'))
    st.plotly_chart(fig)


    st.header('Branża')
    st.subheader('Liczność poszczególnych branż')
    df_industry = df['industry'].value_counts().reset_index()
    df_industry.columns = ['Branża', 'Liczebność']
    df_industry = df_industry.sort_values(by='Liczebność', ascending=False)
    fig = px.bar(df_industry, x='Branża', y='Liczebność', title='Liczba pracowników w poszczególnych branżach')
    fig.update_layout(title=dict(x=0.55, y=0.85, xanchor='center'))
    st.plotly_chart(fig)

    df_industry['Udział procentowy'] = ((df_industry['Liczebność'] / df_industry['Liczebność'].sum()) * 100).round(2)
    st.subheader('Najbardziej popularne branże')
    value_industry = min(5, len(df_industry))
    number_rows_industry = st.number_input('Wybierz liczbę najbardziej popularnych branż do pokazania', min_value=0, max_value=len(df), value=value_industry, step=1, label_visibility="visible")

    st.dataframe(
        df_industry.head(number_rows_industry),
        use_container_width=True,
        hide_index=True
    )


    st.header('Poziom wykształcenia')
    sort_column_values('df_edu_level', df['edu_level'], 'Level', 'Udział procentowy poszczególnych poziomów wykształcenia')

    st.header('Doświadczenie zawodowe')
    sort_column_values('df_experience', df['years_of_experience'], 'Time', 'Udział procentowy poszczególnych okresów')


    st.header('Motywacja')
    motivation_columns = ['motivation_career', 'motivation_challenges', 'motivation_creativity_and_innovation', 'motivation_money_and_job', 'motivation_personal_growth', 'motivation_remote']
    motivation_labels = ['Rozwój osobisty', 'Wyzwania', 'Zarobki i zatrudnienie', 'Kariera', 'Rozwój kreatywności', 'Praca zdalna']
    sort_sum_columns_values('df_motivation_sums', df[motivation_columns], motivation_labels, 'Udział poszczególnych źródeł motywacji')


    st.header('Preferowane metody nauki')
    learning_pref_columns = ['learning_pref_books', 'learning_pref_chatgpt', 'learning_pref_offline_courses', 'learning_pref_online_courses', 'learning_pref_personal_projects', 'learning_pref_teaching', 'learning_pref_teamwork', 'learning_pref_workshops']
    learning_pref_labels = ['Kursy online', 'Projekty indywidualne', 'Książki', 'Warsztaty', 'Praca w zespole', 'Kursy offline', 'Czat GPT', 'Nauczenia innych']
    sort_sum_columns_values('df_learning_pref_sums', df[learning_pref_columns], learning_pref_labels, 'Udział poszczególnych metod nauki')


    st.header('Hobby')
    hobbies_columns = ['hobby_art', 'hobby_books', 'hobby_movies', 'hobby_other', 'hobby_sport', 'hobby_video_games']
    hobbies_labels = ['Filmy', 'Książki', 'Sport', 'Inne', 'Gry wideo', 'Artystyczne']
    sort_sum_columns_values('df_hobbies_sums', df[hobbies_columns], hobbies_labels, 'Udział procentowy poszczególnych hobby')


    st.header('Ulubione zwierzę')
    sort_column_values('df_fav_animals', df['fav_animals'], 'Animal', 'Udział procentowy poszczególnych zwierząt')


    st.header('Ulubione miejsce wypoczynku')
    sort_column_values('df_fav_place', df['fav_place'], 'Place', 'Udział procentowy poszczególnych miejsc')


    st.header('Ulubiony smak')
    sort_column_values('df_fav_taste', df['sweet_or_salty'], 'Taste', 'Udział procentowy poszczególnych smaków')