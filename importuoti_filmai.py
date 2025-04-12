import json
from app import app, db
from models import Filmas, Zanras
from datetime import datetime

with open('imdb_top_25.json', 'r', encoding='utf-8') as f:
    duomenys = json.load(f)

with app.app_context():
    for item in duomenys:
        zanras = Zanras.query.filter_by(pavadinimas=item['zanras']).first()
        if not zanras:
            print(f"Žanras nerastas: {item['zanras']}, praleidžiam filmą: {item['pavadinimas']}")
            continue

            filmas = Filmas(
                pavadinimas=item['pavadinimas'],
                rezisierius=item['rezisierius'],
                isleidimo_data=datetime.strptime(item['isleidimo_data'], '%Y'),
                imdb=float(item['imdb']),
                zanras_id=zanras.id
            )

            db.session.add(filmas)

        db.session.commit()
        print("✅ Visi filmai sėkmingai importuoti.")