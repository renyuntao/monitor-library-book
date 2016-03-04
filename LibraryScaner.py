#!/usr/bin/env python3.4

import subprocess
import urllib
import urllib.request
import urllib.error

URLFilePath = '/path/to/urls.txt'

# Open file that contain the urls
fin = open(URLFilePath)

# Read the urls to a list
urls = fin.readlines()

# Close the file
fin.close()

for line in urls:
	info = line.split(',')
	url = info[0]

	AddPrefix = False

	# If url do not have the prefix 'http://' or 'https://',
	# then add the prefix 'http://' to url
	if 'http://' not in url and 'https://' not in url:
		url = 'http://' + url
		AddPrefix = True

	# Check if the url is valid
	try:
		req = urllib.request.urlopen(url)
	except:
		print('Invalid URL')
		if AddPrefix:
			# Strip the prefix 'http://' of url
			url = url.lstrip('http://')

		# Delete the invalid url
		action = 's@.*' + url + '.*@@g'
		cmd = ['sed','-i']
		cmd.append(action)
		cmd.append(URLFilePath)
		subprocess.call(cmd)

		# Delete the empty line
		cmd = ['sed','-i','/^$/d']
		cmd.append(URLFilePath)
		subprocess.call(cmd)
		continue

	byte_content = req.read()
	try:
		content = byte_content.decode('utf-8')
	except UnicodeDecodeError:
		print('In UnicodeDecodeError')
		try:
			print('in inside try')
			content = byte_content.decode('cp936')
		except UnicodeDecodeError:
			print('UnicodeDecodeError again')
			continue
		

	print('after try')
	BookAvailable = False

	# Check if the book is available
	if '在架上' in content:
		BookAvailable = True
	# Have the possible of '非可借'
	elif '可借' in content:
		BookAvailable = True
	elif '在馆' in content:  
		BookAvailable = True
	else:
		pass

	# The book is available
	if BookAvailable:
		# Strip the newline character
		BookName = info[1]
		recipients = info[2].rstrip('\n')

		# Check if the BookName contain the '《' or '》'
		if '《' not in BookName:	
			BookName = '《' + BookName + '》'

		# Send Email command
		subject = BookName + '可借'
		MessageFile = '/path/to/MailMessage.txt'
		cmd = ['/path/to/SendMail.sh',subject,recipients,MessageFile]

		subprocess.call(cmd)
		print(BookName + '可借')

		if AddPrefix:
			url = url.lstrip('http://')

		# Delete the url that doesn't need monitor any more
		cmd = ['sed','-i']
		action = 's@.*' + url + '.*@@g'
		cmd.append(action)
		cmd.append(URLFilePath)
		subprocess.call(cmd)

		# Delete the empty line
		cmd = ['sed','-i','/^$/d']
		cmd.append(URLFilePath)
		subprocess.call(cmd)
