from fastapi import APIRouter
from app.services.external_api_service import fetch_movie_data
from app.services.llm_service import generate_mock_recommendations
from pydantic import BaseModel

class MessageRequest(BaseModel):
    message: str

router = APIRouter()

@router.post("/recommendations")
def get_recommendations(request: MessageRequest):
    message = request.message

    # Mocked logic to interpret user message
    preferences = {"likes": ["Sci-Fi", "Action"]} if "Sci-Fi" in message else {"likes": ["Drama"]}

    # Fetch movies from external API
    movies = fetch_movie_data()

    # Generate a response using the LLM service
    recommendation_response = generate_mock_recommendations(movies)
    return {"response": recommendation_response}