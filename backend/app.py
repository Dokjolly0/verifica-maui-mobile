# Importazioni
from flask import Flask, request, jsonify
from config import create_app, db
from models import TUsers, TAppartamenti, TPrenotazioni
from datetime import datetime

# Creazione dell'applicazione
app = create_app()

# Funzioni di utilità

def calcola_totale(prezzo_per_notte, data_checkin, data_checkout):
    """
    Calcola il totale della prenotazione in base al prezzo per notte e al periodo
    tra la data di check-in e la data di check-out.
    """
    giorni = (data_checkout - data_checkin).days
    return prezzo_per_notte * giorni

# Endpoint Utenti

@app.route('/users', methods=['POST'])
def manage_users():
    """
    Gestisce la creazione di un nuovo utente o la visualizzazione di tutti gli utenti.
    """
    if request.method == 'POST':
        data = request.json
        print("Received Data:", data)  # Controlla i dati ricevuti
        user = TUsers(**data)
        db.session.add(user)
        db.session.commit()  # Verifica che questo venga chiamato
        return jsonify({"message": "User created"}), 201

    users = TUsers.query.all()
    return jsonify([user.as_dict() for user in users])

@app.route('/users/<stato>', methods=['GET'])
def get_users_by_state(stato):
    """
    Restituisce tutti gli utenti che hanno uno stato specifico.
    """
    users = TUsers.query.filter_by(Stato=stato).all()
    return jsonify([user.as_dict() for user in users])

@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Restituisce la lista di tutti gli utenti.
    """
    users = TUsers.query.all()
    return jsonify([user.as_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Aggiorna le informazioni di un utente specificato dall'ID.
    """
    user = TUsers.query.get_or_404(user_id)

    data = request.json
    if 'Email' in data:
        user.Email = data['Email']
    if 'Password' in data:
        user.Password = data['Password']
    if 'Cognome' in data:
        user.Cognome = data['Cognome']
    if 'Nome' in data:
        user.Nome = data['Nome']
    if 'Stato' in data:
        user.Stato = data['Stato']

    db.session.commit()
    return jsonify({"message": "User updated"}), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = TUsers.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# Endpoint Appartamenti

@app.route('/apartments', methods=['GET', 'POST'])
def manage_apartments():
    """
    Gestisce la creazione di un appartamento o la visualizzazione di tutti gli appartamenti.
    """
    if request.method == 'POST':
        data = request.json
        apartment = TAppartamenti(**data)
        db.session.add(apartment)
        db.session.commit()
        return jsonify({"message": "Apartment created"}), 201

    apartments = TAppartamenti.query.all()
    return jsonify([apartment.as_dict() for apartment in apartments])

@app.route('/apartments/search', methods=['GET'])
def search_apartments():
    """
    Ricerca appartamenti in base a diversi parametri: stato, CAP, e nome del luogo.
    """
    stato = request.args.get('stato')
    cap = request.args.get('cap')
    place_name = request.args.get('place_name')

    apartments = TAppartamenti.query
    if stato:
        apartments = apartments.filter_by(Stato=stato)
    if cap:
        apartments = apartments.filter_by(CAP=cap)
    if place_name:
        apartments = apartments.filter_by(PlaceName=place_name)

    return jsonify([apartment.as_dict() for apartment in apartments.all()])

@app.route('/apartments/<int:apartment_id>', methods=['PUT'])
def update_apartment(apartment_id):
    apartment = TAppartamenti.query.get_or_404(apartment_id)
    data = request.json
    for key, value in data.items():
        setattr(apartment, key, value)
    db.session.commit()
    return jsonify({"message": "Apartment updated"}), 200

@app.route('/apartments/<int:apartment_id>', methods=['DELETE'])
def delete_apartment(apartment_id):
    apartment = TAppartamenti.query.get_or_404(apartment_id)
    db.session.delete(apartment)
    db.session.commit()
    return jsonify({"message": "Apartment deleted"}), 200

# Endpoint Prenotazioni

@app.route('/bookings', methods=['POST'])
def create_booking():
    """
    Crea una nuova prenotazione per un utente e un appartamento, calcolando il totale
    e verificando la disponibilità.
    """
    data = request.json
    user_id = data['UserID']
    apartment_id = data['AppartamentoID']
    data_checkin = datetime.strptime(data['DataCheckin'], '%Y-%m-%d')
    data_checkout = datetime.strptime(data['DataCheckOut'], '%Y-%m-%d')

    # Verifica se l'appartamento è disponibile
    overlapping = TPrenotazioni.query.filter(
        TPrenotazioni.AppartamentoID == apartment_id,
        TPrenotazioni.DataCheckin < data_checkout,
        TPrenotazioni.DataCheckOut > data_checkin
    ).first()

    if overlapping:
        return jsonify({"error": "Apartment is already booked"}), 400

    # Calcola il totale
    apartment = TAppartamenti.query.get(apartment_id)
    totale = calcola_totale(apartment.PrezzoPerNotte, data_checkin, data_checkout)

    # Crea la prenotazione
    booking = TPrenotazioni(
        UserID=user_id,
        AppartamentoID=apartment_id,
        DataCheckin=data_checkin,
        DataCheckOut=data_checkout,
        TotaleDaPagare=totale
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking created", "TotaleDaPagare": totale}), 201


@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = TPrenotazioni.query.all()
    return jsonify([booking.as_dict() for booking in bookings])

@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    # Ottieni il booking da aggiornare
    booking = TPrenotazioni.query.get_or_404(booking_id)
    
    # Ottieni i dati dalla richiesta JSON
    data = request.json
    
    # Converti le date da stringhe a oggetti datetime.date
    if 'DataCheckin' in data:
        data['DataCheckin'] = datetime.strptime(data['DataCheckin'], '%Y-%m-%d').date()
    if 'DataCheckOut' in data:
        data['DataCheckOut'] = datetime.strptime(data['DataCheckOut'], '%Y-%m-%d').date()

    # Aggiorna i campi nel booking
    for key, value in data.items():
        setattr(booking, key, value)

    # Commit delle modifiche al database
    db.session.commit()

    return jsonify({"message": "Booking updated"}), 200

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = TPrenotazioni.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200

# Inizializzazione dell'applicazione

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea le tabelle definite nei modelli
    app.run(debug=True)
