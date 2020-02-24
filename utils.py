import discord
import config
import requests

def MakeEmbed(author=None, author_url=None, title=None, description=None, url=None, thumbnail=None,
              doFooter=False,
              color=None):
    if url is not None:
        if color is None:
            embed = discord.Embed(title=title, description=description, url=url, color=config.MAINCOLOR)
        else:
            embed = discord.Embed(title=title, description=description, url=url, color=color)
    else:
        if color is None:
            embed = discord.Embed(title=title, description=description, color=config.MAINCOLOR)
        else:
            embed = discord.Embed(title=title, description=description, color=color)

    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    if author is not None and author_url is not None:
        embed.set_author(name=author, url=author_url)
    if doFooter is True:
        embed.set_footer(text="HHS Discord Bot.", icon_url="https://cdn.discordapp.com/avatars/565353355678056448/b1e4e12a38f39205a7836a23b5a47311.png?size=256")
    return embed

async def get_weather():
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=42.63&lon=-83.98&appid=2aed60299013fab6b2eadc5e70cb92fa&units=imperial'
    res = requests.get(url)

    data = res.json()

    temp = data['main']['temp']
    maxTemp = data['main']['temp_max']
    minTemp = data['main']['temp_min']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['main']
    icon = data['weather'][0]['icon']

    time = " "

    if str(icon) == '01d':
        icon = ':sunny:'
    elif str(icon) == '02d':
        icon = ':partly_sunny:'
    elif str(icon) == '03d':
        icon = ':white_sun_cloud:'
    elif str(icon) == '04d':
        icon = ':cloud:'
    elif str(icon) == '09d':
        icon = ':cloud_rain:'
    elif str(icon) == '10d':
        icon = ':white_sun_rain_cloud:'
    elif str(icon) == '11d':
        icon = ':thunder_cloud_rain:'
    elif str(icon) == '13d':
        icon = ':cloud_snow:'
    elif str(icon) == '50d':
        icon = ':fog:'
    elif str(icon) == '01n':
        icon = ':last_quarter_moon_with_face:'
        time = " Night "
    elif str(icon) == '02n':
        icon = ':last_quarter_moon_with_face:  :cloud:'
        time = " Night "
    elif str(icon) == '10n':
        icon = ':cloud_rain:'
        time = " Night "
    elif str(icon) == '03n':
        icon = ':white_sun_cloud:'
        time = " Night "
    elif str(icon) == '04n':
        icon = ':cloud:'
        time = " Night "
    elif str(icon) == '09n':
        icon = ':cloud_rain:'
        time = " Night "
    elif str(icon) == '11n':
        icon = ':thunder_cloud_rain:'
        time = " Night "
    elif str(icon) == '13n':
        icon = ':cloud_snow:'
        time = " Night "
    elif str(icon) == '50n':
        icon = ':fog:'
        time = " Night "
    if str(description) == "Clear" and icon == ":sunny:":
        description = "Sunny"
    elif str(description) == "Thunderstorm":
        description = "Thunderstorming"
    elif str(description) == "Drizzle":
        description = "Drizzling"
    elif str(description) == "Rain":
        description = "Rainy"
    elif str(description) == "Snow":
        description = "Snowy"
    elif str(description) == "Mist":
        description = "Misty"
    elif str(description) == "Smoke":
        description = "Smoky"
    elif str(description) == "Haze":
        description = "Hazzy"
    elif str(description) == "Dust":
        description = "Dusty"
    elif str(description) == "Fog":
        description = "Foggy"
    elif str(description) == "Sand":
        description = "Sandy"
    elif str(description) == "Ash":
        description = "Ashy"
    elif str(description) == "Squall":
        description = "Squally?"
    elif str(description) == "Tornado":
        description = "Tornadoing"
    elif str(description) == "Clouds":
        description = "Cloudy"

    new_status = "The {}{}Sky".format(description, time)
    return new_status