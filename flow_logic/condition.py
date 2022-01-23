import re
from df_engine.core import Context, Actor


def talk_about(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return re.search(r"(i want to|let's) talk about .+", request.lower(), re.IGNORECASE) is not None


def birth_date(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return re.search(r"what is .+ age.*", request.lower(), re.IGNORECASE) is not None
