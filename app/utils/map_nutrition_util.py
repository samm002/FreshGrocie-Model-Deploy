def map_nutrition_details(serving):
    nutrition_details = {
        "calcium": f"{serving['calcium']}%",
        "calories": f"{serving['calories']}kcal",
        "carbohydrate": f"{serving['carbohydrate']}g",
        "cholesterol": f"{serving['cholesterol']}mg",
        "fat": f"{serving['fat']}g",
        "fiber": f"{serving['fiber']}g",
        "iron": f"{serving['iron']}%",
        "monounsaturated_fat": f"{serving['monounsaturated_fat']}g",
        "polyunsaturated_fat": f"{serving['polyunsaturated_fat']}g",
        "potassium": f"{serving['potassium']}mg",
        "protein": f"{serving['protein']}g",
        "saturated_fat": f"{serving['saturated_fat']}g",
        "sodium": f"{serving['sodium']}mg",
        "sugar": f"{serving['sugar']}g",
        "vitamin_a": f"{serving['vitamin_a']}%",
        "vitamin_c": f"{serving['vitamin_c']}%",
    }

    return nutrition_details
