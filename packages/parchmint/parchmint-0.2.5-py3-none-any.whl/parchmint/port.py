class Port:
    def __init__(self, json=None):
        self.x: int = -1
        self.y: int = -1
        self.label: str = ""
        self.layer: str = ""

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
        self.x = json["x"]
        self.y = json["y"]
        self.label = json["label"]
        self.layer = json["layer"]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        return {
            "x": self.x,
            "y": self.y,
            "label": self.label,
            "layer": self.layer,
        }
