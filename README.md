# willbot
A dumb bot using the Skype4Py API wrapper for Skype

An annoying bot I wrote to talk in my friend's Skype call.

### Overview
Various commands can be used in the Skype call that willbot is in which are outlined in the file *commands/help.txt*.

Unless he is disabled using the *!disable* command, willbot will also occassionally respond to greetings and various phrases.

### Usage
```
python willbot.py
```

Note that willbot is currently configured (a bit jankily) so that it will work in a group conversation. To make it work in a user-to-user conversation, in *willbot.py*, remove lines 154-157, and change lines 54 and 58 from:
```
convo.SendMessage(responseBlock)
```
to
```
skype.SendMessage(userNameToSendTo, responseBlock)
```

Greetings to users are chosen randomly from the file thats name matches the user's username. These can be customised by editing the files in */greetings/* or by using the command *!addgreeting*.

Random quotes can be customised in the same way, and chat logs must be obtained manually. I suggest using https://github.com/lordgreggreg/skype-log-viewer

### Related projects
https://github.com/Skype4Py/Skype4Py
