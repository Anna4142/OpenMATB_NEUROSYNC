# Copyright 2023, by Julien Cegarra & Benoît Valéry. All rights reserved.
# Institut National Universitaire Champollion (Albi, France).
# License : CeCILL, version 2.1 (see the LICENSE file)

from time import strftime, gmtime
from core.widgets import Timeline, Schedule, Simpletext
from plugins.abstract import AbstractPlugin
from core.constants import COLORS as C
from core.container import Container
from core import validation


class Scheduling(AbstractPlugin):
    def __init__(self, taskplacement='topright', taskupdatetime=1000):
        super().__init__(taskplacement, taskupdatetime)

        # Initialize additional attributes for task scores and person scores
        self.task_scores = {'sysmon': 2, 'track': 1, 'resman': 2, 'communications': 1}  # Example scores
        self.person_score = 0  # Initial person score, could be dynamic based on performance

        self.validation_dict = {
            'minduration': validation.is_positive_integer,
            'displaychronometer': validation.is_boolean,
            'reversechronometer': validation.is_boolean,
            'displayedplugins': (validation.is_in_list, ['sysmon', 'track', 'resman', 'communications'])
        }

        # Update initialization with task scores
        self.parameters.update(dict(
            minduration=8,
            displaychronometer=True,
            reversechronometer=False,
            displayedplugins=['sysmon', 'track', 'communications', 'resman']
        ))

        # Iterate over displayedplugins to set localization if needed
        for i, p in enumerate(self.parameters['displayedplugins']):
            self.parameters['displayedplugins'][i] = _(self.parameters['displayedplugins'][i])

        # Adjusting self.planning to include task scores for decision making
        self.planning = {p: {'running': list(), 'manual': list(), 'score': self.task_scores[p]}
                         for p in self.parameters['displayedplugins']}

        self.colors = dict(line=C['GREY'], running=C['RED'], manual=C['GREEN'])
        self.maximum_time_sec = None

        # Other initial setup as before...

    # Method to update person's score, this can be dynamically called based on performance
    def update_person_score(self, new_score):
        self.person_score = new_score
        self.reassess_task_assignments()

    def reassess_task_assignments(self):
        """
        Reassess task assignments and automation based on the current person score.
        If a person's score is below a threshold, some tasks could be automated to reduce load.
        """
        for task_name, details in self.planning.items():
            task_score = details['score']

            # Example logic for task automation based on person's score
            if self.person_score + task_score > 3:  # Threshold example
                # This task should be automated due to high cumulative score
                self.automate_task(task_name)
            else:
                # Assign the task to the person
                self.assign_task_to_person(task_name)

    def automate_task(self, task_name):
        """
        Automate the specified task by setting its automation flag.
        """
        if task_name in self.parameters['tasks']:
            # Set the 'automaticsolver' flag for the specified task to True
            self.parameters['tasks'][task_name]['automaticsolver'] = True
            print(f"Automating task {task_name} due to high load.")
        else:
            print(f"Task {task_name} not found.")

    def assign_task_to_person(self, task_name):
        """
        Assign the specified task to the person for manual handling.
        """
        # Example: Indicate that the task is to be handled manually
        print(f"Assigning task {task_name} to person for manual handling.")
        # Adjust task settings to ensure it's set for manual handling if needed
    def get_elapsed_time_sec(self):
        return int(self.scenario_time)


    def get_elapsed_time_string(self):
        str_time = strftime('%H:%M:%S', gmtime(self.get_elapsed_time_sec()))
        return _('Elapsed time \t %s') % str_time


    def get_remaining_time_sec(self):
        return int(self.maximum_time_sec) - int(self.scenario_time)


    def get_remaining_time_string(self):
        str_time = strftime('%H:%M:%S', gmtime(self.get_remaining_time_sec()))
        return _('Remaining time \t %s') % str_time


    def set_planning(self, events):  # Executed by the scheduler

        start_stop_labels = ['start', 'stop', 'resume', 'pause']
        auto_labels = ['automaticsolver']

        # Retrieve last event time_sec for reversed chronometer
        self.maximum_time_sec = events[-1].time_sec

        start_time_sec = [e.time_sec for e in events if e.plugin == 'scheduling'
                         if 'start' in e.command[0]][0]

        # For each task...
        for task in self.planning.keys():
            # 1. ...compute running segments
            start_stop_events = [(e.time_sec, e.command[0]) for e in events if e.plugin == task
                           and e.command[0] in start_stop_labels]
            for event in start_stop_events:
                self.planning[task]['running'].append(event[0])
            if len(self.planning[task]['running']) % 2 == 1:
                del(self.planning[task]['running'][-1])

            # 2. ...compute manual segments
            auto_events = [(e.time_sec, e.command[1]) for e in events if e.plugin == task
                           and e.command[0] in auto_labels]

            # If some automation events are specified, compute manual segments accordingly
            if len(auto_events) > 0:
                while auto_events[0][1] is False:  # Be sure to begin with an (automaticsolver, True)
                    del(auto_events[0])

                stop_time = [e[0] for e in start_stop_events if e[1] == 'stop'][0]
                start_time = [e[0] for e in start_stop_events if e[1] == 'start'][0]

                self.planning[task]['manual'].append(start_time)
                for ae in auto_events:
                    self.planning[task]['manual'].append(ae[0])
                if len(self.planning[task]['manual']) % 2 == 1:
                    self.planning[task]['manual'].append(stop_time)

            # Else, running segments are all manual segments
            else:
                self.planning[task]['manual'] = self.planning[task]['running']