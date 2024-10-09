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
            csv_writer.writerow(['session_id', 'action', 'timestamp'])
            
            for line in lines:
                line = line.strip().split(' - ')
                
                timestamp = line[0]
                script_name = line[1]
                log_level = line[2]
                function_name = line[3]
                
                session_message = line[4].split(':')
                session_id = session_message[0]
                action = session_message[1].strip()
                
                # csv_writer.writerow([session_id, action, timestamp])
                
    print('Done parsing log file')

if __name__ == '__main__':
    parse_log_to_csv()