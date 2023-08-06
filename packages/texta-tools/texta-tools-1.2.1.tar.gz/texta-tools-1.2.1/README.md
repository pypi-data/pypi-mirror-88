# TEXTA Tools Python Package

* **Text Processor**
* **Embedding & Phraser**
* **MLP Analyzer**
* **Text Splitter** - Documentation with user guide is available [here](https://git.texta.ee/texta/texta-tools-python/-/wikis/Text-Splitter-Documentation).

## Installation

`pip install texta-tools`

## Testing

`python -m pytest -v tests`



## Using TikaOCR with different languages
1. Install language packs: [https://cwiki.apache.org/confluence/display/tika/TikaOCR](https://cwiki.apache.org/confluence/display/tika/TikaOCR)
2. Override the configured language with your request:

    ``` python
    res = parser.from_file("yourfile.png", requestOptions={"headers": {"X-Tika-OCRLanguage": "est+eng+rus"}})
    ```
