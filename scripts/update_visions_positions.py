from bpm.visions_helper import VisionsHelper
from api.models import VisionsPositions


def run():
    VisionsPositions.objects.all().delete()

    positions = VisionsHelper.get_all_visions_positions()
    for position in positions:
        VisionsPositions.objects.create(description=position["Description"], type=position["PosType"])
