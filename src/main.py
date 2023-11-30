import random
import src.settings as settings
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
motivational_texts = [
    """
    Motivational texts here
    """
]

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES) 
    return creds


def upload_image(file_path, image_name, folder_id):
    """
    Uploads an image file to Google Drive.

    Parameters:
    - file_path (str): The local path of the image file to be uploaded.
    - image_name (str): The desired name for the uploaded image file.
    - folder_id (str): The ID of the Google Drive folder where the image will be uploaded.

    Returns:
    - nothing

    Raises:
    - Exception: If authentication fails or if there is an issue uploading the file.

    Usage:
    ```python
    upload_image('/local/path/to/image.jpg', 'uploaded_image.jpg', 'google_drive_folder_id')
    ```

    Note:
    - Make sure to call `authenticate()` before using this function to obtain valid credentials.
    - The function assumes that the `authenticate` function is defined elsewhere in your code.
    """
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
    """
    Run the Discord bot with specified commands and events.

    Usage:
    - Call this function to start the Discord bot.

    Notes:
    - Ensure that the `settings` module contains the `DISCORD_API_SECRET` token.
    - Import and define the `before_dash`, `after_dash`, and `upload_image` functions from your_module.
    """
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        """
        Runs when bot is ready
        """
        logger.info(f"User: {bot.user.name}, id: {bot.user.id}")

    @bot.event
    async def on_command_error(ctx, error):
        """
        Handle command errors and send appropriate messages.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - error: The error raised during command execution.
        """
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
        """
        Command to visit a location by posting an image with a clue name.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - *cluename: Variable-length argument to represent the clue name.

        Notes:
        - Utilizes the `before_dash` and `after_dash` functions.
        - Assumes the existence of the `folder_dict` and `motivational_texts` variables.

        Usage:
        !v a-1 <img>
        """
        if len(ctx.message.attachments) <= 0:
            return await ctx.send('No attachments attached/detected.')
        for attachment in ctx.message.attachments:
            filename = " ".join(cluename) + "." + attachment.filename.split('.')[-1]

            identifier = before_dash(cluename[0])
            folder_id = folder_dict[identifier]
            number = after_dash(cluename[0])

            filename = f"{identifier}{number}" # Or whatever you want to name the file in google drive

            # Put in folder of your choice but folder must be made in current repository
            file_path = f'images/{identifier}/{filename}.{attachment.filename.split(".")[-1]}' 

            await attachment.save(file_path)
            upload_image(file_path=file_path, image_name=filename, folder_id=folder_id)
        return await ctx.send(f"Successfully uploaded {cluename}")
    
    @bot.command(
        aliases = ['say', 'mq', 'mv']
    )
    async def motivate_me(ctx):
        """
        Command to send a motivational message.

        Parameters:
        - ctx (commands.Context): The context of the command.
        """
        await ctx.send(random.choice(motivational_texts))

    bot.run(token=settings.DISCORD_API_SECRET, root_logger=True)


#Helper to remove trailing digits of a code
def remove_trailing_numbers(input_string):
    """
    Removes trailing digits from the end of a given string.

    Parameters:
    - input_string (str): The input string from which trailing digits will be removed.

    Returns:
    - str: The modified string with trailing digits removed.

    Usage:
    result = remove_trailing_numbers("example123")
    print(result)  # Output: "example"
    """
    modified_string = re.sub(r'\d*$', '', input_string)
    return modified_string

def before_dash(input_string):
    """
    Retrieves the substring before the first occurrence of a dash ("-") in a given string.

    Parameters:
    - input_string (str): The input string from which the substring before the dash will be extracted.

    Returns:
    - str: The substring before the first dash.

    Usage:
    result = before_dash("prefix-suffix")
    print(result)  # Output: "prefix"
    """
    output = input_string.split('-')[0]
    return output

def after_dash(input_string):
    """
    Retrieves the substring after the first occurrence of a dash ("-") in a given string.

    Parameters:
    - input_string (str): The input string from which the substring after the dash will be extracted.

    Returns:
    - str: The substring after the first dash.

    Usage:
    result = after_dash("prefix-suffix")
    print(result)  # Output: "suffix"
    """
    output = input_string.split('-')[1]
    return output


if __name__ == '__main__':
    print(before_dash("fi-bunny"))
    run()