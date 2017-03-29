class TaskWorker:

        def task_update_name(**kwargs):
            print("I will update a name!")
            for k, v in kwargs.items():
                print("{0} = {1}".format(k, v))
