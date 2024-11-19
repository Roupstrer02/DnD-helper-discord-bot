########################################################################
# Programmer: Roupen Kaloustian
# Project Name: Dungeons & Discord
# Tabletop RPG assistant for discord
########################################################################
import discord
import random
import urllib.request
from bs4 import BeautifulSoup

client = discord.Client()

patronsPresent = []
mode = "Innkeeper"

dev_token = ''		#removed for privacy and security
commands_channel_id = 0 #removed for privacy and security

@client.event
async def on_ready():
    commands_channel = client.get_channel(commands_channel_id)

    await commands_channel.send(
        """Time to roll!
            **!roll** to roll dice (e.g: !roll 2d20 d12)
            **!spell** to lookup a spell description (e.g: !spell eldritch blast)
            **!news** to get the latest news from the different regions around Zelandris (e.g: !news Zanthar)""")

@client.event
async def on_message(message):

    commands_channel = client.get_channel(commands_channel_id)
    command = message.content.split(' ')[0].lower()
    #For rolling dice
    #------------------------------------------------------------------------------------
    # known bugs:
    # can't handle multiple dice throw where one is invalid (partially wrong message)
    if command == '!roll':
        dice = message.content.split(' ')[1:]
        
        rolls = ''
        total = 0
        earlyExit = False
        for roll in dice:
            if roll[0] == 'd':
                num = random.randint(1, int(roll[1:]))
                total += num
                rolls += ((str(num)) + ' ')
            elif (roll[0].isdigit()):
                numberOfDice = int(roll.split('d')[0])
                validRoll = numberOfDice <= 100 and numberOfDice > 0 and roll.split('d')[1].isdigit() and int(roll.split('d')[1]) > 0
                if validRoll:
                    for x in range(0, numberOfDice): 
                        num = random.randint(1, int(roll.split('d')[1]))
                        total += num
                        rolls += ((str(num)) + ', ')  
                else:
                    await commands_channel.send("You may roll between 1 and 100 **physically possible dice** at once, no more please.")
            else:
                await commands_channel.send("You want to roll what now?")
                earlyExit = True
        if earlyExit == False:
            await commands_channel.send(str( 'you rolled: ' + rolls + 'total: ' + str(total)))

    #For finding spells
    #------------------------------------------------------------------------------------
    elif command == '!spell':

        #Getting the spell request
        uf = urllib.request.urlopen("http://dnd5e.wikidot.com/spell:" + ' '.join(message.content.split(' ')[1:]).replace(' ','-'))

        #Writing out the spell description        
        html = uf.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find_all('p')
        spell = ""
        for element in text:
            spell += str(element)
        
        spell = spell.replace('<p>','').replace('</p>','\n').replace('<br/>','').replace('<em>','*').replace('</em>','*').replace('<strong>','**').replace('</strong>','**').replace('<a href=','').replace('</a>','')
        print(spell)
        await commands_channel.send(spell)
        #format:
        #https://roll20.net/compendium/dnd5e/speak%20with%20animals#content


    elif command == "!news":
        nation = message.content.split(' ')[1].upper()
        
        #takes the "news story" from a folder, one for each area
        if nation == "EMBERMOORE":
            with open(r'News\Embermoore.txt', 'r') as f:
                data = f.read()
                data = data.replace('Ã©', 'é')
                await commands_channel.send(data)
        elif nation == "TU'HRA":
            with open(r'News\TuHra.txt', 'r') as f:
                data = f.read()
                data = data.replace('Ã©', 'é')
                await commands_channel.send(data)
        elif nation == "ZANTHAR":
            with open(r'News\Zanthar.txt', 'r') as f:
                data = f.read()
                data = data.replace('Ã©', 'é')
                await commands_channel.send(data)
        elif nation == "ILIASING":
            with open(r'News\Iliasing.txt', 'r') as f:
                data = f.read()
                data = data.replace('Ã©', 'é')
                await commands_channel.send(data)






    #================================================================================================================================================
    # Paused content
    # ================================================================================================================================================

    #For getting a drink from Barkeep
    #------------------------------------------------------------------------------------
    # elif command == '!order':
    #     with open('barkeep.yml') as f:
    #         data = yaml.load(f, Loader=SafeLoader)

    #     #have this as a separate .yml file later
    #     menu = {'worker\'s blend': 0.5, 'ithilian pine blend': 5, 'taste of the tundra': 4, 'gold edition - sun\'s shine premium': 25, 'water': 0.25}

    #     content = message.content.split(' ')[1:]
    #     orderingPatron = content[0]
    #     content.remove(orderingPatron)
    #     orderingPatron = orderingPatron.capitalize()
    #     content = ' '.join(content).upper()
    #     order = []

    #     #builds the order form the message
    #     for drink in list(menu.keys()):
    #         if content.find(drink.upper()) != -1:
    #             order.append(drink)

    #     #logic for number of drinks ordered
    #     if orderingPatron in patronsPresent:
    #         if len(order) > 1:
    #             await commands_channel.send("please just buy one drink... you people are crazy enough as is...")
    #         elif len(order) == 1:
    #             await commands_channel.send("Comin' right up!")
                
    #             with open('barkeep.yml', 'r') as f:
    #                 patronGold = data.get(orderingPatron).get('gold')
    #             if patronGold >= menu.get(order[0]):
    #                 await commands_channel.send("*" + orderingPatron + " pays " + str(menu.get(order[0])) + " gold for the drink" + "*")
    #                 data['patrons'][orderingPatron]['gold'] = patronGold - menu.get(order[0])

    #                 #have to set the open type to write (last time, it just wiped the whole file, I think you can't just put a dictionary in as data)
    #                 with open('barkeep.yml', 'w') as f:
    #                     yaml.dump(data, f)
    #             else:
    #                 await commands_channel.send("Your wallet's looking a little empty there " + orderingPatron + "...")

    #         else:
    #             await commands_channel.send("You want a what?...")
    #     else:
    #         await commands_channel.send("They don't seem to be here right now.")
    # #For checking who's in the tavern
    # #------------------------------------------------------------------------------------
    # elif command == '!patrons':      
        
    #     if len(patronsPresent) == 0:
    #         await commands_channel.send("No one seems to be here just yet...")    
    #     else:

    #         patronString = "We've got a few patrons in here tonight:\n\n"

    #         for patron in patronsPresent:
    #             patronString += "- " + patron + '\n'
            

    #         await commands_channel.send(patronString)
    # #For adding a patron to the tavern
    # #------------------------------------------------------------------------------------
    # elif command == "!sit":
    #     with open(r'C:\Users\Roups\Documents\VSCodeProjects\DiscordBots\barkeep.yml', 'r+') as f:
    #         data = yaml.load(f, Loader=SafeLoader)
    #         patrons = data.keys()

    #         content = ' '.join(message.content.split(' ')[1:]).capitalize()

    #         if len(content) > 0:
    #             if (content in list(patrons)) and (content not in patronsPresent):
    #                 await commands_channel.send("Ah! Welcome back my friend!")
    #                 patronsPresent.append(content)
    #             elif content in patronsPresent:
    #                 await commands_channel.send("Hello!... again?")
    #             else:
    #                 await commands_channel.send("Haven't seen you 'round here, welcome to the tavern!")
    #                 new_patron = {
    #                     content.lower().capitalize(): {
    #                         'gold': 25
    #                         }
    #                     }
    #                 yaml.dump(new_patron, f)
    #                 patronsPresent.append(content)
    # #For removing a patron from the tavern
    # #------------------------------------------------------------------------------------
    # elif command == "!leave":
    #     content = ' '.join(message.content.split(' ')[1:]).capitalize()

    #     if len(content) > 0:
    #         if content in patronsPresent:
    #             await commands_channel.send("Alright, i'll see you around friend!")
    #             patronsPresent.remove(content)
    #             print(patronsPresent)
    #         else:
    #             await commands_channel.send("For a patron to leave, they need to be here in the first place...")    
    #For removing a patron from the tavern
    #------------------------------------------------------------------------------------


    #================================================================================================================================================
    # Removed content
    # ================================================================================================================================================

    # For choosing city
    # ------------------------------------------------------------------------------------
    # elif message.content.split(' ')[0] == '!travel':
        
    #     global city
        
    #     city_display_msg = ''

    #     with open('city.yml') as f:
    #         data = yaml.load(f, Loader=SafeLoader)
        
    #     cities = list(data.keys())

        
    #     if ' '.join(message.content.split(' ')[1:]) in cities:

    #         city = ' '.join(message.content.split(' ')[1:])
            
    #         for entry in data.get(city).keys():
    #             city_display_msg += '\t' + entry + '\n'

    #         await commands_channel.send(city_display_msg)
          
    #     else:
    #         await commands_channel.send('This city does not exist :(')

    #For City Exploration
    #------------------------------------------------------------------------------------
    # elif message.content.split(' ')[0] == '!explore':

    #     message = message.content.split(' ')
    #     district_display_msg = ""
    #     #ERROR CHECKING GOES HERE

    #     with open('players.yml') as f:
    #         #data is saved in the variable as a dictionary: key -> [entry1, entry2, entry3]
    #         data = yaml.load(f, Loader=SafeLoader)

    #     players = []
    #     for player in data.get('players'):
    #         players.append(player)

    #     with open('city.yml') as f:
    #         data = yaml.load(f, Loader=SafeLoader)
            
    #     cities = data

    #     for district in cities.get(city):
    #         if district == ' '.join(message[1:]):
    #             district_display_msg += (city + ': ' + ' '.join(message[1:]) + '\n\n')

    #             for entry in cities.get(city).get(district).get('description'):
    #                 district_display_msg += entry + '\n'

    #             district_display_msg += '\n'

    #             #check if district has shop and/or services
    #             if cities.get(city).get(district).get('shop', None) != None:
    #                 district_display_msg += 'items for sale:\n'
                    
    #                 for entry in cities.get(city).get(district).get('shop', None):
    #                     district_display_msg += '\t' + entry + '\n'
                
    #             district_display_msg += '\n'

    #             if cities.get(city).get(district).get('services', None) != None:
    #                 district_display_msg += 'services available \n'

    #                 for entry in cities.get(city).get(district).get('services', None):
    #                     district_display_msg += '\t' + entry + '\n'

    #     await commands_channel.send(district_display_msg)
    #----------------------------------------------------------------------------------------------
    # elif message.content.split(' ')[0].lower() == "!gamba":
        # content = ' '.join(message.content.split(' ')[1:]).capitalize()

        # if len(content) > 0:
        #     gameover = False
        #     if content[0].lower() == "air":
        #         #plinko machine simulation
        #         print()
        #     elif content[0].lower() == "water":
        #         #pick 3 paths, left middle or right, one of them is the waterfall, lasting longer means more money, there's a buy-in
        #         print()
        #     elif content[0].lower() == "earth":
        #         #still don't know
        #         print()
        #     elif content[0].lower() == "fire":
        #         #blackjack, themed around a small fireball not growing too big and burning you
        #         print()
        # else:
        #     await commands_channel.send(
        #         "*In front of you are four tables, each themed to different primal element*\n" + "Care for a game?\n"+"- Air\n"+"- Water\n"+"- Earth\n"+"- Fire\n"
        #         )    


client.run(dev_token)
