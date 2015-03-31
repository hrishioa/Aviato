#from facebook import *
import requests, json, sys
<<<<<<< HEAD

verbose=True
=======
from nltk.stem import WordNetLemmatizer
import nltk

verbose=False

wordnet_lemmatizer = WordNetLemmatizer()
>>>>>>> 7beb4e0751c660d82b02727e9cddb3a37cdd4c7d

KBase = {}

keywords = ['Temple','Beach','Casino','Romance',
'History','Museum','Zoo','Spa','Shopping','Mall','Roller Coaster','Carnival','Skiing','Mountain','Hill',
'Trek','Run','Movie','Religion','Sports','Aquatic sports','Kayaking','snowboarding','snorkeling','diving',
'surfing','wind surfing','jet ski','yacht','temples','outdoor','outdoor sports','indoor sports','wildlife',
'city','urban exploration','hiking','swimming','climbing','mountains','camping','resorts','cruise']

parag_token = "CAAMUZAqD4ZBJgBAOaIayqKRsRrknvu4CWzB7cZAyfcdss8OaZCe1n7LPIH7gxorBUM5OmYmlWw24zN5S0UhzWJt8H9Ww2NRhJUg7ypTjfAZC89v0tGMyCk3txx5tdynQFjmDfUCb7DA7eZC2bGJW9FOIAG7eUrbWOf1DArU6SVDtAlUN0hn955KBYTWPOopliEwmI8oZCWbM5SzHkUGuMSv"

abdullah_token = "CAAMUZAqD4ZBJgBAL50Vt366K0vhU81D2jbKK9TE0IvZAQ99oaN7ENh7lI9X636Ker3vVQ4A8Uw6cWAylfVPwXt32cts57iEOdqTA4PXjGQshbKTtaJFICeIwiPbHPsEyPiLeoAvBmZAeRCDNmtojehUZCFpnCyiEZC6mzIy7ycSfcyM2ArA82t1IBeAFjg7eWoCaDgjemeXxlkJMkxasBK41xLmMVY9tUk08T3QzZBuMZBbMEY2b7aW9"

sean_token = "CAAMUZAqD4ZBJgBAA0mdnVBDDYaNPw4yoheBa7AEOKwRgKbZA4iiihmRyDzsRpe9E5LZBl6Ic0kaZCyH0ncvVk8sZCtN4R3F5ZBXB3vHh2aCnZCZCYQ0WzMIAaBYQzugJhdlbzmu1GjcLdKsm8gcQ2g9gMLtSsIDjdRsaZCiYaJRvPnoGRXDnZAratDToz2RMZB7qZAwWrWZCVarCn5IyXbQb6IjVGY"

token = "CAAMUZAqD4ZBJgBAM8cFZBP8adV7iNvNPmwaIJ3HEc5MMxwxo6DVxGo9i1ZBBZC5iCB8ZCHz8gZC7kzSvUsd7IrjwZBZClFZACbvS79kZCRw4LB11ZC1XPrO76eWDHstNyRWwGWGLE6FxtW2qoaBwwlFsApERbZAuTt7BerQrh0Q1D7dpZBlBDVDhhpYhWCJqpT338kc6HLJ8ZBxwb4JN5wUGZCNrrb2maWrgnncuAZCAZD"

deftoken = sean_token

out_filename = "Sean"

app_id = "866855950022808"
app_secret = "197e26da3c39b02f9f6a0882d78b8fe6"

if len(sys.argv)>1:
	if(sys.argv[1]=='-v'):
		print "Verbose on."
		verbose=True

if len(sys.argv)>2:
	if(sys.argv[2].isdigit()):
		choice = int(sys.argv[2])
		if(choice==1):
			deftoken = token
			out_filename = "hrishi"
		elif(choice==2):
			deftoken = parag_token
			out_filename = "parag"
		elif(choice==3):
			deftoken = sean_token
			out_filename = "sean"
		elif(choice==4):
			deftoken = abdullah_token
			out_filename = "Abdulla"
		print "User selected: %s" % out_filename
<<<<<<< HEAD
=======

#################################################

def getKWJSON(keywords=keywords):
	kw_json = {}

	tag = nltk.pos_tag(keywords)

	#build database
	for i in range(0,len(keywords)):
		#normalise, i.e. lemmatise and lowercase the keyword
		pos = 'v' if tag[i][1][0].lower()=='v' else 'n'
		norm_kw = str(wordnet_lemmatizer.lemmatize(keywords[i].lower(),pos=pos))
		kw_json[norm_kw] = 0
>>>>>>> 7beb4e0751c660d82b02727e9cddb3a37cdd4c7d

#################################################

def getKWJSON(keywords=keywords):
	return {'surf': 0, 'kayaking': 0, 'roller coaster': 0, 'cruise': 0, 'snowboard': 0, 'outdoor': 0, 'skiing': 0, 'run': 0, 'sport': 0, 'mountain': 0, 'resort': 0, 'movie': 0, 'museum': 0, 'aquatic sports': 0, 'camp': 0, 'zoo': 0, 'romance': 0, 'religion': 0, 'hill': 0, 'beach': 0, 'temple': 0, 'spa': 0, 'shopping': 0, 'city': 0, 'dive': 0, 'wildlife': 0, 'urban exploration': 0, 'snorkel': 0, 'outdoor sports': 0, 'trek': 0, 'carnival': 0, 'hike': 0, 'casino': 0, 'yacht': 0, 'wind surfing': 0, 'jet ski': 0, 'mall': 0, 'indoor sports': 0, 'climb': 0, 'swimming': 0, 'history': 0}

def load_KBase(filename):
	return true

def save_KBase(filename):
	return true

def getUser(token=deftoken):
	return getJSON('name',token)

def getJSON(fields, token=deftoken):
	base_url = 'https://graph.facebook.com/me'

	#Sample Fields
	#fields = 'id,name,albums.limit(5)'

	url = '%s?fields=%s&access_token=%s' % (base_url, fields, token)

	content = requests.get(url)
	content_json = json.loads(content.content)

	return content_json

###########################################################################

def getJSONFriend(fid,token=deftoken,page_size=100,after=None):
	url = 'https://graph.facebook.com/%s/photos?limit=%d&access_token=%s' % (fid,page_size,token)
	if(after!=None):
		url = url + '&after=%s' % after

	content = requests.get(url)

	data = json.loads(content.content)

	return data

def getFriendData(fid, token=deftoken, deepScrub=False):
	
	data = getJSONFriend(fid,token)

	db = {}
	db['base_id'] = fid
	db[fid] = {}
	db[fid]['location'] = {}

	while(True):
		try:
			numPhotos = len(data['data'])
		except:
			if(verbose==True):
				print "No photos found for user %s" % fid
			return db
		
		for i in range(0,numPhotos):
			try:
				db[fid]['location'][len(db[fid]['location'])] = data['data'][i]['place']
				if(verbose==True):
					print "Added location info for user %s" % (fid)
			except:
				continue

		try:
			if not('next' in data['paging']):
				if(verbose==True):
					print "No more pages. returning..."
				return db
		except:
			return db

		if(verbose==True):
			print "Found next page: %s" % data['paging']['next']
			data = json.loads(requests.get(data['paging']['next']).content)
			if(verbose==True):
				print "Got next page:"

<<<<<<< HEAD

def getData(token=deftoken,deepScrub=False):
	#first get user data
	base_user = getUser()

	#initialize database and add users
	db = {}
	db[base_user['id']] = {}
	db['base_id'] = base_user['id']
	db[base_user['id']]['profile'] = getJSON('')

=======

def getData(token=deftoken,deepScrub=False):
	#first get user data
	base_user = getUser()

	#initialize database and add users
	db = {}
	db[base_user['id']] = {}
	db['base_id'] = base_user['id']
	db[base_user['id']]['profile'] = getJSON('')

>>>>>>> 7beb4e0751c660d82b02727e9cddb3a37cdd4c7d
	db[base_user['id']]['keywords'] = getKWJSON()

	#Get Photos first to aggregate location data

	#pull photos in a paged fashion
	#photos per page
	ppp = page_size = 100

	#Null pointer value for the after pointer TODO investigate and change
	nullval = None
	db[base_user['id']]['location'] = {}
	loc_pointer = 0
	photos = getJSON('photos.limit('+str(ppp)+')', token)

	page = 0
	while(True):

		#Get the page
		if(page!=0):
			photos = getJSON('photos.limit('+str(ppp)+').after('+str(after_pointer)+')', token)

		after_pointer = photos['photos']['paging']['cursors']['after']
		page_size = len(photos['photos']['data'])

		if(verbose==True):
			print "Page "+str(page)+": Loaded "+str(page_size)+'photos. after = '+str(after_pointer)

		#perform actions with the data at hand
		for i in range(0,page_size):
			location = False

			try:
				location = photos['photos']['data'][i]['place']
			except:
				if(verbose==True):
					print "location data not found at "+str(i)

			if(location != False):
				#Location Data
				db[base_user['id']]['location'][loc_pointer]  = location
				loc_pointer+=1	

				#Also add the location to any people tagged here
				for k in range(0,len(photos['photos']['data'][i]['tags']['data'])):
					if not( 'id' in photos['photos']['data'][i]['tags']['data'][k]):
						if(verbose==True):
							print "Tagger: id not found."
						continue

					tagged_id = photos['photos']['data'][i]['tags']['data'][k]['id']
					if(tagged_id == db['base_id']):
						if(verbose==True):
							print "Tagger: tagged_id is the same as base_id, skipping"
						continue

					#check to see if the user is already present, if not create and add the location data
					if tagged_id not in db:
						if(verbose==True):
							print "Tagger: Creating new database"
						db[tagged_id] = {}
						db[tagged_id]['location'] = {} 
					else:
						if(verbose==True):
							print "Tagger: Found tagged id %s in database" % (tagged_id)

					db[tagged_id]['location'][len(db[tagged_id]['location'])] = location
					
					if(verbose==True):
						print "Successful tag added to %s" % (tagged_id)
			
			try:
				#Extract Keywords
				desc = photos['photos']['data'][i]['name']
				for key,value in db[base_user['id']]['keywords'].items():
					if key in desc:
						db[base_user['id']]['keywords'][key] += 1
			except:
				if(verbose==True):
					print "name data not found at "+str(i)

			try:
				#Extract comments
				comments_no = len(photos['photos']['data'][i]['comments']['data'])
				if(comments_no<1):
					continue
				all_comments = ""
				for j in range(0,comments_no):
					all_comments = all_comments+str(photos['photos']['data'][i]['comments']['data'][j]['message'])+" "
				for key,value in db[base_user['id']]['keywords'].items():
					if key in all_comments:
						db[base_user['id']]['keywords'][key] += 1
			except:
				if(verbose==True):
					print "Comment data not found at "+str(i)

		page+=1

		if(page_size<ppp or after_pointer == nullval):
			if(verbose==True):
				print "Page size is "+str(page_size)+". Qutting."
			break

	if(deepScrub==True):
		for key,value in db.items():
			if(key==db['base_id'] or key=='base_id' or value=='base_id'):
				continue
			if(verbose==True):
				print "Getting friend data for %s" % key
			deepdata = getFriendData(key,token)
			try:
				if(len(deepdata[deepdata['base_id']]['location'])>1):
					db[key] = db[key]+deepdata['base_id']['location']
			except:
				if(verbose==True):
					print "Exception in merging friend data"


	return db

def main():
	print "Program running..."

	print "Base User ID: %s" % (getUser()['id'])
	#print json.dumps(photos,indent=1)

	
	db = getData(deepScrub=True)

	if(verbose==True):
		print "Dumping data to %s." % (out_filename)

	if(out_filename!=None):
		outfile = open(out_filename+'_data.txt','w')
		outfile.write(str(json.dumps(db,indent=1)))
	
	print "Completed Execution."

	return

if __name__ == "__main__":
	main()
