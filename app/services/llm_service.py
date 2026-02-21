from app.services.external_api_service import fetch_movie_data

def generate_mock_recommendations(movies):
    if len(movies) < 2:
        return "No hay suficientes películas para recomendar."

    return f"Te recomiendo ver {movies[0]['title']} o {movies[1]['title']}."