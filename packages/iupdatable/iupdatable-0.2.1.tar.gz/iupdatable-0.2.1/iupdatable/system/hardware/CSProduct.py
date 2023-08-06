import subprocess
from iupdatable.logging import Logger


class CSProduct(object):

    @staticmethod
    def get():
        try:
            completed = subprocess.run('wmic csproduct get /value', stdout=subprocess.PIPE, universal_newlines=True)
            output = str(completed.stdout).strip().replace('\n\n', '\n')
            items = output.split("\n")
            result = {}
            for item in items:
                key_value = item.split("=")
                result[key_value[0]] = key_value[1]
            return result
        except Exception as e:
            Logger.error(repr(e), is_with_debug_info=True)
            return None

    @staticmethod
    def get_caption():
        """
        获取 Caption 的值
        :return: 成功：返回 Caption 的值，如：Computer System Product； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["Caption"]
        else:
            return None

    @staticmethod
    def get_description():
        """
        获取 Description 的值
        :return: 成功：返回 Description 的值，如：Computer System Product； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["Description"]
        else:
            return None

    @staticmethod
    def get_identifying_number():
        """
        获取 IdentifyingNumber 的值
        :return: 成功：返回 IdentifyingNumber 的值，如：PDVC400012152042979202； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["IdentifyingNumber"]
        else:
            return None

    @staticmethod
    def get_name():
        """
        获取 Name 的值
        :return: 成功：返回 Name 的值，如：Veriton M4610G； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["Name"]
        else:
            return None

    @staticmethod
    def get_sku_number():
        """
        获取 SKUNumber 的值
        :return: 成功：返回 SKUNumber 的值，可能为空字符串； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["SKUNumber"]
        else:
            return None

    @staticmethod
    def get_uuid():
        """
        获取 UUID 的值
        :return: 成功：返回 UUID 的值，如：A2DC9CC8-30A8-1120-1228-222416000000； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["UUID"]
        else:
            return None

    @staticmethod
    def get_vendor():
        """
        获取 Vendor 的值
        :return: 成功：返回 Vendor 的值，如：Acer； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["Vendor"]
        else:
            return None

    @staticmethod
    def get_version():
        """
        获取 Version 的值
        :return: 成功：返回 Version 的值，默认可能为空； 失败：返回 None
        """
        cs_product = CSProduct.get()
        if cs_product:
            return cs_product["Version"]
        else:
            return None
