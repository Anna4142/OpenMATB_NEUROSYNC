class LoadBalancer:
    def __init__(self, users_info, tasks):
        self.users = users_info  # [{'id': 'user1', 'cognitive_score': 2}, ...]
        self.tasks = tasks  # [{'id': 'task1', 'required_load': 2}, ...]
        self.assignments = []  # To store task assignments

    def match_task(self, task):
        # Find a user with a matching cognitive score for the task
        for user in self.users:
            if user['cognitive_score'] == task['required_load']:
                return user['id']
        return None

    def allocate_tasks(self):
        # This method will be overridden in derived classes to implement specific algorithms
        raise NotImplementedError("This method should be overridden in derived classes")

    def get_assignments(self):
        return self.assignments
