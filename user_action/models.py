from django.db import models

from deck.models import Deck
from user.models import User


class DeckOpened(models.Model):
    deck_view_id = models.AutoField(primary_key=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_deck_opened'
