import os 
import re 
import certifi
import airportsdata
import pycountry 
from dotenv import load_dotenv

load_dotenv()
os.environ["SSL_CERT_FILE"]=certifi.where()
os.environ["REQUESTS_CA_BUNDLE"]=certifi.where()

API_KEY=os.getenv("AVIATIONSTACK_API_KEY")

DEFAULT_ORIGIN_IATA=os.getenv("DEFAULT_ORIGIN_IATA ","DELHI")

BASE_URL="https://api.aviationstack.com/v1"
AIRPORTS=airportsdata.load("IATA")
COUNTRY_ALIASES = {
    # United States
    "usa": "US",
    "u.s.a": "US",
    "u.s.": "US",
    "us": "US",
    "united states": "US",
    "united states of america": "US",
    "america": "US",

    # United Kingdom
    "uk": "GB",
    "u.k.": "GB",
    "great britain": "GB",
    "britain": "GB",
    "england": "GB",
    "united kingdom": "GB",

    # United Arab Emirates
    "uae": "AE",
    "u.a.e.": "AE",
    "united arab emirates": "AE",

    # South Korea
    "south korea": "KR",
    "republic of korea": "KR",
    "korea": "KR",
    "rok": "KR",

    # North Korea
    "north korea": "KP",
    "dprk": "KP",
    "democratic people's republic of korea": "KP",

    # Russia
    "russia": "RU",
    "russian federation": "RU",

    # China
    "china": "CN",
    "people's republic of china": "CN",
    "pr china": "CN",
    "prc": "CN",

    # Taiwan
    "taiwan": "TW",
    "republic of china": "TW",

    # Czech Republic
    "czech republic": "CZ",
    "czechia": "CZ",

    # Netherlands
    "netherlands": "NL",
    "holland": "NL",

    # Vietnam
    "vietnam": "VN",
    "viet nam": "VN",

    # Turkey
    "turkey": "TR",
    "türkiye": "TR",

    # Iran
    "iran": "IR",
    "islamic republic of iran": "IR",

    # Syria
    "syria": "SY",
    "syrian arab republic": "SY",

    # Palestine
    "palestine": "PS",
    "state of palestine": "PS",

    # Hong Kong
    "hong kong": "HK",
    "hong kong sar": "HK",

    # Macau
    "macau": "MO",
    "macao": "MO",

    # India
    "india": "IN",
    "bharat": "IN",

    # Germany
    "germany": "DE",
    "deutschland": "DE",

    # Japan
    "japan": "JP",
    "nippon": "JP",
    "nihon": "JP",

    # Brazil
    "brazil": "BR",
    "brasil": "BR",

    # Canada
    "canada": "CA",

    # Australia
    "australia": "AU",

    # New Zealand
    "new zealand": "NZ",

    # France
    "france": "FR",

    # Italy
    "italy": "IT",

    # Spain
    "spain": "ES",

    # Portugal
    "portugal": "PT",

    # Mexico
    "mexico": "MX",

    # Singapore
    "singapore": "SG",

    # Malaysia
    "malaysia": "MY",

    # Thailand
    "thailand": "TH",

    # Indonesia
    "indonesia": "ID",

    # Philippines
    "philippines": "PH",

    # Sri Lanka
    "sri lanka": "LK",

    # Nepal
    "nepal": "NP",

    # Bangladesh
    "bangladesh": "BD",

    # Pakistan
    "pakistan": "PK",

    # Afghanistan
    "afghanistan": "AF",

    # Saudi Arabia
    "saudi arabia": "SA",

    # Qatar
    "qatar": "QA",

    # Oman
    "oman": "OM",

    # Kuwait
    "kuwait": "KW",

    # Bahrain
    "bahrain": "BH",

    # Egypt
    "egypt": "EG",

    # South Africa
    "south africa": "ZA",

    # Nigeria
    "nigeria": "NG",

    # Kenya
    "kenya": "KE",

    # Argentina
    "argentina": "AR",

    # Chile
    "chile": "CL",

    # Colombia
    "colombia": "CO",

    # Peru
    "peru": "PE",

    # Switzerland
    "switzerland": "CH",

    # Sweden
    "sweden": "SE",

    # Norway
    "norway": "NO",

    # Denmark
    "denmark": "DK",

    # Finland
    "finland": "FI",

    # Ireland
    "ireland": "IE",

    # Belgium
    "belgium": "BE",

    # Austria
    "austria": "AT",

    # Poland
    "poland": "PL",

    # Greece
    "greece": "GR",
}
COUNTRY_MAIN_AIRPORT = {
    # Asia
    "IN": "DEL",   # India - Delhi
    "CN": "PEK",   # China - Beijing
    "JP": "NRT",   # Japan - Tokyo Narita
    "KR": "ICN",   # South Korea - Incheon
    "SG": "SIN",   # Singapore - Changi
    "MY": "KUL",   # Malaysia - Kuala Lumpur
    "TH": "BKK",   # Thailand - Bangkok
    "ID": "CGK",   # Indonesia - Jakarta
    "PH": "MNL",   # Philippines - Manila
    "VN": "SGN",   # Vietnam - Ho Chi Minh City
    "BD": "DAC",   # Bangladesh - Dhaka
    "PK": "ISB",   # Pakistan - Islamabad
    "NP": "KTM",   # Nepal - Kathmandu
    "LK": "CMB",   # Sri Lanka - Colombo
    "AE": "DXB",   # UAE - Dubai
    "SA": "RUH",   # Saudi Arabia - Riyadh
    "QA": "DOH",   # Qatar - Doha
    "KW": "KWI",   # Kuwait
    "OM": "MCT",   # Oman - Muscat
    "BH": "BAH",   # Bahrain

    # Europe
    "GB": "LHR",   # United Kingdom - London Heathrow
    "FR": "CDG",   # France - Paris Charles de Gaulle
    "DE": "FRA",   # Germany - Frankfurt
    "IT": "FCO",   # Italy - Rome
    "ES": "MAD",   # Spain - Madrid
    "PT": "LIS",   # Portugal - Lisbon
    "NL": "AMS",   # Netherlands - Amsterdam
    "CH": "ZRH",   # Switzerland - Zurich
    "AT": "VIE",   # Austria - Vienna
    "BE": "BRU",   # Belgium - Brussels
    "SE": "ARN",   # Sweden - Stockholm
    "NO": "OSL",   # Norway - Oslo
    "DK": "CPH",   # Denmark - Copenhagen
    "FI": "HEL",   # Finland - Helsinki
    "IE": "DUB",   # Ireland - Dublin
    "PL": "WAW",   # Poland - Warsaw
    "CZ": "PRG",   # Czech Republic
    "GR": "ATH",   # Greece - Athens
    "RU": "SVO",   # Russia - Moscow Sheremetyevo

    # North America
    "US": "JFK",   # United States - New York JFK
    "CA": "YYZ",   # Canada - Toronto Pearson
    "MX": "MEX",   # Mexico - Mexico City

    # South America
    "BR": "GRU",   # Brazil - São Paulo
    "AR": "EZE",   # Argentina - Buenos Aires
    "CL": "SCL",   # Chile - Santiago
    "CO": "BOG",   # Colombia - Bogotá
    "PE": "LIM",   # Peru - Lima

    # Africa
    "ZA": "JNB",   # South Africa - Johannesburg
    "EG": "CAI",   # Egypt - Cairo
    "KE": "NBO",   # Kenya - Nairobi
    "NG": "LOS",   # Nigeria - Lagos
    "MA": "CMN",   # Morocco - Casablanca

    # Oceania
    "AU": "SYD",   # Australia - Sydney
    "NZ": "AKL",   # New Zealand - Auckland
}
CITY_MAIN_AIRPORT = {
    # India
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "hyderabad": "HYD",
    "chennai": "MAA",
    "kolkata": "CCU",
    "pune": "PNQ",
    "ahmedabad": "AMD",
    "goa": "GOI",
    "jaipur": "JAI",
    "kochi": "COK",
    "lucknow": "LKO",
    "chandigarh": "IXC",
    "varanasi": "VNS",
    "amritsar": "ATQ",
    "bhubaneswar": "BBI",
    "indore": "IDR",
    "nagpur": "NAG",
    "patna": "PAT",
    "srinagar": "SXR",

    # USA
    "new york": "JFK",
    "los angeles": "LAX",
    "chicago": "ORD",
    "san francisco": "SFO",
    "washington": "IAD",
    "miami": "MIA",
    "seattle": "SEA",
    "las vegas": "LAS",
    "boston": "BOS",
    "orlando": "MCO",
    "dallas": "DFW",
    "houston": "IAH",

    # UK
    "london": "LHR",
    "manchester": "MAN",
    "edinburgh": "EDI",
    "birmingham": "BHX",

    # France
    "paris": "CDG",
    "nice": "NCE",
    "lyon": "LYS",

    # Germany
    "berlin": "BER",
    "frankfurt": "FRA",
    "munich": "MUC",

    # Italy
    "rome": "FCO",
    "milan": "MXP",
    "venice": "VCE",

    # Spain
    "madrid": "MAD",
    "barcelona": "BCN",

    # Netherlands
    "amsterdam": "AMS",

    # Switzerland
    "zurich": "ZRH",
    "geneva": "GVA",

    # UAE
    "dubai": "DXB",
    "abu dhabi": "AUH",

    # Qatar
    "doha": "DOH",

    # Saudi Arabia
    "riyadh": "RUH",
    "jeddah": "JED",

    # Singapore
    "singapore": "SIN",

    # Malaysia
    "kuala lumpur": "KUL",

    # Thailand
    "bangkok": "BKK",
    "phuket": "HKT",

    # Indonesia
    "jakarta": "CGK",
    "bali": "DPS",
    "denpasar": "DPS",

    # Vietnam
    "ho chi minh city": "SGN",
    "hanoi": "HAN",

    # Japan
    "tokyo": "HND",
    "osaka": "KIX",
    "kyoto": "KIX",
    "nagoya": "NGO",

    # South Korea
    "seoul": "ICN",
    "busan": "PUS",

    # China
    "beijing": "PEK",
    "shanghai": "PVG",
    "guangzhou": "CAN",
    "shenzhen": "SZX",

    # Hong Kong
    "hong kong": "HKG",

    # Taiwan
    "taipei": "TPE",

    # Australia
    "sydney": "SYD",
    "melbourne": "MEL",
    "brisbane": "BNE",
    "perth": "PER",

    # New Zealand
    "auckland": "AKL",
    "christchurch": "CHC",

    # Canada
    "toronto": "YYZ",
    "vancouver": "YVR",
    "montreal": "YUL",

    # Brazil
    "sao paulo": "GRU",
    "rio de janeiro": "GIG",

    # Argentina
    "buenos aires": "EZE",

    # South Africa
    "johannesburg": "JNB",
    "cape town": "CPT",

    # Egypt
    "cairo": "CAI",

    # Kenya
    "nairobi": "NBO",

    # Turkey
    "istanbul": "IST",

    # Russia
    "moscow": "SVO",

    # Nepal
    "kathmandu": "KTM",

    # Bangladesh
    "dhaka": "DAC",

    # Sri Lanka
    "colombo": "CMB",
}
def clean_text(text:str)->str:
    text =text.lower().strip()
    text=re.sub(r"[^a-z0-9\s]"," ",text)
    text=re.sub(r"\s+"," ",text)
    stop_words=[
        "flight","flights","tickets","trip","travel"
        ,"plan","complete","days","day","including","hotel",
        "hotels","sightseeing","under","budget","info","information"
    ]
    words=[w for  w in text.split() if w not in stop_words]
    return " ".join(words).strip()
def country_name_to_code(text: str):
    text = clean_text(text)

    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass

    # Detect country name inside longer text
    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2

    for alias, code in COUNTRY_ALIASES.items():
        if alias in text:
            return code

    return None

