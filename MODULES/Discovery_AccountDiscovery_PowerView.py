# -*- coding: utf-8 -*-
# @File  : SimplePostPowershellModule.py
# @Date  : 2019/1/12
# @Desc  :

from Lib.ModuleAPI import *


class PostModule(PostMSFPowershellFunctionModule):
    NAME_ZH = "获取Windows管理员组用户"
    DESC_ZH = "模块获取主机本地所有用户信息或本地管理员组用户信息"

    NAME_EN = "Get users in Windows Admin Group"
    DESC_EN = "The module obtains the local user information of the host or the user information of the local administrator group"

    MODULETYPE = TAG2TYPE.Discovery
    PLATFORM = ["Windows"]  # 平台
    PERMISSIONS = ["User", "Administrator", ]  # 所需权限
    ATTCK = ["T1087"]  # ATTCK向量
    README = ["https://www.yuque.com/vipersec/module/wk90cy"]
    REFERENCES = ["https://attack.mitre.org/techniques/T1087/"]
    AUTHOR = "Viper"
    OPTIONS = register_options([
        OptionEnum(name='action', name_tag="选项", desc="可以选择获取所有用户或管理员组用户", required=True,
                   default="Get-NetLocalGroupMember -GroupName Administrators",
                   enum_list=[
                       {'name': "本地管理员组用户", 'value': "Get-NetLocalGroupMember -GroupName Administrators"},
                       {'name': "本地所有用户", 'value': "Get-NetLocalGroup | Get-NetLocalGroupMember"},
                       {'name': "域管理员组用户", 'value': "Get-DomainGroupMember \"Domain Admins\""},

                   ],
                   option_length=6,
                   )
    ])

    def __init__(self, sessionid, ipaddress, custom_param):
        super().__init__(sessionid, ipaddress, custom_param)
        self.set_script("PowerView_dev.ps1")  # 设置目标机执行的脚本文件

    def check(self):
        """执行前的检查函数"""
        session = Session(self._sessionid)
        if session.is_windows:
            action = self.param("action")
            self.set_execute_string(action)
            return True, None
        else:
            return False, "此模块只支持Windows的Meterpreter,且必须在域中"

    def callback(self, status, message, data):
        if status:
            self.log_good("模块执行成功")
            self.log_raw(data)
        else:
            self.log_error("模块执行失败")
            self.log_error(message)
