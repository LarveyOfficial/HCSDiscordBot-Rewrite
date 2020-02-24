import config
import discord
from discord.ext import commands
import requests
import utils


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx):
        url = 'http://api.openweathermap.org/data/2.5/weather?lat=42.63&lon=-83.98&appid=2aed60299013fab6b2eadc5e70cb92fa&units=imperial'
        urlMetric = 'http://api.openweathermap.org/data/2.5/weather?lat=42.63&lon=-83.98&appid=2aed60299013fab6b2eadc5e70cb92fa&units=metric'
        res = requests.get(url)
        resMetric = requests.get(urlMetric)

        data = res.json()
        dataMetric = resMetric.json()

        temp = data['main']['temp']
        tempMetric = dataMetric['main']['temp']
        maxTemp = data['main']['temp_max']
        maxTempMetric = dataMetric['main']['temp_max']
        minTemp = data['main']['temp_min']
        minTempMetric = dataMetric['main']['temp_min']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['main']
        icon = data['weather'][0]['icon']

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
            icon = ':last_quarter_moon_with_face: '
        elif str(icon) == '02n':
            icon = ':last_quarter_moon_with_face:  :cloud:'
        elif str(icon) == '10n':
            icon = ':cloud_rain:'
        elif str(icon) == '03n':
            icon = ':white_sun_cloud:'
        elif str(icon) == '04n':
            icon = ':cloud:'
        elif str(icon) == '09n':
            icon = ':cloud_rain:'
        elif str(icon) == '11n':
            icon = ':thunder_cloud_rain:'
        elif str(icon) == '13n':
            icon = ':cloud_snow:'
        elif str(icon) == '50n':
            icon = ':fog:'
        if str(description) == "Clear" and icon == ":sunny:":
            description = "Sunny"
        embed = utils.MakeEmbed(title="The Weather",
                                description='The weather in Hartland, MI is: \n**Description**: {} {} \n**Temperature**: {}°F / {}°C \n**Max Temperature**: {}°F / {}°C \n**Low Temperature**: {}°F / {}°C \n**Wind Speed**: {}mph'.format(
                                    description, icon, temp, tempMetric, maxTemp, maxTempMetric, minTemp, minTempMetric,
                                    wind_speed), doFooter=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(weather(bot))
