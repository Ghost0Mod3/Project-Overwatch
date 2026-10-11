"""
Project Overwatch
RSS Source Registry

URLs are assembled from separate pieces to prevent chat software
from converting addresses into HTML anchor tags.
"""


# ============================================================
# URL BUILDERS
# ============================================================

def secure_url(host, path=""):
    """
    Build an HTTPS URL from separate pieces.
    """

    return (
        "https"
        + "://"
        + str(host).strip()
        + str(path).strip()
    )


def google_news_url(query):
    """
    Build a Google News RSS search feed.

    Example:
        when:24h+Ukraine+missile
    """

    return (
        secure_url(
            "news.google.com",
            "/rss/search"
        )
        + "?q="
        + str(query).strip()
        + "&hl=en-US"
        + "&gl=US"
        + "&ceid=US:en"
    )


# ============================================================
# SOURCE RECORD BUILDER
# ============================================================

def source(
    name,
    category,
    region,
    url,
    aggregated=False,
    enabled=True,
    trust_score=50
):
    """
    Create one standardized Overwatch source record.
    """

    return {
        "name": str(name).strip(),
        "category": str(category).strip().upper(),
        "region": str(region).strip().upper(),
        "url": str(url).strip(),
        "aggregated": bool(aggregated),
        "enabled": bool(enabled),
        "trust_score": int(trust_score)
    }


# ============================================================
# DIRECT RSS SOURCES
# ============================================================

DIRECT_FEEDS = [

    # Global

    source(
        "BBC News",
        "WORLD",
        "GLOBAL",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "BBC World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "Al Jazeera English",
        "WORLD",
        "GLOBAL",
        secure_url(
            "www.aljazeera.com",
            "/xml/rss/all.xml"
        ),
        trust_score=86
    ),

    source(
        "Deutsche Welle All News",
        "WORLD",
        "GLOBAL",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-all"
        ),
        trust_score=88
    ),

    source(
        "Deutsche Welle World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-world"
        ),
        trust_score=88
    ),

    source(
        "France 24",
        "WORLD",
        "GLOBAL",
        secure_url(
            "www.france24.com",
            "/en/rss"
        ),
        trust_score=86
    ),

    source(
        "France 24 Live News",
        "BREAKING",
        "GLOBAL",
        secure_url(
            "www.france24.com",
            "/en/live-news/rss"
        ),
        trust_score=84
    ),

    source(
        "The Guardian World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "www.theguardian.com",
            "/world/rss"
        ),
        trust_score=84
    ),

    source(
        "New York Times World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "rss.nytimes.com",
            "/services/xml/rss/nyt/World.xml"
        ),
        trust_score=86
    ),

    source(
        "Washington Post World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "feeds.washingtonpost.com",
            "/rss/world"
        ),
        trust_score=84
    ),

    source(
        "Wall Street Journal World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "feeds.content.dowjones.io",
            "/public/rss/RSSWorldNews"
        ),
        trust_score=85
    ),

    source(
        "Sky News World",
        "WORLD",
        "GLOBAL",
        secure_url(
            "feeds.skynews.com",
            "/feeds/rss/world.xml"
        ),
        trust_score=82
    ),

    source(
        "South China Morning Post",
        "WORLD",
        "ASIA",
        secure_url(
            "www.scmp.com",
            "/rss/91/feed/"
        ),
        trust_score=80
    ),

    source(
        "ABC Australia",
        "WORLD",
        "OCEANIA",
        secure_url(
            "www.abc.net.au",
            "/news/feed/45910/rss.xml"
        ),
        trust_score=88
    ),

    source(
        "CBC News",
        "WORLD",
        "CANADA",
        secure_url(
            "www.cbc.ca",
            "/webfeed/rss/rss-topstories"
        ),
        trust_score=87
    ),

    source(
        "Times of India",
        "WORLD",
        "SOUTH ASIA",
        secure_url(
            "timesofindia.indiatimes.com",
            "/rssfeedstopstories.cms"
        ),
        trust_score=73
    ),

    source(
        "NDTV",
        "WORLD",
        "SOUTH ASIA",
        secure_url(
            "feeds.feedburner.com",
            "/ndtvnews-top-stories"
        ),
        trust_score=74
    ),

    # United States

    source(
        "NPR News",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "feeds.npr.org",
            "/1001/rss.xml"
        ),
        trust_score=89
    ),

    source(
        "New York Times Top Stories",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "rss.nytimes.com",
            "/services/xml/rss/nyt/HomePage.xml"
        ),
        trust_score=86
    ),

    source(
        "ABC News",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "abcnews.com",
            "/abcnews/topstories"
        ),
        trust_score=80
    ),

    source(
        "CBS News",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "www.cbsnews.com",
            "/latest/rss/main"
        ),
        trust_score=80
    ),

    source(
        "NBC News",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "feeds.nbcnews.com",
            "/nbcnews/public/news"
        ),
        trust_score=80
    ),

    source(
        "Fox News",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "moxie.foxnews.com",
            "/google-publisher/latest.xml"
        ),
        trust_score=72
    ),

    source(
        "PBS NewsHour",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "www.pbs.org",
            "/newshour/feeds/rss/headlines"
        ),
        trust_score=88
    ),

    source(
        "Los Angeles Times",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "www.latimes.com",
            "/index.rss"
        ),
        trust_score=82
    ),

    source(
        "Axios",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "api.axios.com",
            "/feed/top/"
        ),
        trust_score=78
    ),

    source(
        "TIME",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "time.com",
            "/feed/"
        ),
        trust_score=78
    ),

    source(
        "Yahoo News",
        "UNITED STATES",
        "UNITED STATES",
        secure_url(
            "news.yahoo.com",
            "/rss/topstories"
        ),
        trust_score=68
    ),

    source(
        "ProPublica",
        "INVESTIGATIONS",
        "UNITED STATES",
        secure_url(
            "www.propublica.org",
            "/feeds/propublica/main"
        ),
        trust_score=90
    ),

    source(
        "The Atlantic",
        "ANALYSIS",
        "UNITED STATES",
        secure_url(
            "www.theatlantic.com",
            "/feed/all/"
        ),
        trust_score=80
    ),

    source(
        "Politico",
        "POLITICS",
        "UNITED STATES",
        secure_url(
            "www.politico.com",
            "/rss/politicopicks.xml"
        ),
        trust_score=78
    ),

    # BBC regional

    source(
        "BBC Africa",
        "AFRICA",
        "AFRICA",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/africa/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "BBC Asia",
        "ASIA",
        "ASIA",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/asia/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "BBC China",
        "ASIA",
        "CHINA",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/asia/china/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "BBC India",
        "ASIA",
        "INDIA",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/asia/india/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "BBC Middle East",
        "MIDDLE EAST",
        "MIDDLE EAST",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/middle_east/rss.xml"
        ),
        trust_score=92
    ),

    source(
        "BBC Latin America",
        "LATIN AMERICA",
        "LATIN AMERICA",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/world/latin_america/rss.xml"
        ),
        trust_score=92
    ),

    # Deutsche Welle regional

    source(
        "Deutsche Welle Europe",
        "EUROPE",
        "EUROPE",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-eu"
        ),
        trust_score=88
    ),

    source(
        "Deutsche Welle Germany",
        "EUROPE",
        "GERMANY",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-ger"
        ),
        trust_score=88
    ),

    source(
        "Deutsche Welle Asia",
        "ASIA",
        "ASIA",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-asia"
        ),
        trust_score=88
    ),

    source(
        "Deutsche Welle Africa",
        "AFRICA",
        "AFRICA",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-africa"
        ),
        trust_score=88
    ),

    source(
        "Deutsche Welle Business",
        "BUSINESS",
        "GLOBAL",
        secure_url(
            "rss.dw.com",
            "/rdf/rss-en-bus"
        ),
        trust_score=86
    ),

    source(
        "Deutsche Welle Science",
        "SCIENCE",
        "GLOBAL",
        secure_url(
            "rss.dw.com",
            "/xml/rss_en_science"
        ),
        trust_score=86
    ),

    source(
        "Deutsche Welle Environment",
        "ENVIRONMENT",
        "GLOBAL",
        secure_url(
            "rss.dw.com",
            "/xml/rss_en_environment"
        ),
        trust_score=86
    ),

    # Technology, defense, and business

    source(
        "BBC Technology",
        "TECHNOLOGY",
        "GLOBAL",
        secure_url(
            "feeds.bbci.co.uk",
            "/news/technology/rss.xml"
        ),
        trust_score=90
    ),

    source(
        "The Hacker News",
        "CYBER",
        "GLOBAL",
        secure_url(
            "feeds.feedburner.com",
            "/TheHackersNews"
        ),
        trust_score=74
    ),

    source(
        "Defense News",
        "DEFENSE",
        "GLOBAL",
        secure_url(
            "www.defensenews.com",
            "/arc/outboundfeeds/rss/"
        ),
        trust_score=80
    ),

    source(
        "Financial Times",
        "BUSINESS",
        "GLOBAL",
        secure_url(
            "www.ft.com",
            "/?format=rss"
        ),
        trust_score=88
    )
]


# ============================================================
# SEARCH-BASED NEWS AGENCIES
# ============================================================

AGENCY_SEARCHES = [
    (
        "Reuters via Google News",
        "NEWS AGENCY",
        "GLOBAL",
        "when:24h+site:reuters.com",
        90
    ),
    (
        "Associated Press via Google News",
        "NEWS AGENCY",
        "GLOBAL",
        "when:24h+site:apnews.com",
        91
    ),
    (
        "AFP via Google News",
        "NEWS AGENCY",
        "GLOBAL",
        "when:24h+site:afp.com",
        88
    )
]


# ============================================================
# WAR AND CONFLICT MONITORS
# ============================================================

CONFLICT_SEARCHES = [
    (
        "Ukraine War Monitor",
        "CONFLICT",
        "UKRAINE",
        "when:24h+Ukraine+war"
    ),
    (
        "Ukraine Missile Monitor",
        "MISSILE",
        "UKRAINE",
        "when:24h+Ukraine+missile+strike"
    ),
    (
        "Ukraine Drone Monitor",
        "DRONE",
        "UKRAINE",
        "when:24h+Ukraine+drone+attack"
    ),
    (
        "Crimea Monitor",
        "CONFLICT",
        "CRIMEA",
        "when:24h+Crimea+attack"
    ),
    (
        "Black Sea Monitor",
        "NAVAL",
        "BLACK SEA",
        "when:24h+Black+Sea+military"
    ),
    (
        "Russia Military Monitor",
        "DEFENSE",
        "RUSSIA",
        "when:24h+Russia+military"
    ),
    (
        "Russia Missile Monitor",
        "MISSILE",
        "RUSSIA",
        "when:24h+Russia+missile"
    ),
    (
        "Belarus Monitor",
        "CONFLICT",
        "BELARUS",
        "when:24h+Belarus+military"
    ),
    (
        "NATO Monitor",
        "DEFENSE",
        "NATO",
        "when:24h+NATO+military"
    ),
    (
        "NATO Eastern Flank Monitor",
        "DEFENSE",
        "NATO",
        "when:24h+NATO+eastern+flank"
    ),
    (
        "Taiwan Military Monitor",
        "CONFLICT",
        "TAIWAN",
        "when:24h+Taiwan+military"
    ),
    (
        "Taiwan Strait Monitor",
        "NAVAL",
        "TAIWAN STRAIT",
        "when:24h+Taiwan+Strait"
    ),
    (
        "China Military Monitor",
        "DEFENSE",
        "CHINA",
        "when:24h+China+military"
    ),
    (
        "China Naval Monitor",
        "NAVAL",
        "CHINA",
        "when:24h+China+naval"
    ),
    (
        "South China Sea Monitor",
        "CONFLICT",
        "SOUTH CHINA SEA",
        "when:24h+South+China+Sea"
    ),
    (
        "Philippines Security Monitor",
        "CONFLICT",
        "PHILIPPINES",
        "when:24h+Philippines+military"
    ),
    (
        "Japan Security Monitor",
        "DEFENSE",
        "JAPAN",
        "when:24h+Japan+military+security"
    ),
    (
        "Korean Peninsula Monitor",
        "MISSILE",
        "KOREAN PENINSULA",
        "when:24h+North+Korea+missile"
    ),
    (
        "India Pakistan Monitor",
        "CONFLICT",
        "SOUTH ASIA",
        "when:24h+India+Pakistan+military"
    ),
    (
        "Myanmar Conflict Monitor",
        "CONFLICT",
        "MYANMAR",
        "when:24h+Myanmar+conflict"
    ),
    (
        "Afghanistan Security Monitor",
        "CONFLICT",
        "AFGHANISTAN",
        "when:24h+Afghanistan+security"
    ),
    (
        "Israel Gaza Monitor",
        "CONFLICT",
        "MIDDLE EAST",
        "when:24h+Israel+Gaza"
    ),
    (
        "Israel Missile Monitor",
        "MISSILE",
        "ISRAEL",
        "when:24h+Israel+missile"
    ),
    (
        "Gaza Monitor",
        "CONFLICT",
        "GAZA",
        "when:24h+Gaza+strike"
    ),
    (
        "Lebanon Monitor",
        "CONFLICT",
        "LEBANON",
        "when:24h+Lebanon+military"
    ),
    (
        "Syria Monitor",
        "CONFLICT",
        "SYRIA",
        "when:24h+Syria+attack"
    ),
    (
        "Iran Military Monitor",
        "DEFENSE",
        "IRAN",
        "when:24h+Iran+military"
    ),
    (
        "Iran Nuclear Monitor",
        "NUCLEAR",
        "IRAN",
        "when:24h+Iran+nuclear"
    ),
    (
        "Persian Gulf Monitor",
        "NAVAL",
        "PERSIAN GULF",
        "when:24h+Persian+Gulf+military"
    ),
    (
        "Strait of Hormuz Monitor",
        "NAVAL",
        "STRAIT OF HORMUZ",
        "when:24h+Strait+of+Hormuz"
    ),
    (
        "Red Sea Monitor",
        "NAVAL",
        "RED SEA",
        "when:24h+Red+Sea+attack"
    ),
    (
        "Yemen Houthi Monitor",
        "CONFLICT",
        "YEMEN",
        "when:24h+Yemen+Houthi"
    ),
    (
        "Saudi Arabia Security Monitor",
        "CONFLICT",
        "SAUDI ARABIA",
        "when:24h+Saudi+Arabia+security"
    ),
    (
        "Iraq Security Monitor",
        "CONFLICT",
        "IRAQ",
        "when:24h+Iraq+security"
    ),
    (
        "Sudan Conflict Monitor",
        "CONFLICT",
        "SUDAN",
        "when:24h+Sudan+conflict"
    ),
    (
        "Sahel Security Monitor",
        "CONFLICT",
        "SAHEL",
        "when:24h+Sahel+security"
    ),
    (
        "Somalia Monitor",
        "CONFLICT",
        "SOMALIA",
        "when:24h+Somalia+attack"
    ),
    (
        "Ethiopia Monitor",
        "CONFLICT",
        "ETHIOPIA",
        "when:24h+Ethiopia+conflict"
    ),
    (
        "DR Congo Monitor",
        "CONFLICT",
        "DR CONGO",
        "when:24h+DR+Congo+conflict"
    ),
    (
        "Nigeria Security Monitor",
        "CONFLICT",
        "NIGERIA",
        "when:24h+Nigeria+security"
    ),
    (
        "Mozambique Security Monitor",
        "CONFLICT",
        "MOZAMBIQUE",
        "when:24h+Mozambique+insurgency"
    ),
    (
        "Haiti Security Monitor",
        "CONFLICT",
        "HAITI",
        "when:24h+Haiti+security"
    ),
    (
        "Venezuela Security Monitor",
        "CONFLICT",
        "VENEZUELA",
        "when:24h+Venezuela+security"
    ),
    (
        "Mexico Security Monitor",
        "CONFLICT",
        "MEXICO",
        "when:24h+Mexico+security"
    )
]


# ============================================================
# GLOBAL MILITARY MONITORS
# ============================================================

MILITARY_SEARCHES = [
    (
        "Global Military Deployment Monitor",
        "DEFENSE",
        "GLOBAL",
        "when:24h+military+deployment"
    ),
    (
        "Global Missile Launch Monitor",
        "MISSILE",
        "GLOBAL",
        "when:24h+missile+launch"
    ),
    (
        "Global Ballistic Missile Monitor",
        "MISSILE",
        "GLOBAL",
        "when:24h+ballistic+missile"
    ),
    (
        "Global Cruise Missile Monitor",
        "MISSILE",
        "GLOBAL",
        "when:24h+cruise+missile"
    ),
    (
        "Global Drone Attack Monitor",
        "DRONE",
        "GLOBAL",
        "when:24h+drone+attack"
    ),
    (
        "Global Naval Activity Monitor",
        "NAVAL",
        "GLOBAL",
        "when:24h+naval+warship"
    ),
    (
        "Global Submarine Monitor",
        "NAVAL",
        "GLOBAL",
        "when:24h+military+submarine"
    ),
    (
        "Global Military Aviation Monitor",
        "AIR",
        "GLOBAL",
        "when:24h+military+aircraft"
    ),
    (
        "Global Airstrike Monitor",
        "AIR",
        "GLOBAL",
        "when:24h+airstrike"
    ),
    (
        "Global Ground Combat Monitor",
        "GROUND",
        "GLOBAL",
        "when:24h+ground+combat"
    ),
    (
        "Global Nuclear Weapons Monitor",
        "NUCLEAR",
        "GLOBAL",
        "when:24h+nuclear+weapons"
    ),
    (
        "Global Military Exercise Monitor",
        "DEFENSE",
        "GLOBAL",
        "when:24h+military+exercise"
    ),
    (
        "Global Ceasefire Monitor",
        "DIPLOMATIC",
        "GLOBAL",
        "when:24h+ceasefire"
    ),
    (
        "Global Sanctions Monitor",
        "DIPLOMATIC",
        "GLOBAL",
        "when:24h+sanctions"
    )
]


# ============================================================
# CYBER MONITORS
# ============================================================

CYBER_SEARCHES = [
    (
        "Global Cyberattack Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+cyberattack"
    ),
    (
        "Ransomware Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+ransomware"
    ),
    (
        "Data Breach Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+data+breach"
    ),
    (
        "Zero-Day Vulnerability Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+zero-day+vulnerability"
    ),
    (
        "Nation-State Cyber Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+nation-state+cyberattack"
    ),
    (
        "Critical Infrastructure Cyber Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+critical+infrastructure+cyber"
    ),
    (
        "Healthcare Cyber Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+hospital+cyberattack"
    ),
    (
        "Financial Cyber Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+bank+cyberattack"
    ),
    (
        "Government Cyber Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+government+cyberattack"
    ),
    (
        "Telecommunications Cyber Monitor",
        "CYBER",
        "GLOBAL",
        "when:24h+telecommunications+cyberattack"
    )
]


# ============================================================
# UNITED STATES HOMELAND MONITORS
# ============================================================

HOMELAND_SEARCHES = [
    (
        "US Homeland Threat Monitor",
        "HOMELAND",
        "UNITED STATES",
        "when:24h+US+homeland+threat"
    ),
    (
        "US Terrorism Monitor",
        "HOMELAND",
        "UNITED STATES",
        "when:24h+US+terrorism+threat"
    ),
    (
        "US Power Grid Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+power+grid"
    ),
    (
        "US Critical Infrastructure Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+critical+infrastructure"
    ),
    (
        "US Pipeline Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+pipeline+disruption"
    ),
    (
        "US Water System Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+water+system+threat"
    ),
    (
        "US Border Security Monitor",
        "HOMELAND",
        "UNITED STATES",
        "when:24h+US+border+security"
    ),
    (
        "US Aviation Security Monitor",
        "HOMELAND",
        "UNITED STATES",
        "when:24h+US+airport+security"
    ),
    (
        "US Rail Disruption Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+rail+disruption"
    ),
    (
        "US Port Security Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+port+security"
    ),
    (
        "US Communications Outage Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+communications+outage"
    ),
    (
        "US Public Safety Monitor",
        "HOMELAND",
        "UNITED STATES",
        "when:24h+US+public+safety+threat"
    ),
    (
        "US Military Base Monitor",
        "HOMELAND",
        "UNITED STATES",
        "when:24h+US+military+base+security"
    ),
    (
        "US Nuclear Facility Monitor",
        "INFRASTRUCTURE",
        "UNITED STATES",
        "when:24h+US+nuclear+facility"
    )
]


# ============================================================
# ENERGY AND SUPPLY CHAIN MONITORS
# ============================================================

ENERGY_SEARCHES = [
    (
        "Global Energy Security Monitor",
        "ENERGY",
        "GLOBAL",
        "when:24h+energy+security"
    ),
    (
        "Oil Supply Disruption Monitor",
        "ENERGY",
        "GLOBAL",
        "when:24h+oil+supply+disruption"
    ),
    (
        "Natural Gas Disruption Monitor",
        "ENERGY",
        "GLOBAL",
        "when:24h+natural+gas+disruption"
    ),
    (
        "Shipping Disruption Monitor",
        "SUPPLY CHAIN",
        "GLOBAL",
        "when:24h+shipping+disruption"
    ),
    (
        "Global Supply Chain Monitor",
        "SUPPLY CHAIN",
        "GLOBAL",
        "when:24h+supply+chain+disruption"
    ),
    (
        "Semiconductor Supply Monitor",
        "SUPPLY CHAIN",
        "GLOBAL",
        "when:24h+semiconductor+supply+disruption"
    ),
    (
        "Food Security Monitor",
        "SUPPLY CHAIN",
        "GLOBAL",
        "when:24h+food+security+crisis"
    ),
    (
        "Global Port Disruption Monitor",
        "SUPPLY CHAIN",
        "GLOBAL",
        "when:24h+port+disruption"
    )
]


# ============================================================
# DISASTER MONITORS
# ============================================================

DISASTER_SEARCHES = [
    (
        "Global Earthquake Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+major+earthquake"
    ),
    (
        "Global Wildfire Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+major+wildfire"
    ),
    (
        "Global Flood Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+major+flood"
    ),
    (
        "Global Volcano Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+volcano+eruption"
    ),
    (
        "Global Tsunami Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+tsunami+warning"
    ),
    (
        "Global Hurricane Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+hurricane"
    ),
    (
        "Global Cyclone Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+cyclone"
    ),
    (
        "Global Typhoon Monitor",
        "DISASTER",
        "GLOBAL",
        "when:24h+typhoon"
    ),
    (
        "US Severe Weather Monitor",
        "DISASTER",
        "UNITED STATES",
        "when:24h+US+severe+weather"
    ),
    (
        "US Earthquake Monitor",
        "DISASTER",
        "UNITED STATES",
        "when:24h+US+earthquake"
    ),
    (
        "US Wildfire Monitor",
        "DISASTER",
        "UNITED STATES",
        "when:24h+US+wildfire"
    )
]


# ============================================================
# TECHNOLOGY AND SPACE MONITORS
# ============================================================

TECHNOLOGY_SEARCHES = [
    (
        "Artificial Intelligence Security Monitor",
        "TECHNOLOGY",
        "GLOBAL",
        "when:24h+artificial+intelligence+security"
    ),
    (
        "Military AI Monitor",
        "DEFENSE",
        "GLOBAL",
        "when:24h+military+artificial+intelligence"
    ),
    (
        "Satellite Security Monitor",
        "SPACE",
        "GLOBAL",
        "when:24h+military+satellite"
    ),
    (
        "Space Launch Monitor",
        "SPACE",
        "GLOBAL",
        "when:24h+rocket+launch"
    ),
    (
        "Space Weather Monitor",
        "SPACE",
        "GLOBAL",
        "when:24h+solar+storm+space+weather"
    ),
    (
        "Undersea Cable Monitor",
        "INFRASTRUCTURE",
        "GLOBAL",
        "when:24h+undersea+cable+damage"
    ),
    (
        "GPS Disruption Monitor",
        "TECHNOLOGY",
        "GLOBAL",
        "when:24h+GPS+jamming"
    )
]


# ============================================================
# SOURCE GENERATORS
# ============================================================

def build_agency_sources():
    """
    Convert agency tuples into standardized source records.
    """

    generated_sources = []

    for (
        name,
        category,
        region,
        query,
        trust_score
    ) in AGENCY_SEARCHES:

        generated_sources.append(
            source(
                name=name,
                category=category,
                region=region,
                url=google_news_url(query),
                aggregated=True,
                trust_score=trust_score
            )
        )

    return generated_sources


def build_monitor_sources(records):
    """
    Convert monitoring tuples into standardized source records.
    """

    generated_sources = []

    for (
        name,
        category,
        region,
        query
    ) in records:

        generated_sources.append(
            source(
                name=name,
                category=category,
                region=region,
                url=google_news_url(query),
                aggregated=True,
                trust_score=60
            )
        )

    return generated_sources


# ============================================================
# COMPLETE REGISTRY
# ============================================================

RSS_FEEDS = (
    DIRECT_FEEDS
    + build_agency_sources()
    + build_monitor_sources(
        CONFLICT_SEARCHES
    )
    + build_monitor_sources(
        MILITARY_SEARCHES
    )
    + build_monitor_sources(
        CYBER_SEARCHES
    )
    + build_monitor_sources(
        HOMELAND_SEARCHES
    )
    + build_monitor_sources(
        ENERGY_SEARCHES
    )
    + build_monitor_sources(
        DISASTER_SEARCHES
    )
    + build_monitor_sources(
        TECHNOLOGY_SEARCHES
    )
)


# ============================================================
# REGISTRY ACCESS FUNCTIONS
# ============================================================

def get_enabled_sources():
    """
    Return all enabled sources.

    rss_fetcher.py imports this function directly.
    """

    return [
        entry
        for entry in RSS_FEEDS
        if entry.get(
            "enabled",
            True
        )
    ]


def get_sources_by_category(category):
    """
    Return enabled sources from one category.
    """

    requested_category = (
        str(category)
        .strip()
        .upper()
    )

    return [
        entry
        for entry in get_enabled_sources()
        if entry.get(
            "category",
            ""
        ).strip().upper() == requested_category
    ]


def get_sources_by_region(region):
    """
    Return enabled sources from one region.
    """

    requested_region = (
        str(region)
        .strip()
        .upper()
    )

    return [
        entry
        for entry in get_enabled_sources()
        if entry.get(
            "region",
            ""
        ).strip().upper() == requested_region
    ]


def get_source_by_name(source_name):
    """
    Return one enabled source by exact name.
    """

    requested_name = (
        str(source_name)
        .strip()
        .casefold()
    )

    for entry in get_enabled_sources():

        current_name = (
            entry.get(
                "name",
                ""
            )
            .strip()
            .casefold()
        )

        if current_name == requested_name:
            return entry

    return None


def get_source_count():
    """
    Return the number of registered sources.
    """

    return len(
        RSS_FEEDS
    )


# ============================================================
# REGISTRY VALIDATION
# ============================================================

def validate_sources():
    """
    Validate all registered sources.

    Returns an empty list when all records pass.
    """

    problems = []

    required_fields = (
        "name",
        "category",
        "region",
        "url"
    )

    seen_names = set()
    seen_urls = set()

    for index, entry in enumerate(
        RSS_FEEDS
    ):
        source_name = entry.get(
            "name",
            f"Source #{index}"
        )

        for field_name in required_fields:
            field_value = entry.get(
                field_name
            )

            if not field_value:
                problems.append(
                    {
                        "index": index,
                        "source": source_name,
                        "problem": (
                            "Missing required field: "
                            f"{field_name}"
                        )
                    }
                )

        source_url = str(
            entry.get(
                "url",
                ""
            )
        )

        if "<a href" in source_url:
            problems.append(
                {
                    "index": index,
                    "source": source_name,
                    "problem": (
                        "HTML anchor corruption detected"
                    )
                }
            )

        if source_url and not source_url.startswith(
            "https://"
        ):
            problems.append(
                {
                    "index": index,
                    "source": source_name,
                    "problem": (
                        "URL does not begin with HTTPS"
                    )
                }
            )

        normalized_name = (
            str(source_name)
            .strip()
            .casefold()
        )

        if normalized_name in seen_names:
            problems.append(
                {
                    "index": index,
                    "source": source_name,
                    "problem": (
                        "Duplicate source name"
                    )
                }
            )
        else:
            seen_names.add(
                normalized_name
            )

        normalized_url = (
            source_url
            .strip()
            .casefold()
        )

        if normalized_url in seen_urls:
            problems.append(
                {
                    "index": index,
                    "source": source_name,
                    "problem": (
                        "Duplicate source URL"
                    )
                }
            )
        else:
            seen_urls.add(
                normalized_url
            )

    return problems