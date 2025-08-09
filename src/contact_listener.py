import Box2D
from src.food_morsel import FoodMorsel

class ContactListener(Box2D.b2ContactListener):
    def __init__(self, organisms, food_morsels):
        Box2D.b2ContactListener.__init__(self)
        self.organisms = organisms
        self.food_morsels = food_morsels
        self.touching_organisms = set()  # Set of organism pairs that are touching
        self.contact_events = []  # List of contact events for reproduction

        # Spatial hash maps for O(1) lookups
        self.body_to_organism = {}
        self.body_to_food_morsel = {}
        self._rebuild_spatial_hash()

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
        """Find organism that owns the given body using spatial hash."""
        return self.body_to_organism.get(body)

    def is_organism_touching(self, organism):
        """Check if an organism is touching any other organism."""
        organism_id = id(organism)
        for pair in self.touching_organisms:
            if organism_id in pair:
                return True
        return False

    def _food_morsel(self, body_a, body_b):
        """Find food morsel using spatial hash."""
        food_a = self.body_to_food_morsel.get(body_a)
        if food_a:
            return food_a
        return self.body_to_food_morsel.get(body_b)

    def _organism(self, body_a, body_b, food_body):
        """Find organism using spatial hash."""
        other_body = body_b if food_body == body_a else body_a
        return self.body_to_organism.get(other_body)

    def get_contact_events(self):
        """Get and clear the list of contact events."""
        events = self.contact_events.copy()
        self.contact_events.clear()
        return events

    def _rebuild_spatial_hash(self):
        """Rebuild the spatial hash maps for fast body lookups."""
        self.body_to_organism.clear()
        self.body_to_food_morsel.clear()

        # Map organism bodies
        for organism in self.organisms:
            if hasattr(organism, 'body') and organism.body:
                self.body_to_organism[organism.body] = organism

        # Map food morsel bodies
        for food_morsel in self.food_morsels:
            if hasattr(food_morsel, 'body') and food_morsel.body:
                self.body_to_food_morsel[food_morsel.body] = food_morsel

    def add_organism(self, organism):
        """Add organism to spatial hash when new organisms are created."""
        if hasattr(organism, 'body') and organism.body:
            self.body_to_organism[organism.body] = organism

    def remove_organism(self, organism):
        """Remove organism from spatial hash when organisms are destroyed."""
        if hasattr(organism, 'body') and organism.body:
            self.body_to_organism.pop(organism.body, None)

    def add_food_morsel(self, food_morsel):
        """Add food morsel to spatial hash when new food is created."""
        if hasattr(food_morsel, 'body') and food_morsel.body:
            self.body_to_food_morsel[food_morsel.body] = food_morsel

    def remove_food_morsel(self, food_morsel):
        """Remove food morsel from spatial hash when food is eaten."""
        if hasattr(food_morsel, 'body') and food_morsel.body:
            self.body_to_food_morsel.pop(food_morsel.body, None)
