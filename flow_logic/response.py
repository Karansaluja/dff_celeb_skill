import logging
import re

from df_engine.core import Context, Actor
from typing import Any
from fetch_logic.celeb import basic_details


class Responses:
    def __init__(self, celeb_basics: basic_details.BasicDetails, logger: logging.Logger):
        self.celeb_basics = celeb_basics
        self.logger = logger

    @staticmethod
    def bot_intro(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
        return '''Welcome to Celeb Bot.
        You can ask me about any celebrity and I will try my best to answer you.
        Below are the ways in which you can interact with me:
        I want to talk about Leonardo DiCaprio
        When was he born ?
        When was Angelina Jolie born ?
        What are Brad Pitt's popular films?
        '''

    def celeb_start(self, ctx: Context, actor: Actor, *args, **kwargs) -> Any:
        request = ctx.last_request
        if request == "text":
            return
        print("Request {0}".format(request))
        print("Context labels: {}".format(ctx.labels))
        p = re.compile("I want to talk about (.*)")
        result = p.search(request)
        if result is None:  # Moving forward in case of error
            print("Sorry, I didn't get it. You can try asking again.")
            return ""
        name = result.group(1)
        if name not in ["him", "her", "them"]:
            ctx.misc["name"] = name
        # if ctx.misc.get("name") is not None:
        return "Yes, we can talk about"

    def celeb_age(self, ctx: Context, actor: Actor, *args, **kwargs) -> Any:
        print("Dictionary {}".format(ctx.misc))
        return "His age is 45"
