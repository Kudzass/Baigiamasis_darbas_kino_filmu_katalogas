import json
from app import app, db
from models import Filmas, Zanras
from datetime import datetime

with open('imdb_top_25.json', 'r', encoding='utf-8') as f:
    duomenys = json.load(f)

with app.app_context():
    db.create_all()
    for item in duomenys:
        zanras = Zanras.query.filter_by(pavadinimas=item['zanras']).first()
        if not zanras:
            print(f"Žanras nerastas: {item['zanras']}, praleidžiam filmą: {item['pavadinimas']}")
            continue

        metai_raw = item.get('isleidimo_data') or item.get('metai')
        if not metai_raw:
            print(f"❌ Trūksta metų: {item['pavadinimas']}")
            continue

        try:
            isleidimo_data = datetime.strptime(str(metai_raw), '%Y')
        except ValueError:
            print(f"❌ Klaidinga data: {metai_raw} filme {item['pavadinimas']}")
            continue

        try:
            imdb = float(item['imdb'])
        except (ValueError, TypeError):
            imdb = 0.0

        filmas = Filmas(
                pavadinimas=item['pavadinimas'],
                rezisierius=item['rezisierius'],
                isleidimo_data=isleidimo_data,
                imdb=float(item['imdb']),
                zanras_id=zanras.id
        )

        db.session.add(filmas)

    db.session.commit()
    print("✅ Visi filmai sėkmingai importuoti.")