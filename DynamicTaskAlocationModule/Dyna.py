from DynamicTaskAlocationModule.DataSimulators.CogLoadSim import CognitiveLoadSimulator
from DynamicTaskAlocationModule.DataSimulators.TasksSim import TasksScheduleSim
from DynamicTaskAlocationModule.LoadBalancing.MaxMinFairness import MaxMinFairnessBalancer
from DynamicTaskAlocationModule.LoadBalancing.LeastConnections import LeastConnectionsBalancer


class TaskAllocationSystem:
    def __init__(self, n_users, n_tasks):
        # Initialize the cognitive load simulator and tasks schedule simulator
        self.cognitive_simulator = CognitiveLoadSimulator(n_people=n_users)
        self.tasks_simulator = TasksScheduleSim(n_tasks=n_tasks)

        # Generate users and tasks
        self.users_info = self.cognitive_simulator.simulate_scores()
        self.tasks = self.tasks_simulator.generate_tasks()

    def run_least_connections_balancer(self):
        # Apply Least Connections Balancer
        print("Testing Least Connections Balancer:")
        lc_balancer = LeastConnectionsBalancer(self.users_info, self.tasks)
        lc_balancer.allocate_tasks()
        print("Least Connections Assignments:", lc_balancer.get_assignments())

    def run_max_min_fairness_balancer(self):
        # Apply Max-Min Fairness Balancer
        print("\nTesting Max-Min Fairness Balancer:")
        mmf_balancer = MaxMinFairnessBalancer(self.users_info, self.tasks)
        mmf_balancer.allocate_tasks()
        print("Max-Min Fairness Assignments:", mmf_balancer.get_assignments())

if __name__ == "__main__":
    task_system = TaskAllocationSystem(n_users=5, n_tasks=10)
    task_system.run_least_connections_balancer()
    task_system.run_max_min_fairness_balancer()
