from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from models import db, Filmas, Zanras

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    search = request.args.get('search')
    zanras_id = request.args.get('zanras_id')

    filmai_query = Filmas.query

    if search:
        filmai_query = filmai_query.filter(
            Filmas.pavadinimas.ilike(f'%{search}%') |
            Filmas.rezisierius.ilike(f'%{search}%')
        )

    if zanras_id and zanras_id.isdigit():
            filmai_query = filmai_query.filter(Filmas.zanras_id == int(zanras_id))

    filmai = filmai_query.all()
    zanrai = Zanras.query.all()
    return render_template('index.html', filmai=filmai, zanrai=zanrai)



@app.route('/prideti', methods=['GET', 'POST'])
def prideti_filma():
    klaida = None

    if request.method == 'POST':
        pavadinimas = request.form['pavadinimas']
        zanras_id = request.form['zanras_id']
        rezisierius = request.form['rezisierius']
        isleidimo_data = request.form['isleidimo_data']
        imdb = request.form['imdb']

        if not pavadinimas or not zanras_id or not rezisierius or not isleidimo_data or not imdb:
            klaida = "Užpildykite visus laukus."
        else:
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

    zanrai = Zanras.query.all()
    return render_template('add.html', zanrai=zanrai, klaida=klaida)


@app.route('/redaguoti/<int:id>', methods=['GET', 'POST'])
def redaguoti_filma(id):
    filmas = Filmas.query.get_or_404(id)

    if request.method == 'POST':
        filmas.pavadinimas = request.form['pavadinimas']
        filmas.zanras_id = request.form['zanras_id']
        filmas.rezisierius = request.form['rezisierius']

        try:
            filmas.imdb = float(request.form['imdb'])
        except ValueError:
            filmas.imdb = 0.0

        try:
            isleidimo_data_str = request.form['isleidimo_data']
            filmas.isleidimo_data = datetime.strptime(isleidimo_data_str, '%Y')
        except (ValueError, TypeError):
            filmas.isleidimo_data = filmas.isleidimo_data

        db.session.commit()
        return redirect(url_for('index'))

    zanrai = Zanras.query.all()
    return render_template('edit.html', filmas=filmas, zanrai=zanrai)

@app.route('/istrinti/<int:id>', methods=['POST'])
def istrinti_filma(id):
    filmas = Filmas.query.get_or_404(id)
    db.session.delete(filmas)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
