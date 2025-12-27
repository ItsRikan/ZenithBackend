import os
import time
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

from .output_schema import Action
from ..instructions import FRONTLAYER_MODEL_INSTRUCTION
from ..utils import clean_json
from ..cofig import MODEL_LIST, retry_config
from google.generativeai.types import RequestOptions

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


def _call_model_with_retries(model_obj, prompt: str) -> Action:
    """
    Calls the given model with retry/backoff and returns an Action or an error-Action.
    """
    attempts = max(int(retry_config.get("attempts", 3)), 1)
    initial_delay = float(retry_config.get("initial_delay", 1))
    exp_base = float(retry_config.get("exp_base", 2))

    for attempt in range(attempts):
        try:
            resp = model_obj.generate_content(prompt, request_options=RequestOptions(timeout=8))
            text = resp.text if hasattr(resp, "text") else str(resp)
            cleaned = clean_json(text)
            action = Action.model_validate_json(cleaned)
            return action
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
                return Action(action="answer", error="retry", confidence_score=0)
        except exceptions.InvalidArgument as e:
            return Action(action="answer", error="invalid_name", confidence_score=0)
        except exceptions.NotFound as e:
            return Action(action="answer", error="model_not_found", confidence_score=0)
        except Exception as e:
            _note_failure()
            return Action(action="answer", error="unknown", confidence_score=0)

    _note_failure()
    return Action(action="answer", error="model_failed", confidence_score=0)


def decide_action_model(user_query: str,prev_action:dict) -> Action:
    """
    Try models in order from MODEL_LIST. Returns a valid Action or an error Action.
    """
    try:
        global MODEL_LIST
        if _circuit_open():
            return Action(action="answer", error="model_failed", confidence_score=0)

        prompt = FRONTLAYER_MODEL_INSTRUCTION.format(prev_action,user_query)
        for i,model_name in enumerate(MODEL_LIST):
            model_obj = _models.get(model_name)
            if model_obj is None:
                try:
                    model_obj = genai.GenerativeModel(model_name)
                    _models[model_name] = model_obj
                except Exception as e:
                    continue

            action = _call_model_with_retries(model_obj, prompt)

            if not (isinstance(action, Action) and getattr(action, "error", None)):
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
                return action


        return Action(action="answer", error="model_failed", confidence_score=0)
    except Exception as e:
        return Action(action="answer", error="model_failed", confidence_score=0)
