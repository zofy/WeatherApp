import urllib2
import json

from sender import MailManager


# class Locator(object):
#     loc_url = "https://geoiptool.com"
#
#     def __init__(self, loc_data={}):
#         self.loc_data = loc_data
#
#     def __str__(self):
#         return self.loc_data
#
#     def get_location(self):
#         r = requests.get(self.loc_url)
#         soup = BeautifulSoup(r.content, "lxml")
#         items = soup.find_all('div', {"class": "data-item"})
#         for item in items:
#             spans = item.find_all('span')
#             category = str(spans[0].text)[:-1]
#             if category in ('Latitude', 'Longitude', 'City'):
#                 self.loc_data[category] = str(spans[1].text.strip())
#

class Analyzer(object):
    base = 'http://my.meteoblue.com/feed/json_7day_3h_firstday?apikey=sk489ywfh498hjf'

    def __init__(self, loc_dict):
        self.lat = loc_dict.get('lat')
        self.long = loc_dict.get('lng')
        self.city = loc_dict.get('city')

    def __str__(self):
        return 'Getting data for {lat: %s, long: %s, city: %s}' % (self.lat, self.long, self.city)

    def build_url(self):
        return self.base + '&lat=' + str(self.lat) + '&lon=' + str(self.long) + '&city=' + str(self.city)

    def get_data(self):
        meteo_url = self.build_url()
        json_data = urllib2.urlopen(meteo_url)
        data = json.load(json_data)
        return data


# l = Locator()
# print(l.loc_data)
# l.get_location()
# print(l.loc_data)

# data = l.loc_data
# a = Analyzer(data['Latitude'], data['Longitude'], data['City'])
# a = Analyzer()
# print(a)
# url = a.build_url()
# print(url)
#
# weather_data = a.get_data()
#
# print(weather_data)


# m = MailManager('zofy11@gmail.com', str(weather_data))
# m.login_to_server()
# m.send_forecast()
