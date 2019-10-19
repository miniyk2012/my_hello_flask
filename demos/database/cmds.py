import click

from demos.database.app import db


def register(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.echo('first drop all database.')
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')
