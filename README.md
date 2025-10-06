# caneuropy
Simple ML research framework

```shell
python -m venv .venv && source .venv/bin/activate
```

```shell
pip install -U pip setuptools
```

```shell
pip install -r requirements.txt
```

## Dataset mining / creation
```shell
./data create esg
```

```shell
./data create ml-kw-match
```

TODO :D
```shell
./data download ner
./data download newsmon
./data download eurlex
./data prepare ner
./data prepare newsmon
./data prepare eurlex
./data embed newsmon -c bge-m3.yaml -c sl.yaml
./data embed newsmon -c m-gte.yaml
./data embed newsmon -c emb-genna3.yaml -c sl.yaml
./data resample newsmon -c sl.yaml
./data resample newsmon -c sr.yaml
./data resample newsmon
./data sample newsmon -c hard_neg.yaml
./data split ner
./data split newsmon -c sl.yaml
./data split eurlex -c sl.yaml
./data analyze newsmon -c sl.yaml  
./data analyze newsmon -c sr.yaml  
./data analyze newsmon  
./data analyze eurlex
./train seqence newsmon -c xlmr.yaml
./train seqence newsmon -c mm-bert.yaml
./train seqence eurlex -c xlmr.yaml
./train seqence eurlex -c mm-bert.yaml
./train token ner -c xlmr.yaml
./train token ner -c m-bert.yaml
./train token ner -c mm-bert.yaml
./train token ner -c genna3-200m.yaml
./train token ner -c genna3-1b.yaml
./train hard_neg newsmon -c bge-m3.yaml
./train hard_neg newsmon -c m-gte.yaml
./train hard_neg newsmon -c emb-genna3.yaml
./eval seqence newsmon -c xlmr.yaml
./eval seqence newsmon -c mm-bert.yaml
./eval token ner -c xlmr.yaml
./eval token ner -c m-bert.yaml
./eval token ner -c mm-bert.yaml
./eval token ner -c genna3-200m.yaml
./eval token ner -c genna3-1b.yaml
```