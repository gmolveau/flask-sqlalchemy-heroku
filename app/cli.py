import time

import click
from .database import db

@click.command("create_db")
def create_db():
    db.create_all()


@click.command("drop_db")
def drop_db():
    db.drop_all()


@click.command("reset_db")
def reset_db():
    db.drop_all()
    db.create_all()


@click.command("make_admin")
@click.argument("user_id")
def make_admin(user_id):
    time_start = time.time()
    from app.models.user import User
    user = User.query.get(user_id)
    user.isAdmin = True
    db.session.add(user)
    db.session.commit()
    time_end = time.time()
    print("user :", user.username, "is now admin. \n")
    print("temps nécessaire =", str(time_end - time_start), "seconds. \n")


@click.command("schedule_task")
def schedule_task():
    t = "i am a scheduled action, yeah"
    print(t)
    click.echo(t)


def cli_init_app(app):
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(make_admin)
    app.cli.add_command(schedule_task)
