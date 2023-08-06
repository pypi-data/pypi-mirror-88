import os
import json


class Config:
	def __init__(self, directory, filename):
		self.__directory = directory
		self.__filename = filename
		self.__path = os.path.join(directory, filename)

		if not os.path.exists(directory):
			os.makedirs(directory)

	def __get_config_file(self):
		if not os.path.exists(self.__path):
			open(self.__path, "w").close()

		f = open(self.__path, "r+")
		data = f.read()

		try:
			json.loads(data)
		except ValueError:
			f.seek(0)
			f.truncate(0)
			f.write("{}")

		f.seek(0)

		return f

	def get(self, key):
		f = self.__get_config_file()
		data = json.loads(f.read())
		f.close()

		return data[key] if key in data else ""

	def set(self, key, value):
		f = self.__get_config_file()
		data = json.loads(f.read())
		f.seek(0)
		f.truncate(0)

		data[key] = value

		f.write(json.dumps(data, indent=4, sort_keys=True))
		f.close()

	def wipe(self):
		f = self.__get_config_file()
		f.seek(0)
		f.truncate(0)
		f.close()

	def delete(self):
		os.remove(self.__path)

	def get_keys(self):
		f = self.__get_config_file()
		data = json.loads(f.read())
		f.close()

		return list(data.keys())
