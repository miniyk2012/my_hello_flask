import click


def register(app):
    from demos.database import db
    from demos.database.models import (Note, Author, Article, Writer, Book,
                                       Citizen, City, Country, Capital, Student, 
                                       Teacher, student_teacher_table, Post, Comment)
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.echo('wawa first drop all database.')
            db.drop_all()
        db.create_all()
        click.echo('wawa Initialized database.')

    @app.cli.command()
    def dropdb():
        """drop the database."""
        db.drop_all()
        click.echo('database is dropped.')

    @app.shell_context_processor
    def make_shell_context():
        """为flask-shell提供的可用变量"""
        return dict(db=db, Note=Note, Author=Author, Article=Article, Writer=Writer,
                    Book=Book, Citizen=Citizen, City=City, Country=Country, Capital=Capital,
                    Student=Student, Teacher=Teacher, student_teacher_table=student_teacher_table,
                    Post=Post, Comment=Comment)
