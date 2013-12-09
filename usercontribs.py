import requests
import csv
import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	separator = '\t'
	userheader = 'user'
	language = 'en'
	try:
		opts, args = getopt.getopt(argv,"hi:o:s:u:l:",["help","inputfile=","outputfile=","separator=","userheader=","language="])
	except getopt.GetoptError:
		print '''
	usage: usercontribs.py -i <inputfile> -o <outputfile> [-s <separator>] [-u <user header>] [-l <wikipedia language>]
	
	Type -h for help.
	'''
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print '''
	usage: usercontribs.py [-h] -i <inputfile> -o <outputfile> [-s <separator>] [-u <user header>] [-l <wikipedia language>]
		-i, --inputfile: path to your list of wikipedia users
		-o, --outputfile: name of the output file, the file is .tsv
		-s, --separator: set the separator in the input file, default: tab
		-u, --userheader: set the header of your users name list, default: user
		-l, --language: set the wikipedia language, default: en
	'''
			sys.exit()
		elif opt in ("-i", "--inputfile"):
			inputfile = arg
		elif opt in ("-o", "--outputfile"):
			outputfile = arg
		elif opt in ("-s", "--separator"):
			separator = arg
		elif opt in ("-u", "--userheader"):
			userheader = arg
		elif opt in ("-l", "--language"):
			language = arg

	data = csv.DictReader(open(inputfile, 'rb'), delimiter=separator, skipinitialspace=True)

	site_root = 'http://' + language + '.wikipedia.org/w/'
	site_api = site_root + 'api.php'
	site_diff_link = site_root + 'index.php?'

	query_params = {}
	query_params['action'] = 'query'
	query_params['list'] = 'usercontribs'
	query_params['ucdir'] = 'newer'
	query_params['uclimit'] = 500
	query_params['format'] = 'json'

	writer = csv.writer(open(outputfile, 'wb'), delimiter='\t', quotechar='"')

	# NOTE: headers are hardcoded because of not well formatted API response. see there -> http://www.mediawiki.org/wiki/API:Usercontribs
	headers = ['revid','timestamp','user','userid','parentid','title','pageid','ns','size','new','minor','bot','top','link','comment']
	edit_type = ['new','minor','bot','top']
	added_field = ['link']
	writer.writerow(headers)

	data = list(data)
	total = len(data)

	for i, line in enumerate(data):
		user = line[userheader]
		sys.stdout.write('\x1b[2K\r[' + str(i+1) + '/' + str(total) +'] ' + user)
		sys.stdout.flush()
		query_params['ucuser'] = user
		
		r = requests.get(site_api, params = query_params)
		results = r.json()['query']['usercontribs']
		for result in results:
			row = []
			for header in headers:
				try:
					if isinstance(result[header], int):
						row.append(result[header])
					else:
						if header in edit_type:
							row.append('true')
						else:
							row.append(result[header].encode("utf-8"))
				except:
					if header in edit_type:
						row.append('false')
					elif header in added_field:
						link = site_diff_link + 'title=' + result['title'] + '&diff=' + str(result['revid']) + '&oldid=prev'
						row.append(link)
					else:
						row.append('')
			
			writer.writerow(row)
	
	sys.stdout.write('\x1b[2K\r')
	sys.stdout.flush()
	sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])