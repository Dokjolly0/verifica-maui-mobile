-- Creazione delle tabelle
CREATE TABLE TUsers (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Cognome TEXT NOT NULL,
    Nome TEXT NOT NULL,
    Stato TEXT NOT NULL
);

CREATE TABLE TAppartamenti (
    AppartamentoID INTEGER PRIMARY KEY AUTOINCREMENT,
    Descrizione TEXT NOT NULL,
    Stato TEXT NOT NULL,
    CAP TEXT NOT NULL,
    PlaceName TEXT NOT NULL,
    PrezzoPerNotte REAL NOT NULL,
    NumeroOspitiMassimo INTEGER NOT NULL
);

CREATE TABLE TPrenotazioni (
    PrenotazioneID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    AppartamentoID INTEGER NOT NULL,
    DataCheckin DATE NOT NULL,
    DataCheckOut DATE NOT NULL,
    TotaleDaPagare REAL NOT NULL,
    FOREIGN KEY (UserID) REFERENCES TUsers(UserID),
    FOREIGN KEY (AppartamentoID) REFERENCES TAppartamenti(AppartamentoID)
);

-- Popolamento iniziale delle tabelle
INSERT INTO TUsers (Email, Password, Cognome, Nome, Stato) VALUES
('user1@example.com', 'password1', 'Rossi', 'Mario', 'de'),
('user2@example.com', 'password2', 'Dupont', 'Jean', 'fr'),
('user3@example.com', 'password3', 'García', 'Ana', 'es');

INSERT INTO TAppartamenti (Descrizione, Stato, CAP, PlaceName, PrezzoPerNotte, NumeroOspitiMassimo) VALUES
('Appartamento in centro a Roma', 'it', '00100', 'Roma', 100.0, 4),
('Monolocale accogliente a Roma', 'it', '00100', 'Roma', 80.0, 2),
('Attico moderno a Roma', 'it', '00100', 'Roma', 150.0, 6),
('Villa con piscina a Milano', 'it', '20100', 'Milano', 200.0, 8),
('Appartamento sul mare a Napoli', 'it', '80100', 'Napoli', 120.0, 5),
('Loft elegante a Berlino', 'de', '10115', 'Berlino', 110.0, 3),
('Chalet alpino a Zurigo', 'ch', '8001', 'Zurigo', 250.0, 7);
