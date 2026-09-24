"""
Output Parsers for LangChain chains.
Demonstrates both PydanticOutputParser and JsonOutputParser with robust error handling and fallback parsing.
"""

import json
import re
from typing import Type, TypeVar, Any, Dict
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.exceptions import OutputParserException

T = TypeVar("T", bound=BaseModel)


def get_pydantic_parser(pydantic_object: Type[T]) -> PydanticOutputParser[T]:
    """Return a standard LangChain PydanticOutputParser for a given model."""
    return PydanticOutputParser(pydantic_object=pydantic_object)


def get_json_parser() -> JsonOutputParser:
    """Return a standard LangChain JsonOutputParser."""
    return JsonOutputParser()


def sanitize_json_string(raw_text: str) -> str:
    """
    Clean raw LLM string response by removing markdown code blocks,
    leading/trailing whitespace, and unescaped characters.
    """
    text = raw_text.strip()
    # Strip ```json ... ``` or ``` ... ``` code blocks
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if code_block_match:
        text = code_block_match.group(1).strip()
    return text


def parse_llm_output_with_retry(
    raw_response: str,
    pydantic_model: Type[T],
    fallback_defaults: Dict[str, Any] = None
) -> T:
    """
    Attempts to parse LLM raw text output into the specified Pydantic model.
    Includes sanitization, direct JSON parsing, Pydantic validation, and fallback defaults on failure.
    """
    clean_text = sanitize_json_string(raw_response)

    # Strategy 1: LangChain PydanticOutputParser
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    try:
        return parser.parse(clean_text)
    except Exception as e:
        pass

    # Strategy 2: Manual JSON load & Pydantic parse
    try:
        data = json.loads(clean_text)
        if isinstance(data, dict):
            return pydantic_model.model_validate(data)
    except Exception:
        pass

    # Strategy 3: Loose JSON regex extraction (find first '{' to last '}')
    try:
        json_match = re.search(r"\{[\s\S]*\}", clean_text)
        if json_match:
            data = json.loads(json_match.group(0))
            if isinstance(data, dict):
                return pydantic_model.model_validate(data)
    except Exception:
        pass

    # Strategy 4: Fallback defaults if parsing fails completely
    if fallback_defaults:
        try:
            return pydantic_model.model_validate(fallback_defaults)
        except Exception:
            pass

    # Return empty model instance using Pydantic construct/defaults
    try:
        return pydantic_model.model_construct()
    except Exception:
        raise OutputParserException(f"Failed to parse LLM response into {pydantic_model.__name__}: {raw_response[:200]}")


def parse_json_output_with_retry(
    raw_response: str,
    fallback_dict: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Attempts to parse LLM response using JsonOutputParser strategy.
    """
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
