import re
from datetime import timedelta
from typing import Dict, Any

from .common import sanitize_es_result, write_to_file
from ...appcli.data_args import DataArguments
from ...appcli.elastic_query import ElasticQuery
from ...appcli.iterators import DateTimeIterator, DateTimeState, RuntimeData


def contains_any(text: str, keywords: list[str]) -> bool:
    for kw in keywords:
        if kw.islower():
            # Case-sensitive check for fully-lowercase keywords
            if kw in text:
                return True
        else:
            # Case-insensitive for any keyword with non-lowercase chars
            # Use regex with word boundaries to avoid partial-word false positives when desired
            pat = re.compile(re.escape(kw), flags=re.IGNORECASE)
            if pat.search(text):
                return True
    return False


def write(state: DateTimeState):
    global paths
    data_create_path = paths['create']['data']
    file_name = state.data_args.dataset_name + f"-{state.runtime_data.file_num:02d}"
    write_to_file(
        state.runtime_data.items,
        data_create_path,
        file_name
    )
    logger.info("Writing data to %s", data_create_path)
    state.runtime_data.file_num += 1
    state.runtime_data.items = []


def load_data(state: DateTimeState):
    req = ElasticQuery(state.data_args.dataset_src_url, state.data_args.dataset_src_user)
    query_desc: Dict[str, Any] = state.data_args.dataset_src_query

    for category, keywords in query_desc['keywords'].items():
        query = query_desc['template']
        keywords_str = ",\n".join(f'{{ "match_phrase": {{ "text": "{item}" }} }}' for item in keywords)
        query = query.replace('<should_match>', keywords_str)
        results, total = req.query(query, state.step_start, state.step_end)
        for result in results:
            item = sanitize_es_result(result, {'category': category})
            if item is None:
                continue
            body = item['body']
            title = item['title']
            if not body.startswith(title):
                text = title + "\n\n" + body
            else:
                text = body
            if not contains_any(text, keywords):
                continue
            state.runtime_data.items.append(item)
            if len(state.runtime_data.items) % 1000 == 0:
                logger.info(f"Processing {state.progress:.2f} @ step {state.step_start} / {state.end}")
            if state.runtime_data.num_items_per_file == len(state.runtime_data.items):
                write(state)


def main(data_args : DataArguments) -> None:
    # noinspection PyGlobalUndefined
    global logger, paths
    logger.info(f"Downloading {data_args.dataset_name}")
    runtime = RuntimeData(num_items_per_file=100000)
    for state in DateTimeIterator(
        start=data_args.dataset_src_start,
        end=data_args.dataset_src_end,
        step=timedelta(hours=3),
        callback=load_data,
        data_args=data_args,
        runtime_data=runtime
    ):
        # logger.info(f"Processing {state.progress:.2f} @ step {state.step_start} / {state.end}")
        pass
