from df_engine.core.keywords import GLOBAL, TRANSITIONS, RESPONSE
import df_engine.conditions as cnd
from flow_logic import response
import re
import flow_logic.condition as custom_cnd
from df_engine.core import Actor

plot = {
    "global": {
        "start": {
            RESPONSE: "",
            TRANSITIONS: {
                "intro": cnd.regexp(r"hi|hello", re.IGNORECASE),
            }
        },
        "intro": {
            RESPONSE: response.bot_intro,
            TRANSITIONS: {
                ("celeb", "start"): custom_cnd.talk_about,
            }
        },
        "fallback": {
            RESPONSE: "Oops!! something went wrong. Starting again...",
            TRANSITIONS: {
                ("global", "intro"): cnd.true()
            }
        }
    },
    "celeb": {
        "start": {
            RESPONSE: response.celeb_start,
            TRANSITIONS: {
                ("celeb", "age"): custom_cnd.birth_date,
                ("celeb", "profession"): custom_cnd.celeb_profession,
                ("celeb", "start"): custom_cnd.talk_about,
            }
        },
        "profession": {
            RESPONSE: response.celeb_profession,
            TRANSITIONS: {
                ("celeb", "start"): cnd.exact_match("restart"),
                ("global", "intro"): custom_cnd.talk_about,
                ("celeb", "profession"): custom_cnd.celeb_profession,
            }
        },
        "age": {
            RESPONSE: response.celeb_age,
            TRANSITIONS: {
                ("celeb", "start"): cnd.exact_match("restart"),
                ("global", "intro"): custom_cnd.talk_about,
                ("celeb", "profession"): custom_cnd.celeb_profession,
            }
        }
    }
}

actor = Actor(plot=plot, start_label=("global", "start"))
