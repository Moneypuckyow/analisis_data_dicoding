import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

# Set page configuration to widen the layout
st.set_page_config(
    page_title="Bike Rental",
    layout="wide"
)

df = pd.read_csv('day.csv')
df['dteday'] = pd.to_datetime(df['dteday'])
df['hari'] = df['dteday'].dt.day_name()
df['bulan'] = df['dteday'].dt.month_name()
# Mapping code season ke nama musim
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season'] = df['season'].map(season_mapping)

# Mengembalikan nilai temperature ke Celcius
df['temp'] = df['temp']*40

def create_result_avg_day_df(df):
    result_avg_day = df.groupby('hari')[['casual','registered','cnt','temp']].mean().reset_index()
    result_avg_day[['casual','registered','cnt','temp']] = result_avg_day[['casual','registered','cnt','temp']].astype(int)
    return result_avg_day

def create_result_avg_month_df(df):
    result_avg_month = df.groupby('bulan')[['casual','registered','cnt','temp']].mean().reset_index()
    result_avg_month[['casual','registered','cnt','temp']] = result_avg_month[['casual','registered','cnt','temp']].astype(int)
    return result_avg_month

def create_result_avg_season_df(df):
    result_avg_season = df.groupby('season')[['casual','registered','cnt','temp']].mean().reset_index()
    result_avg_season[['casual','registered','cnt','temp']] = result_avg_season[['casual','registered','cnt','temp']].astype(int)
    return result_avg_season

def create_total_rental(df):
    total_rental = df['cnt'].sum()
    return total_rental

def create_avg_rental_day(df):
    avg_rental = int(df['cnt'].mean())
    return avg_rental

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

default_options = ['Summer', 'Winter', 'Fall', 'Spring']
    
options = st.multiselect(
    'Filter Musim',
    ['Summer', 'Winter', 'Fall', 'Spring'],
    default_options
    # ['Fall', 'Spring','Summer','Winter']
    )

options = options if options else default_options

main_df = df[((df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))) &
                (df["season"].isin(options))]

result_avg_day_df = create_result_avg_day_df(main_df)
result_avg_month_df = create_result_avg_month_df(main_df)
result_avg_season_df = create_result_avg_season_df(main_df)

total_rental = create_total_rental(main_df)
avg_rental_day = create_avg_rental_day(main_df)

st.header('Dicoding Data Analisis Submission :sparkles:')

# Streamlit app
st.title("Streamlit App for Visualization")

col1, col2= st.columns(2)
with col1:
    st.metric("Total rentals", value=total_rental)

with col2:
    st.metric("Average rentals per Days", value=avg_rental_day)

# st.subheader('Test')
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
# Create subplots
fig_1 = make_subplots(rows=1, cols=4, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])

# Add traces
fig_1.add_trace(go.Pie(
    values=result_avg_season_df['casual'],
    name="casual",
    labels=result_avg_season_df['season'],
    domain=dict(x=[0, 0.5]),
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=1)

fig_1.add_trace(go.Pie(
    values=result_avg_season_df['registered'],
    labels=result_avg_season_df['season'],
    domain=dict(x=[0.5, 1.0]),
    name="registered",
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=2)

fig_1.add_trace(go.Pie(
    values=result_avg_season_df['cnt'],
    labels=result_avg_season_df['season'],
    domain=dict(x=[0.5, 1.0]),
    name="count",
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=3)

fig_1.add_trace(go.Pie(
    values=result_avg_season_df['temp'],
    labels=result_avg_season_df['season'],
    domain=dict(x=[0.5, 1.0]),
    name="temperature",
    hole=.3,
    textinfo='label+value',
    textposition='inside'),
    row=1, col=4)



# Update layout
fig_1.update_layout(
    title_text="Persentase Rental Permusim ditiap Segment Consumer",
    annotations=[
        dict(text='Casual', x=0.05, y=0, font_size=20, showarrow=False),
        dict(text='Registered', x=0.29, y=0, font_size=20, showarrow=False),
        dict(text='Count', x=0.63, y=0, font_size=20, showarrow=False),
        dict(text='Temperature C°', x=0.99, y=0, font_size=20, showarrow=False)
    ]
)

fig_1.update_traces(marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))

# fig = make_subplots(rows=1, cols=2)
fig_2 = make_subplots(rows=1, cols=4, specs=[[{"type": "domain"},{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])

fig_2.add_trace(go.Pie(
    values=result_avg_day_df['casual'],
    name="label+casual",
    labels=result_avg_day_df['hari'],
    domain=dict(x=[0, 0.5]),
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=1)

fig_2.add_trace(go.Pie(
    values=result_avg_day_df['registered'],
    labels=result_avg_day_df['hari'],
    domain=dict(x=[0.5, 1.0]),
    name="registered",
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=2)

fig_2.add_trace(go.Pie(
    values=result_avg_day_df['cnt'],
    labels=result_avg_day_df['hari'],
    domain=dict(x=[0.5, 1.0]),
    name="count",
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=3)

fig_2.add_trace(go.Pie(
    values=result_avg_day_df['temp'],
    labels=result_avg_day_df['hari'],
    domain=dict(x=[0.5, 1.0]),
    name="temperature",
    hole=.3,
    textinfo='label+value',
    textposition='inside'),
    row=1, col=4)


fig_2.update_layout(
    title_text="Persentase Rental Perhari ditiap Segment Consumer",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text='Casual', x=0.05, y=0, font_size=20, showarrow=False),
        dict(text='Registered', x=0.29, y=0, font_size=20, showarrow=False),
        dict(text='Count', x=0.63, y=0, font_size=20, showarrow=False),
        dict(text='Temperature C°', x=0.99, y=0, font_size=20, showarrow=False)])

fig_2.update_traces(marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))


# fig = make_subplots(rows=1, cols=2)
fig_3 = make_subplots(rows=1, cols=4, specs=[[{"type": "domain"},{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])

fig_3.add_trace(go.Pie(
    values=result_avg_month_df['casual'],
    name="casual",
    labels=result_avg_month_df['bulan'],
    domain=dict(x=[0, 0.5]),
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=1)

fig_3.add_trace(go.Pie(
    values=result_avg_month_df['registered'],
    labels=result_avg_month_df['bulan'],
    domain=dict(x=[0.5, 1.0]),
    name="registered",
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=2)

fig_3.add_trace(go.Pie(
    values=result_avg_month_df['cnt'],
    labels=result_avg_month_df['bulan'],
    domain=dict(x=[0.5, 1.0]),
    name="count",
    hole=.3,
    textinfo='label+percent',
    textposition='inside'),
    row=1, col=3)

fig_3.add_trace(go.Pie(
    values=result_avg_month_df['temp'],
    labels=result_avg_month_df['bulan'],
    domain=dict(x=[0.5, 1.0]),
    name="temperature",
    hole=.3,
    textinfo='label+value',
    textposition='inside'),
    row=1, col=4)


fig_3.update_layout(
    title_text="Persentase Rental Perbulan ditiap Segment Consumer",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text='Casual', x=0.05, y=0, font_size=20, showarrow=False),
        dict(text='Registered', x=0.29, y=0, font_size=20, showarrow=False),
        dict(text='Count', x=0.63, y=0, font_size=20, showarrow=False),
        dict(text='Temperature C°', x=0.99, y=0, font_size=20, showarrow=False)])

fig_3.update_traces(marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))

st.plotly_chart(fig_1, use_container_width=True)
st.plotly_chart(fig_2, use_container_width=True)
st.plotly_chart(fig_3, use_container_width=True)