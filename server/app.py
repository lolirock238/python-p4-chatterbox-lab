from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Get all messages ordered by created_at ascending
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return make_response(jsonify([msg.to_dict() for msg in messages]), 200)
    
    elif request.method == 'POST':
        # Get JSON data from request
        data = request.get_json()
        
        # Create new message
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'PATCH':
        # Get JSON data
        data = request.get_json()
        
        # Update the message body
        message.body = data['body']
        
        db.session.commit()
        
        return make_response(jsonify(message.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        return make_response(jsonify({}), 200)

if __name__ == '__main__':
    app.run(port=5555)