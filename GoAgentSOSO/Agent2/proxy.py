# coding:utf-8

import os, sys
sys.dont_write_bytecode = True

work_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(work_path)
data_path = os.path.join(work_path, 'data')
if not os.path.isdir(data_path): os.mkdir(data_path)

# add python lib path
sys.path.insert(0, work_path + '/lib')
if sys.platform.startswith("linux"):
    sys.path.append(work_path + '/lib.egg')
    # reduce resource request for threading, for OpenWrt
    import threading
    threading.stack_size(128*1024)
elif sys.platform == "darwin":
    sys.path.append(work_path + '/lib.egg')


from xlog import getLogger
xlog = getLogger("gae_proxy")
xlog.set_buffer(500)

from config import config
if config.log_file:
    log_file = os.path.join(data_path, "local.log")
    xlog.set_file(log_file)

xlog.info(config.summary())
xlog.set_time()
if config.LISTEN_DEBUGINFO:
    xlog.set_debug()

import time
import random
import threading
import urllib2
import simple_http_server
import proxy_handler
import connect_control
import connect_manager
from cert_util import CertUtil
from gae_handler import spawn_later
from pac_server import PACServerHandler


def pre_start():

    def get_windows_running_process_list():
        import os
        import glob
        import ctypes
        import collections
        Process = collections.namedtuple('Process', 'pid name exe')
        process_list = []
        if os.name == 'nt':
            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_VM_READ = 0x0010
            lpidProcess= (ctypes.c_ulong * 1024)()
            cb = ctypes.sizeof(lpidProcess)
            cbNeeded = ctypes.c_ulong()
            ctypes.windll.psapi.EnumProcesses(ctypes.byref(lpidProcess), cb, ctypes.byref(cbNeeded))
            nReturned = cbNeeded.value/ctypes.sizeof(ctypes.c_ulong())
            pidProcess = [i for i in lpidProcess][:nReturned]
            has_queryimage = hasattr(ctypes.windll.kernel32, 'QueryFullProcessImageNameA')
            for pid in pidProcess:
                hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, 0, pid)
                if hProcess:
                    modname = ctypes.create_string_buffer(2048)
                    count = ctypes.c_ulong(ctypes.sizeof(modname))
                    if has_queryimage:
                        ctypes.windll.kernel32.QueryFullProcessImageNameA(hProcess, 0, ctypes.byref(modname), ctypes.byref(count))
                    else:
                        ctypes.windll.psapi.GetModuleFileNameExA(hProcess, 0, ctypes.byref(modname), ctypes.byref(count))
                    exe = modname.value
                    name = os.path.basename(exe)
                    process_list.append(Process(pid=pid, name=name, exe=exe))
                    ctypes.windll.kernel32.CloseHandle(hProcess)
        elif sys.platform.startswith('linux'):
            for filename in glob.glob('/proc/[0-9]*/cmdline'):
                pid = int(filename.split('/')[2])
                exe_link = '/proc/%d/exe' % pid
                if os.path.exists(exe_link):
                    exe = os.readlink(exe_link)
                    name = os.path.basename(exe)
                    process_list.append(Process(pid=pid, name=name, exe=exe))
        else:
            try:
                import psutil
                process_list = psutil.get_process_list()
            except Exception as e:
                xlog.exception('psutil.get_windows_running_process_list() failed: %r', e)
        return process_list

    if sys.platform == 'cygwin':
        xlog.info('cygwin is not officially supported, please continue at your own risk :)')
        #sys.exit(-1)
    elif os.name == 'posix':
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (8192, -1))
        except Exception as e:
            pass
    elif os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(u'XX-Mini v%s' % config.version)
        if not config.LISTEN_VISIBLE:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        else:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        blacklist = {'360safe': False,
                     'QQProtect': False, }
        softwares = [k for k, v in blacklist.items() if v]
        if softwares:
            tasklist = '\n'.join(x.name for x in get_windows_running_process_list()).lower()
            softwares = [x for x in softwares if x.lower() in tasklist]
            if softwares:
                title = u'XX-Mini 建议'
                error = u'某些安全软件(如 %s)可能和本软件存在冲突，造成 CPU 占用过高。\n如有此现象建议暂时退出此安全软件来继续运行XX-Mini' % ','.join(softwares)
                ctypes.windll.user32.MessageBoxW(None, error, title, 0)
                #sys.exit(0)
    if config.PAC_ENABLE:
        pac_ip = config.PAC_IP
        url = 'http://%s:%d/%s' % (pac_ip, config.PAC_PORT, config.PAC_FILE)
        spawn_later(600, urllib2.build_opener(urllib2.ProxyHandler({})).open, url)


def main():
    pre_start()

    connect_control.keep_running = True
    connect_manager.https_manager.load_config()
    xlog.debug("## GAEProxy set keep_running: %s", connect_control.keep_running)

    CertUtil.init_ca()

    proxy_daemon = simple_http_server.HTTPServer((config.LISTEN_IP, config.LISTEN_PORT), proxy_handler.GAEProxyHandler)
    proxy_thread = threading.Thread(target=proxy_daemon.serve_forever)
    proxy_thread.setDaemon(True)
    proxy_thread.start()

    if config.PAC_ENABLE:
        pac_daemon = simple_http_server.HTTPServer((config.PAC_IP, config.PAC_PORT), PACServerHandler)
        pac_thread = threading.Thread(target=pac_daemon.serve_forever)
        pac_thread.setDaemon(True)
        pac_thread.start()
        try:
            urllib2.urlopen('http://127.0.0.1:%d/%s' % (config.PAC_PORT, config.PAC_FILE))
        except:
            pass

    while connect_control.keep_running:
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        xlog.info("start to terminate GAE_Proxy")
        os._exit(0)
