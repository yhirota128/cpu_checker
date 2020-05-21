from multiprocessing import Process
import subprocess
import time
from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render


# ただカウントダウンする処理
def count(num):
    while num > 0:
        num -= 1


# テスト用スレッド
class TestThread(Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num

    def run(self):
        count(self.num)


def index(request):
    # CPU情報の取得
    try:
        cpu_info = subprocess.check_output(['cat', '/proc/cpuinfo']).decode('utf-8')
    except Exception as e:
        return HttpResponse(e)

    n = 10000000

    # シングル
    single_start = time.time()
    count(int(n))
    single_end = time.time()

    # マルチプロセス
    mp_jobs = [
        Process(target=count, args=(int(n / 4),)),
        Process(target=count, args=(int(n / 4),)),
        Process(target=count, args=(int(n / 4),)),
        Process(target=count, args=(int(n / 4),)),
    ]
    mp_start = time.time()
    for j in mp_jobs:
        j.start()
    for j in mp_jobs:
        j.join()
    mp_end = time.time()

    # マルチスレッド
    mt_jobs = [
        TestThread(int(n / 4)),
        TestThread(int(n / 4)),
        TestThread(int(n / 4)),
        TestThread(int(n / 4)),
    ]
    mt_start = time.time()
    for j in mt_jobs:
        j.start()
    for j in mt_jobs:
        j.join()
    mt_end = time.time()

    context = {
        'cpu_info': cpu_info,
        'single_time': single_end - single_start,
        'mp_time': mp_end - mp_start,
        'mt_time': mt_end - mt_start,
    }
    return render(request, 'index.html', context)
