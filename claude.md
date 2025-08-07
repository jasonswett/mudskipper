Base hexagon reckoning on https://www.redblobgames.com/grids/hexagons/
I use a flat-side-up orientation.

Don't ever call it a simulation. It's not a simulation. It's a virtual world with virtual life forms.

## Architecture

This project uses pyenv. Remember to do source venv/bin/activate.

## Workflow

Don't make commits before you check with me.
Push after every commit.

Don't comment out code. Just delete it.

In general, always do the simplest thing that could possibly work.

When you want to understand how existing code works, look first to the tests.

Exceptions are occasionally justified, but in general, always use TDD.
1. Decide on the specifications.
2. Encode the specifications in a test.
3. Run the test and observe the failure.
4. Write just enough code to make the failure go away (NOT enough code to necessarily make the test pass).
5. Repeat from step 3 until the test passes.

## Style

### Testing

Only use comments when absolutely necessary.

In this project, the tests are the backbone. The application code is subservient to the tests.
