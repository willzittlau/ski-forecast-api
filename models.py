from api import db

class Areas(db.Model):
    __tablename__ = 'Areas'
    name = db.Column(db.String(), primary_key=True)
    coordinates = db.Column(db.String())
    avalanche_forecast = db.Column(db.String())
    area_type = db.Column(db.String())
    model_elevation = db.Column(db.String())

    def __init__(self, name, coordinates, avalanche_forecast, area_type, model_elevation):
        self.name = name
        self.coordinates = coordinates
        self.avalanche_forecast = avalanche_forecast
        self.area_type = area_type
        self.model_elevation = model_elevation

    def __repr__(self):
        return '<name: {}>'.format(self.name)