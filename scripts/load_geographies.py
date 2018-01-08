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
        # exception handler for DC (since it doesn't have a capital)
        if new_state.abbrev == "DC":
            new_state.capital = "Self"
        new_state.fips_code = state.fips
        new_state.save()


def load_cities():
    City.objects.all().delete()

    # make sure that state objects exist
    if State.objects.exists() is False:
        load_states()

    with open("./data/top100_cities.csv") as top_cities:
        for line in top_cities.readlines()[1:]:
            new_city = City()
            _, new_city.city_name, state, _, _ = line.split(",")
            new_city.state = State.objects.get(name=state)
            new_city.save()


def run():
    # clear all the old objects
    load_states()
    load_cities()


if __name__ == "__main__":
    run()
