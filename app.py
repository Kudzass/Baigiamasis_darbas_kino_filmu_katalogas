from flask import Flask, render_template
from models import db, Filmas, Zanras
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    search = request.args.get('search')

    if search:
        filmai = Filmas.query.filter(
            Filmas.pavadinimas.ilike(f'%{search}%') |
            Filmas.rezisierius.ilike(f'%{search}%')
        ).all()
    else:
        filmai = Filmas.query.all()

    return render_template('index.html', filmai=filmai)

if __name__ == '__main__':
    app.run(debug=True)