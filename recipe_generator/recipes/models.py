from django.db import models
from django.contrib.auth import get_user_model

class Recipe(models.Model):
    # Links each recipe to a user
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # Core recipe details
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()

    # Timestamps for tracking creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Recommended addition

    # Improved string display for admin panel clarity
    def __str__(self):
        return f"{self.title} by {self.user.username}"  # Clearer display in admin panel
