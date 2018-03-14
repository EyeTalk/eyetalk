import numpy as np
from queue import deque


class EyeStateManager:
    SAMPLES_AVERAGED = 6
    BLINK_THRESHOLD = 3
    CHANGE_THRESHOLD = 3

    def __init__(self, choose_label_callback=np.argmax):
        self.sample_queue = deque(maxlen=self.SAMPLES_AVERAGED)
        self.last_id = -1
        
        self.blink_count = 0
        
        self.selected_label = None
        
        self.current_label = None
        self.current_label_count = 0
        
        self.choose_label_callback = choose_label_callback

        self.selection_made = False
        self.new_gazed_button = False
        
    def handle_input(self, detection_id, blink, probabilities):
        
        if detection_id != self.last_id:
            if blink:
                self.blink_count += 1

            else:
                self.selection_made = False
                self.new_gazed_button = False

                if self.blink_count >= self.BLINK_THRESHOLD:
                    self.selection_made = True
                    self.blink_count = 0
                    return

                self.blink_count = 0

                self.sample_queue.appendleft(probabilities)
                average_probabilities = self.calculate_average_probabilites()

                label = self.choose_label_callback(average_probabilities)

                if label == self.current_label:
                    self.current_label_count += 1
                    if self.current_label_count == self.CHANGE_THRESHOLD:
                        self.selected_label = self.current_label
                        self.new_gazed_button = True

                else:
                    self.current_label = label
                    self.current_label_count = 1

            self.last_id = detection_id
            
    def calculate_average_probabilites(self):
        all_data = np.concatenate(tuple(self.sample_queue), axis=0)
        return np.average(all_data, 0)

    def get_label(self):
        return self.selected_label
