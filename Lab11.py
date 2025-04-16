debug = False
import matplotlib.pyplot as mplot
import os
class Assignment():
    Instances = []
    def __init__(self, name, id, point_total):
        assert type(name) == str, "Assignment name must be a string"
        assert type(id) == int, "Assignment id must be a integer"
        assert type(point_total) == int, "Assignment point_total must be a integer"
        self.name = name
        self.id = id
        self.point_total = point_total
        self.student_scores = []
        Assignment.Instances.append(self)
    def get_name(self):
        return self.name
    def get_point_total(self):
        return self.point_total
    def get_id(self):
        return self.id
    def get_assignment_by_name(name : str):
        for instance in Assignment.Instances:
            if instance.get_name() == name:
                return instance
        return -1
    def get_assignment_by_id(id : int):
        for instance in Assignment.Instances:
            if instance.get_id() == id:
                return instance
        return -1
    def add_student_score(self, score : int):
        self.student_scores.append(score)
    def get_normalized_student_scores(self):
        temp_student_scores = self.student_scores.copy()
        temp_student_scores.sort()
        if debug:
            print(f"Sorted Student Scores for Assignment: {self.get_name()} are:\n {temp_student_scores}")
        return temp_student_scores
class Student():
    Instances = []
    def __init__(self, name, id):
        assert type(name) == str, "Student name must be a string"
        assert type(id) == int, "Student id must be a integer"
        self.name = name
        self.id = id
        self.grades = {}
        Student.Instances.append(self)
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_student_by_name(name):
        for instance in Student.Instances:
            if instance.get_name() == name:
                return instance
        return -1
    def get_student_by_id(id):
        for instance in Student.Instances:
            if instance.get_id() == id:
                return instance
        return -1
    def submit_assignment(self, assignment_id : int, points_earned : int):
        assignment_obj = Assignment.get_assignment_by_id(assignment_id)
        self.grades[assignment_obj.get_id()] = points_earned
        assignment_obj.student_scores.append(points_earned)
    def get_grade(self):
        total_points = 0
        total_assignments = 0
        for score in self.grades.values():
            total_points += score
            total_assignments += 1
            if debug:
                print(f"Currently getting {self.get_name()}'s grade. Total points: {total_points} over {total_assignments} assignments.")
        return (round((total_points / total_assignments)))

#Parsing!!! YAYYYY!!!
def parse_students():
    with open('data/students.txt', 'r') as student_file:
        for line in student_file:
            student_id = int(line[:3])
            student_name = line[3:-1]
            new_student = Student(student_name, student_id)
            if debug:
                print(f"New Student! Id: {student_id}, Name: {student_name}")
def parse_assignments():
    with open('data/assignments.txt', 'r') as assignment_file:
        while True:
            assignment_name = assignment_file.readline()[:-1]
            if assignment_name == "":
                break
            assignment_id = int(assignment_file.readline())
            assignment_point_total = int(assignment_file.readline())
            new_assignment = Assignment(assignment_name, assignment_id, assignment_point_total)
            if debug:
                print(f"New Assignment! Id: {assignment_id}, Name: {assignment_name}, Point Total: {assignment_point_total}")
def parse_submissions():
    file_submissions = os.listdir('data/submissions')
    for submission_file_name in file_submissions:
        with open(f"data/submissions/{submission_file_name}", "r") as submission_file:
            raw_data = (submission_file.readline()).split('|')
            student_id = int(raw_data[0])
            assignment_id = int(raw_data[1])
            points_earned = int(raw_data[2])
            selected_student = Student.get_student_by_id(student_id)
            selected_student.submit_assignment(assignment_id, points_earned)
            if debug:
                print(f"New submission added! Student Id: {student_id}, Assignment Id: {assignment_id}, Points Earned: {points_earned}")
parse_students()
parse_assignments()
parse_submissions()
#Now we should have all of the backbone to design the menu.
def option_1(student_name):
    if Student.get_student_by_name(student_name) == -1:
        print("Student not found")
        return
    student_obj = Student.get_student_by_name(student_name)
    print(f"{student_obj.get_grade()}%")
def option_2(assignment_name):
    if Assignment.get_assignment_by_name(assignment_name) == -1:
        print("Assignment not found")
        return
    assignment_obj = Assignment.get_assignment_by_name(assignment_name)
    assignment_scores = assignment_obj.get_normalized_student_scores()
    greatest_score = 0
    lowest_score = 100
    total_points_scored = 0
    total_scores = 0
    for assignment_score in assignment_scores:
        if assignment_score > greatest_score:
            greatest_score = assignment_score
        if assignment_score < lowest_score:
            lowest_score = assignment_score
        total_points_scored += assignment_score
        total_scores += 1
    avg_score = round(total_points_scored / total_scores)
    if debug:
        print(f"Generated assignment statistics for {assignment_name}!")
        print(f"Assignment Scores: {assignment_scores}")
    print(f"Min: {lowest_score}%\n"
          f"Avg: {avg_score}%\n"
          f"Max: {greatest_score}%")
def option_3(assignment_name):
    if Assignment.get_assignment_by_name(assignment_name) == -1:
        print("Assignment not found")
    assignment_obj = Assignment.get_assignment_by_name(assignment_name)
    assignment_scores = assignment_obj.get_normalized_student_scores()
    mplot.hist(assignment_scores, bins = [0, 25, 50, 75, 100], label = f"{assignment_name} Score Distribution")
    mplot.show()
if debug:
    option_1("Michael Potter")
    option_2("Quiz 1")
    option_3("Quiz 1")
while True:
    print("""1. Student grade
2. Assignment statistics
3. Assignment graph
""")
    user_input = input("Enter your selection: ")
    if user_input == "0":
        exit()
    if user_input == "1":
        selected_student = input("What is the student's name: ")
        option_1(selected_student)
    if user_input == "2":
        selected_assignment = input("What is the assignment name: ")
        option_2(selected_assignment)
    if user_input == "3":
        selected_assignment = input("What is the assignment name: ")
        option_3(selected_assignment)