from flask import Flask, request, jsonify
from config import create_app, db
from models import TUsers, TAppartamenti, TPrenotazioni
from datetime import datetime

app = create_app()

# Funzione per calcolare il totale
def calcola_totale(prezzo_per_notte, data_checkin, data_checkout):
    giorni = (data_checkout - data_checkin).days
    return prezzo_per_notte * giorni

# Endpoint Utenti
@app.route('/users', methods=['POST'])
def manage_users():
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
    users = TUsers.query.filter_by(Stato=stato).all()
    return jsonify([user.as_dict() for user in users])

# Nuovo endpoint per ottenere tutti gli utenti
@app.route('/users', methods=['GET'])
def get_all_users():
    users = TUsers.query.all()
    return jsonify([user.as_dict() for user in users])

# Nuovo endpoint per aggiornare un utente tramite ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Trova l'utente nel database
    user = TUsers.query.get_or_404(user_id)

    # Ottieni i dati dal corpo della richiesta
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

    # Salva le modifiche nel database
    db.session.commit()
    return jsonify({"message": "User updated"}), 200

# Endpoint Appartamenti
@app.route('/apartments', methods=['GET', 'POST'])
def manage_apartments():
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

# Endpoint Prenotazioni
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    user_id = data['UserID']
    apartment_id = data['AppartamentoID']
    data_checkin = datetime.strptime(data['DataCheckin'], '%Y-%m-%d')
    data_checkout = datetime.strptime(data['DataCheckOut'], '%Y-%m-%d')

    # Controlla se l'appartamento è disponibile
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Questo crea tutte le tabelle definite nei modelli
    app.run(debug=True)
