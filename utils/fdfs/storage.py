from django.core.files.storage import Storage
from fdfs_client.client import *
from django.conf import settings


class FDFSStorage(Storage):
    """fast_dfs文件存储类"""
    def __init__(self, base_url=None, client_conf=None):
        """
        初始化
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = get_tracker_conf(client_conf)

    def _open(self, name, mode='rb'):
        """打开文件时使用"""
        pass

    def _save(self, name, content):
        """保存文件时使用"""
        # name：选择上传文件的名字
        # content：包含上传文件内容的File对象
        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到fdfs_dfs系统中
        res = client.upload_by_buffer(content.read())
        # 返回一个dict
        # {
        #     'Group name'      : group_name,
        #     'Remote file_id'  : remote_file_id,
        #     'Status'          : 'Upload successed.',
        #     'Local file name' : '',
        #     'Uploaded size'   : upload_size,
        #     'Storage IP'      : storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast dfs失败')
        # 获取返回的文件ID
        b_filename = res.get('Remote file_id')
        filename = b_filename.decode()
        return filename

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        return self.base_url + name

    def exists(self, name):
        """Django判断文件是否可用"""
        return False
