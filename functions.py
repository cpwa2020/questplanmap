import urllib.parse, urllib.request, urllib.error, json
bsrlp = "http://api.pugetsound.onebusaway.org/api/where/"
bsrls = ".json?key=TEST"
import geopy, folium

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
    mapium(lat,lon)
    return dct

def tripsroute(id,flnm='static/mpm.html',zms=10):
    try:
        with urllib.request.urlopen(bsrlp+'trips-for-route/'+str(id)+bsrls) as rspn:
            rspndc = rspn.read().decode()
        rspnld = json.loads(rspndc)
    except urllib.error.URLError as er:
        print('The api might be unavailable now; Error code: '+str(er.code))
    dlr = rspnld['data']['list']
    dct = {}
    for dn in dlr:
        ll = dn['status']['position']
        dct[dn['tripId']] = ll
    plc = rspnld['data']['list'][0]['status']['position']
    flm = folium.Map(location=[plc['lat'],plc['lon']],zoom_start=zms)
    for mm in dct:
        flm.add_child(folium.Marker(location=[dct[mm]['lat'],dct[mm]['lon']]))
    flm.save(outfile=flnm)
    return dct

def mapium(lat,lon,flnm='static/mpm.html',zms=15):
    mpm = folium.Map(location=[lat,lon],zoom_start=zms)
    mpm.add_child(folium.Marker(location=[lat,lon]))
    mpm.save(outfile=flnm)

# testing
#routesnear(url=True)
#routesnear(47.322323,-122.312622)
#routesnear(47.258728,-122.465973)
#routesnear(47.608013,-122.335167)
#tripsroute('40_590')
#mapium(47,-122)