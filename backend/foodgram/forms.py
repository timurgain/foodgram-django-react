from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import IngredientInRecipe, Recipe


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    ingredients = forms.ModelMultipleChoiceField(
        queryset=IngredientInRecipe.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Ingredients',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(RecipeAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['ingredients'].initial = (self.instance
                                                  .ingredientinrecipe_set
                                                  .all())

    def save(self, commit=True):
        recipe = super(RecipeAdminForm, self).save(commit=False)
        if commit:
            recipe.save()

        if recipe.pk:
            recipe.ingreingredientinrecipe_set = (self
                                                  .cleaned_data['ingredients'])
            self.save_m2m()

        return recipe
