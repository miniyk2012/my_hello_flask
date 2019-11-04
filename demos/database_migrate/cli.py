import click

from demos.database_migrate import app, db
from demos.database_migrate.models import User

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.echo('wawa first drop all database.')
        db.drop_all()
    db.create_all()
    click.echo('wawa Initialized database.')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
