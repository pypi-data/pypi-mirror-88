from api.model.ResultVO import *
import threading
from libs.utils import stop_thread
from schedule import TaskThread

class SyncTaskExecutor():
    """
    同步任务执行器（暂时不需要了，当时是为了celery停任务准备的，celery有revoke功能不需要外部干预）
    """

    def __init__(self):
        self.__sync_task_thread_cache = list()

    def run_sync(self, task_thread:TaskThread, task_param):
        """
        同步执行
        :param task_thread:
        :param task_param:
        :return:
        """
        try:
            thread = self.__SyncTaskThread(task_thread, task_param)
            self.__sync_task_thread_cache.append(thread)
            thread.start()
            thread.join()  #等待线程结束
            self.__sync_task_thread_cache.remove(thread)
            return thread.execute_result
        except Exception as e:
            return ResultVO(FAIL_CODE, str(e))

    def stop_job(self, job_id):
        """
        停止任务（kill线程）
        :param job_id:
        :return:
        """
        for i in range(len(self.__sync_task_thread_cache)-1, -1, -1):
            thread = self.__sync_task_thread_cache[i]
            if thread.job_id == job_id:
                self.__sync_task_thread_cache.remove(thread)
                stop_thread(thread)

    def stop_task(self, job_id, task_id):
        """
        停止任务（kill线程）
        :param job_id:
        :param task_id:
        :return:
        """
        for i in range(len(self.__sync_task_thread_cache)-1, -1, -1):
            thread = self.__sync_task_thread_cache[i]
            if thread.job_id == job_id and thread.task_id == task_id:
                self.__sync_task_thread_cache.remove(thread)
                stop_thread(thread)


    class __SyncTaskThread(threading.Thread):
        """
        同步执行任务的线程
        """

        def __init__(self, task_thread, task_param):
            """
            同步执行器线程的构造函数
            :param task_thread: TaskThread
            :param task_param:
            """
            threading.Thread.__init__(self, name="同步任务线程")
            self.task_thread = task_thread
            self.task_param = task_param
            self.job_id = task_param.jobId
            self.task_id = task_param.logId
            self.execute_result = None

        def run(self):
            self.execute_result = self.task_thread.run_sync(self.task_param)