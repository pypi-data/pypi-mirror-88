import logging

from aprsd import plugin
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

LOG = logging.getLogger("APRSD")


class SlackCommandPlugin(plugin.APRSDPluginBase):
    """SlackCommandPlugin.

    This APRSD plugin looks for the location command comming in
    to aprsd, then fetches the caller's location, and then reports
    that location string to the configured slack channel.

    To use this:
        Create a slack bot for your workspace at api.slack.com.
        A good source of information on how to create the app
        and the tokens and permissions and install the app in your
        workspace is here:

            https://api.slack.com/start/building/bolt-python


        You will need the signing secret from the
        Basic Information -> App Credentials form.
        You will also need the Bot User OAuth Access Token from
        OAuth & Permissions -> OAuth Tokens for Your Team ->
        Bot User OAuth Access Token.

        Install the app/bot into your workspace.

        Edit your ~/.config/aprsd/aprsd.yml and add the section
        slack:
            signing_secret: <signing secret token here>
            bot_token: <Bot User OAuth Access Token here>
            channel: <channel name here>
    """

    version = "1.0"

    # matches any string starting with h or H
    command_regex = "^[lL]"
    command_name = "location-slack"

    def _setup_slack(self):
        """Create the slack require client from config."""

        # signing_secret = self.config["slack"]["signing_secret"]
        bot_token = self.config["slack"]["bot_token"]
        self.swc = WebClient(token=bot_token)

        self.slack_channel = self.config["slack"]["channel"]

    def command(self, fromcall, message, ack):
        LOG.info("SlackCommandPlugin")

        self._setup_slack()

        # now call the location plugin to get the location info
        location_plugin = plugin.LocationPlugin(self.config)
        location = location_plugin.command(fromcall, message, ack)
        if location:
            reply = location

            LOG.debug("Sending '{}' to slack channel '{}'".format(reply, self.slack_channel))
            try:
                self.swc.chat_postMessage(channel=self.slack_channel, text=reply)
            except SlackApiError as e:
                LOG.error(
                    "Failed to send message to channel '{}' because '{}'".format(
                        self.slack_channel, str(e)
                    )
                )
        else:
            LOG.debug("SlackCommandPlugin couldn't get location for '{}'".format(fromcall))

        return None
