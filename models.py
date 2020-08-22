from api import db

class Areas(db.Model):
    __tablename__ = 'Areas'
    name = db.Column(db.String(), primary_key=True)
    coordinates = db.Column(db.String())
    avalanche_forecast = db.Column(db.String())
    area_type = db.Column(db.String())
    tz_info = db.Column(db.String())
    NAM_elevation = db.Column(db.String())
    HRDPS_elevation = db.Column(db.String())

    def __init__(self, name, coordinates, avalanche_forecast, area_type, tz_info, NAM_elevation, HRDPS_elevation):
        self.name = name
        self.coordinates = coordinates
        self.avalanche_forecast = avalanche_forecast
        self.area_type = area_type
        self.tz_info = tz_info
        self.NAM_elevation = NAM_elevation
        self.HRDPS_elevation = HRDPS_elevation

    def __repr__(self):
        return '<name: {}>'.format(self.name)