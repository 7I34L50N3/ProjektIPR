from api import AppControler, LoginApi, AdminApi

app_controller = AppControler()

app_controller.add_module(LoginApi())
app_controller.add_module(AdminApi())

app = app_controller.app

if __name__ == "__main__":
    app_controller.run(debug=False, port=5000)