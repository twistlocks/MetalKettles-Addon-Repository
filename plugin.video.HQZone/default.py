import urllib,urllib2,re,cookielib,string,os,xbmc, xbmcgui, xbmcaddon, xbmcplugin, random
from t0mm0.common.net import Net as net

addon_id        = 'plugin.video.HQZone'
selfAddon       = xbmcaddon.Addon(id=addon_id)
datapath        = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
cookie_file     = os.path.join(os.path.join(datapath,''), 'hqzone.lwp')
user            = selfAddon.getSetting('hqusername')
passw           = selfAddon.getSetting('hqpassword')

if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('HQZone', 'Please enter your HQZone account details','or register if you dont have an account','at www.HQZone.Tv','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter Username')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            username=search
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                search = keyb.getText()
                password=search
                selfAddon.setSetting('hqusername',username)
                selfAddon.setSetting('hqpassword',password)
user = selfAddon.getSetting('hqusername')
passw = selfAddon.getSetting('hqpassword')

#############################################################################################################################

def setCookie(srDomain):
        html = net().http_GET(srDomain).content
        r = re.findall(r'<input type="hidden" name="(.+?)" value="(.+?)" />', html, re.I)
        post_data = {}
        post_data['amember_login'] = user
        post_data['amember_pass'] = passw
        for name, value in r:
            post_data[name] = value
        net().http_GET('https://www.rarehost.net/amember/member')
        net().http_POST('https://www.rarehost.net/amember/member',post_data)
        net().save_cookies(cookie_file)
        net().set_cookies(cookie_file)

def Index():
    setCookie('https://www.rarehost.net/amember/member')
    response = net().http_GET('https://www.rarehost.net/amember/member')
    if not 'Edit Profile' in response.content:
        dialog = xbmcgui.Dialog()
        dialog.ok('HQZone', 'Invalid login','Please check your HQZone account details in Add-on settings','')
        quit()
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    notification('HQZone', 'Login Successful', '2000',icon)
    xbmc.sleep(1000)
    free=re.compile('<li><a href="(.+?)">Free Streams</a>').findall(link)[0]
    addDir('[COLOR greenyellow]Free[/COLOR] Streams','https://www.rarehost.net/amember/free/free.php',2,icon,fanart)
    vip=re.compile('<li><a href="(.+?)">VIP Streams</a>').findall(link)
    if len(vip)>0:
        vip=vip[0]
        addDir('[COLOR gold]VIP[/COLOR] Streams','https://www.rarehost.net/amember/vip/vip.php',2,icon,fanart)
        addDir('[COLOR gold]VIP[/COLOR] VOD','url',4,icon,fanart)
    addLink(' ','url','mode',icon,fanart)
    addLink('[COLOR blue]Twitter[/COLOR] Feed','url',100,icon,fanart)
    addDir('HQZone Account Status','url',200,icon,fanart)
    addLink('HQ Zone Support','url',300,icon,fanart)

def getchannels(url):
    if 'vip' in url:baseurl = 'https://www.rarehost.net/amember/vip/'
    else:baseurl = 'https://www.rarehost.net/amember/free/'
    setCookie('https://www.rarehost.net/amember/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('<a href="(.+?)"></br><font color= "\#fff" size="\+1"><b>(.+?)</b>').findall(link)
    for url,channel in match:
        url = baseurl+url
        addLink(channel,url,3,icon,fanart)

def getstreams(url,name):
    setCookie('https://www.rarehost.net/amember/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    swf='http://p.jwpcdn.com/6/11/jwplayer.flash.swf'
    strurl=re.compile("file: '(.+?)',").findall(link)[0]
    playable = strurl+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    try:
        xbmc.Player ().play(playable, liz, False)
    except:
        pass
   
def account():
    setCookie('https://www.rarehost.net/amember/member')
    response = net().http_GET('https://www.rarehost.net/amember/member')
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    stat = ''
    user=re.compile('<div class="am-user-identity-block">(.+?)<').findall(link)[0]
    user = user+'\n'+' '
    accnt=re.compile('<li><strong>(.+?)</strong>(.+?)</li>').findall(link)
    for one,two in accnt:
        one = '[COLOR blue]'+one+'[/COLOR]'
        stat = stat+' '+one+' '+two+'\n'
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]HQZone Account Status[/COLOR]', '',stat,'')
    quit()

def support():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]HQZone Account Support[/COLOR]', 'For account queries please contact us at:','@HQZoneTV (via Twitter)','HQZone@hotmail.com (via Email)')
    quit()
       
def vod():
    setCookie('https://www.rarehost.net/amember/member')
    response = net().http_GET('https://rarehost.net/amember/vip/vod.php')
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    print link
    match=re.compile('<a href="(.+?)"></br><font color= "\#fff" size="\+1"><b>(.+?)</b>').findall(link)
    addDir('HQ Movies','http://movieshd.co/search/2014',50,icon,fanart)
    for url,channel in match:
        channel = channel+'[COLOR red][I] - Coming Soon[/I][/COLOR]'
        url = 'https://rarehost.net'+url
        if not 'Movies' in channel:
            if not 'TV' in channel:
                addLink(channel,'url','1000',icon,fanart)
    
def getmovies(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in match:
                name2 = name.decode("ascii","ignore").replace('&#8217;','').replace('&amp;','').replace('&#8211;','').replace('#038;','')
                if not 'razor' in name2:
                        if not 'Rls' in name2:
                                if not 'DCMA' in name2:
                                        if not 'Privacy' in name2:
                                                if not 'FAQ' in name2:
                                                        if not 'Download' in name2:
                                                                addLink(name2,url,51,icon,fanart)
        match=re.compile('<a class="next page-numbers" href="(.+?)">Next videos &raquo;</a>').findall(link)
        if len(match)>0:
                addDir('Next Page>>',match[0],50,icon,fanart)

def playmovies(name,url):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('src="http://videomega.tv/validatehash.php\?hashkey=(.+?)">').findall(link)
            if len(match)==0:
                match=re.compile("src=\'http://videomega.tv/validatehash.php\?hashkey=(.+?)\'>").findall(link)
            videomega_id_url = "http://videomega.tv/validatehash.php?hashkey="+ match[0]  
            req = urllib2.Request(videomega_id_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('var ref="(.+?)";').findall(link)
            vididresolved = match[0]
            videomega_url = 'http://videomega.tv/iframe.php?ref='+vididresolved
        except:
               req = urllib2.Request(url)
               req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
               response = urllib2.urlopen(req)
               link=response.read()
               response.close()
               match=re.compile("ref=\'(.+?)'").findall(link)
               if (len(match) > 0):
                        videomega_url = "http://videomega.tv/iframe.php?ref=" + match[2]
                        print videomega_url
               if (len(match) == 0):
                        match=re.compile("frameborder='.+?' src='(.+?)?").findall(link)
                        videomega_url = match[0]
        req = urllib2.Request(videomega_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        url = re.compile('document.write.unescape."(.+?)"').findall(link)[0]
        url = urllib.unquote(url)
        stream_url = re.compile('file: "(.+?)"').findall(url)[0]
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(stream_url, liz, False)

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

def twitter():
        text=''
        twit = 'http://twitrss.me/twitter_user_to_rss/?user=@HQZoneTv'
        twit += '?%d' % (random.randint(1, 1000000000000000000000000000000000000000))
        response = net().http_GET(twit)
        link = response.content
        match=re.compile("<description><!\[CDATA\[(.+?)\]\]></description>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)
        for status, dte in match:
            status = cleanHex(status)
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            dte = dte.replace('+0000','').replace('2014','').replace('2015','')
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('[COLOR blue][B]@HQZoneTv[/B][/COLOR]', text)
        quit()

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
              
params=get_params(); url=None; name=None; mode=None; iconimage=None
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass

print "Mode: "+str(mode); print "Name: "+str(name); print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:Index()

elif mode==2:getchannels(url)
elif mode==3:getstreams(url,name)
elif mode==4:vod()

elif mode==50:getmovies(url)
elif mode==51:playmovies(name,url)

elif mode==100:twitter()
elif mode==200:account()
elif mode==300:support()


        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

