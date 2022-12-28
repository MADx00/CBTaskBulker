#import logging
import shutil
from cbapi.response import *
import cbapi
import os
import concurrent.futures
import argparse

cb = CbResponseAPI(timeout=60)
mulitThread_mode = False
lr_threads = 2
get_output = False
clean_dfir_task = False

id_txt_file = "id.txt"
task_src_path = "Task.zip"
sevenZ_src_path = "7za.exe"
run_src_path = "run.bat"

task_dst_directory = r"C:\DFIR_Task"
task_dst_path = r"{}\{}".format(task_dst_directory, task_src_path)
sevenZ_dst_path = r"{}\{}".format(task_dst_directory, sevenZ_src_path)
run_dst_path = r"{}\{}".format(task_dst_directory, run_src_path)

task_run_cmd = r'cmd.exe /c "cd {} && {}"'.format(task_dst_directory, run_src_path)



#-------List Directory-------#
# Input: Agent ID, Directory Full Path
# Outpout: Boolen - True (if Directory Exist), False (if Directory NOT Exist)
def list_dir(agentID, remote_directory):
    try:
        with cb.select(Sensor, agentID).lr_session() as lr_session:
            listed_directory = lr_session.list_directory(remote_directory)
            print("[INFO] [{}] Direcotry existed and its info: {}".format(agentID, listed_directory))
            return(True)
    except cbapi.errors.TimeoutError as  e:
        print("[ERROR] [{}] [list_dir] Timeout Error: {}".format(agentID, e))
    except cbapi.live_response_api.LiveResponseError as e: 
        pass
        print("[INFO] [{}] Direcotry not existed: {}".format(agentID, e))
        return(False)

#-------Create Directory-------#
# Input: Agent ID, Directory Full Path
# Outpout: None
def create_dir(agentID, remote_directory):
    isDirectoryExist = list_dir(agentID, remote_directory)
    with cb.select(Sensor, agentID).lr_session() as lr_session:
        if isDirectoryExist == False:
            lr_session.create_directory(remote_directory)
            print("[INFO] [{}] Task folder created".format(agentID))
        if isDirectoryExist == True:
            print("[INFO] [{}] Task folder existed".format(agentID))

#-------Upload File-------#
# Input: Agent ID
# Outpout: None
# This function assumes it will upload 3 files: "run.bat", "Task.zip", "7za.exe" 
#def upload_file(agentID, local_file, remote_file):
def upload_file(agentID):
    try:
        with cb.select(Sensor, agentID).lr_session() as lr_session:
            lr_session.put_file(open(run_src_path, "rb"), run_dst_path)
            print("[INFO] [{}] run.bat Uploaded".format(agentID))
            lr_session.put_file(open(task_src_path, "rb"), task_dst_path)
            print("[INFO] [{}] Task.zip Uploaded".format(agentID))
            lr_session.put_file(open(sevenZ_src_path, "rb"), sevenZ_dst_path)
            print("[INFO] [{}] 7za.exe Uploaded".format(agentID))
    except cbapi.errors.TimeoutError as e:
        print("[ERROR] [{}] [upload_file] Timeout Error: {}".format(agentID, e))
        pass
    except cbapi.live_response_api.LiveResponseError as e:
        print("[ERROR] [{}] [upload_file] Live Response Error: {}".format(agentID, e))
    except Exception as e:
        print("[ERROR] [{}] [upload_file] General Exception: {}".format(agentID, e))

#-------Run .bat-------#
# Input: Agent ID
# Outpout: None
# The funciton assumes "run.bat" will handle all detailed commands
#def run_bat(agentID, local_file, remote_file):
def run_bat(agentID):
    try:
        with cb.select(Sensor, agentID).lr_session() as lr_session:
            lr_session.create_process(task_run_cmd, wait_for_output=False, wait_for_completion=False)
            print("[INFO] [{}] Task Executed".format(agentID))
    except cbapi.errors.TimeoutError as e:
        print("[ERROR] [{}] [run_bat] Timeout Error: {}".format(agentID, e))
        pass
    except cbapi.live_response_api.LiveResponseError as e:
        print("[ERROR] [{}] [run_bat] Live Response Error: {}".format(agentID, e))
    except Exception as e:
        print("[ERROR] [{}] [run_bat] General Exception: {}".format(agentID, e))

#-------Walk Directory-------#
# Input: Agent ID, Directory Full Path
# Outpout: Array of listed directory (inlcude subdirectories, and files)
def walk_dir(agentID, remote_directory):
    try:
        with cb.select(Sensor, agentID).lr_session() as lr_session:
            print("[INFO] [{}] Start listing files in DFIR_Task".format(agentID))
            walked_directory = lr_session.walk(remote_directory, topdown=False)
    except Exception as e:
        print("[ERROR] [{}] [walk_dir] Generel Exception: {}".format(agentID, e))

    walked_directory_list = []
    for path, subdir_names, file_names in walked_directory:
        for subdir in subdir_names:
            walked_directory_list.append("{}\\{}".format(path,subdir))
        for file in file_names:
            walked_directory_list.append("{}\\{}".format(path,file))
    
    return(walked_directory_list)

#-------Walk Directory-------#
# Input: Agent ID, Array of pathes
# Outpout: None
def clean_folder(agentID, remote_directory_list):
    try:
        with cb.select(Sensor, agentID).lr_session() as lr_session:
            print("[INFO] [{}] Start deleting files in DFIR_Task".format(agentID))
            for item in remote_directory_list:
                lr_session.delete_file(item)
            print("[INFO] [{}] Files in DFIR_Task folder are deleted".format(agentID))
    except Exception as e:
        print("[ERROR] [{}] [clean_folder] Generel Exception: {}".format(agentID, e))

#-------Get Output Files -------#
# Input: Agent ID
# Outpout: None
def get_output_files(agentID):
    remote_ouput_path = task_dst_directory + "\\output"
    try:
        with cb.select(Sensor, agentID).lr_session() as lr_session:
            print("[INFO] [{}] Listing files in DFIR_Task".format(agentID))
            walked_directory = lr_session.walk(remote_ouput_path, topdown=False)
            print(walked_directory)
    except Exception as e:
        print("[ERROR] [{}] [get_output_files] General Exception: {}".format(agentID, e))
    currant_path = os.getcwd()
    local_output_path = currant_path+"\\"+agentID
    if not os.path.isdir(local_output_path):
        os.mkdir(local_output_path)
    for remote_path, subdir_names, remote_file_names in walked_directory:
        for file in remote_file_names:
            file_to_download = remote_path+"\\"+file
            try:
                with cb.select(Sensor,agentID).lr_session() as lr_session:
                    print("[INFO] [{}] Downloading {}".format(agentID, file_to_download))
                    data = lr_session.get_file(file_to_download)
                    local_downlaod_file = local_output_path + "\\" + file
                    with open(local_downlaod_file, "wb") as fw:
                        fw.write(data)
                        print("[INFO] [{}] File is downlaoded {}".format(agentID, file_to_download))
            except Exception as e:
                print("[ERROR] [{}] [get_output_files] General Exception: {}".format(agentID, e))


def run_thread(agentID):

    if get_output:
        get_output_files(agentID)
    elif (clean_dfir_task):
        list_of_paths = walk_dir(agentID, task_dst_directory)
        clean_folder(agentID, list_of_paths)
    else:
        is_task_folder_exist = list_dir(agentID, task_dst_directory)
        if is_task_folder_exist == False:
            create_dir(agentID, task_dst_directory)
        else:
            list_of_paths = walk_dir(agentID, task_dst_directory)
            clean_folder(agentID, list_of_paths)
        upload_file(agentID)
        run_bat(agentID)

def main ():
    file = open(id_txt_file, 'r').read().splitlines()
    agentIDS = [row for row in file]

    if mulitThread_mode == True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=lr_threads) as executer:
            for agentID in agentIDS:
                executer.submit(run_thread, agentID)
    else:
        for agentID in agentIDS:
            run_thread(agentID)


if __name__ == "__main__":
    # Parse Arguments
    parser = argparse.ArgumentParser(description='CBTaskBulker - Run Multiple Tasks through Carbon Black')
    parser.add_argument('--get', action='store_true', help='Get files in output folder', default=False)
    parser.add_argument('--clean', action='store_true', help='Clean DFIR_Task folder', default=False)
    parser.add_argument('--ml', action='store_true', help='Enable Multi Thread mode', default=False)
    parser.add_argument('--threads', type=int, help='Number of threads to be used (Each thread will utilize a dedicated LR session)', default=2)
   
    args = parser.parse_args()

    # Assing Arguments
    mulitThread_mode = args.ml
    lr_threads = args.threads
    get_output = args.get
    clean_dfir_task = args.clean

    # start CBTaskBulker
    main()