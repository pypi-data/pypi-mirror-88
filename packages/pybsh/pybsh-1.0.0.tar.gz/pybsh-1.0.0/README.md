# `pybsh`

Use bash-like syntax for running subcommands in Python

```python
from pybsh import cmd, go

cmd() | "echo hi" | "sed 's/hi/bye/g'" > go
```


## Installation

```bash
pip install pybsh
```

### From Source

```bash
git clone https://github.com/driazati/pybsh.git
cd pybsh
pip install --editable .
```

## API

???