EVENT_RULES = {

    "MISSILE": [
        "missile",
        "rocket",
        "strike",
        "ballistic"
    ],

    "DRONE": [
        "drone",
        "uav",
        "unmanned"
    ],

    "CYBER": [
        "cyber",
        "hack",
        "breach",
        "ransomware"
    ],

    "NAVAL": [
        "warship",
        "destroyer",
        "frigate",
        "submarine",
        "carrier"
    ],

    "AIR": [
        "fighter",
        "bomber",
        "aircraft",
        "air strike",
        "airstrike"
    ],

    "GROUND": [
        "tank",
        "troops",
        "artillery",
        "ground offensive"
    ],

    "DIPLOMATIC": [
        "summit",
        "talks",
        "sanctions",
        "agreement"
    ],

    "HOMELAND": [
        "fbi",
        "homeland security",
        "power grid",
        "critical infrastructure",
        "domestic threat"
    ]
}


def classify_event(title, summary=""):

    text = f"{title} {summary}".lower()

    best_match = "NEWS"
    best_score = 0

    for event_type, keywords in EVENT_RULES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = event_type

    return best_match