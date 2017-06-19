from api import visions


class Epar:
    id = None
    first_name = None
    last_name = None
    full_name = None
    position_title = None


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
