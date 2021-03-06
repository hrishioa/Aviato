#from facebook import *
import requests, json
from nltk.stem import WordNetLemmatizer
import nltk

verbose = False

out_filename = "Hrishi"

wordnet_lemmatizer = WordNetLemmatizer()

KBase = {}

keywords = ['Temple','Beach','Casino','Romance',
'History','Museum','Zoo','Spa','Shopping','Mall','Roller Coaster','Carnival','Skiing','Mountain','Hill',
'Trek','Run','Movie','Religion','Sports','Aquatic sports','Kayaking','snowboarding','snorkeling','diving',
'surfing','wind surfing','jet ski','yacht','temples','outdoor','outdoor sports','indoor sports','wildlife',
'city','urban exploration','hiking','swimming','climbing','mountains','camping','resorts','cruise']

parag_token = "CAAMUZAqD4ZBJgBAOaIayqKRsRrknvu4CWzB7cZAyfcdss8OaZCe1n7LPIH7gxorBUM5OmYmlWw24zN5S0UhzWJt8H9Ww2NRhJUg7ypTjfAZC89v0tGMyCk3txx5tdynQFjmDfUCb7DA7eZC2bGJW9FOIAG7eUrbWOf1DArU6SVDtAlUN0hn955KBYTWPOopliEwmI8oZCWbM5SzHkUGuMSv"

abdullah_token = "CAAMUZAqD4ZBJgBAAFo2RPL9C99iMuCZBvOMemmvp3OaI05oYSx2e3X2ruS5A5g8Gy2xVJJdf8zjMkfLCjs3a92xRCC08xYIODSjLcUsaQvvm4hTaDfF9ryfxCFnrMS3gN8NxtJmUtQFKTZB9BqLeaf4yP5fcJRNY3Bl0sz50TVGkZCKPrA79vkdzLwZBTrvlCL4tAYryfyYvm30EZBcD2Cl"

sean_token = "CAAMUZAqD4ZBJgBAA0mdnVBDDYaNPw4yoheBa7AEOKwRgKbZA4iiihmRyDzsRpe9E5LZBl6Ic0kaZCyH0ncvVk8sZCtN4R3F5ZBXB3vHh2aCnZCZCYQ0WzMIAaBYQzugJhdlbzmu1GjcLdKsm8gcQ2g9gMLtSsIDjdRsaZCiYaJRvPnoGRXDnZAratDToz2RMZB7qZAwWrWZCVarCn5IyXbQb6IjVGY"

token = "CAAMUZAqD4ZBJgBAM8cFZBP8adV7iNvNPmwaIJ3HEc5MMxwxo6DVxGo9i1ZBBZC5iCB8ZCHz8gZC7kzSvUsd7IrjwZBZClFZACbvS79kZCRw4LB11ZC1XPrO76eWDHstNyRWwGWGLE6FxtW2qoaBwwlFsApERbZAuTt7BerQrh0Q1D7dpZBlBDVDhhpYhWCJqpT338kc6HLJ8ZBxwb4JN5wUGZCNrrb2maWrgnncuAZCAZD"

token = token

app_id = "866855950022808"
app_secret = "197e26da3c39b02f9f6a0882d78b8fe6"

#################################################

def getKWJSON(keywords):
	kw_json = {}

	tag = nltk.pos_tag(keywords)

	#build database
	for i in range(0,len(keywords)):
		#normalise, i.e. lemmatise and lowercase the keyword
		pos = 'v' if tag[i][1][0].lower()=='v' else 'n'
		norm_kw = str(wordnet_lemmatizer.lemmatize(keywords[i].lower(),pos=pos))
		kw_json[norm_kw] = 0

	#Json Created
	if(verbose==True):
		print kw_json

	return kw_json

def load_KBase(filename):
	return true

def save_KBase(filename):
	return true

def getJSON(fields, token):
	base_url = 'https://graph.facebook.com/me'

	#Sample Fields
	#fields = 'id,name,albums.limit(5)'

	url = '%s?fields=%s&access_token=%s' % (base_url, fields, token)

	content = requests.get(url)
	content_json = json.loads(content.content)

	return content_json

def getLocations():
	#Get Photos first to aggregate location data

	#pull photos in a paged fashion
	#photos per page
	ppp = page_size = 100

	#Null pointer value for the after pointer TODO investigate and change
	nullval = None
	locations = {}
	locations['name'] = {}
	loc_pointer = 0
	photos = getJSON('photos.limit('+str(ppp)+')')

	page = 0
	while(True):

		#Get the page
		if(page!=0):
			photos = getJSON('photos.limit('+str(ppp)+').after('+str(after_pointer)+')')

		after_pointer = photos['photos']['paging']['cursors']['after']
		page_size = len(photos['photos']['data'])

		if(verbose==True):
			print "Page "+str(page)+": Loaded "+str(page_size)+'photos. after = '+str(after_pointer)

		#perform actions with the data at hand
		for i in range(0,page_size):
			try:
				locations[loc_pointer]  = photos['photos']['data'][i]['place']
				loc_pointer+=1
			except:
				if(verbose==True):
					print "No location data found at "+str(i)

		page+=1

		if(page_size<ppp or after_pointer == nullval):
			if(verbose==True):
				print "Page size is "+str(page_size)+". Qutting."
			break

	return locations

def getLoc_and_Meta(token):
	#Get Photos first to aggregate location data

	#pull photos in a paged fashion
	#photos per page
	ppp = page_size = 100

	#Null pointer value for the after pointer TODO investigate and change
	nullval = None
	locations = {}
	locations['name'] = {}
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
			try:
				#Location Data
				locations[loc_pointer]  = photos['photos']['data'][i]['place']
				loc_pointer+=1
			except:
				if(verbose==True):
					print "location data not found at "+str(i)

			try:
				#Extract Keywords
				desc = photos['photos']['data'][i]['name']
				for key,value in kw_json.items():
					if key in desc:
						kw_json[key] += 1
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
				for key,value in kw_json.items():
					if key in all_comments:
						kw_json[key] += 1
			except:
				if(verbose==True):
					print "Comment data not found at "+str(i)

		page+=1

		if(page_size<ppp or after_pointer == nullval):
			if(verbose==True):
				print "Page size is "+str(page_size)+". Qutting."
			break

	return locations

###########################################################################

def main():
	print "Program running..."


	#print json.dumps(photos,indent=1)

	kw_json = getKWJSON(keywords)

	locations = getLoc_and_Meta()

	if(out_filename!=None):
		outfile = open(out_filename+'_loc.txt','w')
		outfile.write(str(json.dumps(locations,indent=1)))
		outfile = open(out_filename+'_nlp.txt','w')
		outfile.write(str(json.dumps(kw_json,indent=1)))

	print len(locations)
	return

if __name__ == "__main__":
	main()
