from flask import Flask, render_template
from models import db, Filmas, Zanras

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    visi_filmai = Filmas.query.all()
    return render_template('index.html', filmai=visi_filmai)

if __name__ == '__main__':
    app.run(debug=True)
