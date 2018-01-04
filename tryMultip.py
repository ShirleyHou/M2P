import multiprocessing


def func(n):
    for i in range(10000):
        for j in range(10000):
            s = j * i
    print(n)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    pool.map(func, range(10))
    pool.close()
    pool.join()
    print('done')
