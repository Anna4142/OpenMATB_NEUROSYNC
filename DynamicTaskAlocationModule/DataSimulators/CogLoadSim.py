import numpy as np

class CognitiveLoadSimulator:
    def __init__(self, n_people=3, n_samples=10):
        self.n_people = n_people
        self.n_samples = n_samples

    def simulate_scores(self):
        users_info = []
        for i in range(self.n_people):
            scores = np.random.choice([0, 1, 2], self.n_samples)  # Simulate scores for each person
            avg_score = np.mean(scores)
            # Create a dictionary for each user with an ID and the rounded average cognitive score
            user_info = {
                'id': f'user{i + 1}',
                'cognitive_score': round(avg_score)
            }
            users_info.append(user_info)
        return users_info
