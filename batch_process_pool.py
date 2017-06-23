from concurrent.futures import ProcessPoolExecutor
from time import sleep

def do_something(*args):
    sleep(1)
    print('Input:', args)


def main():
    with ProcessPoolExecutor(max_workers=4) as exe:
        for i in range(10):
            print('------------------------')
            cont = True
            x = [i]
            if not cont:
                break
            if x:
                exe.submit(do_something, *x)
            else:
                sleep(0.1)

            #break
        exe.shutdown(wait=True)

if __name__ == '__main__':
    main()
