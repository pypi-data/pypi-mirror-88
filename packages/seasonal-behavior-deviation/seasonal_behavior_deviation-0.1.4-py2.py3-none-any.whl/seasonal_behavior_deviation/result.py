class SBDResult(object):
    def __init__(self, original_data: list) -> None:
        self.original_data = original_data
        self.scores = []
        self.normal_behavior = []
        self.normalized_data = []

    def set_computed_values(self, scores: list, normal_behavior: list, normalized_data: list) -> None:
        self.scores = scores
        self.normal_behavior = normal_behavior
        self.normalized_data = normalized_data
