from fabric.api import local

def host_type():
    local('dir')
    # запуск на удаленной машине
    # run('uname -s')

def hello():
    print("Hello world!")