import subprocess
import re
from datetime import datetime

priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
terminal_statuses = {'Closed', 'Canceled', 'Duplicated', 'Rejected'}

result = subprocess.run(['python', '.ept/skills/tracking-system/tracker/tracker_cli.py', 'list', '--type', 'dev_story'], capture_output=True, text=True)

tickets = []
for line in result.stdout.split('\n'):
    if line.startswith('DEV-STORY-'):
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= 5:
            ticket_id, status, priority, assignee, title = parts[0], parts[1], parts[2], parts[3], parts[4]
            if status not in terminal_statuses:
                detail_result = subprocess.run(['python', '.ept/skills/tracking-system/tracker/tracker_cli.py', 'get', ticket_id], capture_output=True, text=True)
                created = None
                for detail_line in detail_result.stdout.split('\n'):
                    if detail_line.startswith('created'):
                        created = detail_line.split(':', 1)[1].strip()
                        break
                tickets.append({'id': ticket_id, 'title': title, 'status': status, 'priority': priority, 'assignee': assignee, 'created': created, 'priority_order': priority_order.get(priority, 999), 'created_dt': datetime.fromisoformat(created) if created else datetime.max})

tickets.sort(key=lambda x: (x['priority_order'], x['created_dt']))

print('\n' + '='*150)
print('{:<15} {:<60} {:<12} {:<10} {:<15} {:<12}'.format('ID', 'Title', 'Status', 'Priority', 'Assignee', 'Created'))
print('='*150)

for t in tickets:
    print('{:<15} {:<60} {:<12} {:<10} {:<15} {:<12}'.format(t['id'], t['title'], t['status'], t['priority'], t['assignee'], t['created']))

print('='*150)
print('\nTotal active dev_story tickets: {}'.format(len(tickets)))
