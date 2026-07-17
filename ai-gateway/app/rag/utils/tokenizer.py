from __future__ import annotations

import re
from collections import Counter


class Tokenizer:
    """
    Production-ready tokenizer.

    Supports:
        - Word tokenization
        - Sentence tokenization
        - Paragraph tokenization
        - Basic normalization
        - Frequency analysis

    Future extensions:
        - tiktoken
        - HuggingFace tokenizers
        - spaCy
        - NLTK
        - SentencePiece
    """

    WORD_PATTERN = re.compile(r"\b[\w'-]+\b", re.UNICODE)

    SENTENCE_PATTERN = re.compile(
        r"(?<=[.!?])\s+"
    )

    # ---------------------------------------------------------
    # Word Tokenization
    # ---------------------------------------------------------

    def tokenize(
        self,
        text: str,
        lowercase: bool = True,
    ) -> list[str]:

        if lowercase:
            text = text.lower()

        return self.WORD_PATTERN.findall(text)

    # ---------------------------------------------------------
    # Sentence Tokenization
    # ---------------------------------------------------------

    def sentences(
        self,
        text: str,
    ) -> list[str]:

        text = text.strip()

        if not text:
            return []

        return [
            sentence.strip()
            for sentence in self.SENTENCE_PATTERN.split(text)
            if sentence.strip()
        ]

    # ---------------------------------------------------------
    # Paragraph Tokenization
    # ---------------------------------------------------------

    def paragraphs(
        self,
        text: str,
    ) -> list[str]:

        return [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def normalize(
        self,
        text: str,
        lowercase: bool = True,
    ) -> str:

        if lowercase:
            text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def word_count(
        self,
        text: str,
    ) -> int:

        return len(
            self.tokenize(text)
        )

    def unique_words(
        self,
        text: str,
    ) -> int:

        return len(
            set(
                self.tokenize(text)
            )
        )

    def frequencies(
        self,
        text: str,
    ) -> Counter:

        return Counter(
            self.tokenize(text)
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def most_common(
        self,
        text: str,
        n: int = 10,
    ):

        return self.frequencies(
            text
        ).most_common(n)

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def configuration(self):

        return {
            "word_pattern": self.WORD_PATTERN.pattern,
            "sentence_pattern": self.SENTENCE_PATTERN.pattern,
            "lowercase_default": True,
        }

    # ---------------------------------------------------------
    # Dunder
    # ---------------------------------------------------------

    def __len__(self):

        return 2

    def __iter__(self):

        yield from self.configuration().items()