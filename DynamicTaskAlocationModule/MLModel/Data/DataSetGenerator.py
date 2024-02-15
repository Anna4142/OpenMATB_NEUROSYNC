import numpy as np
import pandas as pd


def generate_dataset(num_rows=40000):
    # Task names encoded as integers for simplicity
    # Encoding: System Monitoring=0, Tracking=1, Communications=2, Resources Management=3
    tasks_encoded = np.random.randint(0, 4, num_rows)

    # Cognitive score randomly assigned between 0, 1, 2
    cognitive_scores = np.random.randint(0, 3, num_rows)

    # Time completion randomly assigned in multiples of 0.5, from 0 to 3 hours (converted to minutes)
    time_completion = np.random.choice(np.arange(0, 3.5, 0.5), num_rows)
    # Assignment column with labels that are 0, 1, or 2
    assignments = np.random.randint(0, 3, num_rows)

    # Creating the DataFrame
    generated_dataset = pd.DataFrame({
        'Task': tasks_encoded,
        'Cognitive_Score': cognitive_scores,
        'Time_Completion_Minutes': time_completion,
        'Assignment':assignments
    })

    return generated_dataset


def save_dataset_as_csv(dataset, filename='C:/Users/anush/OneDrive/study/BEN ENGLEHARD LAB/courses/technion courses/year 2 semester one/AI AND ROBOTICS/OpenMATB_NEUROSYNC/Data/generated_dataset_dyna_2.csv'):
    dataset.to_csv(filename, index=False)
    print(f"Dataset saved as {filename}")


if __name__ == "__main__":
    # Generate dataset
    dataset = generate_dataset()

    # Display the first few rows of the dataset
    print(dataset.head())

    # Save the dataset to a CSV file
    save_dataset_as_csv(dataset)
