# metalmetrics

[![Actions Status](https://github.com/craftslab/metalmetrics-py/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/craftslab/metalmetrics-py/actions?query=workflow%3ACI)
[![Docker](https://img.shields.io/docker/pulls/craftslab/metalmetrics-py)](https://hub.docker.com/r/craftslab/metalmetrics-py)
[![License](https://img.shields.io/github/license/craftslab/metalmetrics-py.svg?color=brightgreen)](https://github.com/craftslab/metalmetrics-py/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/metalmetrics.svg?color=brightgreen)](https://pypi.org/project/metalmetrics)
[![Tag](https://img.shields.io/github/tag/craftslab/metalmetrics-py.svg?color=brightgreen)](https://github.com/craftslab/metalmetrics-py/tags)



## Introduction

*metalmetrics* is a worker of *[metalflow](https://github.com/craftslab/metalflow/)* written in Python.



## Requirement

- Python >= 3.7



## Run

- **Local mode**

  ```bash
  git clone https://github.com/craftslab/metalmetrics-py.git
  
  cd metalmetrics-py
  pip install -Ur requirements.txt
  python metrics.py --config-file="config.yml" --output-file="output.json"
  ```



- **Service mode**

  ```bash
  git clone https://github.com/craftslab/metalmetrics-py.git
  
  cd metalmetrics-py
  pip install -Ur requirements.txt
  python metrics.py --config-file="config.yml" --listen-url="127.0.0.1:9090"
  ```



## Docker

- **Local mode**

  ```bash
  git clone https://github.com/craftslab/metalmetrics-py.git
  
  cd metalmetrics-py
  docker build --no-cache -f Dockerfile -t craftslab/metalmetrics-py:latest .
  docker run -it -v /tmp:/tmp craftslab/metalmetrics-py:latest ./metalmetrics --config-file="config.yml" --output-file="/tmp/output.json"
  ```



- **Service mode**

  ```bash
  git clone https://github.com/craftslab/metalmetrics-py.git
  
  cd metalmetrics-py
  docker build --no-cache -f Dockerfile -t craftslab/metalmetrics-py:latest .
  docker run -it -p 9090:9090 craftslab/metalmetrics-py:latest ./metalmetrics --config-file="config.yml" --listen-url="127.0.0.1:9090"
  ```



## Usage

```bash
usage: metrics.py [-h] --config-file CONFIG_FILE
                  [--listen-url LISTEN_URL | --output-file OUTPUT_FILE] [-v]

Metal Metrics

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        config file (.yml)
  --listen-url LISTEN_URL
                        listen url (host:port)
  --output-file OUTPUT_FILE
                        output file (.json|.txt|.xlsx)
  -v, --version         show program's version number and exit
```



## Settings

*metalmetrics* parameters can be set in the directory [config](https://github.com/craftslab/metalmetrics-py/blob/master/metalmetrics/config).

An example of configuration in [config.yml](https://github.com/craftslab/metalmetrics-py/blob/master/metalmetrics/config/config.yml):

```yaml
metadata:
  name: metalmetrics
spec:
  bare:
  - cpu
  - disk
  - io
  - ip
  - kernel
  - mac
  - network
  - os
  - ram
  container:
  kubernetes:
```



## Design

![design](design.png)



## License

Project License can be found [here](LICENSE).



## Reference

- [gRPC in Python](https://grpc.io/docs/languages/python/)
- [health-check-script](https://github.com/SimplyLinuxFAQ/health-check-script)
- [python-diamond](https://github.com/python-diamond/Diamond)
- [sysperf](https://github.com/iandk/sysperf)
