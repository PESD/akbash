from api import synergy


class SynergyHelper:
    def get_synergy_login(visions_id):
        squery = synergy.Select(
            "u.LOGIN_NAME",
            "rev.REV_USER u INNER JOIN rev.EPC_STAFF s ON u.USER_GU = s.STAFF_GU",
            "s.BADGE_NUM=" + str(visions_id)
        )
        sresult = squery.fetch_value()
        if sresult:
            return sresult
        return False