import urllib
import json
import urllib2
from bs4 import BeautifulSoup
import re

def get_rt_results(query):
  key = '8xqcbp2rqrq4df4t98rzcqnh'
  url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=" + key + "&q=" + query + "&page_limit=1"
  result = json.load(urllib.urlopen(url))
  result_count = len(result['movies'])
  review_url = result['movies'][0]['links']['reviews'] + '?apikey=' + key
  review_result = json.load(urllib.urlopen(review_url))
  return({'critic_agg': result['movies'][0]['ratings']['critics_score'],
      'audience_agg': result['movies'][0]['ratings']['audience_score'], 'full':
      result, 'reviews': review_result['reviews'], 'name':
      review_result['links']['alternate'].split('/')[4]})

def get_imdb_results(query):
  url = "http://imdbapi.org/?title=" + query + "&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0"
  result = json.load(urllib.urlopen(url))
  return(result[0]['rating',result])

def get_rt_redirect(id, opener):
  response = opener.open('http://www.rottentomatoes.com/m/' + id)
  return(response.geturl())


def Find(data,review):
      match=re.search(data,review)
      if match:
          numscore=float(match.group(3))/10
          revtext=match.group(5)
          return({"numscore": numscore, "revtext": revtext})
      else:
          print 'not found'
          return({})

def reviewparse(response):
    soup = BeautifulSoup(response.read())
    #soup.find_all(class_='user_review')
    #(this returns 20 reviews, I'm just going to work with one. You'll need a "for" loop)
    #rev = str(soup.find_all(class_='user_review')[0])
    #remove whitespace so it looks nicer
    regex = re.compile(r'[\n\r\t]')
    #clean = regex.sub(' ', str(rev))
    #print(clean)
    revtotal=soup.find_all(class_='user_review')
    cleantotal=[]
    for i in range(0,len(revtotal)):
        dirty = regex.sub(' ', str(revtotal[i]))
        data=r'(stars)\s(score)(\d+)("></span></div>)\s+(.+)\s+(</div>)'
        cleantotal.append(Find(data, dirty))
    return(cleantotal)

def process_single_user_review_div(div):
  #regex = re.compile(r'[\n\r\t]')
  #clean = regex.sub(' ', str(rev))
  return(str(div))

def get_rt_user_reviews(name):
  # So this is really hacky. From the get_rt_results method we get the ID of the 
  # movie, which is a long number. What we want is the movie's key (a version
  # of the name. So we ping the server with the ID, it redirects to the key,
  # and voila.
  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  #correct_url = get_rt_redirect(id, opener)
  response = opener.open('http://www.rottentomatoes.com/m/' + name + '/reviews/?type=user')
  return(reviewparse(response))

def get_everything_from_rt(query):
  rt_results = get_rt_results(query)
  user_reviews = get_rt_user_reviews(rt_results['name'])

  return([rt_results, user_reviews])


