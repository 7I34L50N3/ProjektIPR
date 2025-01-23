from api import AppControler, LoginApi

if __name__ == "__main__":
    app = AppControler()
    app.add_module(LoginApi())
    app.run(debug=False, port=5000)