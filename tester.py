import git
import os
import datetime

student_code_json = {
    "MyProgram.py" :
"""import random
clipboard = []
for x in range(0, 1000):
bottle = random.randint(1,6)
tries = 1
while bottle != 1:
    tries = tries + 1
    bottle = random.randint(1,6)
clipboard.append(tries)
print(clipboard)
print("The assignment is done!! I think!! :)")
""",
    "scratchpad.py" :
"""import random
print(random.randint(1,6))
print(12983712)
"""
}

class Work:

    def __init__(self):
        self.location = "/Users/mightychen/hackathon/repositories/"

    def create_repository(self, user_id, item_id):
        directory = self.location + str(user_id) + "/" + str(item_id)
        new_file = os.path.join(directory, 'META')
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                repo = git.Repo.init(directory)
                # TODO: initialize with student code or smth.
                f = open(new_file, 'w+')
                f.write(str(datetime.datetime.now()) + ",")
                f.write(str(user_id) + ",")
                f.write(str(item_id))
                f.close()
                repo.index.add([new_file])
                repo.index.commit("initial commit")
            else:
                print("A repository already exists!")
                return
        except:
            print("An error occurred.")
            return

    def create_snapshot(self, user_id, item_id, code_json):
        directory = self.location + str(user_id) + "/" + str(item_id)
        repo = git.Repo(directory)
        for file_name, file_content in code_json.items():
            if os.path.exists(directory + "/" + file_name):
                os.remove(directory + "/" + file_name)
            f = open(directory + "/" + file_name, 'w+')
            f.write(file_content)
            f.close()
            repo.index.add([file_name])
        repo.index.commit(str(user_id) + "-" + str(item_id) + "-" + str(datetime.datetime.now()))

    def get_latest_code(self, user_id, item_id):
        directory = self.location + str(user_id) + "/" + str(item_id)
        repo = git.Repo(directory)

        student_code_json = {}
        for file, file_data in repo.index.entries.items():
            blob = git.Blob(repo, binsha=file_data[1])
            student_code_json[file[0]] = blob.data_stream.read().decode('ascii')

        return student_code_json

def main():
    w = Work()
    # open the repository for the first time.
    user_id = 1021579
    item_id = 30
    w.create_repository(user_id, item_id)

    # student compiles the code/autosave/...
    w.create_snapshot(user_id, item_id, student_code_json)

    # recent_student_code = w.get_latest_code(user_id, item_id)
    # print(recent_student_code['MyProgram.py'])


if __name__ == "__main__":
    main()
