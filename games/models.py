from django.db import models
from users.models import User

class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=5, default="-10")

    def __str__(self):
        return self.name

class Vote(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return f"{self.user.username}'s vote for {self.game.name}: {self.value}"
    
class PriceShown(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return f"{self.user.email} was shown {self.game} at {self.value}"

class AverageValue(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="value")
    value = models.DecimalField(decimal_places=2, max_digits=7)