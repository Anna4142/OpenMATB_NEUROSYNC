from DynamicTaskAlocationModule.LoadBalancing.LoadBalancer import LoadBalancer
from DynamicTaskAlocationModule.LoadBalancing.MaxMinFairness import MaxMinFairnessBalancer
from DynamicTaskAlocationModule.LoadBalancing.LeastConnections import LeastConnectionsBalancer
users_info = [
    {'id': 'user1', 'cognitive_score': 2},
    {'id': 'user2', 'cognitive_score': 1}
]

tasks = [
    {'id': 'System Monitoring', 'required_load': 2},
    {'id': 'Tracking', 'required_load': 1},
    {'id': 'Communications', 'required_load': 2},
    {'id': 'Resource Management', 'required_load': 1}
]

# Test Least Connections Balancer
print("Testing Least Connections Balancer:")
lc_balancer = LeastConnectionsBalancer(users_info, tasks)
lc_balancer.allocate_tasks()
print("Least Connections Assignments:", lc_balancer.get_assignments())

# Test Max-Min Fairness Balancer
print("\nTesting Max-Min Fairness Balancer:")
mmf_balancer = MaxMinFairnessBalancer(users_info, tasks)
mmf_balancer.allocate_tasks()
print("Max-Min Fairness Assignments:", mmf_balancer.get_assignments())
