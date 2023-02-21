# chatgpt-irc
An IRC bot that connects to Chat-GPT's davinci model via API and allows you interact with it.

# Usage:
1. Install all the required dependencies (python3, openai via pip, etc.)
2. Head to https://platform.openai.com/account/api-keys and generate a key. You will need an account.
3. Replace "apikey" with your new key.
4. Change the server settings to what you want.
5. Under "response = openai.Completion.create" change the model settings if you feel like it.
6. Change the number in "if i >= 10:" if you want to modify the max amount of lines the bot can send to your channel. Default: 10

Run it and you should be good to go! To chat with the bot, type in ChatGPT: Hi!

# Notes:
This model is not free! You can make a free account and generate a key but you will run out of free credits if you use it long enough. See https://platform.openai.com/account/usage for more details.
It won't always respond to requests if the API is "overloaded". It should print an error message in this case.
Calling the model this way bypasses the normal moderation filter. You may get banned if you get it too spit out too many things the company deems inappropriate usage.
This version of the model has no memory. Though it may trick you into believing otherwise, it won't remember or be able to reference any previous messages.
