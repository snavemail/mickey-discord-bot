import random
import settings
import discord
from discord.ext import commands
from discord.ext import commands
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

logger = settings.logging.getLogger("bot")

SERVICE_ACCOUNT_FILE = 'service_account_file.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

folder_dict = {
    """
    Here go to the google drive folder that you shared or is in a shared folder of your discord bot
    Make a keypair value for your folder and folder_id so you can easily find the folder you wish to send a document
    to from your discord bot
    """
}
motivational_texts = ['One more!', 'You can do it!', 'I believe in you!', 'I think you are so cool!', 'My faith in you has never waivered', 'Your dedication to your craft has got me singing in the shower!', 'Never have I ever seen someone so cool', 'If you do this, you will be blessed with so many coconuts', 'Listen to me! I believe in you', 'Never back down!', 'WE ARE SO BACK', 'Liam believes in you', 'Garrin believes in you', 'Kelsey believes in you', 'Ben believes in you', 'C. Chefalas believes in you', 'Anson believes in you', 'Colton believes in you', 'Der Chi Believes in you', 'President Aoun believes in you', 'Daniel believes in you', 'Jakob believes in you', 'Matt believes in you', 'Ethan believes in you', 'Liam is on a bathroom break', 'Just keep biking, just keep biking 🎵', 'Hot dog, hot dog, hot diggity dog!', 'A man, a plan, a canal -- Panama', 'Jerry believes in you', 'Wen believes in you', 'Grant believes in you']

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES) 
    return creds

def upload_image(file_path, image_name, folder_id):
    creds = authenticate()

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': image_name,  # Change to your desired file name
        'parents': [folder_id],
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    # Event that runs when the bot is ready
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user.name}, id: {bot.user.id}")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Filename bad. Either missing folder for code or written incorrectly")

    @bot.command(
        name='visit',
        aliases = ['v'],
        help='!v [id-num] [attachment], ex: !v a-1 <img>',
        description="Post an image with a clue name to visit it.",
        brief='!v a-1 <img>'
        )
    async def visit(ctx, *cluename):
        if len(ctx.message.attachments) <= 0:
            return await ctx.send('No attachments attached/detected.')
        for attachment in ctx.message.attachments:
            filename = " ".join(cluename) + "." + attachment.filename.split('.')[-1]

            identifier = before_dash(cluename[0])
            print(identifier)
            folder_id = folder_dict[identifier]
            if identifier == "fi":
                new_identifier = "F"
            elif identifier == "cr":
                new_identifier = "C"
            elif identifier == "vi":
                new_identifier = "V"
            else:
                new_identifier = identifier
            
            print(folder_id)
            print(identifier)

            number = after_dash(cluename[0])
            print(number)

            if new_identifier == "C":
                filename = f"{number}-Mickey Mouse Clubhouse"
            elif new_identifier == "F" or new_identifier == "V":
                filename = f"{new_identifier}{number}-Mickey Mouse Clubhouse"
            else:
                filename = f"{new_identifier}{number}"

            print(filename)

            file_path = f'images/{identifier}/{filename}.{attachment.filename.split(".")[-1]}'

            print(file_path)
            await attachment.save(file_path)
            upload_image(file_path=file_path, image_name=filename, folder_id=folder_id)
        return await ctx.send(f"Successfully uploaded {cluename}")
    
    @bot.command(
        aliases = ['say', 'mq', 'mv']
    )
    async def motivate_me(ctx):
        await ctx.send(random.choice(motivational_texts))

    bot.run(token=settings.DISCORD_API_SECRET, root_logger=True)


#Helper to remove trailing digits of a code
def remove_trailing_numbers(input_string):
    modified_string = re.sub(r'\d*$', '', input_string)
    return modified_string

def before_dash(input_string):
    output = input_string.split('-')[0]
    return output

def after_dash(input_string):
    output = input_string.split('-')[1]
    return output


if __name__ == '__main__':
    print(before_dash("fi-bunny"))
    run()