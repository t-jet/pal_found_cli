import subprocess
import re

# Based on get_tickets.py
terminal_statuses = {'Closed', 'Canceled', 'Duplicated', 'Rejected'}

# First, get all active dev_story tickets
result = subprocess.run(['python', '.ept/skills/tracking-system/tracker/tracker_cli.py', 'list', '--type', 'dev_story'], capture_output=True, text=True)

tickets = []
for line in result.stdout.split('\n'):
    if line.startswith('DEV-STORY-'):
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= 5:
            ticket_id, status = parts[0], parts[1]
            if status not in terminal_statuses:
                tickets.append(ticket_id)

if not tickets:
    print("No active tickets found.")
else:
    print(f"Found {len(tickets)} active tickets. Fetching links for each...\n")
    print(f"{'Ticket ID':<15} | {'Link Type':<15} | {'Target ID':<15} | {'Comment'}")
    print("-" * 70)

    for ticket_id in tickets:
        # List links for the ticket
        link_result = subprocess.run(['python', '.ept/skills/tracking-system/tracker/tracker_cli.py', 'link', 'list', ticket_id], capture_output=True, text=True)
        
        # The output format of 'link list' is not explicitly known, but let's assume it's something we can parse.
        # Based on the help, it lists links. Let's see what it looks like first by running it for one ticket if possible, 
        # but for now let's try to parse common patterns or just print the output.
        
        if link_result.stdout.strip():
            # Let's try to parse the output. If it's a table, we might need more logic.
            # For now, let's just print the raw output if it's not empty, or try to find "Blocks"
            lines = link_result.stdout.strip().split('\n')
            for line in lines:
                if "Blocks" in line:
                    # Try to extract parts. This is a guess.
                    # Example line might be: LINK-001 DEV-STORY-001 DEV-STORY-002 Blocks "Comment"
                    # Or it might be a table.
                    print(f"{ticket_id:<15} | {line}")
                elif "Blocks" not in line and len(line.strip()) > 0:
                    # If it's not a "Blocks" link, we might still want to see it if the user wants "all links"
                    # The user said: "List all links for all non-terminal tickets to identify any 'Blocks' relationships."
                    # So I should list ALL links.
                    print(f"{ticket_id:<15} | {line}")

