import discord
from discord.ext import commands
import time
import random
import json
import asyncio

# Configure intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix='$', intents=intents)

# Function to load data from a JSON file
def load_data():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save data to a JSON file
def save_data(data):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Command to enter the casino
@bot.command()
async def enter(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    if user_id in data:
        await ctx.send(f"{ctx.author.mention}, you are already registered in the casino!")
    else:
        data[user_id] = {"chips": 0, "last_claim": 0}  # Initial chips
        save_data(data)
        await ctx.send(f"Welcome to the casino, {ctx.author.mention}! You have 0 chips.")

# Command to check chips
@bot.command()
async def chips(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    if user_id not in data:
        await ctx.send(f"{ctx.author.mention}, you are not registered in the casino. Use `$enter` to start.")
    else:
        balance = data[user_id]["chips"]
        await ctx.send(f"{ctx.author.mention}, you have {balance} chips.")

# Command to claim daily reward
@bot.command()
async def reward(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    if user_id not in data:
        await ctx.send(f"{ctx.author.mention}, you are not registered in the casino. Use `$enter` to start.")
        return

    current_time = time.time()
    last_claim = data[user_id].get("last_claim", 0)
    cooldown = 24 * 60 * 60  # 24 hours in seconds

    if current_time - last_claim < cooldown:
        time_remaining = int(cooldown - (current_time - last_claim))
        hours = time_remaining // 3600
        minutes = (time_remaining % 3600) // 60
        await ctx.send(f"⏳ {ctx.author.mention}, you must wait {hours}h {minutes}m before claiming another reward.")
        return

    reward_chips = 500
    data[user_id]["chips"] += reward_chips
    data[user_id]["last_claim"] = current_time
    save_data(data)

    await ctx.send(f"🎉 {ctx.author.mention}, you have claimed {reward_chips} chips! Come back in 24 hours to claim more.")

# Command to play roulette
@bot.command()
async def roulette(ctx, bet: int, bet_type: str, value: str = None):
    user_id = str(ctx.author.id)
    data = load_data()

    # Check if the user is registered
    if user_id not in data:
        await ctx.send(f"{ctx.author.mention}, you are not registered in the casino. Use `$enter` to start.")
        return

    # Check if the user has enough chips for the bet
    if data[user_id]["chips"] < bet:
        await ctx.send(f"{ctx.author.mention}, you don't have enough chips to bet {bet}.")
        return

    # Check that the bet is within the allowed range (1000 to 1000000)
    if bet < 1000 or bet > 1000000:
        await ctx.send(f"{ctx.author.mention}, the bet must be between 1000 and 1000000 chips.")
        return

    # Emote dictionary by number
    # For this to work correctly, you must add the emoticons to the Discord application and replace the IDs.
    emotes = {
        0: "<:greenZero:1313908422336450684>",
        1: "<:redOne:1313908454645305404>",
        2: "<:blackTwo:1313907793757077564>",
        3: "<:redThree:1313908488820359241>",
        4: "<:blackFour:1313907834961920021>",
        5: "<:redFive:1313908521028288597>",
        6: "<:blackSix:1313907904088379452>",
        7: "<:redSeven:1313908553643196496>",
        8: "<:blackEight:1313907963328598036>",
        9: "<:redNine:1313908586082209843>",
        10: "<:blackOne:1313907765789462581><:blackZero:1313908396004606012>",
        11: "<:redOne:1313908454645305404><:redOne:1313908454645305404>",
        12: "<:blackOne:1313907765789462581><:blackTwo:1313907793757077564>",
        13: "<:redOne:1313908454645305404><:redThree:1313908488820359241>",
        14: "<:blackOne:1313907765789462581><:blackFour:1313907834961920021>",
        15: "<:redOne:1313908454645305404><:redFive:1313908521028288597>",
        16: "<:blackOne:1313907765789462581><:blackSix:1313907904088379452>",
        17: "<:redOne:1313908454645305404><:redSeven:1313908553643196496>",
        18: "<:blackOne:1313907765789462581><:blackEight:1313907963328598036>",
        19: "<:redOne:1313908454645305404><:redNine:1313908586082209843>",
        20: "<:blackTwo:1313907793757077564><:blackZero:1313908396004606012>",
        21: "<:redTwo:1313908473498697910><:redOne:1313908454645305404>",
        22: "<:blackTwo:1313907793757077564><:blackTwo:1313907793757077564>",
        23: "<:redTwo:1313908473498697910><:redThree:1313908488820359241>",
        24: "<:blackTwo:1313907793757077564><:blackFour:1313907834961920021>",
        25: "<:redTwo:1313908473498697910><:redFive:1313908521028288597>",
        26: "<:blackTwo:1313907793757077564><:blackSix:1313907904088379452>",
        27: "<:redTwo:1313908473498697910><:redSeven:1313908553643196496>",
        28: "<:blackTwo:1313907793757077564><:blackEight:1313907963328598036>",
        29: "<:redTwo:1313908473498697910><:redNine:1313908586082209843>",
        30: "<:blackThree:1313907816083226735><:blackZero:1313908396004606012>",
        31: "<:redThree:1313908488820359241><:redOne:1313908454645305404>",
        32: "<:blackThree:1313907816083226735><:blackTwo:1313907793757077564>",
        33: "<:redThree:1313908488820359241><:redThree:1313908488820359241>",
        34: "<:blackThree:1313907816083226735><:blackFour:1313907834961920021>",
        35: "<:redThree:1313908488820359241><:redFive:1313908521028288597>",
        36: "<:blackThree:1313907816083226735><:blackSix:1313907904088379452>",
    }

    # Roulette configuration
    numbers = [
        {"color": "green", "number": 0},
        *[{"color": "red", "number": i} for i in range(1, 37, 2)],  # Odd reds
        *[{"color": "black", "number": i} for i in range(2, 37, 2)],  # Even blacks
    ]
    result = random.choice(numbers)

    # Convert the number to its corresponding emote
    result_emote = emotes[result["number"]]

    # Evaluate the bet result
    winnings = 0
    if bet_type == "number" and value.isdigit():
        if int(value) == result["number"]:
            winnings = bet * 36
    elif bet_type == "color" and value.lower() == result["color"] and value.lower() != "green":
        winnings = bet * 2
    elif bet_type == "color" and value.lower() == result["color"] and value.lower() == "green":
        winnings = bet * 36
    elif bet_type == "even" and result["number"] != 0 and result["number"] % 2 == 0:
        winnings = bet * 2
    elif bet_type == "odd" and result["number"] != 0 and result["number"] % 2 != 0:
        winnings = bet * 2
    elif bet_type == "zero" and result["number"] == 0:
        winnings = bet * 36

    # Update balance and send message
    if winnings > 0:
        data[user_id]["chips"] -= bet
        data[user_id]["chips"] += winnings
        message = f"🎉 {ctx.author.mention}, you won {winnings} chips! The result was {result_emote}."
    else:
        data[user_id]["chips"] -= bet
        message = f"😢 {ctx.author.mention}, you lost. The result was {result_emote}."

    # Save the updated data
    save_data(data)
    await ctx.send(message)

# Function for slots command
@bot.command()
async def slots(ctx, bet: int):
    user_id = str(ctx.author.id)
    data = load_data()

    # Check if the user is registered
    if user_id not in data:
        await ctx.send(f"{ctx.author.mention}, you are not registered in the casino. Use `$enter` to start.")
        return

    # Check if the user has enough chips for the bet
    if data[user_id]["chips"] < bet:
        await ctx.send(f"{ctx.author.mention}, you don't have enough chips to bet {bet}.")
        return

    # Check that the bet is within the allowed range (1000 to 1000000)
    if bet < 1000 or bet > 1000000:
        await ctx.send(f"{ctx.author.mention}, the bet must be between 1000 and 1000000 chips.")
        return

    # Define symbols and probabilities
    # For this to work correctly, you must add the emoticons to the Discord application and replace the IDs.
    symbols = [
        {"name": "berry", "emote": "<:cerezas:1313720692587630653>", "multiplier": 2, "probability": 0.29},
        {"name": "banana", "emote": "<:platano:1313720718508298311>", "multiplier": 2.2, "probability": 0.23},
        {"name": "oranges", "emote": "<:naranja:1313720725831680000>", "multiplier": 2.6, "probability": 0.18},
        {"name": "grapes", "emote": "<:uvas:1313720760715706439>", "multiplier": 2.8, "probability": 0.12},
        {"name": "greenSeven", "emote": "<:GreenSeven:1313720781842284564>", "multiplier": 3, "probability": 0.09},
        {"name": "blueSeven", "emote": "<:BlueSeven:1313720797176528916>", "multiplier": 5, "probability": 0.06},
        {"name": "redSeven", "emote": "<:RedSeven:1313720813412683817>", "multiplier": 10, "probability": 0.03}
    ]

    # Add the probabilities to the total (100% - the sum of the probabilities of the previous symbols)
    loss_probability = 1 - sum([symbol["probability"] for symbol in symbols])

    # Function to select a symbol based on probabilities
    def select_symbol():
        probability = random.random()
        cumulative_probability = 0

        # Probabilities of the symbols are summed until the accumulated probability exceeds the random value.
        for symbol in symbols:
            cumulative_probability += symbol["probability"]
            if probability < cumulative_probability:
                return symbol
        # If no symbol has been found, it means it's a loss
        return {"name": "loss", "emote": ":x:", "multiplier": 0, "probability": loss_probability}

    # Simulation of the 3 spins
    spins = [select_symbol() for _ in range(3)]

    # Show the first spin
    await ctx.send(f"{ctx.author.mention}, spinning the slots!")
    await ctx.send(f"Spin 1: {spins[0]['emote']}")
    await asyncio.sleep(1)

    # Show the second spin
    await ctx.send(f"Spin 2: {spins[1]['emote']}")
    await asyncio.sleep(1)

    # Show the third spin
    await ctx.send(f"Spin 3: {spins[2]['emote']}")
    await asyncio.sleep(1)

    # Calculate if the player has won and calculate winnings
    if spins[0]["name"] == spins[1]["name"] == spins[2]["name"]:
        # The player has won
        if spins[0]["name"] != "loss":
            winnings = round(bet * spins[0]["multiplier"])
            data[user_id]["chips"] += winnings
            await ctx.send(f"🎉 {ctx.author.mention}, you won {winnings} chips! 🎉")
        else:
            await ctx.send(f"😢 {ctx.author.mention}, you lost. Better luck next time. 😢")
    else:
        # The player has lost
        data[user_id]["chips"] -= bet
        await ctx.send(f"😢 {ctx.author.mention}, you lost {bet} chips. Better luck next time. 😢")

    # Save the updated data
    save_data(data)

# Command to play blackjack
@bot.command()
async def blackjack(ctx, bet: int):
    # Collect user data
    user_id = str(ctx.author.id)
    data = load_data()

    # Check if the user is registered
    if user_id not in data:
        await ctx.send(f"{ctx.author.mention}, you are not registered in the casino. Use '$enter' to start.")
        return

    # Check if the user has enough chips for the bet
    if data[user_id]['chips'] < bet:
        await ctx.send(f"{ctx.author.mention}, you don't have enough chips to bet {bet}.")
        return

    # Check that the bet is within the allowed range (1000 to 1000000)
    if bet < 1000 or bet > 1000000:
        await ctx.send(f"{ctx.author.mention}, the bet must be between 1000 and 1000000 chips.")
        return

    # Create a deck of cards
    # For this to work correctly, you must add the emoticons to the Discord application and replace the IDs.
    cards = [
        {"suit": "hearts", "emote": "<:asCorazones:1313920489000800297>", "value": 1, "value2": 11},
        {"suit": "hearts", "emote": "<:dosCorazones:1313920546010038404>", "value": 2, "value2": 2},
        {"suit": "hearts", "emote": "<:tresCorazones:1313920593183379526>", "value": 3, "value2": 3},
        {"suit": "hearts", "emote": "<:cuatroCorazones:1313920624489529384>", "value": 4, "value2": 4},
        {"suit": "hearts", "emote": "<:cincoCorazones:1313920665023152240>", "value": 5, "value2": 5},
        {"suit": "hearts", "emote": "<:seisCorazones:1313920706433515581>", "value": 6, "value2": 6},
        {"suit": "hearts", "emote": "<:sieteCorazones:1313920742597070878>", "value": 7, "value2": 7},
        {"suit": "hearts", "emote": "<:ochoCorazones:1313920782363004968>", "value": 8, "value2": 8},
        {"suit": "hearts", "emote": "<:nueveCorazones:1313920820262735892>", "value": 9, "value2": 9},
        {"suit": "hearts", "emote": "<:diezCorazones:1313920867083751526>", "value": 10, "value2": 10},
        {"suit": "hearts", "emote": "<:jCorazones:1313920909140299816>", "value": 10, "value2": 10},
        {"suit": "hearts", "emote": "<:qCorazones:1313920937778745475>", "value": 10, "value2": 10},
        {"suit": "hearts", "emote": "<:kCorazones:1313920961980137586>", "value": 10, "value2": 10},
        {"suit": "spades", "emote": "<:asPicas:1313921037133545633>", "value": 1, "value2": 11},
        {"suit": "spades", "emote": "<:dosPicas:1313921063389761586>", "value": 2, "value2": 2},
        {"suit": "spades", "emote": "<:tresPicas:1313921090204205239>", "value": 3, "value2": 3},
        {"suit": "spades", "emote": "<:cuatroPicas:1313921146281918505>", "value": 4, "value2": 4},
        {"suit": "spades", "emote": "<:cincoPicas:1313921196085215244>", "value": 5, "value2": 5},
        {"suit": "spades", "emote": "<:seisPicas:1313921227944886283>", "value": 6, "value2": 6},
        {"suit": "spades", "emote": "<:sietePicas:1313921249352618044>", "value": 7, "value2": 7},
        {"suit": "spades", "emote": "<:ochoPicas:1313921279711248404>", "value": 8, "value2": 8},
        {"suit": "spades", "emote": "<:nuevePicas:1313921299923472474>", "value": 9, "value2": 9},
        {"suit": "spades", "emote": "<:diezPicas:1313921320529952888>", "value": 10, "value2": 10},
        {"suit": "spades", "emote": "<:jPicas:1313921341623111771>", "value": 10, "value2": 10},
        {"suit": "spades", "emote": "<:qPicas:1313921368089432266>", "value": 10, "value2": 10},
        {"suit": "spades", "emote": "<:kPicas:1313921390138626183>", "value": 10, "value2": 10},
        {"suit": "diamonds", "emote": "<:asRombos:1313921419507138721>", "value": 1, "value2": 11},
        {"suit": "diamonds", "emote": "<:dosRombos:1313921454466793593>", "value": 2, "value2": 2},
        {"suit": "diamonds", "emote": "<:tresRombos:1313921486339444746>", "value": 3, "value2": 3},
        {"suit": "diamonds", "emote": "<:cuatroRombos:1313921507755560980>", "value": 4, "value2": 4},
        {"suit": "diamonds", "emote": "<:cincoRombos:1313921540290514964>", "value": 5, "value2": 5},
        {"suit": "diamonds", "emote": "<:seisRombos:1313921562352685136>", "value": 6, "value2": 6},
        {"suit": "diamonds", "emote": "<:sieteRombos:1313921581239631974>", "value": 7, "value2": 7},
        {"suit": "diamonds", "emote": "<:ochoRombos:1313921620208914484>", "value": 8, "value2": 8},
        {"suit": "diamonds", "emote": "<:nueveRombos:1313921648528986144>", "value": 9, "value2": 9},
        {"suit": "diamonds", "emote": "<:diezRombos:1313921675313680495>", "value": 10, "value2": 10},
        {"suit": "diamonds", "emote": "<:jRombos:1313921694900944987>", "value": 10, "value2": 10},
        {"suit": "diamonds", "emote": "<:qRombos:1313921715302043679>", "value": 10, "value2": 10},
        {"suit": "diamonds", "emote": "<:kRombos:1313921736844251196>", "value": 10, "value2": 10},
        {"suit": "clubs", "emote": "<:asTreboles:1313921770126049402>", "value": 1, "value2": 11},
        {"suit": "clubs", "emote": "<:dosTreboles:1313921799418806345>", "value": 2, "value2": 2},
        {"suit": "clubs", "emote": "<:tresTreboles:1313921825713033266>", "value": 3, "value2": 3},
        {"suit": "clubs", "emote": "<:cuatroTreboles:1313921856830701648>", "value": 4, "value2": 4},
        {"suit": "clubs", "emote": "<:cincoTreboles:1313921882348589178>", "value": 5, "value2": 5},
        {"suit": "clubs", "emote": "<:seisTreboles:1313921909053980682>", "value": 6, "value2": 6},
        {"suit": "clubs", "emote": "<:sieteTreboles:1313921928125349990>", "value": 7, "value2": 7},
        {"suit": "clubs", "emote": "<:ochoTreboles:1313921953391706162>", "value": 8, "value2": 8},
        {"suit": "clubs", "emote": "<:nueveTreboles:1313921978855456878>", "value": 9, "value2": 9},
        {"suit": "clubs", "emote": "<:diezTreboles:1313922000422699072>", "value": 10, "value2": 10},
        {"suit": "clubs", "emote": "<:jTreboles:1313922019787669504>", "value": 10, "value2": 10},
        {"suit": "clubs", "emote": "<:qTreboles:1313922038519300187>", "value": 10, "value2": 10},
        {"suit": "clubs", "emote": "<:kTreboles:1313922055070285937>", "value": 10, "value2": 10}
    ]
    # Shuffle the cards
    random.shuffle(cards)

    # Deal two cards to the player and the dealer
    player_hand = [cards.pop(), cards.pop()]
    dealer_hand = [cards.pop(), cards.pop()]

    # Function to calculate total with Aces
    def calculate_total_with_aces(hand):
        total = sum(card["value"] for card in hand)
        aces = sum(1 for card in hand if card["value"] == 11)  # Count Aces as 11
        while total > 21 and aces > 0:
            total -= 10  # Convert an Ace from 11 to 1
            aces -= 1
        return total

    # Show player's cards and one of the dealer's cards
    player_hand_emotes = " ".join([card["emote"] for card in player_hand])
    dealer_hand_emotes = " ".join([card["emote"] for card in dealer_hand[:-1]]) + " <:reverseCard:1356923674564755580>"
    await ctx.send(f"{ctx.author.mention}, your cards are: {player_hand_emotes} ({calculate_total_with_aces(player_hand)})\nThe dealer has: {dealer_hand_emotes} ({calculate_total_with_aces(dealer_hand[:-1])})")

    # Check if the dealer has blackjack
    dealer_values = [card["value"] for card in dealer_hand]
    if 10 in dealer_values and (1 in dealer_values or 11 in dealer_values):
        time.sleep(2)
        tmp = 0
        for card in dealer_hand:
            tmp += card["value"]

        if tmp == 21:
            await ctx.send(f"😢 {ctx.author.mention}, the dealer has blackjack. You lost your {bet} chips bet.")
        save_data(data)
        return

    # Check if the player has blackjack
    if [card["value"] for card in player_hand[:-1]] == 10 or [card["value2"] for card in player_hand[:-1]] == 11:
        time.sleep(2)
        tmp = 0
        for card in dealer_hand:
            tmp += card["value"]

        if tmp == 21:
            await ctx.send(f"🎉 {ctx.author.mention}, you have blackjack! You won {bet * 2.5} chips.")
            data[user_id]["chips"] += bet * 1.5
        save_data(data)
        return

    # Ask the player if they want to hit
    while True:
        # Check if the player's cards have the same value
        if player_hand[0]["value"] == player_hand[1]["value"] or player_hand[0]["value2"] == player_hand[1]["value2"] and data[user_id]["chips"] >= bet * 2 and len(player_hand) == 2:
            await ctx.send(f"{ctx.author.mention} What do you want to do? \n1. Hit\n2. Split cards\n3. Double down and hit\n4. Stand")
            try:
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention}, response time expired. The game is canceled.")
                return
            if response.content == '1':
                player_hand.append(cards.pop())
                player_hand_emotes = " ".join([card["emote"] for card in player_hand])
                await ctx.send(f"Your cards are: {player_hand_emotes} ({calculate_total_with_aces(player_hand)})")
            elif response.content == '2':
                bet *= 2
                player_hand_1 = [player_hand[0], cards.pop()]
                player_hand_2 = [player_hand[1], cards.pop()]
                player_hand_emotes_1 = " ".join([card["emote"] for card in player_hand_1])
                player_hand_emotes_2 = " ".join([card["emote"] for card in player_hand_2])
                await ctx.send(f"Your cards are: {player_hand_emotes_1} ({calculate_total_with_aces(player_hand_1)}) and {player_hand_emotes_2} ({calculate_total_with_aces(player_hand_2)})")
                await ctx.send(f"{ctx.author.mention} What do you want to do for the first hand? \n1. Hit\n2. Stand")
                try:
                    response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send(f"{ctx.author.mention}, response time expired. The game is canceled.")
                    return
                if response.content == '1':
                    player_hand_1.append(cards.pop())
                    player_hand_emotes_1 = " ".join([card["emote"] for card in player_hand_1])
                    await ctx.send(f"Your cards are: {player_hand_emotes_1} ({calculate_total_with_aces(player_hand_1)})")
                    if sum([card["value"] for card in player_hand_1]) > 21:
                        break
                elif response.content == '2':
                    await ctx.send(f"Your cards are: {player_hand_emotes_1} ({calculate_total_with_aces(player_hand_1)}) and {player_hand_emotes_2} ({calculate_total_with_aces(player_hand_2)})")
                    await ctx.send(f"{ctx.author.mention} What do you want to do for the second hand? \n1. Hit\n2. Stand")
                    try:
                        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(f"{ctx.author.mention}, response time expired. The game is canceled.")
                        return
                    if response.content == '1':
                        player_hand_2.append(cards.pop())
                        player_hand_emotes_2 = " ".join([card["emote"] for card in player_hand_2])
                        await ctx.send(f"Your cards are: {player_hand_emotes_2} ({calculate_total_with_aces(player_hand_2)})")
                        if sum([card["value"] for card in player_hand_2]) > 21:
                            break
                    elif response.content == '2':
                        break
            elif response.content == '3':
                bet *= 2
                player_hand.append(cards.pop())
                player_hand_emotes = " ".join([card["emote"] for card in player_hand])
                await ctx.send(f"Your cards are: {player_hand_emotes} ({calculate_total_with_aces(player_hand)})")
                break
            elif response.content == '4':
                break
        # Check if the player has at least double the bet
        elif data[user_id]["chips"] >= bet * 2 and len(player_hand) == 2:
            await ctx.send(f"{ctx.author.mention} What do you want to do? \n1. Hit\n2. Double down and hit\n3. Stand")
            try:
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention}, response time expired. The game is canceled.")
                return
            if response.content == '1':
                player_hand.append(cards.pop())
                player_hand_emotes = " ".join([card["emote"] for card in player_hand])
                await ctx.send(f"Your cards are: {player_hand_emotes} ({calculate_total_with_aces(player_hand)})")
                if sum([card["value"] for card in player_hand]) > 21:
                    break
            elif response.content == '2':
                bet *= 2
                player_hand.append(cards.pop())
                player_hand_emotes = " ".join([card["emote"] for card in player_hand])
                await ctx.send(f"Your cards are: {player_hand_emotes} ({calculate_total_with_aces(player_hand)})")
                break
            elif response.content == '3':
                break
        # The player does not have double the bet
        else:
            await ctx.send(f"{ctx.author.mention} What do you want to do? \n1. Hit\n2. Stand")
            try:
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention}, response time expired. The game is canceled.")
                return
            if response.content == '1':
                player_hand.append(cards.pop())
                player_hand_emotes = " ".join([card["emote"] for card in player_hand])
                await ctx.send(f"Your cards are: {player_hand_emotes} ({calculate_total_with_aces(player_hand)})")
                if sum([card["value"] for card in player_hand]) > 21:
                    break
            elif response.content == '2':
                break
    # Check if the player busted
    if calculate_total_with_aces(player_hand) > 21:
        await ctx.send(f"😢 {ctx.author.mention}, you busted. You lost your {bet} chips bet.")
        data[user_id]["chips"] -= bet
        save_data(data)
        return

    # Show the dealer's hand
    dealer_hand_emotes = " ".join([card["emote"] for card in dealer_hand])
    await ctx.send(f"The dealer has: {dealer_hand_emotes} ({calculate_total_with_aces(dealer_hand)})")
    time.sleep(3)

    # Play the dealer's hand
    while calculate_total_with_aces(dealer_hand) < 17:
        dealer_hand.append(cards.pop())
        dealer_hand_emotes = " ".join([card["emote"] for card in dealer_hand])
        await ctx.send(f"The dealer has: {dealer_hand_emotes} ({calculate_total_with_aces(dealer_hand)})")
        await asyncio.sleep(1)
        if calculate_total_with_aces(dealer_hand) > 21:
            await ctx.send(f"🎉 {ctx.author.mention}, the dealer busted. You won {bet*2} chips.")
            data[user_id]["chips"] += bet
            save_data(data)
            return
        time.sleep(3)

    # Compare hands and determine the outcome
    player_total = calculate_total_with_aces(player_hand)
    dealer_total = calculate_total_with_aces(dealer_hand)
    if player_total > dealer_total:
        await ctx.send(f"🎉 {ctx.author.mention}, you won {bet*2} chips.")
        data[user_id]["chips"] += bet
        save_data(data)
    elif player_total < dealer_total:
        await ctx.send(f"😢 {ctx.author.mention}, you lost {bet} chips.")
        data[user_id]["chips"] -= bet
        save_data(data)
    else:
        await ctx.send(f"🤝 {ctx.author.mention}, it's a tie. You didn't win or lose any chips.")

# Help command
@bot.command()
async def help(ctx):
    help_text = """
    Welcome to the casino help system! Here are the available commands:

    **$enter** - Type this command when starting the bot to enter the casino.
    **$chips** - Shows your chip balance.
    **$reward** - Allows you to claim 500 chips once every day. This may vary with shop rewards.
    **$roulette <bet> <bet_type> [value]** - Allows you to bet an amount X on the roulette.
    **$slots <bet>** - Allows you to bet an amount on the slot machine.
    **$help** - Displays this information you are reading.

    Good luck at the casino! 🎰
    """
    await ctx.send(help_text)

# TODO Asynchronous function to play a poker game

# TODO A reward shop where you can redeem rewards such as reducing the chip claim cooldown or increasing chips per reward

# Start the bot
TOKEN = '------------' # Replace with your bot token
bot.run(TOKEN)
