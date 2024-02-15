from DynamicTaskAlocationModule.LoadBalancing.LoadBalancer import LoadBalancer


class MaxMinFairnessBalancer(LoadBalancer):
    def allocate_tasks(self):
        # Initialize or reset the assignments
        self.assignments = []

        # Sort tasks by required_load to prioritize assigning heavier tasks first
        sorted_tasks = sorted(self.tasks, key=lambda x: x['required_load'], reverse=True)

        # Keep track of total cognitive load assigned to each user
        user_loads = {user['id']: 0 for user in self.users}

        for task in sorted_tasks:
            # Filter users who can take the task based on cognitive score matching
            possible_users = [user for user in self.users if user['cognitive_score'] == task['required_load']]

            if not possible_users:
                continue  # If no users match the task requirement, skip the task

            # Among the possible users, find the one with the minimum total assigned cognitive load
            min_load_user = min(possible_users, key=lambda x: user_loads[x['id']])

            # Assign the task to this user
            self.assignments.append((task['id'], min_load_user['id']))

            # Update the total cognitive load assigned to the chosen user
            user_loads[min_load_user['id']] += task['required_load']

    def get_assignments(self):
        return self.assignments
