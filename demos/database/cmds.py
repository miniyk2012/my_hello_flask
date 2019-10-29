import click


def register(app):
    from demos.database.app import db

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.echo('wawa first drop all database.')
            db.drop_all()
        db.create_all()
        click.echo('wawa Initialized database.')
