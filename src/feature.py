import ipaddress
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class FeatureExtraction:
    def __init__(self, url):
        self.features = []
        self.url = url
        self.domain = ""
        self.urlparse = ""
        self.response = ""
        self.soup = ""

        try:
            self.response = requests.get(url, timeout=3)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except:
            pass

        try:
            self.urlparse = urlparse(url)
            self.domain = self.urlparse.netloc
        except:
            pass

        # Generate all 31 features to match the trained model
        self.features.append(self.UsingIP())
        self.features.append(self.longUrl())
        self.features.append(self.shortUrl())
        self.features.append(self.symbol())
        self.features.append(self.redirecting())
        self.features.append(self.prefixSuffix())
        self.features.append(self.SubDomains())
        self.features.append(self.Hppts())
        self.features.append(self.DomainRegLen())
        self.features.append(self.Favicon())
        self.features.append(self.NonStdPort())
        self.features.append(self.HTTPSDomainURL())
        self.features.append(self.RequestURL())
        self.features.append(self.AnchorURL())
        self.features.append(self.LinksInScriptTags())
        self.features.append(self.ServerFormHandler())
        self.features.append(self.InfoEmail())
        self.features.append(self.AbnormalURL())
        self.features.append(self.WebsiteForwarding())
        self.features.append(self.StatusBarCust())
        self.features.append(self.DisableRightClick())
        self.features.append(self.UsingPopupWindow())
        self.features.append(self.IframeRedirection())
        self.features.append(self.AgeofDomain())
        self.features.append(self.DNSRecording())
        self.features.append(self.WebsiteTraffic())
        self.features.append(self.PageRank())
        self.features.append(self.GoogleIndex())
        self.features.append(self.LinksPointingToPage())
        self.features.append(self.StatsReport())
        # Add one more feature to make it 31 total
        self.features.append(self.URLLength())

    # 1. UsingIP
    def UsingIP(self):
        try:
            ipaddress.ip_address(self.domain)
            return -1
        except:
            return 1

    # 2. longUrl
    def longUrl(self):
        if len(self.url) < 54:
            return 1
        if len(self.url) >= 54 and len(self.url) <= 75:
            return 0
        return -1

    # 3. shortUrl
    def shortUrl(self):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', self.url)
        if match:
            return -1
        return 1

    # 4. Symbol@
    def symbol(self):
        if re.findall("@", self.url):
            return -1
        return 1
    
    # 5. Redirecting//
    def redirecting(self):
        if self.url.rfind('//')>6:
            return -1
        return 1
    
    # 6. prefixSuffix
    def prefixSuffix(self):
        try:
            match = re.findall('\-', self.domain)
            if match:
                return -1
            return 1
        except:
            return -1
    
    # 7. SubDomains
    def SubDomains(self):
        dot_count = len(re.findall("\.", self.url))
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1

    # 8. HTTPS
    def Hppts(self):
        try:
            https = self.urlparse.scheme
            if 'https' in https:
                return 1
            return -1
        except:
            return 1

    # 9. DomainRegLen (simplified)
    def DomainRegLen(self):
        return 0  # Default neutral value

    # 10. Favicon (simplified)
    def Favicon(self):
        try:
            if self.soup and self.soup.find('link', rel='icon'):
                return 1
            return -1
        except:
            return -1

    # 11. NonStdPort
    def NonStdPort(self):
        try:
            port = self.domain.split(":")
            if len(port) > 1:
                return -1
            return 1
        except:
            return 1

    # 12. HTTPSDomainURL
    def HTTPSDomainURL(self):
        try:
            if 'https' in self.domain:
                return -1
            return 1
        except:
            return 1

    # 13. RequestURL (simplified)
    def RequestURL(self):
        return 1  # Default safe

    # 14. AnchorURL (simplified)
    def AnchorURL(self):
        return 0  # Default neutral

    # 15. LinksInScriptTags (simplified)
    def LinksInScriptTags(self):
        return 0  # Default neutral

    # 16. ServerFormHandler (simplified)
    def ServerFormHandler(self):
        return -1  # Default suspicious

    # 17. InfoEmail (simplified)
    def InfoEmail(self):
        return 1  # Default safe

    # 18. AbnormalURL
    def AbnormalURL(self):
        return 1  # Default safe

    # 19. WebsiteForwarding (simplified)
    def WebsiteForwarding(self):
        return 0  # Default neutral

    # 20. StatusBarCust (simplified)
    def StatusBarCust(self):
        return 1  # Default safe

    # 21. DisableRightClick (simplified)
    def DisableRightClick(self):
        return 1  # Default safe

    # 22. UsingPopupWindow (simplified)
    def UsingPopupWindow(self):
        return 1  # Default safe

    # 23. IframeRedirection (simplified)
    def IframeRedirection(self):
        return 1  # Default safe

    # 24. AgeofDomain (simplified)
    def AgeofDomain(self):
        return -1  # Default suspicious

    # 25. DNSRecording (simplified)
    def DNSRecording(self):
        return -1  # Default suspicious

    # 26. WebsiteTraffic (simplified)
    def WebsiteTraffic(self):
        return 0  # Default neutral

    # 27. PageRank (simplified)
    def PageRank(self):
        return -1  # Default suspicious

    # 28. GoogleIndex (simplified)
    def GoogleIndex(self):
        return 1  # Default safe

    # 29. LinksPointingToPage (simplified)
    def LinksPointingToPage(self):
        return 1  # Default safe

    # 30. StatsReport (simplified)
    def StatsReport(self):
        return 1  # Default safe

    # 31. URLLength (additional feature to make 31 total)
    def URLLength(self):
        return len(self.url)

    def getFeaturesList(self):
        return self.features

# Keep the simplified functions for backward compatibility
def extract_features(url):
    """Extract features using FeatureExtraction class"""
    extractor = FeatureExtraction(url)
    return extractor.getFeaturesList()