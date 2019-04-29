import ScoreSaber
from functools import wraps
import time
from tqdm import tqdm
from multiprocessing import Pipe,Process


def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        process_time =  time.time() - start
        print(f"{func.__name__}は{process_time}秒かかりました")
        return result
    return wrapper

def no_multiprocess():
    my_userid,my_rank = ScoreSaber.srch_usr_name("fox100")
    aboveusr_id = ScoreSaber.get_ranker(my_rank-1)

    my_songdata = ScoreSaber.all_song_data(my_userid)
    aboveusr_songdata = ScoreSaber.all_song_data(aboveusr_id)

    pp_gap = ScoreSaber.compare_song_pp(my_songdata, aboveusr_songdata)
    f = "finished"
    return f,  pp_gap[0]



def multiprocessed():
    main_to_sub,sub_to_main = Pipe() #通信用パイプ生成
    my_userid,my_rank = ScoreSaber.srch_usr_name("fox100")
    aboveusr_id = ScoreSaber.get_ranker(my_rank-1)

    def sub_proc(abov_id,pipe):#サブプロセス化する関数
        aboveusr_songdata = ScoreSaber.all_song_data(abov_id)
        pipe.send(aboveusr_songdata)
        return True
    pr = Process(target=sub_proc, args=(aboveusr_id, sub_to_main))
    pr.start()
    my_songdata = ScoreSaber.all_song_data(my_userid)
    aboveusr_songdata = main_to_sub.recv()
    pr.join()

    pp_gap = ScoreSaber.compare_song_pp(my_songdata, aboveusr_songdata)
    f = "finished"
    return f,  pp_gap[0]

if __name__ == '__main__':
    print(multiprocessed())

