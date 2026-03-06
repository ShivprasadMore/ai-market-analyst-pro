"""
Utilities for handling JSON data, specifically for cleaning AI responses.
"""
import json
import re
import logging

logger = logging.getLogger(__name__)

def clean_and_parse_json(text: str) -> dict:
    """
    Cleans a string potentially containing markdown JSON blocks and parses it.
    
    Args:
        text: The raw response text from the AI.
        
    Returns:
        The parsed dictionary.
        
    Raises:
        json.JSONDecodeError: If JSON parsing fails after cleaning.
        ValueError: If no JSON structure is found in the text.
    """
    if not text:
        raise ValueError("Empty response text")

    # Remove markdown code fences if present
    json_str = text.strip()
    json_str = re.sub(r'^```json\s*', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'^```\s*', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'\s*```$', '', json_str, flags=re.MULTILINE)
    
    # Try to find the first '{' and last '}' to extract the JSON object
    try:
        start_idx = json_str.index('{')
        end_idx = json_str.rindex('}') + 1
        json_str = json_str[start_idx:end_idx]
    except ValueError:
        logger.error(f"No JSON object found in text. First 200 chars: {text[:200]}")
        # Potential fallback: if it looks like keys are present but braces missing
        if '"summary_title":' in json_str or 'summary_title:' in json_str:
            logger.info("Interpreting content as potentially missing outer braces; attempting repair.")
            json_str = "{" + json_str + "}"
        else:
            raise ValueError("No valid JSON structure found in response")

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed at char {e.pos}: {e.msg}")
        logger.debug(f"Attempted to parse (truncated): {json_str[:500]}...")
        # One last ditch effort: remove common LLM trailing commas or extra text
        try:
            # Clean trailing commas in lists/objects before closing braces/brackets
            json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
            return json.loads(json_str)
        except:
            raise e
