from api import visions
from api.models import Employee, Location, Position
from django.core.exceptions import ObjectDoesNotExist


class Epar:
    id = None
    name = None
    position_title = None

    def __init__(self, id, name, position_title):
        self.id = id
        self.name = name
        self.position_title = position_title


class VisionsEmployee:
    id = None
    name = None

    def __init__(self, id, name):
        self.id = id
        self.name = name


class VisionsImportEmployee:
    id = None
    first_name = None
    last_name = None
    ssn = None

    def __init__(self, id, first_name, last_name, ssn):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn


class VisionsPosition:
    id = None
    description = None
    dac = None
    position_ranking = None

    def __init__(self, id, description, dac, position_ranking):
        self.id = id
        self.description = description
        self.dac = dac
        self.position_ranking = position_ranking


class VisionsHelper:
    def verify_epar(epar_id):
        vsquery = visions.Select("ID", "viwHPEmpPARs", ID=epar_id)
        vsresult = vsquery.fetch_value()
        if(vsresult):
            return True

    def verify_employee(visions_id):
        if not visions.Viwpremployees().ID(visions_id):
            return False
        return True

    def get_visions_positions_from_dict(db_result_dict):
        positions = []
        for row in db_result_dict:
            position = VisionsPosition(row["ID"], row["Description"], row["tblAPReqLocationsID"], row["PositionRankingType"])
            positions.append(position)
        return positions

    def get_epar(epar_id):
        vsquery = visions.Select("ID, Name, PositionDescription", "viwHPEmpPARs", ID=epar_id)
        vsresult = vsquery.fetch_all_dict()
        if vsresult:
            row = vsresult[0]
            return Epar(row["ID"], row["Name"], row["PositionDescription"])
        return None

    def get_epar_positions(epar_id):
        db_positions = visions.Select("pos.ID, pos.Description, pos.tblAPReqLocationsID, pos.PositionRankingType", "tblHPEmpPARPositions pp INNER JOIN viwPRPositions pos ON pp.tblPRPositionsID = pos.ID", tblHPEmpParID=epar_id)
        return VisionsHelper.get_visions_positions_from_dict(db_positions.fetch_all_dict())

    def get_all_epars():
        vsquery = visions.Select("ID, Name, PositionDescription", "viwHPEmpPARs", Type="New Hire Assignment")
        vsresult = vsquery.fetch_all_dict()
        epars = []
        for row in vsresult:
            epar = Epar(row["ID"], row["Name"], row["PositionDescription"])
            epars.append(epar)
        return epars

    def get_employee(id):
        return VisionsEmployee(id, visions.Viwpremployees().Name(id))

    def get_all_employees():
        db_employees = visions.Viwpremployees("ID, Name", status="Active").fetch_all_dict()
        employees = []
        for row in db_employees:
            employee = VisionsEmployee(row["ID"], row["Name"])
            employees.append(employee)
        return employees

    def get_employees_for_import():
        db_employees = visions.Viwpremployees("ID, FirstName, LastName, EmployeeSSN", status="Active").fetch_all_dict()
        employees = []
        for row in db_employees:
            employee = VisionsImportEmployee(row["ID"], row["FirstName"], row["LastName"], row["EmployeeSSN"])
            if Employee.should_import_employee(employee):
                employees.append(employee)
        return employees

    def get_position_location(visions_dac_id):
        try:
            return Location.objects.get(visions_dac_id=visions_dac_id)
        except ObjectDoesNotExist:
            return False

    def get_positions_for_employee(visions_id):
        db_positions = visions.Viwprpositions(
            "ID, Description, tblAPReqLocationsID, PositionRankingType",
            "tblPREmployeesID={} AND RecordType='Position' AND PositionType='Open'".format(visions_id)
        )
        return VisionsHelper.get_visions_positions_from_dict(db_positions.fetch_all_dict())

    def get_tcp_id_for_employee(visions_id):
        db_result = visions.Viwprpositions(
            "TCIJob",
            "tblPREmployeesID={}".format(visions_id)
        )
        for row in db_result.fetch_all_dict():
            if row["TCIJob"] and row["TCIJob"] > 0:
                return row["TCIJob"]
        return False

    def get_all_visions_positions():
        db_result = visions.Viwprpositions(
            "DISTINCT PosType, Description",
            "PositionID <> '' AND PositionID IS NOT NULL ORDER BY PosType, Description"
        )
        return db_result.fetch_all_dict()
