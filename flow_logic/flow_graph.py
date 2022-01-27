from df_engine.core.keywords import GLOBAL, TRANSITIONS, RESPONSE
import df_engine.conditions as cnd
from flow_logic import response
import re
import flow_logic.condition as custom_cnd
from df_engine.core import Actor

plot = {
    GLOBAL: {
        TRANSITIONS: {
            ("lang", "switch_hindi"): cnd.exact_match("switch to hindi"),
            ("lang", "switch_english"): cnd.exact_match("switch to english")
        }
    },
    "lang": {
        "switch_hindi": {
            RESPONSE: response.switch_to_hindi,
            TRANSITIONS: {
                ("celeb", "start"): custom_cnd.talk_about,
            }
        },
        "switch_english": {
            RESPONSE: response.switch_to_english,
            TRANSITIONS: {
                ("celeb", "start"): custom_cnd.talk_about
            }
        }
    },
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
                ("celeb", "death"): custom_cnd.celeb_death,
                ("celeb", "profession"): custom_cnd.celeb_profession,
                ("celeb", "start"): custom_cnd.talk_about,
                ("celeb", "ml_answer"): custom_cnd.any_celeb_query,
            }
        },
        "profession": {
            RESPONSE: response.celeb_profession,
            TRANSITIONS: {
                ("celeb", "age"): custom_cnd.birth_date,
                ("celeb", "profession"): custom_cnd.celeb_profession,
                ("celeb", "start"): custom_cnd.talk_about,
                ("celeb", "death"): custom_cnd.celeb_death,
                ("global", "intro"): cnd.exact_match("restart"),
                ("celeb", "ml_answer"): custom_cnd.any_celeb_query,
            }
        },
        "age": {
            RESPONSE: response.celeb_age,
            TRANSITIONS: {
                ("global", "intro"): cnd.exact_match("restart"),
                ("celeb", "start"): custom_cnd.talk_about,
                ("celeb", "profession"): custom_cnd.celeb_profession,
                ("celeb", "death"): custom_cnd.celeb_death,
                ("celeb", "ml_answer"): custom_cnd.any_celeb_query,
            }
        },
        "death":{
            RESPONSE: response.celeb_death,
            TRANSITIONS: {
                ("global", "intro"): cnd.exact_match("restart"),
                ("celeb", "start"): custom_cnd.talk_about,
                ("celeb", "profession"): custom_cnd.celeb_profession,
                ("celeb", "age"): custom_cnd.birth_date,
                ("celeb", "ml_answer"): custom_cnd.any_celeb_query,
            }
        },
        "ml_answer": {
            RESPONSE: response.celeb_resp_from_bio,
            TRANSITIONS: {
                ("global", "intro"): cnd.exact_match("restart"),
                ("celeb", "age"): custom_cnd.birth_date,
                ("celeb", "death"): custom_cnd.celeb_death,
                ("celeb", "profession"): custom_cnd.celeb_profession,
                ("lang", "switch_hindi"): cnd.exact_match("switch to hindi"),
                ("lang", "switch_english"): cnd.exact_match("switch to english"),
                ("celeb", "ml_answer"): custom_cnd.any_celeb_query,
            }
        }
    }
}

actor = Actor(plot=plot, start_label=("global", "start"))
