import time

import click
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
app = create_app()

@app.cli.command("create_db")
def create_db():
    db.create_all()

@app.cli.command("drop_db")
def drop_db():
    db.drop_all()

@app.cli.command("reset_db")
def reset_db():
    db.drop_all()
    db.create_all()

@app.cli.command("make_admin")
@click.argument("user_id")
def make_admin(user_id):
    time_start = time.time()
    from app.models.user import User
    user = User.query.get(user_id)
    user.isAdmin = True
    db.session.add(user)
    db.session.commit()
    time_end = time.time()
    print("user :",user.username,"is now admin. \n")
    print("temps nécessaire =",str(time_end - time_start),"seconds. \n")

@app.cli.command("schedule_task")
def schedule_task():
    t = "i am a scheduled action, yeah"
    print(t)
    app.logger.debug(t)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
