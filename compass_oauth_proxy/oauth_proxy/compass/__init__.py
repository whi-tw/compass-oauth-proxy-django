from datetime import datetime
from ntpath import join
import requests

from bs4 import BeautifulSoup

from .exceptions import CompassAuthException


class CompassProfileData:
    member_number: int
    forename: str
    surname: str
    known_as: str
    email: str
    join_date: datetime


class CompassSession:
    baseurl: str = "https://compass.scouts.org.uk"
    # baseurl = "https://acdcb1e5aa8ee40de7065ecae80715ce.m.pipedream.net"
    profile_data: CompassProfileData

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
            self.fill_profile_data()
        else:
            raise CompassAuthException

    def _request(self, method: str, path: str, *args, **kwargs):
        return self.session.request(method, f"{self.baseurl}{path}", *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request("POST", *args, **kwargs)

    def _get(self, *args, **kwargs):
        return self._request("GET", *args, **kwargs)

    def fill_profile_data(self):
        self.profile_data = CompassProfileData()

        pp_profile = self._get("/MemberProfile.aspx")
        profile_s = BeautifulSoup(pp_profile.text, "html.parser")
        self.profile_data.member_number = int(profile_s.find(id="myCN").get("value"))
        join_date = profile_s.find("td", text="Date of Joining:").next_sibling.text
        self.profile_data.join_date = datetime.strptime(join_date, "%d %B %Y")

        pp_profile = self._get(
            "/Popups/Profile/EditProfile.aspx",
            params={"StartPage": 1, "UseCN": self.profile_data.member_number},
        )
        profile_s = BeautifulSoup(pp_profile.text, "html.parser")
        self.profile_data.forename = profile_s.find(
            id="ctl00_workarea_txt_p1_forenames"
        ).get("data-db")
        self.profile_data.surname = profile_s.find(
            id="ctl00_workarea_txt_p1_surname"
        ).get("data-db")
        self.profile_data.known_as = profile_s.find(
            id="ctl00_workarea_txt_p1_known_as"
        ).get("data-db")
        primary_email_no = profile_s.find(id="ctl00_workarea_h_txt_p2_emailp2main").get(
            "value"
        )
        self.profile_data.email = profile_s.find(
            id=f"ctl00_workarea_txt_p2_email{primary_email_no}"
        ).get("value")
