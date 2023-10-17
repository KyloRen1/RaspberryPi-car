from client.ui.view import ControllerView


def main():
    app = ControllerView("Controller", "org.beeware.widgets.buttons")
    return app

if __name__ == "__main__":
    app = main()
    app.main_loop()