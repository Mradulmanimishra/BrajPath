"""Check database contents."""
from app.db.session import SessionLocal
from app.db.models import Temple

db = SessionLocal()
temples = db.query(Temple).all()
print(f'✅ Database has {len(temples)} temples')
for t in temples:
    print(f'  - {t.name_en}')
db.close()
