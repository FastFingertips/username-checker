from urllib.request import Request, urlopen
from urllib.error import HTTPError
import sys

class bcolors: # # define ANSI escape sequences for colored output
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

sites = {
    "Bitbucket":"https://bitbucket.org/<username>/",
    "Github":"https://github.com/<username>/",
    "Twitter":"https://twitter.com/<username>/",
    "Instagram":"https://instagram.com/<username>/",
    "Medium":"https://medium.com/@<username>/",
    "Reddit":"https://www.reddit.com/user/<username>/",
    "Facebook":"http://facebook.com/<username>/",
    "Last.fm":"https://www.last.fm/user/<username>/",
    'Letterboxd':'https://letterboxd.com/<username>/',
    "Trakt.tv":"https://trakt.tv/users/<username>/",
    "IMDB":"https://www.imdb.com/name/<username>/",
    "Goodreads":"https://www.goodreads.com/user/show/<username>/",
    "Pinterest":"https://www.pinterest.com/<username>/",
    "Tumblr":"https://<username>.tumblr.com/",
    "Twitch":"https://www.twitch.tv/<username>/",
    "Youtube":"https://www.youtube.com/user/<username>/",
    "Vimeo":"https://vimeo.com/<username>/",
    "Soundcloud":"https://soundcloud.com/<username>/",
    "Twitch.tv":"https://www.twitch.tv/<username>/",
    "Gitlab":"https://gitlab.com/<username>/",
    "Steam":"https://steamcommunity.com/id/<username>/",
    "Data.world":"https://data.world/<username>/",
    # Sites behaving inconsistently
    # "Netflix":"https://www.netflix.com/browse/my-list/<username>/",
    # "Spotify":"https://open.spotify.com/user/<username>/",
    }

responseReasons = {
    200:'   Already Taken   ',
    403:'     Forbidden     ',
    404:'     Available     ',
    503:'Service Unavailable'}

def checkSites(sites, username=None):
    if username == None:
        username = input("Enter username: ")

    print(f"Checking for availability of {username}, please wait...")    

    longestSiteName = max(len(name) for name in sites.keys())

    for site in sites:
        print(f"{site} {' '*(longestSiteName-len(site))}", end='')
        url = sites[site].replace("<username>",username)
        request = Request(url, None, {'User-Agent': 'FastFingertips'}) 
        parse(request, username) 

def middleware(request, username):
    try:
        response = urlopen(request)
    except HTTPError as e:
        if e.code == 404:
            return (404, "Available")
        else:
            return (e.code, e.reason)
    else:
        if response.getcode() == 200:
            return (200, "Already exists")

# used for generating colored responses
def parse(request, username):
    response = middleware(request, username)
    responseCode = response[0]
    responseReason = responseReasons[response[0]]
    longestSiteUrl = max(len(url) for url in sites.values())
    fullUrl = request.get_full_url()
    whiteSpaces = ' '*(longestSiteUrl-len(fullUrl)-5)
    terminalMsg = f'[{responseCode}] {fullUrl}{whiteSpaces} ({responseReason})'


    if response[0] == 200:
        print(f"{bcolors.FAIL}{terminalMsg}{bcolors.ENDC}")
    elif response[0] == 404:
        print(f"{bcolors.OKGREEN}{terminalMsg}{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}{terminalMsg}{bcolors.ENDC}")


if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except:
        username = None
    checkSites(sites, username)