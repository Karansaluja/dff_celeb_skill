# -*- coding: utf-8 -*-
import os
from constants import constants
from google.cloud import translate_v3
from df_engine.core import Context

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = constants.GCP_KEY


def translate_query(text: str,source_lang: str, target_lang: str):
    translate_client = translate_v3.TranslationServiceClient()
    output = translate_client.translate_text(target_language_code=target_lang, contents=[text],
                                             parent=constants.PARENT_PROJECT,
                                             source_language_code=source_lang, mime_type="text/plain")
    return output.translations[0].translated_text


def check_and_translate_fwd(ctx: Context):
    lang = ctx.misc.get("lang")
    if lang is not None and lang == "hi":
        return translate_query(ctx.last_request, "hi", "en")
    else:
        return ctx.last_request


def check_and_translate_back(ctx: Context, response: str):
    lang = ctx.misc.get("lang")
    if lang is not None and lang == "hi":
        print(ctx.last_request)
        return translate_query(response, "en", "hi")
    else:
        return response
