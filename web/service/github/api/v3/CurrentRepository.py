#!python3
#encoding:utf-8
import os.path
import web.log.Log
class CurrentRepository(object):
    def __init__(self, db, path, **params):
        self.__db = db
        self.__path = None
        self.__name = None
        self.Path = path
        self.__description = None
        self.__homepage = None
        web.log.Log.Log().Logger.debug(params)
        if None is not params:
            if 'description' in params.keys():
                self.__description = params['description']
            if 'homepage' in params.keys():
                self.__homepage = params['homepage']

    @property
    def Path(self):
        return self.__path
    @Path.setter
    def Path(self, value):
        if os.path.isdir(value):
            self.__path = value
            if value.endswith('/'):
                value = os.path.basename(value[:-1])
            self.__name = os.path.basename(value)

    @property
    def Name(self):
        return self.__name

    @property
    def Description(self):
        return self.__description

    @property
    def Homepage(self):
        return self.__homepage

    # 将来的には拡張する
    # * リモートリポジトリの状態(private,has_wiki)を変更する
    # * GitHubサーバとの連動(Sync()メソッドでAPIから取得しDBを更新する)
