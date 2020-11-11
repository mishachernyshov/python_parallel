import numpy as np
import time
import requests
from concurrent.futures import ThreadPoolExecutor as tpe
from concurrent.futures import ProcessPoolExecutor as ppe
import multiprocessing
import threading
import matplotlib.pyplot as plt


urls = ['http://youngdeveloper.com.ua/img/cpp_logo.png',
        'http://www.pngmart.com/files/7/Python-PNG-File.png',
        'https://logos-download.com/wp-content/uploads/2016/10/Java_logo_icon.png'] * 20


def get_time_execution(function, *args):
    start = time.time()
    function(*args)
    return time.time() - start


def evaluateFuncEfficiency(func, times, *args):
    efficiency = float('inf')
    current_eff = None
    for k in range(times):
        current_eff = get_time_execution(func, *args)
        if current_eff < efficiency:
            efficiency = current_eff
    return efficiency


def save_image(url):
    res = requests.get(url)
    binary = res.content

    with open('photo' + str(np.random.randint(9999)) +
              '.png', 'wb') as f:
        f.write(binary)


def sequential_image_saving(collection):
    for k in collection:
        save_image(k)


def concThPoolSaveIm(thread_num, collection):
    with tpe(thread_num) as executor:
        executor.map(save_image, collection)


def concPrPoolSaveIm(thread_num, collection):
    with ppe(thread_num) as executor:
        executor.map(save_image, collection)


def concPrMultiProcPoolSaveIm(thread_num, collection):
    with multiprocessing.Pool(thread_num) as p:
        p.map(save_image, collection)


def oneThreadSavingIm(collection, count, start_value):
    for k in range(start_value, start_value + count):
        save_image(collection[k])


def generalParallelSaveIm(parallelism_instrument,
        parallel_func, thread_num, collection):
    col_length = len(collection)
    if col_length <= thread_num:
        appointed_thread_count = col_length
        thread_coefficients = [1] * col_length
    else:
        appointed_thread_count = thread_num
        thread_coefficients = \
            [col_length // thread_num] * thread_num
        for k in range(col_length % thread_num):
            thread_coefficients[k] += 1
    current_start_value = 0

    threads = []

    for k in range(appointed_thread_count):
        current_thread = multiprocessing.Process(target=
            parallel_func, args=
            (collection, thread_coefficients[k], current_start_value))
        current_start_value += thread_coefficients[k]
        threads.append(current_thread)
        current_thread.start()

    for k in range(appointed_thread_count):
        threads[k].join()


def thThreadingSaveIm(thread_num, collection):
    generalParallelSaveIm(threading.Thread, oneThreadSavingIm,
        thread_num, collection)


def procMultiProcSaveIm(thread_num, collection):
    generalParallelSaveIm(multiprocessing.Process, oneThreadSavingIm,
        thread_num, collection)


def funcEfficiencyResult(func, repeat_count, collection):
    cpu_count = multiprocessing.cpu_count()
    efficiency_results = [0] * cpu_count
    for k in range(1, cpu_count + 1):
        efficiency_results[k - 1] = \
            evaluateFuncEfficiency(func, repeat_count, k, collection)
    return efficiency_results


def funcEfficiencyVisualization(effic_list, tools_name):
    cpu_count = list(range(1, multiprocessing.cpu_count() + 1))

    for k in range(len(effic_list)):
        plt.plot(cpu_count, effic_list[k], label=tools_name[k])
    plt.xlabel('Кількість потоків/процесів')
    plt.ylabel('Час виконання')
    plt.title('Продуктивність засобів паралелізму')
    plt.legend()
    plt.show()


def bestResVisualization(effic_list, tools_name):
    plt.barh(tools_name, effic_list, color='#57b41e', align='center')
    plt.tight_layout()
    plt.title('Порівняння ефективності функцій')
    plt.xlabel('Найкращий час')
    plt.ylabel('Засіб паралелізму')
    plt.gcf().set_size_inches(8, 7)
    plt.show()


def printStatistics(effic_list, tools_name):
    for k in range(len(effic_list)):
        print(tools_name[k] + ':')
        for i, effic in enumerate(effic_list[k]):
            print('\t' + str(i + 1) + ' потока(-ів)/процеса(-ів): ' +
                  str(effic) + ' c')


if __name__ == '__main__':
    repeat_count = 7
    functions_list = [concThPoolSaveIm, concPrPoolSaveIm,
        concPrMultiProcPoolSaveIm, thThreadingSaveIm, procMultiProcSaveIm]
    functions_descriptions = ['concurrent.futures.ThreadPoolExecutor',
        'concurrent.futures.ProcessPoolExecutor',
        'multiprocessing.Pool', 'threading.Thread', 'multiprocessing.Process']
    functions_efficiency = []

    for k in functions_list:
        functions_efficiency.append(list(
            map(lambda eff: round(eff, 4),
                funcEfficiencyResult(concThPoolSaveIm, repeat_count, urls))))

    printStatistics(functions_efficiency, functions_descriptions)
    funcEfficiencyVisualization(functions_efficiency, functions_descriptions)

    the_most_efficient_time = list(map(min, functions_efficiency))
    the_most_efficient_time.append(round(
        evaluateFuncEfficiency(sequential_image_saving, repeat_count, urls), 4))
    functions_descriptions.append('Послідовне виконання')
    bestResVisualization(the_most_efficient_time, functions_descriptions)

    print(functions_descriptions[-1] + ': ' + str(the_most_efficient_time[-1]) + ' c')
    print('Найефективніший засіб паралелізму: ' +
          functions_descriptions[the_most_efficient_time.index(min(the_most_efficient_time))])
