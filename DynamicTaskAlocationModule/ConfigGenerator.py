import os

class ScenarioFileGenerator:
    def __init__(self, task_assignments, output_directory="senarios/"):
        """
        Initializes the scenario file generator.

        :param task_assignments: A dictionary with user IDs as keys and a list of tuples (task_name, task_alias) as values.
        :param output_directory: The directory where the scenario files will be saved.
        """
        self.task_assignments = task_assignments
        self.output_directory = output_directory
        # Ensure the output directory exists
        os.makedirs(self.output_directory, exist_ok=True)

    def generate_scenario_files(self):
        """
        Generates scenario files for each user based on their task assignments.
        """
        scenario_template = """# Scenario for {user_id} - {task_name} Task
# This file is configured to run the {task_name} task for 3 minutes

# 1. Set tasks parameters
# 1.a. {task_name} parameters

# 2. Start tasks that will be used
0:00:00;{task_alias};start

# 3. Set scenario events
# 3.a. {task_name} events

# 4. Stop tasks
0:03:00;{task_alias};stop
"""

        for user_id, tasks in self.task_assignments.items():
            for task_name, task_alias in tasks:
                scenario_content = scenario_template.format(user_id=user_id, task_name=task_name, task_alias=task_alias)
                file_path = os.path.join(self.output_directory, f"{user_id}_{task_alias}_scenario.txt")
                with open(file_path, "w") as file:
                    file.write(scenario_content)
                print(f"Scenario file generated for {user_id}: {file_path}")


