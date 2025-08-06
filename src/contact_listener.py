import Box2D
from src.food_morsel import FoodMorsel

class ContactListener(Box2D.b2ContactListener):
    def __init__(self, organisms, food_morsels):
        Box2D.b2ContactListener.__init__(self)
        self.organisms = organisms
        self.food_morsels = food_morsels
        self.touching_organisms = set()  # Set of organism pairs that are touching

    def BeginContact(self, contact):
        body_a = contact.fixtureA.body
        body_b = contact.fixtureB.body

        # Check for organism-organism collision
        organism_a = self._get_organism(body_a)
        organism_b = self._get_organism(body_b)

        if organism_a and organism_b:
            # Two organisms are touching
            pair = tuple(sorted([id(organism_a), id(organism_b)]))  # Use IDs to ensure consistent ordering
            self.touching_organisms.add(pair)
            return

        # Check for organism-food collision
        food_morsel = self._food_morsel(body_a, body_b)
        if not food_morsel or food_morsel.eaten:
            return

        organism = self._organism(body_a, body_b, food_morsel.body)
        if not organism:
            return

        food_morsel.eaten = True
        organism.nourish()

    def EndContact(self, contact):
        body_a = contact.fixtureA.body
        body_b = contact.fixtureB.body

        # Check for organism-organism collision ending
        organism_a = self._get_organism(body_a)
        organism_b = self._get_organism(body_b)

        if organism_a and organism_b:
            # Two organisms stopped touching
            pair = tuple(sorted([id(organism_a), id(organism_b)]))
            self.touching_organisms.discard(pair)  # Remove if exists

    def _get_organism(self, body):
        """Find organism that owns the given body."""
        for organism in self.organisms:
            if organism.body == body:
                return organism
        return None

    def is_organism_touching(self, organism):
        """Check if an organism is touching any other organism."""
        organism_id = id(organism)
        for pair in self.touching_organisms:
            if organism_id in pair:
                return True
        return False

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
