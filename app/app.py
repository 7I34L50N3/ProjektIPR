from api2 import AppControler, LoginApi, LogoutApi, ChangePasswordApi, AdminApi, UserApi
from test import GroupApi

app_controller = AppControler()

app_controller.add_module(LoginApi())
app_controller.add_module(LogoutApi())
app_controller.add_module(ChangePasswordApi())
app_controller.add_module(AdminApi())
app_controller.add_module(UserApi())
app_controller.add_module(GroupApi())

app = app_controller.app

if __name__ == "__main__":
    app_controller.run(debug=False, port=5000)