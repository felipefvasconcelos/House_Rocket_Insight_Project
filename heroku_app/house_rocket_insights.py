# ------------------------------------------
#Libraries
# ------------------------------------------
import pandas as pd
import folium
import streamlit as st
import geopandas
import plotly.express as px

from geopy.distance import great_circle
from folium.plugins import MarkerCluster
from datetime import datetime
from streamlit_folium import folium_static

# ------------------------------------------
# settings
# ------------------------------------------
st.set_page_config(layout='wide')
# ------------------------------------------
# Helper Functions
# ------------------------------------------
st.cache( allow_output_mutation=True )
def get_data( path ):
    data = pd.read_csv( path )
    return data

@st.cache( allow_output_mutation=True )
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile

def data_clean(data):
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    data.drop_duplicates(subset="id", keep='last', inplace=True)
    data = data[(data['bedrooms'] != 0) & (data['bedrooms'] != 11) & (data['bedrooms'] != 33)]
    return data

def house_recommendation(data):
    decision_df = data[['id', 'zipcode', 'date', 'condition', 'grade', 'price']].copy()
    zc_median_price = decision_df[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    decision_df = pd.merge(decision_df, zc_median_price, on='zipcode', how='inner').rename(columns={'price_x': 'buying_price', 'price_y': 'median_price'})
    decision_df['buying_price'] = decision_df['buying_price'].astype('float64')
    decision_df['recommendation'] = decision_df[['condition', 'buying_price', 'median_price']].apply(lambda x:'buy' if (x['condition'] >= 3) & (x['buying_price'] < x['median_price']) else
                                                                                                              'no_buy', axis=1)
    return decision_df

def filter_decision(decision_df):
    st.title('House Rocket Insights - Dashboard')
    st.header('Data Overview - Purchase Recommendation')
    f_recommendation = st.checkbox('Show only houses recommended to buy')
    c1, c2, c3 = st.columns((4, 1, 4))
    with c1:
        f_zipcode = st.multiselect('Enter zipcodes', decision_df['zipcode'].sort_values().unique())
        f_condition = st.multiselect('Enter condition', decision_df['condition'].sort_values().unique())
    with c3:
        min_date = datetime.strptime(decision_df['date'].min(), '%Y-%m-%d')
        max_date = datetime.strptime(decision_df['date'].max(), '%Y-%m-%d')
        f_date = st.slider('Select date', min_date, max_date, max_date)
        f_buying_price = st.slider('Select maximum price',
                                   int(decision_df['buying_price'].min()),
                                   int(decision_df['buying_price'].max()),
                                   value=int(decision_df['buying_price'].max()))
    if f_recommendation:
        f_decision1 = decision_df[decision_df['recommendation'] == 'buy']
    else:
        f_decision1 = decision_df.copy()
    f_decision1['date'] = pd.to_datetime(f_decision1['date'])
    f_decision2 = f_decision1[(f_decision1['date'] <= f_date) & (f_decision1['buying_price'] <= f_buying_price)]
    if (f_zipcode != []) & (f_condition != []):
        f_decision3 = f_decision2.loc[(f_decision2['zipcode'].isin(f_zipcode)) & (f_decision2['condition'].isin(f_condition)), :]
    elif (f_zipcode != []) & (f_condition == []):
        f_decision3 = f_decision2.loc[f_decision2['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == []) & (f_condition != []):
        f_decision3 = f_decision2.loc[f_decision2['condition'].isin(f_condition), :]
    else:
        f_decision3 = f_decision2.copy()
    st.write(f_decision3)
    return None

def profit_expectation(decision_df):
    season_df = decision_df[decision_df['recommendation'] == 'buy'].copy()
    season_df['month'] = pd.to_datetime(season_df['date']).dt.month
    season_df['season'] = season_df['month'].apply(lambda x: 'spring' if (x >= 3) & (x < 6) else
                                                             'summer' if (x >= 6) & (x < 9) else
                                                             'fall' if (x >= 9) & (x < 12) else
                                                             'winter')
    median_season_df = season_df[['buying_price', 'zipcode', 'season']].groupby(['season', 'zipcode']).median().sort_values(by='zipcode').reset_index()
    # Create columns for median price of each season
    median_season_df = median_season_df.pivot(index='zipcode', columns='season', values='buying_price').reset_index()
    median_season_df.columns = ['zipcode', 'fall_median', 'spring_median', 'summer_median', 'winter_median']
    # merging data to suggest price for sale
    dataset = pd.merge(season_df, median_season_df, on='zipcode', how='inner')
    dataset = dataset[['id', 'date', 'zipcode', 'buying_price', 'median_price', 'season', 'fall_median', 'spring_median','summer_median', 'winter_median']].copy()
    # add column with suggest sale price
    dataset['fall_selling_price'] = dataset[['buying_price', 'fall_median']].apply(lambda x: x['buying_price'] * 1.3 if x['buying_price'] <= x['fall_median'] else
                                                                                             x['buying_price'] * 1.1, axis=1)
    dataset['spring_selling_price'] = dataset[['buying_price', 'spring_median']].apply(lambda x: x['buying_price'] * 1.3 if x['buying_price'] <= x['spring_median'] else
                                                                                                 x['buying_price'] * 1.1, axis=1)
    dataset['summer_selling_price'] = dataset[['buying_price', 'summer_median']].apply(lambda x: x['buying_price'] * 1.3 if x['buying_price'] <= x['summer_median'] else
                                                                                                 x['buying_price'] * 1.1, axis=1)
    dataset['winter_selling_price'] = dataset[['buying_price', 'winter_median']].apply(lambda x: x['buying_price'] * 1.3 if x['buying_price'] <= x['winter_median'] else
                                                                                                 x['buying_price'] * 1.1, axis=1)
    # Add columns with min and max selling_price
    dataset['min_selling_price'] = dataset[['fall_selling_price', 'spring_selling_price', 'summer_selling_price', 'winter_selling_price']].min(axis=1)
    dataset['max_selling_price'] = dataset[['fall_selling_price', 'spring_selling_price', 'summer_selling_price', 'winter_selling_price']].max(axis=1)
    # Creating column with recommended season for selling (make sure to cover all possibilities)
    dataset['sell_at'] = dataset[['fall_selling_price', 'spring_selling_price', 'summer_selling_price', 'winter_selling_price', 'max_selling_price']].apply(lambda x:
                                     'fall' if (x['max_selling_price'] == x['fall_selling_price']) &
                                               (x['max_selling_price'] != x['spring_selling_price']) &
                                               (x['max_selling_price'] != x['summer_selling_price']) &
                                               (x['max_selling_price'] != x['winter_selling_price']) else
                                     'summer' if (x['max_selling_price'] == x['summer_selling_price']) &
                                                 (x['max_selling_price'] != x['spring_selling_price']) &
                                                 (x['max_selling_price'] != x['fall_selling_price']) &
                                                 (x['max_selling_price'] != x['winter_selling_price']) else
                                     'spring' if (x['max_selling_price'] == x['spring_selling_price']) &
                                                 (x['max_selling_price'] != x['fall_selling_price']) &
                                                 (x['max_selling_price'] != x['summer_selling_price']) &
                                                 (x['max_selling_price'] != x['winter_selling_price']) else
                                     'winter' if (x['max_selling_price'] == x['winter_selling_price']) &
                                                 (x['max_selling_price'] != x['spring_selling_price']) &
                                                 (x['max_selling_price'] != x['summer_selling_price']) &
                                                 (x['max_selling_price'] != x['fall_selling_price']) else
                                     'fall_or_summer' if (x['max_selling_price'] == x['fall_selling_price']) &
                                                         (x['max_selling_price'] == x['summer_selling_price']) &
                                                         (x['max_selling_price'] != x['winter_selling_price']) &
                                                         (x['max_selling_price'] != x['spring_selling_price']) else
                                     'fall_or_spring' if (x['max_selling_price'] == x['fall_selling_price']) &
                                                         (x['max_selling_price'] == x['spring_selling_price']) &
                                                         (x['max_selling_price'] != x['winter_selling_price']) &
                                                         (x['max_selling_price'] != x['summer_selling_price']) else
                                     'fall_or_winter' if (x['max_selling_price'] == x['fall_selling_price']) &
                                                         (x['max_selling_price'] == x['winter_selling_price']) &
                                                         (x['max_selling_price'] != x['spring_selling_price']) &
                                                         (x['max_selling_price'] != x['summer_selling_price']) else
                                     'summer_or_spring' if (x['max_selling_price'] == x['summer_selling_price']) &
                                                           (x['max_selling_price'] == x['spring_selling_price']) &
                                                           (x['max_selling_price'] != x['fall_selling_price']) &
                                                           (x['max_selling_price'] != x['winter_selling_price']) else
                                     'summer_or_winter' if (x['max_selling_price'] == x['summer_selling_price']) &
                                                           (x['max_selling_price'] == x['winter_selling_price']) &
                                                           (x['max_selling_price'] != x['fall_selling_price']) &
                                                           (x['max_selling_price'] != x['spring_selling_price']) else
                                     'spring_or_winter' if (x['max_selling_price'] == x['spring_selling_price']) &
                                                           (x['max_selling_price'] == x['winter_selling_price']) &
                                                           (x['max_selling_price'] != x['fall_selling_price']) &
                                                           (x['max_selling_price'] != x['summer_selling_price']) else
                                     'fall_or_summer_or_spring' if (x['max_selling_price'] == x['fall_selling_price']) &
                                                                   (x['max_selling_price'] == x['summer_selling_price']) &
                                                                   (x['max_selling_price'] == x['spring_selling_price']) &
                                                                   (x['max_selling_price'] != x['winter_selling_price']) else
                                     'fall_or_summer_or_winter' if (x['max_selling_price'] == x['fall_selling_price']) &
                                                                   (x['max_selling_price'] == x['summer_selling_price']) &
                                                                   (x['max_selling_price'] == x['winter_selling_price']) &
                                                                   (x['max_selling_price'] != x['spring_selling_price']) else
                                     'fall_or_spring_or_winter' if (x['max_selling_price'] == x['fall_selling_price']) &
                                                                   (x['max_selling_price'] == x['spring_selling_price']) &
                                                                   (x['max_selling_price'] == x['winter_selling_price']) &
                                                                   (x['max_selling_price'] != x['summer_selling_price']) else
                                     'summer_or_spring_or_winter' if (x['max_selling_price'] == x['summer_selling_price']) &
                                                                     (x['max_selling_price'] == x['spring_selling_price']) &
                                                                     (x['max_selling_price'] == x['winter_selling_price']) &
                                                                     (x['max_selling_price'] != x['fall_selling_price']) else
                                     'any_season', axis=1)
    # add column with expected profit
    dataset['max_profit'] = dataset[['buying_price', 'max_selling_price']].apply(lambda x: x['max_selling_price'] - x['buying_price'], axis=1)
    dataset['min_profit'] = dataset[['buying_price', 'min_selling_price']].apply(lambda x: x['min_selling_price'] - x['buying_price'], axis=1)
    # summarizing data
    summ_dataset = dataset[['id', 'zipcode', 'buying_price', 'min_selling_price', 'max_selling_price', 'min_profit', 'max_profit', 'sell_at']].copy()
    return summ_dataset

def profit_expectation_table(summ_dataset):
    # NEW SESSION -> SELLING DETAILS
    st.header('Selling Details')
    # Filters
    c1, c2, c3 = st.columns((4, 1, 4))
    with c1:
        f_id = st.multiselect('Enter house ID', summ_dataset['id'].sort_values().unique())
        f_zipcode2 = st.multiselect('Enter desired zipcodes', summ_dataset['zipcode'].sort_values().unique())
        f_sell_at = st.multiselect('Enter season you want to sell', summ_dataset['sell_at'].sort_values().unique())
    with c3:
        f_buying_price2 = st.slider('Select maximum buying price',
                                    int(summ_dataset['buying_price'].min()),
                                    int(summ_dataset['buying_price'].max()),
                                    value=int(summ_dataset['buying_price'].max()))
        f_max_profit = st.slider('Select maximum profit expected',
                                 int(summ_dataset['max_profit'].min()),
                                 int(summ_dataset['max_profit'].max()),
                                 value=int(summ_dataset['max_profit'].max()))
    # Applying filtres
    summ_dataset2 = summ_dataset[(summ_dataset['max_profit'] <= f_max_profit) & (summ_dataset['buying_price'] <= f_buying_price2)]
    def data_filter(id, zip, sell):
        #     Os parâmetros da função são os valores digitados nos campos do form.
        #     Os 3 ifs verificam se os campos foram preenchidos, caso algum campo
        #     do formulário não tenha sido preenchido essa verificação atribui a
        #     esses campos a respectiva coluna no dataframe original assim o filtro
        #     "ignorará" esse campo na busca considerando apenas os que foram
        #     preenchidos. A função retorna um dataframe menor com os dados filtrados.
        if (id == []):
            id = summ_dataset2['id']
        if (zip == []):
            zip = summ_dataset2['zipcode']
        if (sell == []):
            sell = summ_dataset2['sell_at']
        summ_dataset3 = summ_dataset2.loc[(summ_dataset2['id'].isin(id)) & (summ_dataset2['zipcode'].isin(zip)) & (summ_dataset2['sell_at'].isin(sell)), :]
        return summ_dataset3
    summ_dataset3 = data_filter(f_id, f_zipcode2, f_sell_at)
    st.write(summ_dataset3)
    return summ_dataset3

def visual_attributes(data, summ_dataset3, geofile):
    coordinates = data[['id', 'lat', 'long']].copy()
    coordinates['query'] = coordinates[['lat', 'long']].apply(lambda x: str(x['lat']) + ',' + str(x['long']), axis=1)
    lake_tuple = 47.640883, -122.259250
    coordinates['distance_lake'] = coordinates['query'].apply(lambda x: great_circle(lake_tuple, x).km)
    coo_dataset = pd.merge(summ_dataset3, coordinates, on='id', how='inner')
    df_map = coo_dataset
    # density qty map
    density_map = folium.Map(location=[coo_dataset['lat'].mean(), coo_dataset['long'].mean()], default_zoom_start=15)
    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df_map.iterrows():
        folium.Marker(
            [row['lat'],
             row['long']],
            popup='House id: {0}. \n Buy for ${1} \n Sell for: ${2} \n Sell at {3}'.format(
                row['id'],
                row['buying_price'],
                row['max_selling_price'],
                row['sell_at']
            )
        ).add_to(marker_cluster)
    geofile = geofile[geofile['ZIP'].isin(data['zipcode'].tolist())]
    folium.features.Choropleth(data=df_map,
                               geo_data=geofile,
                               columns=['zipcode', 'max_profit'],
                               key_on='feature.properties.ZIP',
                               fill_color='YlOrRd',
                               fill_opacity=0.7,
                               line_opacity=0.2,
                               legend_name='Expected Profit').add_to(density_map)
    c1, c2, c3 = st.columns((5, 1, 5))
    c1.subheader('Most Profitable Houses Filtered')
    c3.subheader('Density Map with Most Profitable Houses')
    profit_chart = summ_dataset3[['id', 'max_profit']].reset_index().sort_values(by='max_profit', ascending=False)
    profit_chart['id'] = profit_chart['id'].apply(str)
    profit_chart = profit_chart.head(10)
    profit_plot = px.bar(profit_chart, x='id', y='max_profit', height=600)
    profit_plot.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    profit_plot.update_layout(margin_autoexpand=False)
    c1.plotly_chart(profit_plot, use_container_width=True)
    with c3:
        folium_static(density_map)
    return None

if __name__ == "__main__":
    #ETL
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    #Load data
    data = get_data(path)
    geofile = get_geofile(url)

    #Trasform Data
    data = data_clean(data)
    decision_df = house_recommendation(data)
    filter_decision(decision_df)
    summ_dataset = profit_expectation(decision_df)
    summ_dataset3 = profit_expectation_table(summ_dataset)
    visual_attributes(data, summ_dataset3, geofile)




