import random

class TasksScheduleSim:
    def __init__(self, n_tasks=10):
        self.n_tasks = n_tasks
        self.task_types = [
            {'id': 'System Monitoring', 'required_load': 2},
            {'id': 'Tracking', 'required_load': 1},
            {'id': 'Communications', 'required_load': 2},
            {'id': 'Resource Management', 'required_load': 1}
        ]

    def generate_tasks(self):
        tasks = []
        for _ in range(self.n_tasks):
            task_choice = random.choice(self.task_types)  # Randomly select one of the task types
            # Copy the task choice to ensure unique task entries if needed
            task = task_choice.copy()
            tasks.append(task)
        return tasks
