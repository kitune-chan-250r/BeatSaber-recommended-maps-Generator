from multiprocessing import Pipe,Process


def mainproc(arg):
    for i in range(0, 5):
        print("main_proc " + str(i))
    return arg

def subproc(arg, pipe):
    for i in range(0, 5):
        print("sub_proc " + str(i))
        pipe.send(arg)
    return True #7

if __name__ == '__main__':
    
    main_to_sub,sub_to_main = Pipe() 
    username = "neko"
    pr = Process(target=subproc, args=(username, sub_to_main))
    pr.start()
    mainres = mainproc(5)
    result = main_to_sub.recv()
    pr.join()

    

    print(result)
    print(mainres)
