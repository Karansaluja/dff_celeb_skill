from df_engine.core import Context, Actor
import re


def talk_about(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return re.search(r"(i (want to|wanna)|let's) talk about .+", request.lower(), re.IGNORECASE) is not None


def birth_date(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return re.search(r"(what is|when was) .+ (age|born).*", request.lower(), re.IGNORECASE) is not None


def celeb_profession(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return re.search(r"what is (.+'s|his|her) profession.*", request.lower(), re.IGNORECASE) is not None
