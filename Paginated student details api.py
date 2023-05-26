import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load student details from a CSV file
def load_student_details():
    with open('student_details.csv', 'r') as file:
        reader = csv.DictReader(file)
        student_details = list(reader)
    return student_details

# Paginate student details based on page number and page size
def paginate_student_details(student_details, page_number, page_size):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    paginated_data = student_details[start_index:end_index]
    return paginated_data

# Filter student details based on criteria
def filter_student_details(student_details, filter_criteria):
    filtered_data = []
    for student in student_details:
        if filter_criteria.get('id') and student['id'] != filter_criteria['id']:
            continue
        if filter_criteria.get('name') and student['name'] != filter_criteria['name']:
            continue
        if filter_criteria.get('total_marks') and student['total_marks'] != filter_criteria['total_marks']:
            continue
        filtered_data.append(student)
    return filtered_data

# Load Student Details API
@app.route('/students', methods=['GET'])
def get_student_details():
    student_details = load_student_details()

    page_number = int(request.args.get('page_number', 1))
    page_size = int(request.args.get('page_size', 10))

    paginated_data = paginate_student_details(student_details, page_number, page_size)
    return jsonify(paginated_data)

# Server-side Filtering API
@app.route('/students/filter', methods=['POST'])
def filter_student():
    student_details = load_student_details()

    filter_criteria = request.json
    filtered_data = filter_student_details(student_details, filter_criteria)
    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run()