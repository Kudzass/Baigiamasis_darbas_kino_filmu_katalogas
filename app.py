from flask import Flask, render_template, request, redirect, url_for
from models import db, Filmas, Zanras
from datetime import datetime

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

@app.route('/prideti', methods=['GET', 'POST'])
def prideti_filma():
    if request.method == 'POST':
        pavadinimas = request.form['pavadinimas']
        zanras_id = request.form['zanras_id']
        rezisierius = request.form['rezisierius']
        isleidimo_data = request.form['isleidimo_data']
        imdb = request.form['imdb']

        try:
            isleidimo_data = datetime.strptime(isleidimo_data, '%Y')
        except ValueError:
            isleidimo_data = None

        try:
            imdb = float(imdb)
        except ValueError:
            imdb = 0.0

        naujas_filmas = Filmas(
            pavadinimas=pavadinimas,
            zanras_id=zanras_id,
            rezisierius=rezisierius,
            isleidimo_data=isleidimo_data,
            imdb=imdb
        )
        db.session.add(naujas_filmas)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
