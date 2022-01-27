from df_engine.core import Context, Actor
import re
from fetch_logic.translation import cloud_translate


def talk_about(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = cloud_translate.check_and_translate_fwd(ctx)
    return re.search(r"(i (want to|wanna)|let's) talk about .+", request, re.IGNORECASE) is not None


def birth_date(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = cloud_translate.check_and_translate_fwd(ctx)
    return re.search(r"(what is|when was) .+ (age|born).*", request, re.IGNORECASE) is not None


def celeb_profession(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = cloud_translate.check_and_translate_fwd(ctx)
    return re.search(r"what is (.+'s|his|her) profession.*", request, re.IGNORECASE) is not None


def celeb_death(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = cloud_translate.check_and_translate_fwd(ctx)
    return re.search(r"(when did|is|are) (.+|he|she|they) (die|alive).*", request, re.IGNORECASE) is not None

def any_celeb_query(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = cloud_translate.check_and_translate_fwd(ctx)
    if ctx.misc.get("name") is not None or ctx.misc.get("id") is not None:
        return re.search(r"\w", request) is not None
    return False




