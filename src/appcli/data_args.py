from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class DataArguments:
    dataset_name: str = ""
    dataset_url: str = ""
    dataset_config_name: str = ""
    max_seq_length: int = 512
    overwrite_cache: bool = False
    preprocessing_num_workers: int = 4
    dataset_src_url: str = ""
    dataset_src_start: str = ""
    dataset_src_end: str = ""
    dataset_src_user: str = ""
    dataset_src_query: Dict[str, Any] = field(default_factory=dict)
