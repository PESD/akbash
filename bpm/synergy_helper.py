from api import synergy


class SynergyHelper:
    def get_synergy_login(visions_id):
        if not visions_id:
            return False
        squery = synergy.Select(
            "u.LOGIN_NAME",
            "rev.REV_USER u INNER JOIN rev.EPC_STAFF s ON u.USER_GU = s.STAFF_GU",
            "s.BADGE_NUM=" + str(visions_id) + " AND u.DISABLED = 'N'"
        )
        sresult = squery.fetch_value()
        if sresult:
            return sresult
        return False

    def verify_synergy_username(synergy_username):
        if not synergy_username:
            return False
        squery = synergy.Select(
            "LOGIN_NAME",
            "rev.REV_USER",
            "LOGIN_NAME= '" + synergy_username + "' AND DISABLED = 'N'"
        )
        sresult = squery.fetch_value()
        if sresult:
            return sresult
        return False
