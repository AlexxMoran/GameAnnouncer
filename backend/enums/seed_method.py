from enum import Enum


class SeedMethod(str, Enum):
    RANDOM = "random"
    QUALIFICATION_SCORE = "qualification_score"
