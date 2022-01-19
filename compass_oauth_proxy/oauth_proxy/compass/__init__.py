import requests

from .profile import CompassProfile
from .exceptions import CompassAuthException


class CompassSession:
    baseurl: str = "https://compass.scouts.org.uk"
    # baseurl = "https://acdcb1e5aa8ee40de7065ecae80715ce.m.pipedream.net"

    profile: CompassProfile

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    def __init__(self, username: str, password: str):
        self._get("/login/User/Login")
        auth = self._post(
            "/Login.ashx",
            data={"EM": username, "PW": password, "ON": 10000001},
            allow_redirects=False,
            headers={"Referer": f"{self.baseurl}/login/User/Login"},
        )
        if auth.status_code == 200 and not "<title>Compass - Failed Login" in auth.text:
            self._get("/ScoutsPortal.aspx")
            self._populate_member_data()
        else:
            raise CompassAuthException

    def _request(self, method: str, path: str, *args, **kwargs):
        return self.session.request(method, f"{self.baseurl}{path}", *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request("POST", *args, **kwargs)

    def _get(self, *args, **kwargs):
        return self._request("GET", *args, **kwargs)

    def _populate_member_data(self):
        pp_profile = self._get("/MemberProfile.aspx")
        member_no = CompassProfile.get_member_number_from_profile(pp_profile.text)
        pp_profile_edit = self._get(
            "/Popups/Profile/EditProfile.aspx",
            params={"StartPage": 1, "UseCN": member_no},
        )
        self.profile = CompassProfile(member_no)
        self.profile.populate_profile_data(pp_profile_edit.text)
