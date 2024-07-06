import json
import os

class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_config()

    def load_config(self):
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_config(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def does_user_exist(self, user_id):
        return str(user_id) in self.data

    def add_user(self, user_id):
        user_id_str = str(user_id)
        if not self.does_user_exist(user_id):
            self.data[user_id_str] = {"courses": {}}
            self.save_config()

    def add_course_to_user(self, user_id, course_name):
        user_id_str = str(user_id)
        self.add_user(user_id)  # Ensures user exists
        if course_name not in self.data[user_id_str]['courses']:
            self.data[user_id_str]['courses'][course_name] = {"level": 1, "module": 1}
            self.save_config()

    def update_course_level(self, user_id, course_name, level):
        user_id_str = str(user_id)
        self.add_course_to_user(user_id, course_name)  # Ensures course exists
        self.data[user_id_str]['courses'][course_name]['level'] = level
        self.save_config()

    def update_course_module(self, user_id, course_name, module):
        user_id_str = str(user_id)
        self.add_course_to_user(user_id, course_name)  # Ensures course exists
        self.data[user_id_str]['courses'][course_name]['module'] = module
        self.save_config()

    def get_user_courses(self, user_id):
        user_id_str = str(user_id)
        if self.does_user_exist(user_id):
            return self.data[user_id_str]['courses']
        return {}