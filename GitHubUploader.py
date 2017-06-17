#!/usr/bin/python3
#!python3
#encoding:utf-8
import sys
import os.path
import subprocess
import configparser
import argparse
import web.service.github.api.v3.AuthenticationsCreator
import web.service.github.api.v3.AuthenticationData
#import web.service.github.api.v3.CurrentUser
import web.service.github.api.v3.CurrentRepository
import web.service.github.api.v3.Client
import database.src.Database
import cui.uploader.Main
import web.log.Log
import database.src.contributions.Main

class Main:
    def __init__(self):
        pass

    def Run(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-u', '--username')
        parser.add_argument('-d', '--description')
        parser.add_argument('-l', '--homepage', '--link', '--url')
#        parser.add_argument('-m', '--message')
        parser.add_argument('-m', '--messages', action='append')
        args = parser.parse_args()
#        print(args)
#        print('path_dir_pj: {0}'.format(args.path_dir_pj))
#        print('-u: {0}'.format(args.username))
#        print('-d: {0}'.format(args.description))
#        print('-l: {0}'.format(args.homepage))

        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
#        path_dir_db = os.path.abspath(config['Path']['DB'])
        # 相対パスなら
        if config['Path']['DB'].startswith('./'):
            # python起動パスでなく、このファイルをrootとする
            path_dir_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), config['Path']['DB'][2:])
        else:
            path_dir_db = os.path.abspath(config['Path']['DB'])
#        print(path_dir_db)
        web.log.Log.Log().Logger.debug(path_dir_db)
        
        if None is args.username:
            args.username = config['GitHub']['User']
#            print('default-username: {0}'.format(args.username))
#        print(os.path.join(path_dir_db, 'GitHub.Accounts.sqlite3'))
#        print(os.path.join(path_dir_db, 'GitHub.Repositories.{0}.sqlite3'.format(args.username)))
        
#        self.__db = database.src.Database.Database()
        self.__db = database.src.Database.Database(os.path.abspath(os.path.dirname(__file__)))
        self.__db.Initialize()
        
        if None is self.__db.Accounts['Accounts'].find_one(Username=args.username):
#            print('指定したユーザ {0} はDBに存在しません。GitHubUserRegister.pyで登録してください。')
            web.log.Log.Log().Logger.warning('指定したユーザ {0} はDBに存在しません。GitHubUserRegister.pyで登録してください。'.format(args.username))
            return
        
        # Contributionsバックアップ
        self.__UpdateAllUserContributions(path_dir_db)
#        self.__UpdateAllUserContributions(path_dir_db, username=args.username)
        
        # アップローダ起動
        creator = web.service.github.api.v3.AuthenticationsCreator.AuthenticationsCreator(self.__db, args.username)
        authentications = creator.Create()
#        user = web.service.github.api.v3.CurrentUser.CurrentUser(self.__db, args.username)
        repo = web.service.github.api.v3.CurrentRepository.CurrentRepository(self.__db, args.path_dir_pj, description=args.description, homepage=args.homepage)
        authData = web.service.github.api.v3.AuthenticationData.AuthenticationData()
        authData.Load(self.__db.Accounts, args.username)
        client = web.service.github.api.v3.Client.Client(self.__db, authentications, authData=authData, repo=repo)
#        main = cui.uploader.Main.Main(self.__db, client, authData, repo)
        main = cui.uploader.Main.Main(self.__db, client, authData, repo, args)
        main.Run()

    def __UpdateAllUserContributions(self, path_dir_db, username=None):
        m = database.src.contributions.Main.Main(path_dir_db)
        if None is not username:
            m.Run(username)
        else:
            for a in self.__db.Accounts['Accounts'].find():
                m.Run(a['Username'])


if __name__ == '__main__':
    main = Main()
    main.Run()
