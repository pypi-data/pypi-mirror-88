# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '2.0.0-rc1'
major           = '2'
minor           = '0'
patch           = '0-rc1'
rc              = '0'
istaged         = True
commit          = 'd82d59e6e731a3de4057249239c90b81360a0e01'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
