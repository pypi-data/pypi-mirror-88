import regex as re
from typing import List, Dict, Union, Tuple
from . import exceptions

SPLIT_OPTIONS = [
    "DOUBLE_NEWLINE",
    "NEWLINE",
    "WORD_LIMIT",
    "CHAR_LIMIT",
    "CUSTOM"
]


# current implementation of WORD split will destroy whitespace formatting!
# what if doc consists of one looooong string without any whitespaces?

class TextSplitter:
    """ Split text into subsections based on given character/word limit.

    Parameters
    ----------
    split_by : str
        Method used for splitting the text.
    split_pattern : str
        Custom character/string_pattern for splitting the text.
        Has effect only if split_by = 'CUSTOM'.
    strip_whitespaces : bool
        If enabled, whitespaces (newlines etc.) are stripped from each page.

    Attributes
    ------------
    split_by : str
        Stores parameter `split_by`.
    split_pattern : str
        Stores parameter `split_pattern`.
    strip_whitespaces : bool
        Stores parameter `strip_whitespaces`.
    default_word_limit : int
        Default max number of words per one chunk.
    default_char_limit : int
        Default max number of characters per one chunk.
    """
    def __init__(self, split_by: str = "CHAR_LIMIT", split_pattern: str = "", strip_whitespaces: bool = True):
        self.split_by = self._validate_split_option(split_by)
        self.split_pattern = split_pattern
        self.strip_whitespaces = strip_whitespaces
        self.default_word_limit = 700
        self.default_char_limit = 4000

    def _validate_split_option(self, split_by: str):
        if split_by not in SPLIT_OPTIONS:
            raise exceptions.InvalidSplitMethodError(f"""Invalid argument for param `split_by`: `{split_by}`.
                Make sure to use one of the following: {SPLIT_OPTIONS}""")
        return split_by

    def get_split_options(self) -> List[str]:
        """ Retrieve list of available options for splitting the text.
        """
        return SPLIT_OPTIONS

    def _split_by_pattern(self, text: str, split_pattern: str) -> List[Dict[str, Union[str, int]]]:
        """ Split by string pattern specified with param `split_pattern`.

        Parameters
        ----------
        text : str
            Text to split.
        split_pattern : str
            Pattern used for splitting.
        """
        if self.strip_whitespaces:
            splits = [t.strip() for t in text.split(split_pattern) if t.strip()]
        else:
            splits = [t for t in text.split(split_pattern) if t.strip()]

        return [{"text": t, "page": i+1} for i, t in enumerate(splits)]

    def _split_by_word_limit(self, text: str, max_limit: int) -> List[Dict[str, Union[str, int]]]:
        """ Split into chunks of length `max_limit` (each chunk consists of `max_limit` words).

        Parameters
        ----------
        text : str
            Text to split.
        max_limit: int
            Maximum number of words per one chunk.
        """
        chunks = []
        words = [t for t in text.split()]

        n_chunks = int(len(words)/max_limit)

        for i in range(n_chunks+1):
            slice_start = i*max_limit
            slice_end = i*max_limit + max_limit

            chunk_words = words[slice_start:slice_end]
            chunk = " ".join(chunk_words)

            # Remove trailing whitespaces
            if self.strip_whitespaces:
                chunk = chunk.strip()

            if chunk:
                chunks.append(chunk)

        return [{"text": t, "page": i+1} for i, t in enumerate(chunks)]

    def _split_by_char_limit(self, text: str, max_limit: int) -> List[Dict[str, Union[str, int]]]:
        """ Split into chunks of length `max_limit` (each chunk consists of `max_limit` characters).

        Parameters
        ----------
        text : str
            Text to split.
        max_limit: int
            Maximum number of characters per one chunk.
        """
        chunks = []
        n_chunks = int(len(text)/max_limit)

        offset = 0
        for i in range(n_chunks+1):
            slice_start = i*max_limit + offset
            slice_end = i*max_limit + max_limit + offset

            chunk = text[slice_start:slice_end]

            # Add non-whitespace characters from the begging of next chunk
            # to avoid splitting words:
            for c in text[slice_end:]:
                if not re.match(r"\s", c):
                    chunk+=c
                    offset+=1
                else:
                    break

            # Remove trailing whitespaces
            if self.strip_whitespaces:
                chunk = chunk.strip()

            if chunk:
                chunks.append(chunk)

        return [{"text": t, "page": i+1} for i, t in enumerate(chunks)]

    def split(self, text: str, max_limit: int = None) -> List[Dict[str, Union[str, int]]]:
        """ Split text into smaller chunks.

        Parameters
        ----------
        text : str
            Text to split.
        max_limit : int
            Max number of words or characters per each chunk. Has effect only if `split_by == 'WORD_LIMIT'` or
            `split_by == 'CHAR_LIMIT'`.

        Returns
        --------
        split_result: List[Dict[str, Union[str, int]]]
            List of dicts with text chunks and corresponding page numbers, e.g:
            [{'text': chunk_1, 'page': 1}, {'text': chunk_2, 'page': 2}]

        """
        if self.split_by == "DOUBLE_NEWLINE":
            split_result = self._split_by_pattern(text, "\n\n")

        elif self.split_by == "NEWLINE":
            split_result = self._split_by_pattern(text, "\n")

        elif self.split_by == "WORD_LIMIT":
            if not max_limit:
                max_limit = self.default_word_limit
            split_result = self._split_by_word_limit(text, max_limit)

        elif self.split_by == "CHAR_LIMIT":
            if not max_limit:
                max_limit = self.default_char_limit
            split_result = self._split_by_char_limit(text, max_limit)

        elif self.split_by == "CUSTOM":
            split_result = self._split_by_pattern(text, self.split_pattern)


        return split_result
