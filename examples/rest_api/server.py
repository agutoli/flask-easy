from flask import Flask
from flask.ext.easy import Easy

app = Flask(__name__)

# rest api
rest = Easy(app)

urls = [ 
  ('/user', 'api.user.show', ['GET']),
  ('/user', 'api.user.create', ['POST', 'PUT']),
  ('/user/<int:user_id>', 'api.user.show_by_id', ['GET']),
  ('/user/<int:user_id>', 'api.user.update', ['POST', 'PUT']),
  ('/user/<int:user_id>', 'api.user.delete', ['DELETE']),
]

rest.add_url_rules(urls)

if __name__ == "__main__":
    app.run()

