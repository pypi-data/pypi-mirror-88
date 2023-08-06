# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-08-12 09:06:24
@LastEditTime: 2020-12-16 13:53:10
@LastEditors: HuangJingCan
@Description: 淘宝top接口基础类
"""
from seven_cloudapp.handlers.seven_base import *

from seven_top import top

from seven_cloudapp.models.enum import *

from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *


class TopBaseHandler(SevenBaseHandler):
    """
    @description: 淘宝top接口基础类
    """
    def get_sku_info(self, num_iids, access_token):
        """
        @description: 获取sku信息
        @param num_iids：num_iids
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            resp = self.get_goods_list_for_goodsids(num_iids, access_token)

            # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token)
            if "items_seller_list_get_response" in resp.keys():
                if "items" in resp["items_seller_list_get_response"].keys():
                    return self.reponse_json_success(resp["items_seller_list_get_response"])
                else:
                    prize = ActPrizeModel().get_entity("goods_id=%s and sku_detail<>'' and is_sku=1 ", params=int(num_iids))
                    if prize:
                        sku_detail = json.loads(prize.sku_detail.replace('\'', '\"'))
                        return self.reponse_json_success(sku_detail["items_seller_list_get_response"])
                    else:
                        return self.reponse_json_error("NoSku", "对不起，找不到该商品的sku")
            else:
                return self.reponse_json_success(resp)
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_sku_name(self, num_iids, sku_id, access_token):
        """
        @description: 获取sku名称
        @param num_iids：num_iids
        @param sku_id：sku_id
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsSellerListGetRequest()

            req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
            req.num_iids = num_iids

            resp = req.getResponse(access_token)

            # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token)
            if "items_seller_list_get_response" in resp.keys():
                if "items" in resp["items_seller_list_get_response"].keys():
                    props_names = resp["items_seller_list_get_response"]["items"]["item"][0]["props_name"].split(';')
                    for sku in resp["items_seller_list_get_response"]["items"]["item"][0]["skus"]["sku"]:
                        if sku["sku_id"] == sku_id:
                            props_name = [i for i in props_names if sku["properties"] in i]
                            if len(props_name) > 0:
                                # self.logger_info.info(props_name[0][(len(sku["properties"]) + 1):])
                                return props_name[0][(len(sku["properties"]) + 1):]
                            else:
                                # self.logger_info.info(sku["properties_name"].split(':')[1])
                                return sku["properties_name"].split(':')[1]
            return ""
        except Exception as ex:
            return ""

    def get_taobao_order(self, open_id, access_token, start_created="", end_created=""):
        """
        @description: 获取淘宝订单
        @param open_id：open_id
        @param access_token：access_token
        @param start_created：开始时间
        @param end_created：结束时间
        @return 
        @last_editors: HuangJingCan
        """
        all_order = []
        has_next = True

        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.OpenTradesSoldGetRequest()

            req.fields = "tid,status,payment,price,created,orders,num,pay_time"
            req.type = "fixed"
            req.buyer_open_id = open_id
            req.page_size = 10
            req.page_no = 1
            req.use_has_next = "true"

            if start_created == "":
                start_timestamp = TimeHelper.get_now_timestamp() - 90 * 24 * 60 * 60
                start_created = TimeHelper.timestamp_to_format_time(start_timestamp)
            # start_created = "2020-06-01 00:00:00"
            req.start_created = start_created
            if end_created != "":
                req.end_created = end_created

            while has_next:
                resp = req.getResponse(access_token)

                # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token + "【获取订单】")
                if "open_trades_sold_get_response" in resp.keys():
                    if "trades" in resp["open_trades_sold_get_response"].keys():
                        all_order = all_order + resp["open_trades_sold_get_response"]["trades"]["trade"]
                    req.page_no += 1
                    has_next = resp["open_trades_sold_get_response"]["has_next"]

            return all_order
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def rewards_status(self):
        """
        @description: rewards_status
        @param 
        @return: 
        @last_editors: CaiYouBin
        """
        status = [
            #等待卖家发货
            "WAIT_SELLER_SEND_GOODS",
            #卖家部分发货
            "SELLER_CONSIGNED_PART",
            #等待买家确认收货
            "WAIT_BUYER_CONFIRM_GOODS",
            #买家已签收（货到付款专用）
            "TRADE_BUYER_SIGNED",
            #交易成功
            "TRADE_FINISHED"
        ]
        return status

    def refund_status(self):
        """
        @description: 给予奖励的子订单退款状态
        @param 
        @return: 
        @last_editors: CaiYouBin
        """
        status = [
            #没有退款
            "NO_REFUND",
            #退款关闭
            "CLOSED",
            #卖家拒绝退款
            "WAIT_SELLER_AGREE"
        ]
        return status

    def instantiate_new(self, description, icon):
        """
        @description: 实例化
        @param description：活动简介
        @param icon：活动图标
        @return app_info
        @last_editors: HuangJingCan
        """
        app_name = config.get_value("project_name")
        template_id = config.get_value("client_template_id")
        template_version = ""
        access_token = self.get_taobao_param().access_token
        user_nick = self.get_taobao_param().user_nick
        if not user_nick:
            return self.reponse_json_error("Error", "对不起,请先授权登录")
        open_id = self.get_taobao_param().open_id
        store_user_nick = user_nick.split(':')[0]
        if not store_user_nick:
            return self.reponse_json_error("Error", "对不起，请先授权登录")
        app_info_model = AppInfoModel()
        store_user_nick = user_nick.split(':')[0]
        app_info = app_info_model.get_entity("store_user_nick=%s", params=store_user_nick)
        # 有效时间获取
        dead_date = self.get_dead_date(store_user_nick)
        if app_info:
            if dead_date != "expire":
                app_info.expiration_date = dead_date
            access_token = self.get_token()
            if access_token != "":
                app_info.access_token = access_token
            app_info_model.update_entity(app_info, "expiration_date,access_token")
            return self.reponse_json_success({"app_id": app_info.app_id, "store_user_nick": app_info.store_user_nick, "user_nick": user_nick, "access_token": app_info.access_token})
        else:
            # 记得删除过审核后
            # return self.reponse_json_success({"app_id": "112233445566", "store_user_nick": "西红柿炒蛋889", "user_nick": "西红柿炒蛋889", "access_token": "50000400807diMFrvoI14d2fae2PaOPg86ivFqRczOkBbAw5MyWDohSIZSfhw2L7ASf"})
            if self.get_is_test():
                return self.reponse_json_success()
            if ":" in user_nick:
                return self.reponse_json_error("Error", "对不起，初次创建活动包含实例化，请试用主账号进行创建。")
            base_info = BaseInfoModel().get_entity()
            template_version = base_info.client_ver

        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateInstantiateRequest()

            req.clients = "taobao,tmall"
            req.description = description
            shop_info = self.get_shop(access_token)

            # self.logger_info.info("【实例化名称】" + ":" + str(app_name))
            req.ext_json = "{ \"name\":\"" + app_name + "\"}"
            req.icon = icon
            req.alias = app_name
            req.template_id = template_id
            req.template_version = template_version
            resp = req.getResponse(access_token)

            #录入数据库
            result_app = resp["miniapp_template_instantiate_response"]
            app_info = AppInfo()
            app_info.clients = req.clients
            app_info.app_desc = result_app["app_description"]
            app_info.app_icon = result_app["app_icon"]
            app_info.app_id = result_app["app_id"]
            app_info.app_name = result_app["app_name"]
            app_info.app_ver = result_app["app_version"]
            app_info.app_key = result_app["appkey"]
            app_info.preview_url = result_app["pre_view_url"]
            app_info.template_id = req.template_id
            app_info.template_ver = req.template_version
            app_info.access_token = access_token

            if "shop_seller_get_response" in shop_info.keys():
                app_info.store_name = shop_info["shop_seller_get_response"]["shop"]["title"]
                app_info.store_id = shop_info["shop_seller_get_response"]["shop"]["sid"]

            user_seller = self.get_user_seller(access_token)
            if "user_seller_get_response" in user_seller.keys():
                app_info.seller_id = user_seller["user_seller_get_response"]["user"]["user_id"]

            app_info.is_instance = 1
            app_info.store_user_nick = store_user_nick
            app_info.owner_open_id = open_id
            app_info.instance_date = self.get_now_datetime()
            app_info.modify_date = self.get_now_datetime()
            #上线
            online_app_info = self.online_app(app_info.app_id, template_id, template_version, app_info.app_ver, access_token)
            if "miniapp_template_onlineapp_response" in online_app_info.keys():
                app_info.app_url = online_app_info["miniapp_template_onlineapp_response"]["app_info"]["online_url"]

            app_info.id = app_info_model.add_entity(app_info)

            self.create_operation_log(OperationType.add.value, app_info.__str__(), "instantiate_app", None, self.json_dumps(app_info))

            return self.reponse_json_success({"app_id": app_info.app_id, "store_user_nick": store_user_nick, "user_nick": user_nick, "access_token": access_token})
        except Exception as ex:
            self.logger_error.error(str(ex))
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=" in content:
                        if "名称已经存在" in content:
                            return self.reponse_json_error("CreateError", content[len("submsg="):], {"icon": icon, "app_name": app_name})
                        if "应用名称不合法" in content:
                            return self.reponse_json_error("CreateError", content[len("submsg="):], {"icon": icon, "app_name": app_name})
                        return self.reponse_json_error("CreateError", content[len("submsg="):], {"icon": icon, "app_name": app_name})

    def instantiate(self, user_nick, act_name, description, icon, name_ending):
        """
        @description: 实例化
        @param user_nick：用户昵称
        @param act_name：活动名称
        @param description：活动简介
        @param icon：活动图标
        @param name_ending：名称结尾
        @return app_info
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id

        app_info_model = AppInfoModel()
        store_user_nick = user_nick.split(':')[0]
        app_info = app_info_model.get_entity("store_user_nick=%s", params=store_user_nick)
        if not app_info:
            if ":" in user_nick:
                return self.reponse_json_error("Error", "对不起，初次创建活动包含实例化，请试用主账号进行创建。")
            base_info_model = BaseInfoModel()
            base_info = base_info_model.get_entity()
            template_id = config.get_value("client_template_id")
            template_version = base_info.client_ver
            access_token = self.get_taobao_param().access_token
            app_info = self.instantiate_app(user_nick, open_id, description, icon, act_name, template_id, template_version, 1, access_token, name_ending)

            if isinstance(app_info, dict):
                if "error" in app_info.keys():
                    return self.reponse_json_error(app_info["error"], app_info["message"])

            self.create_operation_log(OperationType.add.value, app_info.__str__(), "instantiate", None, self.json_dumps(app_info))

        return app_info

    def instantiate_app(self, user_nick, open_id, description, icon, name, template_id, template_version, isfirst, access_token, name_ending):
        """
        @description: 实例化
        @param user_nick：用户昵称
        @param open_id：用户唯一标识
        @param description：活动简介
        @param icon：活动图标
        @param name：活动名称
        @param template_id：模板id
        @param template_version：模板版本
        @param isfirst：是否第一次
        @param access_token：access_token
        @param name_ending：name_ending
        @return app_info
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateInstantiateRequest()

            req.clients = "taobao,tmall"
            req.description = description
            shop_info = self.get_shop(access_token)

            if isfirst == 1:
                app_name = shop_info["shop_seller_get_response"]["shop"]["title"] + name_ending
            else:
                app_name = name
            # self.logger_info.info("【实例化名称】" + ":" + str(app_name))
            req.ext_json = "{ \"name\":\"" + app_name + "\"}"
            req.icon = icon
            req.name = app_name
            req.alias = config.get_value("project_name")
            req.template_id = template_id
            req.template_version = template_version
            resp = req.getResponse(access_token)

            #录入数据库
            result_app = resp["miniapp_template_instantiate_response"]
            app_info_model = AppInfoModel()
            app_info = AppInfo()
            app_info.clients = req.clients
            app_info.app_desc = result_app["app_description"]
            app_info.app_icon = result_app["app_icon"]
            app_info.app_id = result_app["app_id"]
            app_info.app_name = result_app["app_name"]
            app_info.app_ver = result_app["app_version"]
            app_info.app_key = result_app["appkey"]
            app_info.preview_url = result_app["pre_view_url"]
            app_info.template_id = req.template_id
            app_info.template_ver = req.template_version

            if "shop_seller_get_response" in shop_info.keys():
                app_info.store_name = shop_info["shop_seller_get_response"]["shop"]["title"]
                app_info.store_id = shop_info["shop_seller_get_response"]["shop"]["sid"]

            user_seller = self.get_user_seller(access_token)
            if "user_seller_get_response" in user_seller.keys():
                app_info.seller_id = user_seller["user_seller_get_response"]["user"]["user_id"]

            app_info.is_instance = 1
            app_info.store_user_nick = user_nick.split(':')[0]
            app_info.owner_open_id = open_id
            app_info.instance_date = self.get_now_datetime()
            app_info.modify_date = self.get_now_datetime()
            #上线
            online_app_info = self.online_app(app_info.app_id, template_id, template_version, app_info.app_ver, access_token)
            if "miniapp_template_onlineapp_response" in online_app_info.keys():
                app_info.app_url = online_app_info["miniapp_template_onlineapp_response"]["app_info"]["online_url"]

            app_info.id = AppInfoModel().add_entity(app_info)

            return app_info
        except Exception as ex:
            self.logger_error.error(str(ex))
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=" in content:
                        if "名称已经存在" in content:
                            if isfirst == 1:
                                return self.instantiate_app(user_nick, open_id, description, icon, name, template_id, template_version, 0, access_token, name_ending)
                            else:
                                return {"error": "CreateError", "message": content[len("submsg="):]}
                        if "应用名称不合法" in content:
                            if isfirst == 1:
                                return self.instantiate_app(user_nick, open_id, description, icon, name, template_id, template_version, 0, access_token, name_ending)
                            else:
                                return {"error": "CreateError", "message": content[len("submsg="):]}
                        return {"error": "CreateError", "message": content[len("submsg="):]}

    def online_app(self, app_id, template_id, template_version, app_version, access_token):
        """
        @description: app上线
        @param app_id：app_id
        @param template_id：模板id
        @param template_version：模板版本
        @param app_version：app版本
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateOnlineappRequest()

            req.clients = "taobao,tmall"
            req.app_id = app_id
            req.template_id = template_id
            req.template_version = template_version
            req.app_version = app_version
            resp = req.getResponse(access_token)
            return resp
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_shop(self, access_token):
        """
        @description: 获取店铺信息
        @param access_token：access_token
        @return: 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ShopSellerGetRequest()

            req.fields = "sid,title,pic_path"
            resp = req.getResponse(access_token)
            return resp
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_user_seller(self, access_token):
        """
        @description: 获取关注店铺用户信息
        @param access_token：access_token
        @return: 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.UserSellerGetRequest()

            req.fields = "user_id,nick,sex"
            resp = req.getResponse(access_token)
            return resp
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_dead_date(self, user_nick):
        """
        @description: 获取过期时间
        @param user_nick：用户昵称
        @return 
        @last_editors: HuangJingCan
        """
        if self.get_is_test() == True:
            return config.get_value("test_dead_date")
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.VasSubscribeGetRequest()

            req.article_code = config.get_value("article_code")
            req.nick = user_nick
            resp = req.getResponse(self.get_taobao_param().access_token)
            if "article_user_subscribe" not in resp["vas_subscribe_get_response"]["article_user_subscribes"].keys():
                return "expire"
            else:
                return resp["vas_subscribe_get_response"]["article_user_subscribes"]["article_user_subscribe"][0]["deadline"]
        except Exception as ex:
            self.logger_info.info("get_dead_date:" + str(ex))
            return config.get_value("test_dead_date")

    def get_token(self):
        """
        @description: 获取授权token
        @param 
        @return: 
        @last_editors: CaiYouBin
        """
        if self.get_is_test() == True:
            return ""
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsOnsaleGetRequest()

            req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
            req.page_no = 1
            req.page_size = 10
            resp = req.getResponse(self.get_taobao_param().access_token)

            return self.get_taobao_param().access_token
        except Exception as ex:
            return ""

    def get_goods_list(self, page_index, page_size, goods_name, order_tag, order_by, access_token):
        """
        @description: 导入商品列表（获取当前会话用户出售中的商品列表）
        @param page_index：页索引
        @param page_size：页大小
        @param goods_name：商品名称
        @param order_tag：order_tag
        @param order_by：排序类型
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsOnsaleGetRequest()

            req.fields = "num_iid,title,nick,price,input_str,property_alias,sku,props_name,pic_url"
            req.page_no = page_index + 1
            req.page_size = page_size
            if goods_name != "":
                req.q = goods_name
            req.order_by = order_tag + ":" + order_by

            resp = req.getResponse(access_token)
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index

            # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token)
            return self.reponse_json_success(resp)
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_goods_list_client(self, page_index, page_size, access_token):
        """
        @description: 导入商品列表（客户端）
        @param page_index：页索引
        @param page_size：页大小
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsOnsaleGetRequest()

            req.fields = "num_iid,title,nick,pic_url,price"
            req.page_no = page_index + 1
            req.page_size = page_size

            resp = req.getResponse(access_token)
            # self.logger_info.info(str(resp))
            goods_list = []
            if "items_onsale_get_response" in resp.keys():
                if "items" in resp["items_onsale_get_response"]:
                    if "item" in resp["items_onsale_get_response"]["items"]:
                        if len(resp["items_onsale_get_response"]["items"]["item"]) > 10:
                            goods_index_list = range(len(resp["items_onsale_get_response"]["items"]["item"]))
                            indexs = random.sample(goods_index_list, 10)
                            for i in range(0, 10):
                                goods_list.append(resp["items_onsale_get_response"]["items"]["item"][indexs[i]])
                        else:
                            goods_list = resp["items_onsale_get_response"]["items"]["item"]

                        random.randint(0, len(resp["items_onsale_get_response"]["items"]["item"]))
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index

            return self.reponse_json_success(goods_list)
        except Exception as ex:
            # self.logger_info.info(str(ex) + "【access_token】：" + self.get_taobao_param().access_token)
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_goods_info(self, num_iid, access_token):
        """
        @description: 导入商品列表
        @param num_iids：num_iids
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemSellerGetRequest()

            req.fields = "num_iid,title,nick,pic_url,price,item_img.url,outer_id,sku,approve_status,prop_img"
            req.num_iid = num_iid
            resp = req.getResponse(access_token)
            # self.logger_info.info(str(resp))
            return self.reponse_json_success(resp)
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=该商品已被删除" in content:
                        return self.reponse_json_error("GoodsDel", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def app_update(self):
        """
        @description: app更新
        @param 
        @return 
        @last_editors: HuangJingCan
        """
        app_id = self.get_param("app_id")
        client_template_id = config.get_value("client_template_id")
        test_client_ver = config.get_value("test_client_ver")
        access_token = self.get_taobao_param().access_token

        base_info = BaseInfoModel().get_entity()
        client_ver = base_info.client_ver

        app_info_model = AppInfoModel()
        app_info = app_info_model.get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("NoApp", "对不起，找不到该APP")
        old_app_info = app_info

        #指定账号升级
        if test_client_ver:
            user_nick = self.get_taobao_param().user_nick
            if user_nick:
                if user_nick == config.get_value("test_user_nick"):
                    client_ver = test_client_ver

        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateUpdateappRequest()

            req.clients = "taobao,tmall"
            req.app_id = app_id
            req.template_id = client_template_id
            req.template_version = client_ver
            resp = req.getResponse(access_token)

            if resp and ("miniapp_template_updateapp_response" in resp.keys()):
                app_version = resp["miniapp_template_updateapp_response"]["app_version"]
                online_app_info = self.online_app(app_id, client_template_id, client_ver, app_version, access_token)
                if "miniapp_template_onlineapp_response" in online_app_info.keys():
                    app_info.app_ver = resp["miniapp_template_updateapp_response"]["app_version"]
                    app_info.template_ver = client_ver
                    app_info.modify_date = self.get_now_datetime()
                    app_info_model.update_entity(app_info)

            # self.logger_info.info(str(resp) + "【更新】")
            self.create_operation_log(OperationType.update.value, app_info.__str__(), "AppUpdateHandler", self.json_dumps(old_app_info), self.json_dumps(app_info))
            return self.reponse_json_success()
        except Exception as ex:
            if "submsg" in str(ex):
                self.logger_error.error(str(ex) + "【更新】")
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def change_throw_goods_list_status(self, throw_goods_ids, url, status):
        """
        @description: change_throw_goods_list_status
        @param throw_goods_ids：throw_goods_ids
        @param url：链接地址
        @param status：状态
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappDistributionItemsBindRequest()

            req.target_entity_list = throw_goods_ids
            req.url = url
            req.add_bind = status
            resp = req.getResponse(self.get_taobao_param().access_token)
            return resp
        except Exception as ex:
            # self.logger_info.info(str(ex) + "【access_token】：" + self.get_taobao_param().access_token)
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_goods_list_for_goodsids(self, num_iids, access_token):
        """
        @description: 批量获取商品详细信息
        @param num_iids：商品id列表
        @param access_token：access_token
        @return list
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsSellerListGetRequest()

            req.fields = "num_iid,title,nick,pic_url,price,input_str,property_alias,sku,props_name,outer_id,prop_img"
            req.num_iids = num_iids
            resp = req.getResponse(access_token)
            return resp
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return {"error_code": "NoPower", "error_message": content[len("submsg="):]}
                    if "submsg=" in content:
                        return {"error_code": "Error", "error_message": content[len("submsg="):]}

    def get_taobao_order_info(self, order_no, access_token):
        """
        @description: 获取单笔订单
        @param order_no：订单编号
        @param access_token：access_token
        @return: 
        @last_editors: CaiYouBin
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.OpenTradeGetRequest()

            req.fields = "tid,status,payment,price,created,orders,num,pay_time,buyer_open_uid"
            req.tid = order_no
            resp = req.getResponse(access_token)
            if "open_trade_get_response" in resp.keys():
                if "trade" in resp["open_trade_get_response"]:
                    return resp["open_trade_get_response"]["trade"]
                return None
            return resp
        except Exception as ex:
            # self.logger_info.info(str(ex) + "【access_token】：" + self.get_taobao_param().access_token)
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_coupon_details(self, right_ename):
        """
        @description: 获取优惠券详情信息(请求top接口)
        @param right_ename:奖池ID
        @return: dict
        @last_editors: LaiKaiXiang
        """
        right_ename = self.get_param("right_ename")
        access_token = self.get_taobao_param().access_token
        resp = ""
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.AlibabaBenefitQueryRequest()
            req.ename = right_ename
            req.app_name = "promotioncenter-" + config.get_value("server_template_id")
            req.award_type = "1"
            resp = req.getResponse(access_token)
            return resp
        except Exception as ex:
            # self.logger_error.error(str(ex) + "【获取优惠券详情信息】")
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])