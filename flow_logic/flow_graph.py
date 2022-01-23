import logging

from df_engine.core.keywords import GLOBAL, TRANSITIONS, RESPONSE
from flow_logic.response import *
from flow_logic import condition as custom_cnd
import df_engine.conditions as cnd
from fetch_logic.celeb import basic_details
from typing import Union
from df_engine.core.plot import Plot


class FlowGraph:
    def __init__(self, celeb_basics: basic_details.BasicDetails, logger: logging.Logger):
        self.basic_details = celeb_basics
        self.responses = Responses(celeb_basics=celeb_basics, logger=logger)
        self.logger = logger
        self.plot = {
            "global": {
                "start": {
                    RESPONSE: "",
                    TRANSITIONS: {
                        "intro": cnd.regexp(r"hi|hello", re.IGNORECASE),
                    }
                },
                "intro": {
                    RESPONSE: self.responses.bot_intro,
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
                    RESPONSE: self.responses.celeb_start,
                    TRANSITIONS: {
                        ("celeb", "age"): custom_cnd.birth_date,
                    }
                },
                "age": {
                    RESPONSE: self.responses.celeb_age,
                    TRANSITIONS: {
                        ("global", "start"): cnd.exact_match("mera naam joker")
                    }
                }
            }
        }


"""
responses

def initialize_plot_dependencies(cb: basic_details.BasicDetails, logger: logging.Logger):
    global responses
    responses = Responses(celeb_basics=cb, logger=logger)


plot = {
    "global": {
        "start": {
            RESPONSE: "",
            TRANSITIONS: {
                "intro": cnd.regexp(r"hi|hello", re.IGNORECASE),
            }
        },
        "intro": {
            RESPONSE: responses.bot_intro,
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
            RESPONSE: responses.celeb_start,
            TRANSITIONS: {
                ("celeb", "age"): custom_cnd.birth_date,
            }
        },
        "age": {
            RESPONSE: responses.celeb_age,
            TRANSITIONS: {
                ("global", "start"): cnd.exact_match("mera naam joker")
            }
        }
    }
}
"""

