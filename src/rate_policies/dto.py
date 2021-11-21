from pydantic import BaseModel


class RequestUsage(BaseModel):
    user_id: int
    use_deer_name: int
    use_end_lat: float
    use_ned_lng: float
    use_start_at: str
    use_end_at: str
