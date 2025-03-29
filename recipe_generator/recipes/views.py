from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages framework

# 🚨 CREATE RECIPE
@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Assign the logged-in user
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('view_past_recipes')
    else:
        form = RecipeForm()

    return render(request, 'recipes/create_recipe.html', {'form': form})
# 🚨 VIEW PAST RECIPES
@login_required
def view_past_recipes(request):
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')

    # Handle empty list gracefully
    if not recipes.exists():
        messages.info(request, "You haven't added any recipes yet.")

    return render(request, 'recipes/view_past_recipes.html', {'recipes': recipes})

# 🚨 EDIT RECIPE
@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    # Ensure only the owner can edit the recipe
    if recipe.user != request.user:
        messages.error(request, "You are not authorized to edit this recipe.")
        return redirect('view_past_recipes')

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('view_past_recipes')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'form': form})

# 🚨 DELETE RECIPE
@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    # Ensure only the owner can delete the recipe
    if recipe.user != request.user:
        messages.error(request, "You are not authorized to delete this recipe.")
        return redirect('view_past_recipes')

    if request.method == 'POST':  # Confirmation step
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('view_past_recipes')

    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})
