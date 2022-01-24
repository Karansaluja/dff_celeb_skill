from df_engine.core import Context, Actor
from typing import Any
import re
from fetch_logic.celeb import basic_details, bio_answers
from fetch_logic.translation import cloud_translate


def bot_intro(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    return '''Welcome to Celeb Bot.
    You can ask me about any celebrity and I will try my best to answer you.
    Below are the ways in which you can interact with me:
    I want to talk about Leonardo DiCaprio
    When was he born ?
    When was Angelina Jolie born ?
    What are Brad Pitt's popular films?
    '''


def process_utterance(text: str, pattern, group_num: int) -> str:
    result = pattern.search(text.lower())
    if result is not None:
        return result.group(group_num)
    print("Sorry, I didn't get it. You can try asking again.")
    return ""


def celeb_start(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    request = ctx.last_request
    if request == "text" or request is None:
        return
    request = cloud_translate.check_and_translate_fwd(ctx)
    p = re.compile("(i (want to|wanna)|let's) talk about (.+)")
    name = process_utterance(request, p, 3)
    if len(name) == 0:
        return
    if name not in ["him", "her", "them"]:
        ctx.misc["name"] = name.lower()
    result = basic_details.get_basic_details(ctx.misc.get("name"))
    ctx.misc["id"] = result["_id"]
    if result is not None:
        return cloud_translate.check_and_translate_back(ctx,"Yes, we can talk about {}".format(ctx.misc.get("name")))
    else:
        return cloud_translate.check_and_translate_back(ctx,"Sorry,I don't know about {}." \
               " But there are a lot of other celebs we can talk about.".format(ctx.misc.get("name")))


def celeb_age(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    if ctx.last_request == "text" or ctx.last_request is None:
        return
    ctx.add_request(cloud_translate.check_and_translate_fwd(ctx))
    p = re.compile("(what is|when (was|were)) (.+) (age|born).*")
    name = process_utterance(ctx.last_request, p, 3)
    if len(name) == 0:
        return
    if name not in ["his", "her", "they", "he", "she", "their"]:
        ctx.misc["name"] = name.lower()
    celeb_name = ctx.misc.get("name")
    celeb_details = basic_details.get_basic_details(celeb_name=celeb_name)
    if celeb_details is not None and len(celeb_details["birth_year"]) > 0:
        return cloud_translate.check_and_translate_back(ctx, "{0} was born in {1}".format(celeb_name, celeb_details["birth_year"]))
    else:
        return cloud_translate.check_and_translate_back(ctx, "Sorry, I couldn't find birth information.")


def celeb_profession(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    if ctx.last_request == "text" or ctx.last_request is None:
        return
    ctx.add_request(cloud_translate.check_and_translate_fwd(ctx))
    p = re.compile("what is (.+'s|his|her) profession.*")
    name = process_utterance(ctx.last_request, p, 1)
    if len(name) == 0:
        return
    if name not in ["his", "her", "their"]:
        ctx.misc["name"] = name.lower()
    celeb_name = ctx.misc.get("name")
    celeb_details = basic_details.get_basic_details(celeb_name=celeb_name)
    if celeb_details is not None:
        return cloud_translate.check_and_translate_back(ctx, "{0}'s primary profession"
                                             " is {1}".format(celeb_name, celeb_details["primary_profession"][0]))
    else:
        return cloud_translate.check_and_translate_back(ctx,"Sorry, I couldn't find profession information.")


def celeb_resp_from_bio(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    if ctx.last_request == "text" or ctx.last_request is None:
        return
    ctx.add_request(cloud_translate.check_and_translate_fwd(ctx))
    return cloud_translate.check_and_translate_back(ctx, bio_answers.get_celeb_answer(ctx, ctx.last_request))


def switch_to_hindi(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    if ctx.last_request == "text" or ctx.last_request is None:
        return
    ctx.misc["lang"] = "hi"
    return "अब हम हिंदी में बात कर सकते हैं"


def switch_to_english(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    if ctx.last_request == "text" or ctx.last_request is None:
        return
    ctx.misc["lang"] = "en"
    return "Now we can talk in English"
