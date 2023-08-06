from flask import jsonify, request, current_app
from datetime import date
from polzybackend.authenticate import bp
from polzybackend.models import User
from polzybackend import auth
from polzybackend.utils.import_utils import get_permissions


@bp.route('/login', methods=['POST'])
def login():
    # get request data
    data = request.get_json()
    
    # check for required fields in data
    required_fields = [
        'email',
        'stage',
        'language',
    ]
    for field in required_fields:
        value = data.get(field)  
        if value is None:
            return {'error': f'User data does not contain {field}'}, 400

    # get user from db
    email = data['email']
    user = User.query.filter_by(email=email).first()
    # check if user found
    if user is None:
        return {'error': f'User {email} does not exist'}, 404

    # update current stage and language
    user.set_stage(data['stage'])
    user.set_language(data['language'])

    # update company if user has only one
    #if len(user.companies) == 1:
    #    user.set_company(company=user.companies[0].company)

    return jsonify(user.to_json()), 200


@bp.route('/permissions', methods=['POST'])
@auth.login_required
def get_user_permissions():
    # get request data
    data = request.get_json()

    # get company id
    company_id = data.get('id')
    if company_id is None:
        return {'error': 'Company data does not contain company id'}, 400

    # update company
    user = auth.current_user()
    try:
        company_details = user.set_company(company_id=company_id)
    except Exception as e:
        return {'error': f'Set company failed: {e}'}, 400

    #return {'success': 'Success'}, 200
    return jsonify({
        'permissions': get_permissions(user),
        'company': company_details,
    }), 200
