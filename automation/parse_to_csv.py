import sys 
import csv 

if (len(sys.argv) != 2):
    print("Usage: python parse_to_csv.py <log_file>")
    sys.exit(1)


log_file = sys.argv[1]


def parse_log_to_csv():
    with open(log_file, 'r') as file:
        lines = file.readlines()
        
        with open('parsed_log.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['case_id', 'task_id', 'timestamp', 'resource', 'message'])
            
            for line in lines:
                line = line.strip().split(' - ')
                if (len(line) != 5):
                    continue
                timestamp = line[0]
                script_name = line[1]
                log_level = line[2]
                function_name = line[3]
                
                session_task_message = line[4].split(': ')
                
                task_id = session_task_message[0].split(' ')[0]
                session_id = session_task_message[0].split(' ')[1]
                
                if len(session_task_message) > 1:
                    message = session_task_message[1].strip()
                    csv_writer.writerow([session_id, task_id, timestamp, function_name, message])

                
    print('Done parsing log file')

if __name__ == '__main__':
    parse_log_to_csv()