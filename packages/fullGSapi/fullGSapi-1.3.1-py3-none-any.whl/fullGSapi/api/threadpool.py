from queue import Queue

from threading import Thread

class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks, stay_alive):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.stay_alive = stay_alive
        self.start()

    def run(self):
        while self.stay_alive[0] or not self.tasks.empty():
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        self.workers = []
        self.stay_alive = [True]
        for _ in range(num_threads):
            self.workers.append(Worker(self.tasks, self.stay_alive))

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()

    def wait_completion_and_destroy(self):
        self.stay_alive.insert(0, False)
        self.wait_completion()

        
            