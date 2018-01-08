import us
from emails.models import State, City

def load_states():
    State.objects.all().delete()
    # load the states
    for state in us.states.STATES:
        new_state = State()
        new_state.name = state.name
        new_state.abbrev = state.abbr
        new_state.capital = state.capital
        new_state.fips_code = state.fips
        new_state.save()

def load_cities():
    City.objects.all().delete()
    for

def run():
    # clear all the old objects
    load_states()


if __name__ == "__main__":
    run()
