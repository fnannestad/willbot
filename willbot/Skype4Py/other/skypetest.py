python
import Skype4Py
import sys

skype = Skype4Py.Skype()
skype.Attach()
user = sys.argv[1]
message = ' '.join(sys.argv[2:])
skype.SendMessage(user, message)