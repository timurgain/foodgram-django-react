import io

from django.http import HttpResponse

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.models import IngredientInRecipe, Recipe


def get_ingredients_from_shopping_cart(request) -> dict:
    """Collects and returns ingredients from a shopping cart recipes."""

    ingredients = {}
    recipes = Recipe.objects.filter(carts__user=request.user)

    for recipe in recipes:
        ingredients_in_recipe = (IngredientInRecipe.objects
                                 .filter(recipe=recipe))

        for obj in ingredients_in_recipe:
            if obj.ingredient.name in ingredients:
                ingredients[obj.ingredient.name][0] += obj.amount
            else:
                ingredients.update({
                    obj.ingredient.name: [obj.amount,
                                          obj.ingredient.measurement_unit]
                })
    return ingredients


def get_shopping_file_txt(ingredients: dict) -> HttpResponse:
    """Converts dict of ingredients into HttpResponse with txt file attachment.
    """
    shopping_file = ''
    for key, value in ingredients.items():
        shopping_file += f"{key} - {value[0]} {value[1]}\n"
    response = HttpResponse(content=shopping_file,
                            content_type='text/plain')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_file.txt"')
    return response


def get_shopping_file_pdf(ingredients: dict) -> HttpResponse:
    """Converts dict of ingredients into HttpResponse with pdf file attachment.
    """
    # https://docs.djangoproject.com/en/4.0/howto/outputting-pdf/#how-to-create-pdf-files
    params = {
        'X_START': 50,
        'Y_START': 800,
        'HEAD_FONT_SIZE': 16,
        'TEXT_FONT_SIZE': 12,
    }

    buffer = io.BytesIO()
    pdf_obj = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont(
        'Comfortaa-light', 'data/Comfortaa-Light.ttf'))
    pdf_obj.setFont('Comfortaa-light', params['HEAD_FONT_SIZE'])
    pdf_obj.drawString(
        params['X_START'], params['Y_START'], "Foodgram ingredients list:")

    pdf_obj.setFont('Comfortaa-light', params['TEXT_FONT_SIZE'])
    for key, value in ingredients.items():
        params['Y_START'] -= (params['TEXT_FONT_SIZE'] * 2)
        ingredient = f"- {key} - {value[0]} {value[1]}"
        pdf_obj.drawString(params['X_START'], params['Y_START'], ingredient)

    pdf_obj.showPage()
    pdf_obj.save()
    buffer.seek(0)
    response = HttpResponse(content=buffer, content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_file.pdf"')
    return response
