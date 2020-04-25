# szurubooru-auto-tagger
---
A small iqdb auto tagger for szurubooru 

## Requirements
- [Python 3.8](https://www.python.org/downloads/)
- Python Module "requests": ```python -m pip install requests ```
- Python Module "beautifulsoup4": ```python -m pip install beautifulsoup4 ```
- Python Module "lxml": ```python -m pip install lxml ```

## Disclaimer
This Project is still very early in development. Bugs are guaranteed.
Batch Tagging waits 10s after each request, so IQDB won't block your IP due to flooding!

## Usage
#### Batch Tagging:
```
python AutoTagger.py --username User --password Pass --adress YourBooruAdress --mode 2 --poststart 10 --postend 15
```
#### Single Tagging:
```
python AutoTagger.py --username User --password Pass --adress YourBooruAdress --poststart 10
```

| Argument  |  Meaning  | Example |
|---|---|---|
| --username  |  Your Account Username - needs high enough privileges  | --username Auto-Tagger |
| --password  |  Your Account Password | --password ILikeHentai |
| --adress | Your Public Szurubooru-Adress - needs to be accessible from outside!  | --adress http://example.com/ |
| --mode  | Tagging Mode - 1 = Single Post - 2 = Batch | --mode 1 (default) |
| --poststart  | ID of your Post - when using 'mode = 2' this needs to be smaller than 'postend' | --poststart 10 |
| --postend  | ID of your Post - onyl if 'mode = 2' - for batch tagging  | --postend 15 |



### Tagging with embedded auth

#### You can skip `--username`, `--password` and `--adress` by editing the python file:
```Python
embeddedauth = False #set this to "True" to skip command args

booruadresse = "http://website:80/" #Insert here your Public Booru Adress - must be reachable from outside            
booruloginname = "username" #Booru Username - must have high enough privileges                                        
booruloinpassw = "password" # Booru User Password                                                                     
```

#### Batch Tagging:
```
python AutoTagger.py --poststart 10 --postend 15
```
#### Single Tagging:
```
python AutoTagger.py --poststart 10
```
