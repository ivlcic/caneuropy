from dataclasses import dataclass

@dataclass
class DataArguments:
    dataset_name: str = ""
    dataset_url: str = ""
    dataset_config_name: str = ""
    max_seq_length: int = 512
    overwrite_cache: bool = False
    preprocessing_num_workers: int = 4