import json
import re

def trim_text(text: str): 
    """ Removes spaces and newline characters. """ 
    return text.strip().replace("\n", " ")

def extract_json(text_response):
    pattern = r'\{[^{}]*\}'
    matches = re.finditer(pattern, text_response)
    json_objects = []
    for match in matches:
        json_str = match.group(0)
        try:
            # Replace single quotes with double quotes for valid JSON
            json_str = json_str.replace("'", '"')
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            # Extend the search for incomplete JSON strings
            extended_json_str = extend_search(text_response, match.span())
            try:
                extended_json_str = extended_json_str.replace("'", '"')
                json_obj = json.loads(extended_json_str)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                continue
    return json_objects if json_objects else None

def extend_search(text, span):
    start, end = span
    nest_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            nest_count += 1
        elif text[i] == '}':
            nest_count -= 1
            if nest_count == 0:
                return text[start:i + 1]
    return text[start:end]

if __name__ == "__main__":
    text_response = "json {'amount': 1600.00, 'category': 'food'}"
    extracted_json = extract_json(text_response)
    print(extracted_json)