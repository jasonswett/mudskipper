import Box2D
from src.food_morsel import FoodMorsel

class ContactListener(Box2D.b2ContactListener):
    def __init__(self, organisms, food_morsels):
        Box2D.b2ContactListener.__init__(self)
        self.organisms = organisms
        self.food_morsels = food_morsels
        self.touching_organisms = set()  # Set of organism pairs that are touching
        self.contact_events = []  # List of contact events for reproduction

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

            # Add contact event for reproduction (only if this pair hasn't already been recorded)
            world_manifold = contact.worldManifold
            contact_position = world_manifold.points[0] if world_manifold.points else (0, 0)

            # Check if this pair already has a contact event
            pair_exists = any(
                (event['organism_a'] == organism_a and event['organism_b'] == organism_b) or
                (event['organism_a'] == organism_b and event['organism_b'] == organism_a)
                for event in self.contact_events
            )

            if not pair_exists:
                self.contact_events.append({
                    'organism_a': organism_a,
                    'organism_b': organism_b,
                    'position': contact_position
                })
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

    def get_contact_events(self):
        """Get and clear the list of contact events."""
        events = self.contact_events.copy()
        self.contact_events.clear()
        return events
