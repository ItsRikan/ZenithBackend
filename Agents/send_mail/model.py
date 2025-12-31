import os
import time
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv
from google.generativeai.types import RequestOptions

from .output_schema import MailSchema
from ..instructions import MAIL_MODEL_INSTRUCTION
from ..utils import clean_json
from ..cofig import MODEL_LIST, retry_config

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


genai.configure(api_key=GOOGLE_API_KEY)


_models: dict[str, object] = {}
for mname in MODEL_LIST:
    try:
        _models[mname] = genai.GenerativeModel(mname)
    except Exception as e:
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


def _call_model_with_retries(model_obj, prompt: str) -> MailSchema:
    """
    Calls the given model with retry/backoff and returns an Action or an error-Action.
    """
    attempts = max(int(retry_config.get("attempts", 3)), 1)
    initial_delay = float(retry_config.get("initial_delay", 1))
    exp_base = float(retry_config.get("exp_base", 2))

    for attempt in range(attempts):
        try:
            resp = model_obj.generate_content(prompt,request_options=RequestOptions(timeout=8))
            text = resp.text if hasattr(resp, "text") else str(resp)
            cleaned = clean_json(text)
            valid_mail = MailSchema.model_validate_json(cleaned)
            return valid_mail
        except (
            exceptions.ServiceUnavailable,
            exceptions.DeadlineExceeded,
            exceptions.ResourceExhausted,
            exceptions.TooManyRequests,
        ) as e:
            if attempt < attempts - 1:
                delay = initial_delay * (exp_base ** attempt)
                time.sleep(delay)
                continue
            else:
                _note_failure()
                return MailSchema(reason_if_mail_rejected="Internal Error",error="retry",confidence_score=0,necessity_score_of_mail=0.5)
        except exceptions.InvalidArgument as e:
            return MailSchema(reason_if_mail_rejected="Internal Error",error="invalid_name",confidence_score=0,necessity_score_of_mail=0.5)
        except exceptions.NotFound as e:
            return MailSchema(reason_if_mail_rejected="Internal Error",error="model_not_found",confidence_score=0,necessity_score_of_mail=0.5)
        except Exception as e:
            _note_failure()
            return MailSchema(reason_if_mail_rejected="Internal Error",error="unknown",confidence_score=0,necessity_score_of_mail=0.5)

    _note_failure()
    return MailSchema(reason_if_mail_rejected="Internal Error",error="model_failed",confidence_score=0,necessity_score_of_mail=0.5)


def mail_formatter_model(input_object:dict) -> MailSchema:
    """
    Try models in order from MODEL_LIST. Returns a valid Action or an error Action.
    """
    global MODEL_LIST
    if _circuit_open():
        return MailSchema(reason_if_mail_rejected="Internal Error",error="model_failed",confidence_score=0,necessity_score_of_mail=0.5)
    prompt = MAIL_MODEL_INSTRUCTION.format(input_object)
    for i,model_name in enumerate(MODEL_LIST):
        model_obj = _models.get(model_name)
        if model_obj is None:
            try:
                model_obj = genai.GenerativeModel(model_name)
                _models[model_name] = model_obj
            except Exception as e:
                continue

        final_answer:MailSchema = _call_model_with_retries(model_obj, prompt)

        if not (isinstance(final_answer, MailSchema) and getattr(final_answer, "error", None)):
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
            return final_answer


    return MailSchema(reason_if_mail_rejected="Model failed due to internal error! API token limit exceede",error="model_failed",confidence_score=0,necessity_score_of_mail=0.5)
