# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-24 17:26:33
@LastEditTime: 2020-12-09 11:50:30
@LastEditors: HuangJingCan
@Description: 基础信息相关
"""
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *


class LeftNavigationHandler(TopBaseHandler):
    """
    @description: 左侧导航栏
    """
    def get_async(self):
        """
        @description: 左侧导航栏
        @param {*}
        @return 字典
        @last_editors: HuangJingCan
        """
        user_nick = self.get_taobao_param().user_nick
        if not user_nick:
            return self.reponse_json_error("Error", "对不起,请先授权登录")
        store_user_nick = user_nick.split(':')[0]
        if not store_user_nick:
            return self.reponse_json_error("Error", "对不起，请先授权登录")
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")

        app_info = None
        app_id = self.get_param("app_id")
        if app_id:
            app_info = AppInfoModel().get_entity("app_id=%s", params=app_id)

        # 左上角信息
        info = {}
        info["company"] = "天志互联"
        info["miniappName"] = config.get_value("project_name")
        info["logo"] = config.get_value("project_logo")

        # 左边底部菜单
        helper_info = {}
        helper_info["customer_service"] = "http://amos.alicdn.com/getcid.aw?v=2&uid=%E5%A4%A9%E5%BF%97%E4%BA%92%E8%81%94&site=cntaobao&s=1&groupid=0&charset=utf-8"
        helper_info["video_url"] = base_info.video_url
        helper_info["study_url"] = base_info.study_url
        helper_info["is_remind_phone"] = base_info.is_remind_phone
        helper_info["phone"] = app_info.app_telephone

        # 过期时间
        renew_info = {}
        renew_info["surplus_day"] = 0
        dead_date = ""
        if app_info:
            dead_date = app_info.expiration_date
        else:
            dead_date = self.get_dead_date(store_user_nick)
        renew_info["dead_date"] = dead_date
        if dead_date != "expire":
            renew_info["surplus_day"] = TimeHelper.difference_days(dead_date, self.get_now_datetime())

        data = {}
        data["app_info"] = info
        data["helper_info"] = helper_info
        data["renew_info"] = renew_info
        if base_info.product_price:
            data["renew_prices"] = ast.literal_eval(base_info.product_price)

        self.reponse_json_success(data)


class RightExplainHandler(SevenBaseHandler):
    """
    @description: 右侧各种教程和说明导航
    """
    def get_async(self):
        """
        @description: 右侧各种教程和说明导航
        @param {*}
        @return dict
        @last_editors: HuangJingCan
        """
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = []

        if base_info.course_strategy:
            data = ast.literal_eval(base_info.course_strategy)

        self.reponse_json_success(data)


class FriendLinkHandler(SevenBaseHandler):
    """
    @description: 获取友情链接
    """
    def get_async(self):
        """
        @description: 获取友情链接
        @param {*}
        @return list
        @last_editors: HuangJingCan
        """
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = []

        if base_info.friend_link:
            data = ast.literal_eval(base_info.friend_link)

        self.reponse_json_success(data)


class UpdateInfoHandler(SevenBaseHandler):
    """
    @description: 获取更新信息
    """
    @filter_check_params("app_id")
    def get_async(self):
        """
        @description: 获取更新信息
        @param app_id：app_id
        @return dict
        @last_editors: HuangJingCan
        """
        app_id = self.get_param("app_id")

        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")
        app_info = AppInfoModel().get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("AppInfoError", "App信息出错")

        data = {}

        data["client_ver"] = base_info.client_ver
        data["server_ver"] = base_info.server_ver
        data["client_now_ver"] = app_info.template_ver
        data["update_function"] = []
        if base_info.update_function:
            data["update_function"] = ast.literal_eval(base_info.update_function)

        self.reponse_json_success(data)


class OnlineLiveUrlHandler(SevenBaseHandler):
    """
    @description: 小程序链接
    """
    @filter_check_params("app_id,act_id")
    def get_async(self):
        """
        @description: 小程序链接
        @param app_id：app_id
        @param act_id：活动id
        @return dict
        @last_editors: HuangJingCan
        """
        app_id = self.get_param("app_id")
        act_id = int(self.get_param("act_id", 0))

        if act_id <= 0:
            return self.reponse_json_error("ActError", "无效活动")

        app_info = AppInfoModel().get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("AppInfoError", "App信息出错")

        data = {}

        data["online_url"] = f"https://m.duanqu.com/?_ariver_appid={app_id}&query=" + CodingHelper.url_encode(f"actid={act_id}")
        data["live_url"] = f"https://market.m.taobao.com/app/taefed/shopping-delivery-wapp/index.html#/putin?mainKey=form&appId={app_id}"

        self.reponse_json_success(data)


class DecorationPosterHandler(SevenBaseHandler):
    """
    @description: 装修海报
    """
    def get_async(self):
        """
        @description: 装修海报
        @param {*}
        @return dict
        @last_editors: HuangJingCan
        """
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = {}

        if base_info.decoration_poster:
            data["decoration_poster"] = ast.literal_eval(base_info.decoration_poster)

        self.reponse_json_success(data)