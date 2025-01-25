from api import AppControler, LoginApi, LogoutApi, ChangePasswordApi, AdminApi, GroupApi, AccountInfoApi
from api2 import UserApi
from test import StudentApi

app_controller = AppControler()

app_controller.add_module(LoginApi())
app_controller.add_module(LogoutApi())
app_controller.add_module(ChangePasswordApi())
app_controller.add_module(AdminApi())
app_controller.add_module(UserApi())
app_controller.add_module(GroupApi())
app_controller.add_module(StudentApi())
app_controller.add_module(AccountInfoApi())

app = app_controller.app

if __name__ == "__main__":
    app_controller.run(debug=False, port=5000)