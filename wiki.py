from bs4 import BeautifulSoup
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}


class Wikipedia:
    title: str
    lang: str
    headers: dict
    paragraphs: list
    infobox: dict

    def __init__(self, title: str, length=10) -> None:
        self.title = title
        self.length = length
        self.paragraphs = []
        self.infobox = {}

    def __str__(self) -> str:
        """
        Return a string representation of an instance of this class
        """
        return f'Title: {self.title}'

    def __repr__(self) -> str:
        """
        Return a string representation of an instance of this class
        """
        return self.__str__()

    def clean(self) -> None:
        """
        Removes any unnecessary data from self.paragraphs
        """
        while '' in self.paragraphs:
            self.paragraphs.pop(self.paragraphs.index(''))

    def request(self) -> dict:
        """
        Return a dictionary containing the necessary data from a
        specific wikipedia article
        """
        url = "https://en.wikipedia.org/wiki/" + self.title.replace('%20', '_')
        page = requests.get(url, headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="firstHeading")

        paragraphs = soup.find(id="bodyContent").find_all("p")
        for para in paragraphs[:self.length]:
            self.paragraphs.append(para.get_text().strip())

        if 'Other reasons this message may be displayed:' in self.paragraphs:
            return {'status': 0}

        infobox = soup.find(id='bodyContent').findAll('tr')
        for info in infobox[:30]:
            th = info.find('th')
            td = info.find('td')
            try:
                if th and td:
                    self.infobox[th.text.strip()] = td.text.strip()
            except:
                return {'status': 0}

        self.title = title.string.strip()
        self.clean()
        return {
            'status': 1,
            "Title": self.title,
            'paragraphs': self.paragraphs,
            'infobox': self.infobox
        }
