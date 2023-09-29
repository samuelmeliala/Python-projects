import os
import telebot
import requests, json
from pytube import YouTube

api = '6410053635:AAFG-nGiRsQkg9sjbbJJXn1uQbnz_IE2c2w'
api_weather = "70c107c2d7ec5f0e088519364895d5ba"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def greet(message):
    spill = ('''
            Welcome to Sugeng 08 Bot!
             
            Weather Service:
            /weather [city name] to see the weather at the city.
            
            Download Video:
            /ytdownload [YouTube Link] to download a YouTube video from link provided
             ''')
    bot.reply_to(message, spill)
    
@bot.message_handler(commands=['weather'])
def weather(message):
    text = message.text
    city_name = text[8:]
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_weather,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    
    if weather_data["cod"] == 200:
        main = weather_data["main"]
        weather = weather_data["weather"][0]
        
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        
        response_message = f"Weather in{city_name}:\n" \
                            f"Temperature: {temperature}°C\n" \
                            f"Pressure: {pressure} hPa\n" \
                            f"Humidity: {humidity}%\n" \
                            f"Description: {description.capitalize()}"
    else:
        response_message = "City not found or an error occured."
    
    bot.reply_to(message, response_message)
    
@bot.message_handler(commands=['ytdownload'])
def download_video(message):
    text = message.text
    youtube_link = text[10:]  # Extract the YouTube link from the command

    try:
        yt = YouTube(youtube_link)
        video_stream = yt.streams.get_highest_resolution()  # You can choose other streams if needed
        video_stream.download()

        # Send the downloaded video to the user
        video_file = yt.title + ".mp4"
        bot.send_video(message.chat.id, open(video_file, 'rb'))

        # Clean up the downloaded file
        os.remove(video_file)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

print('bot running')    
bot.polling()
