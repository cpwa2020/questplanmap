import urllib.parse, urllib.request, urllib.error, json
bsrlp = "http://api.pugetsound.onebusaway.org/api/where/"
bsrls = ".json?key=TEST"
import geopy, folium
from geopy.geocoders import Nominatim
glctr = Nominatim(user_agent="map_plan")
mpmk = []

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

def tripsroute(aid,id,flnm='static/mpm.html',zms=10):
    fid = str(aid) + '_' + str(id)
    try:
        with urllib.request.urlopen(bsrlp+'trips-for-route/'+fid+bsrls) as rspn:
            rspndc = rspn.read().decode()
        rspnld = json.loads(rspndc)
    except urllib.error.URLError as er:
        print('The api might be unavailable now; Error code: '+str(er.code))
    dlr = rspnld['data']['list']
    if len(dlr) <= 0:
        return {'error: no applicable data':''}
    dct = {}
    for dn in dlr:
        ll = dn['status']['position']
        dct[dn['tripId']] = ll
    plc = rspnld['data']['list'][0]['status']['position']
    flm = folium.Map(location=[plc['lat'],plc['lon']],zoom_start=zms)
    for mk in mpmk:
        rvrk = str(glctr.reverse((mk[0],mk[1])))
        mkltln = rvrk+': ('+str(mk[0])+', '+str(mk[1])+')'
        flm.add_child(folium.Marker(location=[mk[0],mk[1]],popup=mkltln,icon=folium.Icon(color='orange',icon='home',prefix='fa')))
    for mm in dct:
        rvrm = str(glctr.reverse((dct[mm]['lat'],dct[mm]['lon'])))
        mmltln = rvrm+': ('+str(dct[mm]['lat'])+', '+str(dct[mm]['lon'])+')'
        flm.add_child(folium.Marker(location=[dct[mm]['lat'],dct[mm]['lon']],popup=mmltln,icon=folium.Icon(color='green',icon='bus',prefix='fa')))
    flm.save(outfile=flnm)
    return dct

def mapium(lat,lon,flnm='static/mpm.html',zms=15):
    rvr = str(glctr.reverse((lat,lon)))
    ltln = rvr+': ('+str(lat)+', '+str(lon)+')'
    mpm = folium.Map(location=[lat,lon],zoom_start=zms)
    for mk in mpmk:
        rvrk = str(glctr.reverse((mk[0],mk[1])))
        mkltln = rvrk+': ('+str(mk[0])+', '+str(mk[1])+')'
        mpm.add_child(folium.Marker(location=[mk[0],mk[1]],popup=mkltln,icon=folium.Icon(color='orange',icon='home', prefix='fa')))
    mpm.add_child(folium.Marker(location=[lat,lon],popup=ltln))
    mpm.save(outfile=flnm)

def svlctn(lctnh,lctns,lctnw,lctno=""):
    lcl = locals()
    ltl = []
    for lc in lcl:
        if lcl[lc] != '':
            ltl.append(lcl[lc])
    mpmk.clear()
    for lt in ltl:
        ltd = glctr.geocode(lt)
        mpmk.append((ltd.latitude, ltd.longitude))

# testing
#routesnear(url=True)
#routesnear(47.322323,-122.312622)
#routesnear(47.258728,-122.465973)
#routesnear(47.608013,-122.335167)
#tripsroute('40_590')
#mapium(47,-122)