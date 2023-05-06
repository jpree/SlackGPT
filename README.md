# SlackGPT a Language Model Slack Plugin
This repo contains a Slack plugin that utilizes OpenAI's language models to generate responses to messages. The plugin uses the [Slack Bolt](https://api.slack.com/tools/bolt) Python library to interact with the Slack API and the [ChatOpenAI](https://github.com/LangChain/langchain/tree/main/langchain/chat_models) module from [LangChain](https://github.com/LangChain/langchain) to generate text responses.
## Installation
### Docker
1. Clone this repo to your local environment
2. Install Docker if you haven't already
3. Set up a Slack bot and obtain its API token. Make sure the bot has access to the channels you want the plugin to operate in.
4. Set up the OpenAI API key.
5. Build the Dockerfile by running the following command:
``` 
   docker build -t slack-gpt .
```
6. Run the Dockerfile with the following command, making sure to pass in the environment variable values for SLACK_BOT_TOKEN, SLACK_APP_TOKEN, and OPENAI_API_KEY:
```  
   docker run -it -e SLACK_BOT_TOKEN -e SLACK_APP_TOKEN -e OPENAI_API_KEY slack-gpt
```   
### Local Environment
1. Clone this repo to your local environment
2. Install the requirements by running pip install -r requirements.txt
3. Set up a Slack bot and obtain its API token. Make sure the bot has access to the channels you want the plugin to operate in.
4. Set up the OpenAI API key and set it as an environment variable named OPENAI_API_KEY.
5. Set up the SLACK_APP_TOKEN and SLACK_BOT_TOKEN as environment variables.
## Usage
To use the plugin, follow the installation instructions above to set up the Slack bot and OpenAI API key, then run the following command:
python main.py
## Functionality
The plugin listens for messages in Slack channels and responds with generated text using OpenAI's language models. The responses are contextually relevant and generated based on previous messages in the channel, thanks to the [ChatOpenAI](https://github.com/LangChain/langchain/tree/main/langchain/chat_models) model.
The plugin supports the following functionality:
* Responding to direct mentions by generating text based on the previous messages in the channel.
* Responding to messages in the channel with generated text based on the previous messages in the channel.

## Slack App Permissions
The following table outlines the Slack app permissions required for SlackGPT to function properly:
| Permission | Description |
| --- | --- |
| app_mentions:read | View messages that directly mention @SlackGPT in conversations that the app is in |
| chat:write | Send messages as @SlackGPT |
| chat:write.public | Send messages to channels @SlackGPT isn't a member of |
| mpim:write | Start group direct messages with people |
| channels:history | View messages and other content in public channels, private channels, direct messages, and group direct messages that SlackGPT has been added to |
| groups:history | View messages and other content in public channels, private channels, direct messages, and group direct messages that SlackGPT has been added to |
| im:history | View messages and other content in public channels, private channels, direct messages, and group direct messages that SlackGPT has been added to |
| mpim:history | View messages and other content in public channels, private channels, direct messages, and group direct messages that SlackGPT has been added to |
| im:read | View basic information about direct and group direct messages that SlackGPT has been added to |
| mpim:read | View basic information about direct and group direct messages that SlackGPT has been added to |
| channels:read | View basic information about public channels in a workspace |

SlackGPT requires permission to view messages that directly mention @SlackGPT in conversations that the app is in, as well as permission to send messages as @SlackGPT and to start group direct messages with people. Additionally, the app needs permission to view messages and other content in public channels, private channels, direct messages, and group direct messages that SlackGPT has been added to, as well as permission to view basic information about direct and group direct messages that SlackGPT has been added to, and basic information about public channels in a workspace.
These permissions are necessary for SlackGPT to function properly and generate contextually relevant responses based on the messages in the Slack channels it is added to. It is important to only grant the necessary permissions to SlackGPT for security reasons.

### Installation

To install SlackChat in your Slack workspace, follow these steps:

1. Create a new Slack app on the [Slack API website](https://api.slack.com/apps?new_app=1).
2. Give your app a name and select a workspace for development.
3. In the left sidebar, click on "Manifest" to open the manifest editor.
4. Copy and paste the provided JSON manifest into the editor, then click "Save" to apply the changes.
5. In the left sidebar, navigate to "OAuth & Permissions."
6. Verify that the scopes from the manifest have been added automatically in the "Scopes" section.
7. Click "Install App" in the left sidebar, then click "Install App to Workspace."
8. Review the requested permissions on the permission request page, then click "Allow."
9. Store the bot user's access token from the "Install App" page securely as you'll need it to interact with the Slack API.

Once installed, you can start using SlackChat in your workspace. Enjoy the power of generative AI at your fingertips!

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.