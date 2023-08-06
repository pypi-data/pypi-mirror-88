import os
import sys
import inspect


class Directory(object):

    @staticmethod
    def get_current_directory() -> str:
        """"
        获取程序的当前路径
        :return:
        成功：当前程序的完整路径，如：d:\test
        失败：返回空字符串
        """
        try:
            # determine if application is a script file or frozen exe
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                frame = inspect.stack()[1]
                module = inspect.getmodule(frame[0])
                filename = module.__file__
                application_path = os.path.dirname(filename)
            return application_path
        except Exception as e:
            print('get_current_directory Exception:')
            print(repr(e))
            return ""

    @staticmethod
    def get_files(directory_name: str, is_include_dir=False) -> []:
        """
        返回指定目录中的文件名（包括它们的路径）,是否包含子目录可选。
        :param directory_name: 完整的文件夹路径，如：d:\test
        :param is_include_dir: 是否包含子目录，默认不包含
        :return: 成功：返回文件名集合，失败：返回空的数组
        """
        try:
            full_path_list = []
            file_names = os.listdir(directory_name)
            file_names.sort()
            for file_name in file_names:
                full_path = os.path.join(directory_name, file_name)
                if os.path.isdir(full_path):
                    if is_include_dir:
                        full_path_list.append(full_path)
                else:
                    full_path_list.append(full_path)
            return full_path_list
        except Exception as e:
            print('get_files Exception:')
            print(repr(e))
            return []
