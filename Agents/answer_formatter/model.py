import os
import time
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv
from google.generativeai.types import RequestOptions

from .output_schema import AnswerSchma
from ..instructions import ANSWER_FORMATER_INSTRUCTIONS
from ..utils import clean_json
from ..cofig import MODEL_LIST, retry_config
from ..logger import logging
from ..details import CREATOR_EMAIL


load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logging.warning("GOOGLE_API_KEY not set")

genai.configure(api_key=GOOGLE_API_KEY)


_models: dict[str, object] = {}
for mname in MODEL_LIST:
    try:
        _models[mname] = genai.GenerativeModel(mname)
    except Exception as e:
        logging.exception(f"Failed to instantiate model {mname}: {e}")
        _models[mname] = None

_FAIL_COUNT = 0
_FAIL_THRESHOLD = 6  
_CIRCUIT_RESET_SEC = 60
_last_fail_ts = 0


def _circuit_open() -> bool:
    global _FAIL_COUNT, _last_fail_ts
    if _FAIL_COUNT >= _FAIL_THRESHOLD:
        if time.time() - _last_fail_ts < _CIRCUIT_RESET_SEC:
            return True
        _FAIL_COUNT = 0
    return False


def _note_failure():
    global _FAIL_COUNT, _last_fail_ts
    _FAIL_COUNT += 1
    _last_fail_ts = time.time()


def _call_model_with_retries(model_obj, prompt: str) -> AnswerSchma:
    """
    Calls the given model with retry/backoff and returns an Action or an error-Action.
    """
    attempts = max(int(retry_config.get("attempts", 3)), 1)
    initial_delay = float(retry_config.get("initial_delay", 1))
    exp_base = float(retry_config.get("exp_base", 2))

    for attempt in range(attempts):
        try:
            logging.debug("fetching response")
            resp = model_obj.generate_content(prompt,request_options=RequestOptions(timeout=8))
            logging.debug("Got response From answer Formatter | Note the time it must be 8 secs")
            text = resp.text if hasattr(resp, "text") else str(resp)
            cleaned = clean_json(text)
            final_answer = AnswerSchma(message=cleaned)
            return final_answer
        except (
            exceptions.ServiceUnavailable,
            exceptions.DeadlineExceeded,
            exceptions.ResourceExhausted,
            exceptions.TooManyRequests,
        ) as e:
            logging.warning(f"Transient model error ({type(e).__name__}): {e}; attempt {attempt+1}/{attempts}")
            if attempt < attempts - 1:
                delay = initial_delay * (exp_base ** attempt)
                logging.warning(f"Sleeping for {delay} seconds")
                time.sleep(delay)
                continue
            else:
                _note_failure()
                return AnswerSchma(message="Internal Error",error="retry")
        except exceptions.InvalidArgument as e:
            logging.exception(f"InvalidArgument for model call: {e}")
            return AnswerSchma(message="Internal Error",error="invalid_name")
        except exceptions.NotFound as e:
            logging.exception(f"Model not found: {e}")
            return AnswerSchma(message="Internal Error",error="model_not_found")
        except Exception as e:
            logging.exception(f"Unexpected error calling model: {type(e)}  |  {e}")
            _note_failure()
            return AnswerSchma(message="Internal Error",error="unknown")

    _note_failure()
    return AnswerSchma(message="Internal Error",error="model_failed")


def answer_formatter_model(user_query: str,answer:str) -> AnswerSchma:
    """
    Try models in order from MODEL_LIST. Returns a valid Action or an error Action.
    """
    try:
        global MODEL_LIST
        if _circuit_open():
            logging.warning("Circuit open: skipping model calls")
            return AnswerSchma(message="Internal Error",error="model_failed")
        prompt = ANSWER_FORMATER_INSTRUCTIONS.format(user_query,answer)
        logging.debug(f"Availble Models before Swapping In Last Layer : {MODEL_LIST}")
        for i,model_name in enumerate(MODEL_LIST):
            logging.debug(f"Last Layer :Going With Model {model_name} where model no.= {i}")
            model_obj = _models.get(model_name)
            if model_obj is None:
                try:
                    model_obj = genai.GenerativeModel(model_name)
                    _models[model_name] = model_obj
                except Exception as e:
                    logging.exception(f"Failed to instantiate fallback model {model_name}: {e}")
                    continue

            final_answer = _call_model_with_retries(model_obj, prompt)

            if not (isinstance(final_answer, AnswerSchma) and getattr(final_answer, "error", None)):
                global _FAIL_COUNT
                _FAIL_COUNT = 0
                try:
                    for m in reversed(range(i+1)):
                        if m<=0:
                            break
                        n=m-1
                        MODEL_LIST[m],MODEL_LIST[n] = MODEL_LIST[n],MODEL_LIST[m]
                except:
                    pass
                logging.debug(f"Availble Models after Swapping In Last Layer : {MODEL_LIST}")
                return final_answer

            logging.info(f"Model {model_name} returned error={final_answer.error}; trying next model if available.")

        logging.error("All models failed to produce a valid final_answer")
        return AnswerSchma(message="Model failed due to internal error! May be API token limit exceede",error="model_failed")
    except Exception as e:
        logging.exception(f"Type : {type(e)} | error={e}")
        return AnswerSchma(message=f"Model failed due to internal error! Can you please mail to {CREATOR_EMAIL} manually about this issue",error="model_failed")