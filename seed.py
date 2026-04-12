from app import app, db
from models import User, JournalEntry
from faker import Faker
from random import choice

fake = Faker()

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        users = []
        for _ in range(3):
            user = User(username = fake.user_name())
            user.password_hash = "password123"
            db.session.add(user)
            users.append(user)
            
        db.session.commit()
        
        moods = ["happy", "reflective", "productive", "tired", "excited", "calm"]
        for user in users:
            for _ in range(8):
                entry = JournalEntry(
                    title=fake.sentence(nb_words=6),
                    content=fake.paragraph(nb_sentences=5),
                    mood=choice(moods),
                    user_id=user.id
                )
                db.session.add(entry)
        
        db.session.commit()
        print("Database seeded!")
        
if __name__=='__main__':
    seed()