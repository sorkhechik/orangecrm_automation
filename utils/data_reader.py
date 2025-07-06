import yaml

class DataReader:
    @staticmethod
    def load_yaml(file_path):
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file: {e}")

    @staticmethod
    def get_password_by_username(file_path, username):
        data = DataReader.load_yaml(file_path)
        for user in data["users"]:
            if user["username"] == username:
                return user["password"]
        raise ValueError(f"Username '{username}' not found in {file_path}")