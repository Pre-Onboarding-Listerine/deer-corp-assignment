from src.rate_policies.domain.models import DeerUsage


class FeeCalculator:
    def __init__(self, user_id: int):
        self.user_id = user_id
        
    @classmethod
    def of(cls, user_id: int):
        return cls(user_id=user_id)

    def calculate_with(self, usage: DeerUsage):
        pass
