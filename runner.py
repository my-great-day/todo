from app import todo, db

if __name__ == '__main__':
    db.create_all()
    todo.run()
