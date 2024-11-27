from flask import request, jsonify
from models import db, TUsers, TAppartamenti, TPrenotazioni
from datetime import datetime

# Funzione per calcolare il totale
def calcola_totale(prezzo_per_notte, data_checkin, data_checkout):
    giorni = (data_checkout - data_checkin).days
    return prezzo_per_notte * giorni

# Gestione degli utenti
def manage_users(app):
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.json
        user = TUsers(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201

    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = TUsers.query.all()
        return jsonify([user.as_dict() for user in users])

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = TUsers.query.get_or_404(user_id)
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": "User updated"}), 200

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = TUsers.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

# Gestione degli appartamenti
def manage_apartments(app):
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

# Gestione delle prenotazioni
def manage_bookings(app):
    @app.route('/bookings', methods=['POST'])
    def create_booking():
        data = request.json
        user_id = data['UserID']
        apartment_id = data['AppartamentoID']
        data_checkin = datetime.strptime(data['DataCheckin'], '%Y-%m-%d')
        data_checkout = datetime.strptime(data['DataCheckOut'], '%Y-%m-%d')

        overlapping = TPrenotazioni.query.filter(
            TPrenotazioni.AppartamentoID == apartment_id,
            TPrenotazioni.DataCheckin < data_checkout,
            TPrenotazioni.DataCheckOut > data_checkin
        ).first()

        if overlapping:
            return jsonify({"error": "Apartment is already booked"}), 400

        apartment = TAppartamenti.query.get(apartment_id)
        totale = calcola_totale(apartment.PrezzoPerNotte, data_checkin, data_checkout)

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
        booking = TPrenotazioni.query.get_or_404(booking_id)
        data = request.json
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return jsonify({"message": "Booking updated"}), 200

    @app.route('/bookings/<int:booking_id>', methods=['DELETE'])
    def delete_booking(booking_id):
        booking = TPrenotazioni.query.get_or_404(booking_id)
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking deleted"}), 200
