from api.models import Location


def run():
    # Update existing Locations
    bethune = Location.objects.get(location_number="101")
    bethune.visions_dac_id = 2
    bethune.visions_dac_name = "Bethune Elementary"
    bethune.save()

    capitol = Location.objects.get(location_number="102")
    capitol.visions_dac_id = 3
    capitol.visions_dac_name = "Capitol Elementary"
    capitol.save()

    dunbar = Location.objects.get(location_number="104")
    dunbar.visions_dac_id = 4
    dunbar.visions_dac_name = "Dunbar Elementary"
    dunbar.save()

    edison = Location.objects.get(location_number="105")
    edison.visions_dac_id = 5
    edison.visions_dac_name = "Edison Elementary"
    edison.save()

    emerson = Location.objects.get(location_number="106")
    emerson.visions_dac_id = 6
    emerson.visions_dac_name = "Emerson Elementary"
    emerson.save()

    garfield = Location.objects.get(location_number="108")
    garfield.visions_dac_id = 7
    garfield.visions_dac_name = "Garfield Elementary"
    garfield.save()

    magnet = Location.objects.get(location_number="109")
    magnet.visions_dac_id = 8
    magnet.visions_dac_name = "Magnet Elementary"
    magnet.save()

    heard = Location.objects.get(location_number="112")
    heard.visions_dac_id = 10
    heard.visions_dac_name = "Heard Elementary"
    heard.save()

    herrera = Location.objects.get(location_number="113")
    herrera.visions_dac_id = 11
    herrera.visions_dac_name = "Herrera Elementary"
    herrera.save()

    kenilworth = Location.objects.get(location_number="115")
    kenilworth.visions_dac_id = 12
    kenilworth.visions_dac_name = "Kenilworth Elementary"
    kenilworth.save()

    lowell = Location.objects.get(location_number="118")
    lowell.visions_dac_id = 13
    lowell.visions_dac_name = "Lowell Elementary"
    lowell.save()

    shaw = Location.objects.get(location_number="123")
    shaw.visions_dac_id = 17
    shaw.visions_dac_name = "Shaw Montessori"
    shaw.save()

    faith = Location.objects.get(location_number="130")
    faith.visions_dac_id = 51
    faith.visions_dac_name = "Faith North Early Childhood Learning Center"
    faith.save()

    ps = Location.objects.get(location_number="128")
    ps.visions_dac_id = 22
    ps.visions_dac_name = "Plant Services"
    ps.save()

    # Create new Locations
    Location.objects.create(
        name="Management Information Systems",
        short_name="MIS",
        location_number="542",
        visions_dac_id=25,
        visions_dac_name="Mgmt Information Services"
    )

    Location.objects.create(
        name="Superintendent",
        short_name="Superintendent",
        location_number="539",
        visions_dac_id=48,
        visions_dac_name="Superintendent"
    )

    Location.objects.create(
        name="Business Services",
        short_name="Business Services",
        location_number="533",
        visions_dac_id=46,
        visions_dac_name="Business Services"
    )

    Location.objects.create(
        name="Student Services",
        short_name="Student Services",
        location_number="545",
        visions_dac_id=28,
        visions_dac_name="Student Services"
    )

    Location.objects.create(
        name="Substitute",
        short_name="Substitute",
        location_number="599",
        visions_dac_id=50,
        visions_dac_name="Substitute"
    )

    Location.objects.create(
        name="Human Resources",
        short_name="Human Resources",
        location_number="535",
        visions_dac_id=47,
        visions_dac_name="Human Resources"
    )

    Location.objects.create(
        name="Curriculum & Instruction",
        short_name="Curriculum",
        location_number="565",
        visions_dac_id=34,
        visions_dac_name="Curriculum & Instruction"
    )

    Location.objects.create(
        name="PEER",
        short_name="PEER",
        location_number="561",
        visions_dac_id=49,
        visions_dac_name="PEER"
    )

    Location.objects.create(
        name="Child Nutrition",
        short_name="Child Nutrition",
        location_number="536",
        visions_dac_id=23,
        visions_dac_name="Child Nutrition"
    )

    Location.objects.create(
        name="Whittier",
        short_name="Whittier",
        location_number="125",
        visions_dac_id=16,
        visions_dac_name="Whittier Elementary"
    )
