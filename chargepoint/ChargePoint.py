#!/usr/bin/env python
from suds.client import Client
from suds.wsse import Security, UsernameToken


class ChargePointAPIAccount(object):
    '''
    Account Information
    '''
    def __init__(self, key, pw, url):
        self.client=Client(url)
        self.security=Security()
        self.security.tokens.append(UsernameToken(key,pw))
        self.client.set_options(wsse=self.security)


class StationInformation(ChargePointAPIAccount):
    '''
    Access the ChargePoint Network Station Information API
    '''
    def __init__(   self, key, pw,
                    url='https://webservices.chargepointportal.net:8081/coulomb_api_1.1.wsdl'):
        ChargePointAPIAccount.__init__(self,key,pw,url)

    def SearchByZipCode(self, ZipCode='93906', Proximity=1.5, ProximityUnit='M'):
        searchRequest = self.client.factory.create('stationSearchRequest')
        searchRequest.postalCode=ZipCode
        searchRequest.Proximity=Proximity
        searchRequest.proximityUnit=ProximityUnit
        reply=self.client.service.getAllUSStations(searchRequest)
        #needs error checking by response code
        stationsInZipCode=[]
        for station in reply.stationData:
            print station.postalCode
            if station.postalCode == ZipCode:
                stationsInZipCode.append(station)

        return stationsInZipCode

    def SearchByGeo(self, Latitude='36.673192', Longitude = '-121.605089', Proximity=20, ProximityUnit='M'):
        searchRequest = self.client.factory.create('stationSearchRequest')
        searchRequest.Geo.lat=Latitude
        searchRequest.Geo.long=Longitude
        searchRequest.Proximity=Proximity
        searchRequest.proximityUnit=ProximityUnit
        reply=self.client.service.getAllUSStations(searchRequest)
        #needs error checking by response code

        stationsByGeo=[]
        for station in reply:
            
            stationsByGeo.append(station)

        return stationsByGeo


if __name__ == "__main__":
    import ConfigParser
    try:
        Config = ConfigParser.ConfigParser()
        Config.read('./hcc.conf')
        key=Config.get('Account', 'key')
        pw=Config.get('Account', 'password')
        url=Config.get('Account', 'url')
    except:
        print "Exception parsing config file"

    s=StationInformation(key,pw)

 #   results= s.SearchByZipCode('93906',20)
 #   print 'Length of result '+str(len(results))
 #   print '*******'

    results = s.SearchByGeo()
    for l in results:
        print l
        print '*******'
