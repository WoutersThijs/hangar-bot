# HangarBot
Custom bot for Hangar22 private Discord

## Documentation
### Telegram listening
The bot is able to listen to Telegram channels and forward the incomming message to a specified Discord chat. The use of commands makes this fully customizable.

#### Commands
Commands configure the chat you are typing in.

##### - /hb tg status
The status argument tells you if Telegram listening has been turned on / off and lists the channels it's listening to.

##### - /hb tg on
This argument turns Telegram listening on for the chat the command has been sent in.

##### - /hb tg off
This argument turns Telegram listening on for the chat the command has been sent in.

##### - /hb add [channel_name]
With this command you can add a Telegram channel to listen to. The channel name should be the name of the link of the channel. You can find this in the Telegram channel info. The link starts with t.me/[channel_name].

##### - /hb add [channel_name]
With this command you can remove a Telegram channel from the list. The channel name should be the name of the link of the channel. You can find this in the Telegram channel info. The link looks like: t.me/[channel_name].

##### - /hb tg reload
This command should be used after you have made changes to the setup. It was possible to refresh the configuration on each command execution but this caused a little bit of delay.
