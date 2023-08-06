from . import utiles
from .models import Match

"""
    Text winnowing module:
        Function for Manipulation format Text:
          - winnowing
          - winnow
          - ngram
"""


@utiles.type_check
def winnowing(tokens: filter, k: int) -> list:
    return list(map(lambda ngram: __winnow(ngram, k), __ngram(tokens, k)))


@utiles.type_check
def __winnow(ngram: list, k: int) -> Match:
    ngram = zip(*ngram)
    ngram = list(ngram)
    text = " ".join(ngram[1])
    return Match(
        first_index=ngram[0][0],
        last_index=ngram[0][-1] + 1,
        text=text,
        sources=[]
    )


@utiles.type_check
def __ngram(tokens: filter, k: int):
    tokens = list(tokens)
    n = len(tokens)
    if n and n < k:
        yield tokens
    else:
        for i in range(n - k + 1):
            yield tokens[i:i + k]
