import re
import requests

class CyberHouseClient:
    _name=''
    _logger=None
    def __init__(self, logger, url="http://localhost:8080/"):
        self._logger=logger
        self._url=url
        self._logger.info("Starting CyberHouseClient")

    def connect_cyberhouse(self):
        self._logger.info(self._name)
        return self._name

    def request(self, text):

        # api-endpoint [OpenAI GPT2 Scratch Pad](https://github.com/NaxAlpha/gpt-2xy)
        # docker run -p 18080:8080 --rm -d gpt-2xy
        URL = self._url

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'text':text}

        # sending get request and saving the response as response object
        r = requests.post(url = URL, data = PARAMS)

        data = r.content
        clean = data.decode("utf-8")
        self._logger.info(clean)
        # extracting data in json format
        '''
        data = r.json()


        # extracting latitude, longitude and formatted address
        # of the first matching location
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        formatted_address = data['results'][0]['formatted_address']

        # printing the output
        print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
              %(latitude, longitude,formatted_address))
        '''
        #clean_text = re.sub(r"[^A-Za-z0-9\s]+", "", data)
        #formatted_output = str(data).replace('\\n', '\n').replace('\\t', '\t')
        #clean_text = " ".join(formatted_output.split())

        #print_text(sample_text, clean_text)
        return clean
