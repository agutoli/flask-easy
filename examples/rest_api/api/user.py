from flask.ext.easy import Response as res

def create():
    return 'create_user'

@res.type('application/json')
def show():
    return '{}'

def show_by_id(user_id):
    return 'show_user_by_id: %s' % user_id

def update(user_id):
    return 'update_user %s' % user_id

def delete(user_id):
    return 'delete_user %s' % user_id


