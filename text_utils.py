
import re


def clean_text(text):
    """
    Lowercase and clean a single review string before it gets vectorized.

    Steps:
    1. Lowercase everything, so "Great" and "great" are treated the same.
    2. Remove HTML tags - the IMDB dataset is full of "<br /><br />"
       line breaks, which would otherwise get treated as words.
    3. Remove URLs, just in case a review contains a link.
    4. Remove anything that isn't a letter or whitespace (numbers,
       punctuation, symbols) - punctuation adds noise to the vocabulary
       without adding much sentiment signal.
    5. Collapse repeated whitespace into single spaces and trim the ends.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)            # strip HTML tags like <br />
    text = re.sub(r"http\S+|www\.\S+", " ", text)    # strip URLs
    text = re.sub(r"[^a-z\s]", " ", text)            # keep only letters/spaces
    text = re.sub(r"\s+", " ", text).strip()         # collapse whitespace

    return text