from bs4 import BeautifulSoup


class CompassProfile:
    member_number: int
    forename: str
    surname: str
    nickname: str
    email: str

    def __init__(self, member_number: str) -> None:
        self.member_number = int(member_number)

    def __str__(self) -> str:
        return self.name()

    def get_first_name(self) -> str:
        if self.nickname != "":
            return f"{self.nickname}"
        return self.forename.split(" ")[0]

    def name(self) -> str:
        return f"{self.get_first_name()} {self.surname}"

    def populate_profile_data(self, profile_page_content: str) -> None:
        profile_s = BeautifulSoup(profile_page_content, "html.parser")

        self.forename = profile_s.find(id="ctl00_workarea_txt_p1_forenames").get(
            "data-db"
        )
        self.surname = profile_s.find(id="ctl00_workarea_txt_p1_surname").get("data-db")
        self.nickname = profile_s.find(id="ctl00_workarea_txt_p1_known_as").get(
            "data-db"
        )
        primary_email_no = profile_s.find(id="ctl00_workarea_h_txt_p2_emailp2main").get(
            "value"
        )
        self.email = profile_s.find(
            id=f"ctl00_workarea_txt_p2_email{primary_email_no}"
        ).get("value")

    @staticmethod
    def get_member_number_from_profile(profile_page_content: str) -> int:
        profile_s = BeautifulSoup(profile_page_content, "html.parser")
        return profile_s.find(id="myCN").get("value")
