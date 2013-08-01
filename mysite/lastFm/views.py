# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection,transaction
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# import datetime,time
import xml.etree.ElementTree as ET
import urllib,urllib2,json,httplib2,xmltodict,urlparse,random
# import pylast
import py7D

SPLIT_BAR = '|'
LOVE_KEY = '1'
HATE_KEY = '2'
CYCLE_KEY = '3'
SKIP_KEY = '4'

#7digital configuration
DATA_SOURCE_PERFIX = 'http://api.7digital.com/1.2/'
oauth_consumer_key='7d8vzkxr4dh6'
oauth_consumer_secret='7yqsh4f7y2ftxpze'

#lastFm configuration
LASTFM_API_KEY = "fc2da26a4bf1a511281e242d53dc1cfc" 
LASTFM_API_SECRET = "86e9fe3f56355580d4af27ce526e3cd0"
# lastfm_username = "SylvainCheung"
# lastfm_password_hash = pylast.md5("Jacknife540")

# NETWORK = pylast.LastFMNetwork(api_key = LASTFM_API_KEY, api_secret = LASTFM_API_SECRET, username = lastfm_username, password_hash = lastfm_password_hash)
# COUNTRY = pylast.Country('china',NETWORK)

def getTrack(request):
    lastfm_title,lastfm_artist = getHotTracks()
    query = lastfm_title + ' ' + lastfm_artist
    query = query.replace(' ','%20')
    track_id,artist_name,title = trackQueryHelper(query)
    if track_id == "":
        return HttpResponse(0)
    else:
        preview_url = py7D.preview_url(track_id)
        getTrackTags(artist_name, title, track_id)
        isLove = checkIfLove(request.user,track_id)
        if isLove is True:
            love_flag = '1'
        else:
            love_flag = '0'
        return HttpResponse(preview_url + SPLIT_BAR + artist_name + SPLIT_BAR + title + SPLIT_BAR + track_id + SPLIT_BAR + SPLIT_BAR + love_flag)

def getHotTracks():
    url = "http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=china&limit=40&api_key=" + LASTFM_API_KEY
    http_response, content = httplib2.Http().request(url)
    doc = ET.fromstring(content)
    random_rank = str(random.randint(1,40))
    for track in doc.iter('track'):
        if track.get('rank') == random_rank:
            title = track.find('name').text
            artist = track.find('artist').find('name').text
            break
    return title,artist

def searchTrack(request):
    query = request.GET['query']
    query = query.replace(' ','%20')
    track_id,artist_name,title = trackQueryHelper(query)
    if track_id == "":
        return HttpResponse(0)
    else:
        preview_url = py7D.preview_url(track_id)
        getTrackTags(artist_name, title, track_id)
        isLove = checkIfLove(request.user,track_id)
        if isLove is True:
            love_flag = '1'
        else:
            love_flag = '0'
        return HttpResponse(preview_url + SPLIT_BAR + artist_name + SPLIT_BAR + title + SPLIT_BAR + track_id + SPLIT_BAR + SPLIT_BAR + love_flag)

def trackQueryHelper(queryString):
    url = DATA_SOURCE_PERFIX + "track/search?q=" + queryString + "&oauth_consumer_key=" + oauth_consumer_key +"&country=GB&streamable=true&page=1&pagesize=1"
    print url
    http_response, content = httplib2.Http().request(url)
    api_response = xmltodict.parse(content, xml_attribs=True)
    result_count = api_response['response']['searchResults']['totalItems']
    if result_count == '0':
        track_id = ""
        artist_name = ""
        title = ""
        # cover_img = ""
        return track_id,artist_name,title
    else:
        track_id = api_response['response']['searchResults']['searchResult']['track']['@id']
        artist_name = api_response['response']['searchResults']['searchResult']['track']['artist']['name']
        title = api_response['response']['searchResults']['searchResult']['track']['title']
        # cover_img = api_response['response']['searchResults']['searchResult']['track']['release']['image']
        return track_id,artist_name,title

def getRecommendation(request):
    cur_title = request.GET['curTitle']
    cur_artist = request.GET['curArtist']
    last_title,last_artist = getSimilarTrack(cur_title,cur_artist)
    query = queryAppender(last_title,last_artist)
    track_id,artist_name,title = trackQueryHelper(query)
    if track_id == "":
        return HttpResponse(0)
    else:
        preview_url = py7D.preview_url(track_id)
        getTrackTags(artist_name, title, track_id)
        isLove = checkIfLove(request.user,track_id)
        if isLove is True:
            love_flag = '1'
        else:
            love_flag = '0'
        return HttpResponse(preview_url + SPLIT_BAR + artist_name + SPLIT_BAR + title + SPLIT_BAR + track_id + SPLIT_BAR + SPLIT_BAR + love_flag)
    return HttpRespons(preview_url)

def getSimilarTrack(qTitle,qArtist):
    qTitle = qTitle.replace(' ','%20')
    qArtist = qArtist.replace(' ','%20')
    match_point = 0
    while ( match_point <= 0.4):
        match_point = random.random()
    print "===============getSimilar match_point=" + str(match_point)
    find_flag = 0
    url = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=" + qArtist + "&track=" + qTitle + "&limit=30" + "&api_key=" + LASTFM_API_KEY
    print url
    http_response, content = httplib2.Http().request(url)
    doc = ET.fromstring(content)
    element = doc.find('similartracks').find('track')
    if element is None:
        title,artist = getHotTracks()
    else:
        while(find_flag == 0):
            for track in doc.iter('track'):
                if track.find('match').text <= str(match_point):
                    title = track.find('name').text
                    artist = track.find('artist').find('name').text
                    find_flag = 1
                    break
            match_point = match_point + 0.2
    return title,artist

def getHotList(request):
    url = "http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=china&limit=18&api_key=" + LASTFM_API_KEY
    http_response, content = httplib2.Http().request(url)
    doc = ET.fromstring(content)
    info = []
    for track in doc.iter('track'):
        info.append(track.find('name').text + SPLIT_BAR + track.find('artist').find('name').text + '&p&')
    return HttpResponse(info)

def getFavList(request):
    cursor = connection.cursor()
    username = request.GET['username']
    user_id = str(getMyUserId(username,cursor))
    sql = "select title,artist from track_info where track_id in (select track_id from user_behavior where user_id = " + user_id +" and status_id = 1)"
    print sql
    re = cursor.execute(sql).fetchall()
    i = 0
    data = []
    for row in re:
        data.append(row[0] + SPLIT_BAR + row[1] + '&p&')
        i = i + 1
    i = str(i)
    data.append('&Count=' + i)
    connection.close()
    print data
    return HttpResponse(data)

def queryAppender(arg1, arg2):
    arg = arg1 + ' ' + arg2
    arg = arg.replace(' ','%20')
    return arg

def getTrackTags(artist, title, track_id):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql1 = "select * from track_info where track_id=" + track_id
    cursor.execute(sql1)
    if cursor.fetchall():
        connection.close()
    else:
        artist = artist.replace(' ','%20')
        title = title.replace(' ','%20')
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&api_key=" + LASTFM_API_KEY + "&artist=" + artist + "&track=" + title + "&autocorrect[1]"
        print url
        http_response, content1 = httplib2.Http().request(url)
        doc1 = ET.fromstring(content1)
        artist = artist.replace('%20',' ')
        title = title.replace('%20',' ')
        tag_info = {}
        i = 0
        tag_info[0] = 'null'
        tag_info[1] = 'null'
        tag_info[2] = 'null'
        element = doc1.find('toptags').find('tag')
        if element is None:
            tag_info[0] = 'null'
            tag_info[1] = 'null'
            tag_info[2] = 'null'
        else:
            for tag in doc1.iter('tag'):
                if i > 2:
                    break
                else:
                    tag_info[i] = tag.find('name').text
                    i = i + 1
        title = title.replace('"','')
        artist = artist.replace('"','')
        sql = 'insert into track_info values(' + track_id + ',"' + title + '","' + artist + '","' + tag_info[0] + '","' + tag_info[1] + '","' + tag_info[2] + '",null,null,null)'
        print sql
        cursor.execute(sql)
        if transaction.is_dirty():
            transaction.commit()
        connection.close()

def tagGetTopTrack(tag):
    tag = tag.replace(' ','%20')
    url = "http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&limit=40&tag=" + tag + "&api_key=" + LASTFM_API_KEY
    print url
    http_response, content = httplib2.Http().request(url)
    doc = ET.fromstring(content)
    random_rank = str(random.randint(1,40))
    for track in doc.iter('track'):
        if track.get('rank') == random_rank:
            title = track.find('name').text
            artist = track.find('artist').find('name').text
            break
    return title,artist

def love(request):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    track_id = request.GET['track_id']
    username = request.GET['username']
    user_id = str(getMyUserId(username,cursor))
    print "===========start insert btn-action============"
    exist = checkExist(user_id,track_id,cursor)
    if exist is True:
        connection.close
        return HttpResponse(0)
    else:
        sql = 'insert into user_behavior values(' + user_id + ',' + track_id + ',' + LOVE_KEY + ',null,null,null)'
        print sql
        cursor.execute(sql)
        if transaction.is_dirty():
            transaction.commit()
        connection.close
        return HttpResponse(0)

def hate(request):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    track_id = request.GET['track_id']
    username = request.GET['username']
    user_id = str(getMyUserId(username,cursor))
    print "===========start insert btn-action============"
    exist = checkExist(user_id,track_id,cursor)
    if exist is True:
        connection.close
        return HttpResponse(0)
    else:
        sql = 'insert into user_behavior values(' + user_id + ',' + track_id + ',' + HATE_KEY + ',null,null,null)'
        print sql
        cursor.execute(sql)
        if transaction.is_dirty():
            transaction.commit()
        connection.close
        return HttpResponse(0)

def skip(request):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    track_id = request.GET['track_id']
    username = request.GET['username']
    user_id = str(getMyUserId(username,cursor))
    print "===========start insert btn-action============"
    exist = checkExist(user_id,track_id,cursor)
    if exist is True:
        connection.close
        return HttpResponse(0)
    else:
        sql = 'insert into user_behavior values(' + user_id + ',' + track_id + ',' + SKIP_KEY + ',null,null,null)'
        print sql
        cursor.execute(sql)
        if transaction.is_dirty():
            transaction.commit()
        connection.close
        return HttpResponse(0)

def cycle(request):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    track_id = request.GET['track_id']
    username = request.GET['username']
    user_id = str(getMyUserId(username,cursor))
    print "===========start insert btn-action============"
    exist = checkExist(user_id,track_id,cursor)
    if exist is True:
        connection.close
        return HttpResponse(0)
    else:
        sql = 'insert into user_behavior values(' + user_id + ',' + track_id + ',' + CYCLE_KEY + ',null,null,null)'
        print sql
        cursor.execute(sql)
        if transaction.is_dirty():
            transaction.commit()
        connection.close
        return HttpResponse(0)

def getMyUserId(username,cursor):
    sql = "select id from auth_user where username='" + username + "'"
    print sql
    cursor.execute(sql)
    user_id = cursor.fetchone()[0]
    return user_id

def checkExist(user_id,track_id,cursor):
    sql = "select user_id from user_behavior where user_id=" + user_id + " and track_id=" + track_id
    print sql
    cursor.execute(sql)
    re = cursor.fetchone()
    print re
    if re is None:
        return False
    else:
        return True

def checkIfLove(user, track_id):
    cursor = connection.cursor()
    user_id = getMyUserId(user.username,cursor)
    sql = "select * from user_behavior where user_id=" + str(user_id) + " and track_id=" + str(track_id) + " and status_id=1"
    print sql
    cursor.execute(sql)
    re = cursor.fetchone() 
    if re is None:
        isLove = False
    else:
        isLove = True
    connection.close
    return isLove

def cancelLove(request):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    track_id = request.GET['track_id']
    username = request.GET['username']
    user_id = str(getMyUserId(username,cursor))
    sql = 'delete from user_behavior where user_id=' + user_id + ' and track_id=' + track_id + ' and status_id=1'
    print sql
    cursor.execute(sql)
    if transaction.is_dirty():
        transaction.commit()
    connection.close
    return HttpResponse(0)