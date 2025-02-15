#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : jade_tools.py
# @Author   : jade
# @Date     : 2021/5/25 10:28
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import os
import queue
import sys
import datetime
import time
import shutil
from jade.jade_progress_bar import ProgressBar
import socket
import platform
from cryptography.fernet import Fernet
import zipfile
import signal
import string
import random

def zh_ch(string):
    """
    解决cv2.namedWindow中文乱码问题
    :param string:
    :return:
    """
    return string.encode("gbk").decode('UTF-8', errors='ignore')

def Exit(exit_number,process_id_queue=None):
    """
    强制结束
    """
    time.sleep(1)
    if process_id_queue:
        clear_process_queue(process_id_queue)
    os._exit(exit_number)

def getNumberofString(string):
    """
    提取字符串中的数字
    :param string:
    :return:
    """
    return "".join(list(filter(str.isdigit, string)))


def CreateSavePath(file_dir):
    """
    新建文件夹
    :param string:
    :return:返回文件夹名称
    """
    if os.path.exists(file_dir) is not True:
        os.makedirs(file_dir)
    return file_dir


def JudgeWhetherIPAddress(ip):
    """
    判断是否为IP地址
    :param string:
    :return:
    """
    if len(ip.split(".")) == 4:
        return True
    else:
        return False

def getConfig(config,section, configname,default_value=None,config_dic=None,JadeLog=None):
    """
    读取ini参数
    """
    try:
        configparam = (config.get(section, configname)).split("#")[0].rstrip()
        return configparam
    except Exception as e:
        if config_dic is not None:
            config_dic.update({configname:default_value})
        if JadeLog:
            JadeLog.ERROR("读取{}参数异常,请检查参数是否正常".format(configname))
        else:
            pass
        return default_value


def getBoolConfig(config, section, configname):
    """
    读取ini参数,强制返回Bool
    :param string:
    :return:
    """
    try:
        configparam = (config.get(section, configname)).split("#")[0].rstrip()
    except:
        print("读取{}参数异常,请检查参数是否正常".format(configname))
        sys.exit()
    if configparam == "False":
        return False
    elif configparam == "True":
        return True
    else:
        print("读取{}参数异常,参数内容为:{}错误,请检查参数是否正常".format(configname,configparam))
        sys.exit()


def getSectionsConfig(config,section_list,configname):
    config_list = []
    for section in section_list:
        try:
            configparam = (config.get(section, configname)).split("#")[0].rstrip()
            config_list.append(configparam)
        except Exception as e:
            print("读取{}参数异常,请检查参数是否正常,出错原因为 = {},发生异常文件{},发生异常所在的行数{}".format(configname.e,
                                                                                        e.__traceback__.tb_frame.f_globals[
                                                                                            "__file__"],
                                                                                        e.__traceback__.tb_lineno))
            sys.exit()
    return config_list

def getSectionList(config,section_name="Camera"):
    section_list = []
    for section in config.sections():
        if section_name in section:
            section_list.append(section)
    return section_list

def getSectionConfigs(config,section):
    try:
        configsList = []
        itemList = config.items(section)
        for item in itemList:
            configsList.append(item[1].split("#")[0].rstrip())
    except Exception as e:
        print("读取{}参数异常,请检查参数是否正常,异常原因为{}".format(section, e))
        sys.exit()
    return configsList


def resource_path(relative_path):
    """
    生成资源文件目录访问路径,用于打包成可执行文件
    :param string:
    :return:
    """
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def GetSeqNumber():
    """
    返回序列号,精确到s
    :param string:
    :return:
    """
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y%m%d%H%M%S%f")
    return otherStyleTime


def timestr_to_time(time_str):
    """
    字符串转时间
    :param string:
    :return: Int
    """

    return time.mktime(time.strptime(time_str,"%Y-%m-%d %H:%M:%S"))

def timerfc_to_str(time_rfc):
    """
    RFC 2832格式转时间字符串格式
    """
    return timeint_to_timestr(time.mktime(time.strptime(time_rfc,'%a, %d %b %Y %H:%M:%S %z')))


def timefloat_to_timestr(floatstring):
    """
    时间字符串戳转时间字符串
    :param string:
    :return: string
    """
    floattime = float(floatstring)
    timeArray = time.localtime(floattime)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def timeint_to_timestr(timeInt):
    """
    时间戳转时间字符串
    :param Int:
    :return: string
    """
    timeArray = time.localtime(timeInt)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def GetChineseTimeStamp():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y{y}%m{m}%d{d} %H:%M:%S").format(y='年',m='月',d='日')
    pathname = otherStyleTime
    return pathname

def GetTimeStamp():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    pathname = otherStyleTime
    return pathname

def GetYear():
    today  = datetime.datetime.now()
    return today.year

def GetTime():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d-%H-%M-%S")
    pathname = otherStyleTime
    data_ms = datetime.datetime.now().microsecond / 1000
    time_stamp = "%s-%03d" % (pathname, data_ms)
    return time_stamp

#合并文件路径
def OpsJoin(path1,path2):
    return os.path.join(path1,path2)

#返回上一层目录
def GetPreviousDir(savepath):

    return os.path.dirname(savepath)
#返回最后一层的目录
def GetLastDir(savepath):
    return os.path.basename(savepath)


#获取文件夹下，后缀为.的文件
def GetFilesWithLastNamePath(dir,lastname):
    imagename_list = os.listdir(dir)
    image_list = []
    for image_name in imagename_list:
        last = "."+image_name.split(".")[-1]
        if last == lastname:
            image_list.append(os.path.join(dir,image_name))
    return (image_list)

#获取一个文件夹下所有的图片列表
def GetAllImagesNames(dir):
    imagename_list = os.listdir(dir)
    image_list = []
    for image_name in imagename_list:
        if image_name[-4:].lower() == ".jpg" or image_name[-4:].lower() == ".png":
            image_list.append(image_name)
    return (image_list)

#获取一个文件夹下所有的图片路径
def GetAllImagesPath(dir):
    imagename_list = os.listdir(dir)
    image_list = []
    for image_name in imagename_list:
        if image_name[-4:].lower() == ".jpg" or image_name[-4:].lower() == ".png":
            image_list.append(OpsJoin(dir,image_name))
    return (image_list)

#获取今天的日期
def GetToday():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    pathname = otherStyleTime.split(" ")[0]
    return pathname

#获取当前的时间
def GetHourTime():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d %H-%M-%S")
    pathname = otherStyleTime.split(" ")[1]
    return pathname



##文件夹下文件重新命名
def RenameImageWithDir(dir):
    image_path_list = GetAllImagesPath(dir)
    progressBar = ProgressBar(len(image_path_list))
    for image_path in image_path_list:
        shutil.copy(image_path,os.path.join(dir,GetSeqNumber()+".jpg"))
        os.remove(image_path)
        progressBar.update()

class DetectResultModel():
    def __init__(self,boxes,label_texts,labelIds,scores):
        self.boxes = boxes
        self.label_texts = label_texts
        self.label_ids = labelIds
        self.scores = scores

"""
获取当前IP地址
"""
def get_ip_address(ip_address="127.0.0.1"):
    """
            查询本机ip地址
            :return: ip
            """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ip_address, 80))
        ip = s.getsockname()[0]
        s.close()
    finally:
        pass
    return ip
"""
获取操作系统
"""
def getOperationSystem():
    return platform.system()

"""
Windows与Linux直接路径转换
"""
def ConvertPath(file_path):
    if ":" in file_path:
        if getOperationSystem() == "Windows":
            file_path = file_path.replace("\\", "/")
        elif getOperationSystem() == "Linux":
            try:
                file_path = file_path.replace("\\","/")
            except:
                pass
            try:
                file_path = "/mnt/" + file_path.split(":")[0].lower() + file_path.split(":")[1]
            except:
                pass
    else:
        if getOperationSystem() == "Windows":
            try:
                file_path = file_path.split("/mnt/")[1][0].upper() + ":" + file_path.split("/mnt/")[1][1:]
                file_path = file_path.replace("\\", "/")
            except:
                pass
        elif getOperationSystem() == "Linux":
            try:
                file_path = file_path.replace("\\", "/")
            except:
                pass
    return file_path

"""
更新
"""
def update_lib(lib_path):
    if os.path.exists(lib_path):
        if os.path.isdir(lib_path):
            CreateSavePath(GetLastDir(lib_path))
            if getOperationSystem() == 'Windows':
                file_list = GetFilesWithLastNamePath(lib_path, '.pyd')
            elif getOperationSystem() == 'Linux':
                file_list = GetFilesWithLastNamePath(lib_path, '.so')
            for file in file_list:
                try:
                    shutil.copy(file, GetLastDir(lib_path))
                    print("正在拷贝文件{},到{}成功".format(file,GetLastDir(lib_path)))
                except:
                    print("正在拷贝文件{},到{}失败".format(file,GetLastDir(lib_path)))
                    pass
            if getOperationSystem() == 'Windows':
                exec_file_list = GetFilesWithLastNamePath(lib_path, '.exe')
            elif getOperationSystem() == "Linux":
                exec_file_list = GetFilesWithLastNamePath(lib_path, '.AppImage')
            for exec_file in exec_file_list:
                try:
                    shutil.copy(exec_file, os.path.abspath(""))
                    print("正在拷贝文件{},到{}成功".format(exec_file,os.path.abspath("")))
                except:
                    print("正在拷贝文件{},到{}失败".format(exec_file,os.path.abspath("")))
                    pass
            shutil.rmtree(lib_path)


def encryption_model(model_path,save_root_path=None,key=None):
    if key is None:
        key = Fernet.generate_key()
        # 保存license
    f = Fernet(key)
    try:
        save_path = os.path.join(GetPreviousDir(model_path),GetLastDir(model_path).split(".")[0]+"_en."+GetLastDir(model_path).split(".")[1])
    except:
        save_path =  os.path.join(GetPreviousDir(model_path),GetLastDir(model_path)+"_en")
    if save_root_path:
        print(save_path)
        save_path = save_root_path + save_path[len(save_path.split("\\")[0]):]
        print(save_path)
        CreateSavePath(GetPreviousDir(save_path))
    if os.path.exists(model_path) and os.path.isfile(model_path):
        with open(save_path, 'wb') as ew:
            # 二进制读取模型文件
            content = open(model_path, 'rb').read()
            # 根据密钥解密文件
            encrypted_content = f.encrypt(content)
            # print(encrypted_content)
            # 保存到新文件
            ew.write(encrypted_content)
    else:
        raise  FileExistsError("确认待加密的文件是否存在,文件路径为:{}".format(model_path))


def decryption_model(model_path,key=None,is_byte=False,save_model_path=None):
    if key is None:
        raise  "没有密码无法解密"
    f = Fernet(key)
    en_model_file = open(model_path, 'rb').read()
    en_model_file = f.decrypt(en_model_file)
    if is_byte:
        return en_model_file
    if save_model_path is None:
        try:
            save_model_path = os.path.join(GetPreviousDir(model_path),GetLastDir(model_path).split(".")[0]+"_dep."+GetLastDir(model_path).split(".")[1])
        except:
            save_model_path = os.path.join(GetPreviousDir(model_path), GetLastDir(model_path) + "_en_dep")
    with open(save_model_path, "wb") as f:
        f.write(en_model_file)
    ## 注意返回正确的
    return save_model_path

def test_load_onnx(model):
    import onnx
    import onnxruntime
    sess = onnxruntime.InferenceSession(model, providers=['CUDAExecutionProvider'])
"""
获取文件夹下所有文件
    for model_path in findAllFile(model_root_path):
            print(model_path)
"""
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname
def zip_file(dirpath,save_path):
    output_name = save_path
    parent_name = os.path.dirname(dirpath)
    zip = zipfile.ZipFile(output_name, "w", zipfile.ZIP_DEFLATED)
    # 多层级压缩
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(root, file)
            writepath = os.path.relpath(filepath, parent_name)
            zip.write(filepath, writepath)
def GetReadMe():
	with open("README.md","rb") as f:
		content = f.read()
		return str(content,encoding="utf-8")

class GracefulKiller:
    kill_now = False
    signals = {
        signal.SIGINT: 'SIGINT',
        signal.SIGTERM: 'SIGTERM'
    }

    def __init__(self,func,*args):
        self.func = func
        self.args = args
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.func(self.args[0][0],self.args[0][1],self.args[0][2])
        time.sleep(1)
        self.kill_now = True



def GetExitSignal(func,*args):
    killer = GracefulKiller(func,args)
    while not killer.kill_now:
        time.sleep(1)
    Exit(-1)
def ldk_release(ldkqueue,JadeLog=None,process_id_queue=None):
    if JadeLog:
        JadeLog.DEBUG("准备释放加密狗登录", True)
    if process_id_queue:
        JadeLog.DEBUG("准备清除子进程",True)
        clear_process_queue(process_id_queue)
    if ldkqueue.qsize() > 0:
        pyldk, handle = ldkqueue.get()
        pyldk.adapter.logout(handle)
# 根据字符窜长度随机生成字符串
def generate_random_string(length):
    # 设置包含所有大小写字母、数字的字符集合
    characters = string.ascii_letters + string.digits

    # 从字符集合中随机选取指定长度的字符并组合起来形成随机字符串
    return ''.join([random.choice(characters) for _ in range(length)])
def get_file_size(filename):
    size = os.path.getsize(filename)
    return size

def clear_process_queue(process_id_queue):
    for i in range(process_id_queue.qsize()):
        clear_process(process_id_queue.get())


def clear_process(process_id):
    import psutil
    try:
        process = psutil.Process(process_id)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
    except:
        pass


if __name__ == '__main__':
    key = "HgEWN6tv_HeVqbh7M_Q-XT6NCVETFeIspgE17Xh30Co="
    #encryption_model("container_det_768-576_slim.onnx","HgEWN6tv_HeVqbh7M_Q-XT6NCVETFeIspgE17Xh30Co=")
    model = decryption_model("container_det_768-576_slim_en.onnx",key=key,is_byte=True)
    test_load_onnx(model)
