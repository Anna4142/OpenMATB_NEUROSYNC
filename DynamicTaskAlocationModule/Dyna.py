# Assuming scenario_file_generator.py is in the same directory
from DynamicTaskAlocationModule.ConfigGenerator  import ScenarioFileGenerator
from DynamicTaskAlocationModule.DataSimulators.CogLoadSim import CognitiveLoadSimulator
from DynamicTaskAlocationModule.DataSimulators.TasksSim import TasksScheduleSim
from DynamicTaskAlocationModule.LoadBalancing.MaxMinFairness import MaxMinFairnessBalancer
from DynamicTaskAlocationModule.LoadBalancing.LeastConnections import LeastConnectionsBalancer

class TaskAllocationSystem:
    def __init__(self, n_users, n_tasks):
        self.cognitive_simulator = CognitiveLoadSimulator(n_people=n_users)
        self.tasks_simulator = TasksScheduleSim(n_tasks=n_tasks)
        self.users_info = self.cognitive_simulator.simulate_scores()
        self.tasks = self.tasks_simulator.generate_tasks()

    def run_least_connections_balancer(self):
        print("Testing Least Connections Balancer:")
        lc_balancer = LeastConnectionsBalancer(self.users_info, self.tasks)
        lc_balancer.allocate_tasks()
        print("Least Connections Assignments:", lc_balancer.get_assignments())
        self.generate_scenario_files(lc_balancer.get_assignments(), "least_connections")

    def run_max_min_fairness_balancer(self):
        print("\nTesting Max-Min Fairness Balancer:")
        mmf_balancer = MaxMinFairnessBalancer(self.users_info, self.tasks)
        mmf_balancer.allocate_tasks()
        print("Max-Min Fairness Assignments:", mmf_balancer.get_assignments())
        self.generate_scenario_files(mmf_balancer.get_assignments(), "max_min_fairness")

    def generate_scenario_files(self, assignments, balancer_type):
        task_assignments = {}
        for task, user in assignments:
            if user not in task_assignments:
                task_assignments[user] = []
            task_assignments[user].append((task, task.lower().replace(" ", "_")))
        generator = ScenarioFileGenerator(task_assignments, f"./scenario_files/{balancer_type}/")
        generator.generate_scenario_files()

if __name__ == "__main__":
    task_system = TaskAllocationSystem(n_users=5, n_tasks=10)
    task_system.run_least_connections_balancer()
    task_system.run_max_min_fairness_balancer()
