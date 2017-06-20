from api import visions


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

    def get_epar(epar_id):
        vsquery = visions.Select("ID, Name, PositionDescription", "viwHPEmpPARs", ID=epar_id)
        vsresult = vsquery.fetch_all_dict()
        if vsresult:
            row = vsresult[0]
            return Epar(row["ID"], row["Name"], row["PositionDescription"])
        return None

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