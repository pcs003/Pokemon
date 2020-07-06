from flask import Flask, request, jsonify
import json
import base64
import re
import string
import sqlite3
app = Flask(__name__)

class File:
	filedata = ''
	fileid = ''
	alreadyparsed = False
	dropped = False

print("Starting Pokemon Server!")
# Listen for post requests
@app.route('/', methods=['GET', 'POST'])
def server():
	conn = connect('/home/ec2-user/Pokemon/pokemon.db')
	curs = conn.cursor()
	if request.method == 'POST':
		print("detected post request")
		requestdata = request.get_json()
		# if fileids is in data
		if requestdata.get('fileids') != None:
			print("detected fileids in form data")
			fileids = requestdata.get('fileids')
			# TODO query database and find which file ids needed
			for f in fileids:
				print(type(f))
				print(f)
				statement = "SELECT ReplayID FROM replays WHERE FileID=" + 

			data = {
				'log': 'Received post request and fileids',
				'idsneeded': fileids
			}
			return jsonify(data)

		# if files and neededids are in data
		elif (requestdata.get('files') != None and
				requestdata.get('idsneeded') != None):
			print("detected files and idsneeded in form data")
			files = requestdata.get('files')
			idsneeded = requestdata.get('idsneeded')
			return decodeandparse(files, idsneeded)			

		else:
			print("did not detect fileids, files, idsneeded in form data")
			# TODO change to sending back a status code as well
			data = {
				'log': 'Received post request but did not find fileids or (files and idsneeded)'
			}
			return jsonify(data)

	# TODO change to sending back a status code as well
	print("did not detect post request")
	data = {
		'log': 'Did not receive post request'
	}
	return jsonify(data)


def decodeandparse(files, idsneeded):
	# decode files to string
	decodedfiles = []
	printable = set(string.printable)
	for i in range(len(files)):
		newfile = File()
		replay = base64.b64decode(files[i]).decode("utf-8")
		# replace non ascii characters
		newfile.filedata = ''.join(filter(lambda x: x in printable, replay))
		newfile.fileid = idsneeded[i]
		decodedfiles.append(newfile)

	# Parse files for replayid
	filestoparse = []
	for d in decodedfiles:
		# get replayid
		if re.search('(?<=gen[0-9]ou-)[0-9]+', d.filedata) != None:
			replayid = re.search('(?<=gen[0-9]ou-)[0-9]+', d.filedata).group(0)	
			# Query database to see if this replayid wasn't already parsed
			if True:
				# add file to filestoparse
				filestoparse.append(d)
			else:
				# set alreadyparsed flag to true
				d.alreadyparsed = True
		else:
			# Replayid wasn't found
			d.dropped = True
		print(replayid)

	# Calculate stats for filestoparse
	for f in filestoparse:
		calculatestats(f)

	# calculate stats for log statement
	parsedids = []
	alreadyparsed = []
	droppedfiles = []
	for d in decodedfiles:
		if not d.alreadyparsed and not d.dropped:
			parsedids.append(d.fileid)
		elif d.alreadyparsed:
			alreadyparsed.append(d.fileid)
		elif d.dropped:
			droppedfiles.append(d)
	logstring = 'Updated replays with fileids: ' + ' '.join(parsedids) \
	+ ' ignored replays with fileids: ' + ' '.join(alreadyparsed) \
	+ ' could not parse: ' + str(len(droppedfiles)) + ' files'
	data = {
		'log': logstring
	}
	return jsonify(data)

# Calculates stats for a file
def calculatestats(f):
	print("put stats code here")
	# return f in case 


if __name__ == "__main__":
    app.run(host='0.0.0.0')
