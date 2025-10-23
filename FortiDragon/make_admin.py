from FortiDragon.db import get_db
from FortiDragon import create_app

app = create_app()
with app.app_context():
    db = get_db()
    db.execute("UPDATE user SET role='admin' WHERE username=?", ("jamie",))
    db.commit()
    print("User role updated to admin.")