# szurubooru-auto-tagger
---
A small iqdb auto tagger for szurubooru 

## Requirements
- [Python 3.12](https://www.python.org/downloads/)
- Python Module "requests": ``` pip install requests ```
- Python Module "beautifulsoup4": ``` pip install beautifulsoup4 ```
- Python Module "lxml": ``` pip install lxml ```

## Setup
Please add your szurubooru endpoint, username and password inside the `config.py` file.

## Usage
#### Batch Tagging:
```python
python AutoTagger.py --post 10 --postend 15
```
#### Single Tagging:
```python
python AutoTagger.py --post 10
```

| Argument  |  Meaning  | Example |
|---|---|---|
| --post     | ID of your Post you want to tag | --post 10 |
| --postend  | (optional) When specified, it will tag all posts between `post` and `postend`  | --postend 15 |

