import json
import re
from typing import Type, TypeVar, Any, Dict
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.exceptions import OutputParserException

T = TypeVar("T", bound=BaseModel)


def get_pydantic_parser(pydantic_object: Type[T]) -> PydanticOutputParser[T]:
    return PydanticOutputParser(pydantic_object=pydantic_object)


def get_json_parser() -> JsonOutputParser:
    return JsonOutputParser()


def sanitize_json_string(raw_text: str) -> str:
    text = raw_text.strip()
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if code_block_match:
        text = code_block_match.group(1).strip()
    return text


def parse_llm_output_with_retry(
    raw_response: str,
    pydantic_model: Type[T],
    fallback_defaults: Dict[str, Any] = None
) -> T:
    clean_text = sanitize_json_string(raw_response)
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    try:
        return parser.parse(clean_text)
    except Exception as e:
        pass

    try:
        data = json.loads(clean_text)
        if isinstance(data, dict):
            return pydantic_model.model_validate(data)
    except Exception:
        pass

    try:
        json_match = re.search(r"\{[\s\S]*\}", clean_text)
        if json_match:
            data = json.loads(json_match.group(0))
            if isinstance(data, dict):
                return pydantic_model.model_validate(data)
    except Exception:
        pass

    if fallback_defaults:
        try:
            return pydantic_model.model_validate(fallback_defaults)
        except Exception:
            pass

    try:
        return pydantic_model.model_construct()
    except Exception:
        raise OutputParserException(f"Failed to parse LLM response into {pydantic_model.__name__}: {raw_response[:200]}")


def parse_json_output_with_retry(
    raw_response: str,
    fallback_dict: Dict[str, Any] = None
) -> Dict[str, Any]:
    
    clean_text = sanitize_json_string(raw_response)
    json_parser = JsonOutputParser()

    try:
        return json_parser.parse(clean_text)
    except Exception:
        pass

    try:
        return json.loads(clean_text)
    except Exception:
        pass

    try:
        json_match = re.search(r"\{[\s\S]*\}", clean_text)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception:
        pass

    return fallback_dict if fallback_dict is not None else {}
