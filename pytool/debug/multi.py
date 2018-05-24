import multiprocessing
from time import sleep

semaphore = multiprocessing.Semaphore(2)

def do_job(id):
    print("start job")
    with semaphore:
        sleep(1)
    print("Finished job")

def main():
    pool = multiprocessing.Pool(6)
    for job_id in range(6):
        print("Starting job")
        pool.apply_async(do_job, [job_id])
    print("test")
    pool.close()
    print("test1")
    pool.join()
    print("test2")

if __name__ == "__main__":
    main()