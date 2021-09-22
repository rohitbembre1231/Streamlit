import streamlit as st
import requests
from datetime import datetime,timedelta
import pandas as pd

from twilio.rest import Client


API_KEY="36a0960427856b0d7ffd43f178228430"


url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}'


# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url.format(city, API_KEY))
    if result:
        json = result.json()
        # st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp, 1), round(temp_feels, 1),
               humid, lon, lat, icon, des]
        return res, json
    else:
        print("error in search !")


# Function for HISTORICAL DATA
def get_hist_data(lat, lon, start):
    res = requests.get(url_1.format(lat, lon, start, API_KEY))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
    return data, temp




# Let's write the Application

st.set_page_config(layout="centered")
st.title("❍❍❖📅WEATHER FORECASTER🌥️❖❍❍")
st.subheader("𝐌𝐚𝐝𝐞 𝐁𝐲 𝐋𝐮𝐛𝐧𝐚, 𝐑𝐨𝐡𝐢𝐭 & 𝐊𝐨𝐦𝐚𝐥 😊")


image0 = 'Weather.jpg'
st.image(image0, use_column_width=True)

st.header("🌐 𝐄𝐧𝐭𝐞𝐫 𝐓𝐡𝐞 𝐍𝐚𝐦𝐞 𝐎𝐟 𝐘𝐨𝐮𝐫 𝐂𝐢𝐭𝐲 ")
col1, col2 = st.columns(2)

with col1:

    city_name = st.text_input("𝐄𝐧𝐭𝐞𝐫 𝐓𝐡𝐞 𝐍𝐚𝐦𝐞 𝐎𝐟 𝐘𝐨𝐮𝐫 𝐂𝐢𝐭𝐲")



with col2:
    if city_name:
        res, json = getweather(city_name)
        # st.write(res)
        st.success(f" 🌡️ Temperature: " + str(round(res[1], 2))+"°C")
        st.info('Feels Like: ' + str(round(res[2], 2)))
        st.info('Humidity: ' + str(round(res[3],2)))
        st.subheader('Status: ' + res[7])
        web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
        st.markdown(web_str)

if city_name:
    show_hist = st.expander(label='Last 5 Days History')
    with show_hist:
        start_date_string = st.date_input('Current Date')
        # start_date_string = str('2021-06-26')
        date_df = []
        max_temp_df = []
        for i in range(5):
            date_Str = start_date_string - timedelta(i)
            start_date = datetime.strptime(str(date_Str), "%Y-%m-%d")
            timestamp_1 = datetime.timestamp(start_date)
            # res , json = getweather(city_name)
            his, temp = get_hist_data(res[5], res[4], int(timestamp_1))
            date_df.append(date_Str)
            max_temp_df.append(max(temp) - 273.5)

        df = pd.DataFrame()
        df['Date'] = date_df
        df['Max temp'] = max_temp_df
        st.table(df)

    st.map(pd.DataFrame({'lat': [res[5]], 'lon': [res[4]]}, columns=['lat', 'lon']))

                                           ####   REMINDER   #####

OWN_endpoint="https://api.openweathermap.org/data/2.5/onecall"
api_key= "36a0960427856b0d7ffd43f178228430"

account_sid = "ACbe589631e1e0ab7506292e3bebe9d183"
auth_token = "b299d3634c62f06f649a755714eb9d20"

weather_params={
    "lat":18.919226,
    "lon":73.327721,
    "appid":api_key,
    "exclude":"current,minutely,daily"
}

response=requests.get(OWN_endpoint, params=weather_params)
response.raise_for_status()
weather_data=response.json()
weather_slice=weather_data["hourly"][:12]

will_rain=False

for hour_data in weather_slice:
    condition_code= hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain=True


if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="The Dark Clouds⛈️Are Sourrounded In Your City....It's Going To Rain Today. Remember To Bring Your Umbrella☂️...Thank You😊",
        from_='+18572147479',
        to='+917066668543'
    )
    print(message.status)