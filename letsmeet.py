from app import create_app, db

from flask.ext.script import Manager, Shell

if __name__ == '__main__':

    app = create_app('default')
    manager = Manager(app)

    def make_shell_context():
        return dict(app=app,db=db)
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.run()
