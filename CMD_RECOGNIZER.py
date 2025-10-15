from thefuzz import fuzz
import config

def matching(fuzzy_str: str) -> str:
    if fuzzy_str is not None:
        fuzzy_str = fuzzy_str.lower()

        for key, values in config.VA_CMD.items():
            for value in values:
                if fuzz.ratio(value.lower(), fuzzy_str) >= 75:
                    return key
    return ''
