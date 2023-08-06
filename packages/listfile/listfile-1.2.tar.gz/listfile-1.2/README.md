# listfile
ListPath class for simply dealing with a list of Path objects

### Run a test with ./listfile.py
    
Test for a mixed bag of directories and files
The result should be a flattened list. Note that (empty) the directory `notebooks` will be generated.

    % xin = [['.',['..'],'a b',['.','demo.ipynb',['notebooks/demo.ipynb']]],'hello']
    % xout = ListPath(xin)
    
    % print(f'{xin} ->\n {xout}')
    [['.', ['..'], 'a b', ['.', 'demo.ipynb', ['notebooks/demo.ipynb']]], 'hello'] ->
    [PosixPath('/Users/plewis/Documents/GitHub/listfile'), PosixPath('/Users/plewis/Documents/GitHub'), PosixPath('/Users/plewis/Documents/GitHub/listfile/a b'), PosixPath('/Users/plewis/Documents/GitHub/listfile'), PosixPath('/Users/plewis/Documents/GitHub/listfile/demo.ipynb'), PosixPath('/Users/plewis/Documents/GitHub/listfile/notebooks/demo.ipynb'), PosixPath('/Users/plewis/Documents/GitHub/listfile/hello')]
    
    % xout.report()
    info: read  : [ True  True False  True False False False]
    info: write : [ True  True  True  True  True  True  True]
    info: isdir : [ True  True False  True False False False]
    info: isfile: [False False  True False  True  True  True]
    info: exists: [ True  True False  True False False False]

Give it a string. We want this maintained as
a string, not split into chars (as with normal list)

    % xin = 'hello world'
    % xout = ListPath(xin)
    % print(f'{xin} -> {xout}')
    hello world -> [PosixPath('/Users/plewis/Documents/GitHub/listfile/hello world')]
    
    % xout.report()
    info: read  : [False]
    info: write : [ True]
    info: isdir : [False]
    info: isfile: [ True]
    info: exists: [False]

Remove duplicates test
    
    % xin = ['hello world',['.','./hello world'],'.']
    % xout = ListPath(xin,unique=True)
    % print(f'{xin} ->\n {xout}')
    ['hello world', ['.', './hello world'], '.'] ->
    [PosixPath('/Users/plewis/Documents/GitHub/listfile'), PosixPath('/Users/plewis/Documents/GitHub/listfile/hello world')]
    
    % xout.report()
    info: read  : [ True False]
    info: write : [ True  True]
    info: isdir : [ True False]
    info: isfile: [False  True]
    info: exists: [ True False]

Test write permission and use of name= kwarg

    % xin = ['/tmp','/doesnt exist/x']
    % xout = ListPath(xin,name='tester.dat')

    % print(f'{xin} ->\n {xout}')
    ['/tmp', '/doesnt exist/x'] ->
    [PosixPath('/private/tmp/tester.dat'), PosixPath('/doesnt exist/x')]

    % xout.report()
    info: read  : [False False]
    info: write : [ True False]
    info: isdir : [False False]
    info: isfile: [ True False]
    info: exists: [False False]

