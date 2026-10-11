KEYWORDS = {

    # Global conflicts
    "missile": 50,
    "strike": 40,
    "drone": 45,
    "attack": 35,
    "explosion": 30,

    # Military
    "military": 30,
    "troops": 40,
    "tank": 35,
    "fighter": 35,
    "warship": 40,
    "carrier": 40,

    # Regions
    "ukraine": 50,
    "russia": 45,
    "taiwan": 50,
    "china": 40,
    "iran": 45,
    "israel": 45,

    # Homeland security
    "cyber": 50,
    "hack": 50,
    "breach": 45,
    "power grid": 60,
    "critical infrastructure": 75,

    # Domestic alerts
    "terrorism": 75,
    "homeland security": 75,
    "fbi": 25,
    "cisa": 25
}


def calculate_relevance(title, summary=""):

    text = (
        f"{title} {summary}"
    ).lower()

    score = 0

    for keyword, value in KEYWORDS.items():

        if keyword in text:
            score += value

    return score