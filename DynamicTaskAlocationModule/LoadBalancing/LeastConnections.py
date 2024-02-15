from DynamicTaskAlocationModule.LoadBalancing.LoadBalancer import LoadBalancer
class LeastConnectionsBalancer(LoadBalancer):
    def allocate_tasks(self):
        user_task_counts = {user['id']: 0 for user in self.users}  # Initialize task counts

        for task in self.tasks:
            possible_users = [user for user in self.users if user['cognitive_score'] == task['required_load']]
            if not possible_users:
                continue  # Skip if no matching user

            # Find the user with the least number of tasks
            least_loaded_user = min(possible_users, key=lambda x: user_task_counts[x['id']])
            self.assignments.append((task['id'], least_loaded_user['id']))
            user_task_counts[least_loaded_user['id']] += 1
