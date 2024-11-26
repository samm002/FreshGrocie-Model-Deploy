from ..utils import map_nutrition_details

class NutritionService:
  def __init__(self, fatsecret_client):
    self.fatsecret_client = fatsecret_client

  def get_nutrition_detail(self, food_id):
    try:
      result = self.fatsecret_client.make_request(
          method='GET',
          api_method='food.get',
          food_id=str(food_id)
      )
      
      food_data = result['food']
      
      servings = food_data['servings']['serving']
      serving = next((serving for serving in servings if serving['serving_description'] == '100 g'), None) or servings
      
      food_detail = {
        'detail': serving['serving_url'],
        'nutrition_detail': map_nutrition_details(serving)
      }
      
      return food_detail
    except Exception as e:
      return {'error': str(e)}