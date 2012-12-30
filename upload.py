# -*- coding: utf-8 -*-
import wikiUpload
import os
import sys
from wikiConf import conf
'''
upload.py - i-ghost
Requires: Python 2.6 and http://upload.gaiatools.com/files/wikitools_mod_5.7z
Uploads PNGs in /png and categorises them based on class names.
'''

if len(sys.argv) < 2:
	sys.exit("""This script simply uploads all files found in /png
	
Specify misc to categorise uploads as misc images, or anything else
to categorise as a hat upload. The script will determine if the file
is a painted variant and upload it as such.

Specify ignore if you want to use your own summary.
	
Examples: 'upload.py misc' or 'upload.py ignore "My description"'
	
Adjust line 61 of this script if overwriting images.""")
type = sys.argv[1]

DEBUG = False

l = []
classes = [
		'Scout',
		'Soldier',
		'Pyro',
		'Demoman',
		'Heavy',
		'Engineer',
		'Medic',
		'Sniper',
		'Spy',
		]
#build list of files in /png
for i in os.listdir('png'):
	if i[-4:] != '.png':
		continue
	l.append(i)
	
spew = sys.stdout
try:
	sys.stdout = open(os.devnull, 'w')
	w = wikiUpload.wikiUploader(conf['wikiUser'], conf['wikiPass'], conf['wikiAPI'])
	sys.stdout = spew
except:
	sys.stdout = spew
	sys.exit('Couldn\'t login.')


def upload(file, content):
	print 'Uploading %s...' % (file)
	if DEBUG:
		print '\n' + content
	sys.stdout = open(os.devnull, 'w')
	w.upload('png\\' + file, file, pagecontent=content) #append ',overwrite=True, reupload=True' if reuploading
	sys.stdout = spew

uString = ''
#iterate over sorted list and upload
for i in sorted(l):
	if type.upper() == 'IGNORE':
		try:
			uString = sys.argv[2]
		except:
			pass
		upload(i, uString)
	elif type.upper() == 'MISC':
		if 'painted'.upper() not in i.upper(): # it's not a painted variant
			uString = '{{ScreenshotTF2}}\n[[Category:Misc images]]\n' # base string
			for x in classes:
				if x.upper() in i.upper(): #if we find a class name, categorise it
					uString += '[[Category:%s images]]\n' % (x)
					sx = False
					while not sx:
						try:
							upload(i, uString)
							sx = True
						except:
							pass
		else: #it's a painted misc variant, so add the correct template
			uString = '{{subst:pid|misc}}'
			sx = False
			while not sx:
				try:
					upload(i, uString)
					sx = True
				except:
					pass
	else: #not a misc
		if 'painted'.upper() not in i.upper():
			uString = '{{ScreenshotTF2}}\n[[Category:Hat images]]\n'
			for x in classes:
				if x.upper() in i.upper():
					uString += '[[Category:%s images]]\n' % (x)
					sx = False
					while not sx:
						try:
							upload(i, uString)
							sx = True
						except:
							pass
		else: #it's a painted hat variant, so add the correct template
			uString = '{{subst:pid}}'
			sx = False
			while not sx:
				try:
					upload(i, uString)
					sx = True
				except:
					pass
print '\n\nAll done.'