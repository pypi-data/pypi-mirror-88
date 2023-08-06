# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 14:38:22
@LastEditTime: 2020-12-10 15:03:24
@LastEditors: ChenXiaolei
@Description: 
"""

# 框架引用
from seven_framework.web_tornado.base_tornado import *
from .handlers.system import *

class Application(tornado.web.Application):
    def __init__(self):
        application_settings = dict(
            # 如需使用cookie 请解除注释此句,并在handler中继承含有cookie的 base_handler
            cookie_secret=config.get_value("cookie_secret"),
            pycket=config.get_value("pycket"),
            # 键为template_path固定的，值为要存放HTML的文件夹名称
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            autoescape=None,
            xsrf_cookies=True)

        handlers = []

        # 模块的路由可以独立开
        handlers.extend(self.seven_studio_route())

        super().__init__(handlers, **application_settings)

    def seven_studio_route(self):
        return [
            # 登陆、注销
            (r"/Core/GetGeetestCode", core.GeetestCodeHandler),
            (r"/power/loginPlatform", core.LoginPlatformHandler),
            (r"/power/logout", core.LogoutHandler),
            (r"/core/uploadfiles", core.UploadFilesHandler),
            # 用户、角色
            (r"/power/GetUserInfo", power.GetUserInfoHandler),
            (r"/power/FocusPassword", power.FocusPasswordHandler),
            (r"/power/FocusChangeUserPw", power.FocusChangeUserPwHandler),
            (r"/power/ChangeCurrUserPw", power.ChangeCurrUserPwHandler),
            (r"/Power/SaveUser", power.SaveUserHandler),
            (r"/Power/SaveCurrUser", power.SaveCurrUserHandler),
            (r"/Power/GetUserList", power.GetUserListHandler),
            (r"/Power/GetUserProductList", power.GetUserProductListHandler),
            (r"/Power/GetRoleList", power.GetRoleListHandler),
            (r"/Power/GetUserRoleList", power.GetUserRoleListHandler),
            (r"/Power/GetRoleUserList", power.GetRoleUserListHandler),
            (r"/Power/SaveRole", power.SaveRoleHandler),
            (r"/Power/RemoveRoleUser", power.RemoveRoleUserHandler),
            (r"/Power/DeleteRole", power.DeleteRoleHandler),
            (r"/Power/DeleteUser", power.DeleteUserHandler),
            (r"/Power/ModifyUserStatus", power.ModifyUserStatusHandler),
            (r"/Power/CopyUserRole", power.CopyUserRoleHandler),
            (r"/Power/RemoveUserAllRole", power.RemoveUserAllRoleHandler),
            (r"/Power/ResetUserPassword", power.ResetUserPasswordHandler),
            (r"/Power/ResetUserFaildLoginCount", power.ResetUserFaildLoginCountHandler),
            # 产品管理
            (r"/Power/GetProductList", product.GetProductListHandler),
            (r"/Power/GetAllProductList", product.GetAllProductListHandler),
            (r"/Power/SaveProduct", product.SaveProductHandler),
            (r"/Power/DeleteProduct", product.DeleteProductHandler),
            # 文件管理
            (r"/File/GetStoragePathList", file.GetStoragePathListHandler),
            (r"/File/GetResourceList", file.GetResourceListHandler),
            (r"/File/GetRestrictList", file.GetRestrictListHandler),
            (r"/File/GetWaterImageList", file.GetWaterImageListHandler),
            (r"/File/GetHistoryList", file.GetHistoryListHandler),
            (r"/File/GetResourceInfo", file.GetResourceInfoHandler),
            (r"/File/GetStoragePathData", file.GetStoragePathDataHandler),
            (r"/File/GetWaterImageData", file.GetWaterImageDataHandler),
            (r"/File/SaveStoragePath", file.SaveStoragePathHandler),
            (r"/File/DeleteStoragePath", file.DeleteStoragePathHandler),
            (r"/File/SaveResource", file.SaveResourceHandler),
            (r"/File/DeleteResource", file.DeleteResourceHandler),
            (r"/File/SaveRestrict", file.SaveRestrictHandler),
            (r"/File/DeleteRestrict", file.DeleteRestrictHandler),
            (r"/File/SaveWaterImage", file.SaveWaterImageHandler),
            (r"/File/DeleteWaterImage", file.DeleteWaterImageHandler),
            (r"/File/DeleteHistory", file.DeleteHistoryHandler),
            # 菜单
            (r"/power/PowerPlatformMenu", menu.PowerPlatformMenuHandler),
            (r"/Power/GetMenuCoteSelect", menu.MenuCoteSelectHandler),
            (r"/Power/GetMenuCoteList", menu.MenuCoteListHandler),
            (r"/Power/PowerMenuTree", menu.PowerMenuTreeHandler),
            (r"/Power/MenuPowerInfo", menu.MenuPowerInfoHandler),
            (r"/Power/MenuTree", menu.MenuTreeHandler),
            (r"/Power/SaveFastMenu", menu.AddFastMenuHandler),
            (r"/Power/DeleteMenu", menu.DeleteMenuHandler),
            (r"/Power/SaveMenu", menu.SaveMenuHandler),
            (r"/Power/SaveCopyMenu", menu.SaveCopyMenuHandler),
            (r"/Power/MoveMenu", menu.MoveMenuHandler),
            (r"/Power/SaveMenuCote", menu.SaveMenuCoteHandler),
            (r"/Power/DeleteMenuCote", menu.DeleteMenuCoteHandler),
            (r"/Power/SyncSql", menu.SyncSqlHandler),
            (r"/Power/InsertSql", menu.InsertSqlHandler),
            (r"/Power/UpdateSql", menu.UpdateSqlHandler),
            # 配置
            (r"/settings/base", settings.BaseSettingsHandler),
        ]


def main():
    logger_info.info('application begin')
    try:
        if platform.system() == "Windows":
            import asyncio
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
        # 从配置中获取启动监听端口
        http_server.listen(config.get_value("run_port"))
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        print("服务已停止运行")


if __name__ == "__main__":
    main()
