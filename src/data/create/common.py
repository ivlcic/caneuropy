import regex
import csv
import json
from pathlib import Path
from typing import Dict, Any, Union, List

__SOURCE_PATT = regex.compile(r'^[\p{Nd}\p{Lu}\s]+(?:[,\s]+)?(?:\s*(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})(?:[,\s]+)?(?:\s*\p{Lu}{2,}[\p{Nd}\p{Lu}\s]+(?:[,\s]+)?(?:\s*\d{1,2}[:.]\d{2})?)?)?\s*$')

def write_to_file(items: List[Dict[str, Any]], path: Union[str, Path], file_name: str) -> None:
    if not items:
        return
    field_names = items[0].keys()
    csv_path = Path(path / f"{file_name}.csv")
    jsonl_path = Path(path / f"{file_name}.jsonl")
    with csv_path.open("a", newline="", encoding="utf-8") as cf:
        with jsonl_path.open("a", encoding="utf-8") as jf:
            writer = csv.DictWriter(cf, fieldnames=field_names)
            if csv_path.stat().st_size == 0:
                writer.writeheader()
            for item in items:
                writer.writerow(item)
                jf.write(json.dumps(item, ensure_ascii=False) + "\n")
    pass


def sanitize_es_result(result: Dict[str, Any], append: Dict[str, Any] = None) -> Union[Dict[str, Any], None]:
    if 'translations' not in result or 'language' not in result:
        return None
    if 'media' not in result or 'country' not in result:
        return None

    media = result['media']
    language = result['language']
    if language not in result['translations']:
        return None

    created = None
    if 'created' in result:
        created = result['created']

    published = None
    if 'published' in result:
        published = result['published']

    url = ''
    if 'url' in result:
        url = result['url']

    translation = result['translations'][language]
    if 'title' not in translation:
        return None
    title = translation['title'].strip()

    body = ''
    if 'body' in translation:
        body = translation['body']

    body = body.replace(url, '').strip()

    if body.startswith(title):
        body = body[len(title):].strip()

    country = ''
    if 'country' in result and 'name' in result['country']:
        country = result['country']['name']

    section = ''
    section_uuid = ''
    if 'rubric' in result and 'name' in result['rubric']:
        section = result['rubric']['name']
        section_uuid = result['rubric']['uuid']

    media_type = ''
    if 'tags' in media:
        for tag in media['tags']:
            if 'class' in tag and 'name' in tag and tag['class'].endswith('MediaType'):
                media_type = tag['name']

    if 'tv' == media_type or 'radio' == media_type:
        lines = body.split("\n")
        if len(lines) > 1:
            match = __SOURCE_PATT.match(lines[0])
            if match is not None:
                body = "\n".join(lines[1:])

    body = body.strip()

    out = {}
    out['uuid'] = result['uuid']
    out['created'] = created
    out['published'] = published

    # insert my_dict right after 'published'
    if append:
        for k, v in append.items():
            out[k] = v

    out['media_uuid'] = media['uuid']
    out['media_name'] = media['name']
    out['section_uuid'] = section_uuid
    out['section_name'] = section
    out['media_type'] = media_type
    out['country'] = country
    out['language'] = language
    out['title'] = title
    out['url'] = url
    out['body'] = body
    return out