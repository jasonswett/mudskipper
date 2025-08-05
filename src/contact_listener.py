import Box2D
from src.food_morsel import FoodMorsel

class ContactListener(Box2D.b2ContactListener):
    def __init__(self, organisms, food_morsels):
        Box2D.b2ContactListener.__init__(self)
        self.organisms = organisms
        self.food_morsels = food_morsels

    def BeginContact(self, contact):
        body_a = contact.fixtureA.body
        body_b = contact.fixtureB.body

        food_morsel = self._food_morsel(body_a, body_b)
        if not food_morsel or food_morsel.eaten:
            return
            
        organism = self._organism(body_a, body_b, food_morsel.body)
        if not organism:
            return
            
        food_morsel.eaten = True
        organism.nourish()

    def _food_morsel(self, body_a, body_b):
        for food_morsel in self.food_morsels:
            if food_morsel.body == body_a or food_morsel.body == body_b:
                return food_morsel
        return None

    def _organism(self, body_a, body_b, food_body):
        other_body = body_b if food_body == body_a else body_a
        for organism in self.organisms:
            if organism.body == other_body:
                return organism
        return None
