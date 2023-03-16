import urllib.parse, urllib.request, urllib.error, json
bsrlp = "http://api.pugetsound.onebusaway.org/api/where/"
bsrls = ".json?key=TEST"

def routesnear(lat=47.653435,lon=-122.305641,url=False,id=True,aid=True):
    try:
        with urllib.request.urlopen(bsrlp+'routes-for-location'+bsrls+'&lat='+str(lat)+'&lon='+str(lon)) as rspn:
            rspndc = rspn.read().decode()
        rspnld = json.loads(rspndc)
    except urllib.error.URLError as er:
        print('The api might be unavailable now; Error code: '+str(er.code))
    dlr = rspnld['data']['list']
    dct = []
    for dn in dlr:
        if id:
            idtx = ' ('+dn['id']+'): '
        else:
            idtx = ': '
        if aid:
            aidtx = ' ('+dn['agencyId']+')'
        else:
            aidtx = ''
        if dn['description'] == '':
            dntx = '[no description]'
        else:
            dntx = dn['description']
        dct.append(dn['shortName']+idtx+dntx+aidtx)
        if url:
            if (dn['url'] != ''):
                dct.append('link: '+dn['url'])
    return dct

def tripsroute(id):
    try:
        with urllib.request.urlopen(bsrlp+'trips-for-route/'+id+bsrls) as rspn:
            rspndc = rspn.read().decode()
        rspnld = json.loads(rspndc)
    except urllib.error.URLError as er:
        print('The api might be unavailable now; Error code: '+str(er.code))
    dlr = rspnld['data']['list']
    dct = {}
    for dn in dlr:
        ll = dn['status']['position']
        dct[dn['tripId']] = ll
    return dct

# testing
#routesnear(url=True)
#routesnear(47.322323,-122.312622)
#routesnear(47.258728,-122.465973)
#routesnear(47.608013,-122.335167)