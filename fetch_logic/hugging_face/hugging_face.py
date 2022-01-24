from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from constants import constants
import torch

qna_model = AutoModelForQuestionAnswering.from_pretrained(constants.MODEL_NAME, cache_dir=constants.CACHE_LOCATION)
qna_tokenizer = AutoTokenizer.from_pretrained(constants.MODEL_NAME, cache_dir=constants.CACHE_LOCATION)


def get_ml_answer(query: str, doc: str):
    tokens = doc.split()
    tokens = tokens[:400]
    doc = ' '.join(tokens)
    in_tok = qna_tokenizer.encode_plus(query, doc,
                                       return_tensors='pt', truncation=True, max_length=512)

    # getting scores from tokens
    ans_str_sc, ans_en_sc = qna_model(**in_tok, return_dict=False)

    # getting the position
    ans_st = torch.argmax(ans_str_sc)
    ans_en = torch.argmax(ans_en_sc) + 1

    # ids are then converted to tokens
    ans_tok = qna_tokenizer.convert_ids_to_tokens(in_tok["input_ids"][0][ans_st:ans_en])

    # getting the answer
    return qna_tokenizer.convert_tokens_to_string(ans_tok)