from app import app, db
from models import Zanras

zanru_sarasas = [
    "Veiksmo", "Trileris", "Fantastika", "Dokumentika", "Animacija", "Romantinis",
    "Siaubo", "Nuotykių", "Kriminalinis", "Vesternas", "Biografinis", "Istorinis",
    "Muzikalas", "Sporto", "Mistinis", "Karinis", "Šeimai", "Fantastinis",
    "Tragi-komedija", "Mokslinė fantastika", "Drama",
]

with app.app_context():
    for pavadinimas in zanru_sarasas:
        if not Zanras.query.filter_by(pavadinimas=pavadinimas).first():
            db.session.add(Zanras(pavadinimas=pavadinimas))
    db.session.commit()
    print("✅ Žanrai sėkmingai pridėti.")
