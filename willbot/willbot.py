import Skype4Py
import sys
import linecache
import random
import time
import string
import os

def Commands(Message, Status):
	global running
	global messageCount
	
	if Status == 'RECEIVED':
		messageCount += 1
		message = Message.Body.lower()
		#remove punctuation from handles so they match file names
		handle = Message.FromHandle.lower().translate(string.maketrans("",""), string.punctuation)
		response = ''
		print 'MESSAGE RECIEVED [count: ' + str(messageCount) + ', sender: ' + handle + ']'
			
		if running == True:
			if messageCount >= 20 or message == '!random':
				response = randomLine(generateFilePath('commands', 'randomquotes.txt'))
			elif message == '!commands' or message == '!help':
				response = readFile('help.txt')
			elif message == '!disable':
				response = disableBot()
			elif '!addrandom' in message:
				response = addToFile(generateFilePath('commands', 'randomquotes.txt'), message)
			elif '!addgreeting' in message:
				tokens = message.split()
				response = addToFile(generateFilePath('greetings', tokens[1] + '.txt'), " ".join(tokens[1:]))
			elif '!find' in message or '!count' in message or '!countcsv' in message:
				response = searchLogs(message)
			elif message == '!rankings':
				response = readFile('rankings.txt')
			else:
				response = processMessage(message, handle)
		elif message == '!enable':
			response = enableBot()
			
		#print out messages in chunks of 10 lines so that skype lags less
		if not response == '':
			#make responses seem more natural by waiting 2s before responding
			time.sleep(2)
			responseBlock = ''
			linesInBlock = 0
			print '\nSENDING RESPONSE...'
			for line in response.splitlines():
				responseBlock += line + '\n'
				linesInBlock += 1
				print str(linesInBlock) + '\t' + line
				if linesInBlock >= 10:
					convo.SendMessage(responseBlock)
					responseBlock = ''
					linesInBlock = 0
			if not responseBlock == '':
				convo.SendMessage(responseBlock)
			print '\n'

def generateFilePath(subfolder, filename):
	return os.getcwd() + '\\' + subfolder + '\\' + filename
	
def generateRandom(chance):
	return random.randint(1, chance) == chance
	
def enableBot():
	global running
	print 'ENABLED'
	running = True
	return '========== WILLBOT ENABLED =========='
					
def disableBot():
	global running
	print 'DISABLED'
	running = False
	return '========== WILLBOT DISABLED =========='
	
def readFile(filename):
	data = None
	with open (generateFilePath('commands', filename), 'r') as textfile:
		data = textfile.read()
	return data
		
def randomLine(fileName):
	global messageCount
	length = sum(1 for line in open(fileName))
	lineNumber = random.randint(1, length)
	messageCount = 0
	return linecache.getline(fileName, lineNumber).strip()
		
def addToFile(filename, message):
	phrase = " ".join(message.split()[1:])
	with open(filename, 'r+') as file:
		exists = False
		for line in file:
			line = line.rstrip()
			if phrase == line:
				return 'ERROR: PHRASE ALREADY EXISTS'
		file.write('\n' + phrase)		
	print 'ADDED PHRASE [' + phrase + ']'
	return 'ADDED PHRASE [' + phrase + ']'
	
def processMessage(message, handle):
	messageLength = len(message)
	messageTokens = message.split()
	response = ''
	if 'hi' in messageTokens or 'hello' in messageTokens or 'hey' in messageTokens:
		if generateRandom(3): response = randomLine(generateFilePath('greetings', handle + '.txt'))
	elif 'play' in messageTokens:
		if generateRandom(4): response = 'maybe later bud'
	elif messageTokens[0] == '!enable':
		response = 'WILLBOT ALREADY ENABLED'
	return response

def searchFile(filename, phrase):
	message = unicode('')
	lineCount = 0
	with open(generateFilePath('chatlogs', filename)) as f:
		while True:
			line = unicode(f.readline(), errors='replace').lower()
			if not line: 
				break
			elif phrase in line:
				lineCount += 1
				message += line
	print 'SEARCHED FILE [name: ' + filename[-11:] + ' lines: ' + str(lineCount) + ']'
	return message, lineCount
	
def searchLogs(message):
	tokens = message.split()
	command = tokens[0]
	phrase = " ".join(tokens[1:])
	response = ''
	totalCount = 0
	for file in os.listdir(os.getcwd() + '\\chatlogs'):
		lines, lineCount = searchFile(file, phrase)
		if command == '!find':
			response += lines
		elif command == '!count':
			response += 'Occurrences in ' + file[-11:-4] + ': ' + str(lineCount) + '\n'
		elif command == '!countcsv':
			response += file[-11:-4] + ', ' + str(lineCount) + '\n'
		totalCount += lineCount
	return response + '--------------------------------------\nTOTAL LINES CONTAINING "' + phrase + '": ' + str(totalCount)
					
###GLOBAL VARIABLES###
running = True
messageCount = 0

###SETUP###
skype = Skype4Py.Skype()
convo = None
for chat in skype.ActiveChats:
	#check that it is a group chat
	if len(chat.Members) > 2:
		convo = chat
skype.OnMessageStatus = Commands
skype.Attach()
print '\nBOT STARTED...\n'
while True:
    pass