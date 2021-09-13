import discord
from discord.ext import commands
import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup

from myconstants import zodiacSigns, zodiacAvatars

# Horoscope Alterations
class Outline(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Horoscope function - get daily horoscope from horoscope.com based from zodiac sign
    @commands.command(aliases=['sfu'])
    async def outline(self, ctx, course, section = "D100"):
        course_name = course[0:len(course)-3]
        course_number = course[len(course)-3:]
        
        try:
            source = requests.get(f'http://www.sfu.ca/outlines.html?2021/fall/{course_name}/{course_number}/{section}',timeout=5).text

        except Timeout:
            await ctx.send("Error accessing server data, please try again later")
            
        else:
            soup = BeautifulSoup(source, 'lxml')
            embed_description = ""
            embed_title = course_name[0] + " " + course_number[0] + " - "
            courses_name = soup.find("h2", {"id": "title"}).text
            courses_name = courses_name.split()
            for i in range(0,len(courses_name)):
                embed_title = embed_title + courses_name[i] + " "
            
            time = soup.find("li", {"class": "course-times"}).text
            time = time.split()
            prereq = soup.find("li", {"class": "prereq"}).text
            prereq = prereq.split()
            instructor = soup.find("li", {"class": "instructor"}).text
            instructor = instructor.split()

            for i in range(0, len(time)):
                embed_description = embed_description + time[i] + " "
                if time[i] == "Location:" or time[i] == "Burnaby" or time[i] == "Surrey":
                        embed_description = embed_description + "\n"
            
            embed_description = embed_description + "\n \n"

            for i in range(0, len(prereq)):
                embed_description = embed_description + prereq[i] + " "
            
            embed_description = embed_description + "\n \n"

            for i in range(0, len(instructor)):
                embed_description = embed_description + instructor[i] + " "
            
            
            embed = discord.Embed(title=embed_title,
                              description=embed_description, color=0xa6192e)
            
            
            await ctx.send(embed=embed)


    # If user doesn't provide zodiac sign, or enters to many parametres
    @outline.error
    async def outline_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Error Occured. Make sure the class exists and is offered in the Fall 2021 semester")
        await channel.send(f"{ctx.message.author} experienced a error using outline/sfu. {error}")


def setup(client):
    client.add_cog(Outline(client))
