

# CRUD app  create 
# first name , latname , email

# from flask import request , jsonify
# from config import app, db
# from  models import Contact

# @app.route('/contacts' , methods=['GET']) 

# def get_contacts():
#     contacts = Contact.query.all()
#     json_contacts = map(lambda x:x.to_json() , contacts)
#     return jsonify({'contacts' :json_contacts})

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
   
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = [contact.to_json() for contact in contacts]
    return jsonify({'contacts': json_contacts})

@app.route('/create-contacts', methods=['POST'])
def create_contacts():
    first_name= request.json.get('firstName')
    last_name= request.json.get('lastName')
    email= request.json.get('email')

    if not first_name or not last_name or not email :
        return (
        jsonify({'message':'hey all field are required first and last name + email  ...' } ),
        400 ,
          )
    
    new_contact = Contact(first_name= first_name , last_name=last_name , email=email)
    try :
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': str(e)}) ,400
    
    return jsonify({'message' :'User Created Succesfuly !'}) ,200


@app.route('/update-contact/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'message': 'Contact not found.'}), 404

    data = request.json
    if 'firstName' in data:
        contact.first_name = data['firstName']
    if 'lastName' in data:
        contact.last_name = data['lastName']
    if 'email' in data:
        contact.email = data['email']

    try:
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
@app.route('/delete-contact/<int:contact_id>' , methods =['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)

    if not contact :
        return jsonify({'message' :'Contact not Found'}) , 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({'message': "Contact Deleted Succesfully "}) , 201


if __name__ == '__main__':
    app.run(debug=True)