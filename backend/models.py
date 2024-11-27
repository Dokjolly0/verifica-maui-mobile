from config import db

class TUsers(db.Model):
    __tablename__ = 'TUsers'
    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Cognome = db.Column(db.String(100), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Stato = db.Column(db.String(10), nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class TAppartamenti(db.Model):
    __tablename__ = 'TAppartamenti'
    AppartamentoID = db.Column(db.Integer, primary_key=True)
    Descrizione = db.Column(db.String(255), nullable=False)
    Stato = db.Column(db.String(10), nullable=False)
    CAP = db.Column(db.String(10), nullable=False)
    PlaceName = db.Column(db.String(100), nullable=False)
    PrezzoPerNotte = db.Column(db.Float, nullable=False)
    NumeroOspitiMassimo = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class TPrenotazioni(db.Model):
    __tablename__ = 'TPrenotazioni'
    PrenotazioneID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('TUsers.UserID'), nullable=False)
    AppartamentoID = db.Column(db.Integer, db.ForeignKey('TAppartamenti.AppartamentoID'), nullable=False)
    DataCheckin = db.Column(db.Date, nullable=False)
    DataCheckOut = db.Column(db.Date, nullable=False)
    TotaleDaPagare = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
