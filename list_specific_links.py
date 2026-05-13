import subprocess

def list_links_for_tickets(ticket_ids):
    print(f"{'Ticket ID':<15} | {'Link ID':<12} | {'Source':<15} | {'Target':<15} | {'Type':<15} | {'Role'}")
    print("-" * 90)

    for ticket_id in ticket_ids:
        # List links for the ticket
        result = subprocess.run(['python', '.ept/skills/tracking-system/tracker/tracker_cli.py', 'link', 'list', ticket_id], capture_output=True, text=True)
        
        if not result.stdout.strip():
            continue

        lines = result.stdout.strip().split('\n')
        # Skip the header lines
        # Found X link(s) for ...
        # ====================================================================================================
        # Link ID         Source             Target          Type            Role
        # ----------------------------------------------------------------------------------------------------
        
        found_links = False
        for line in lines:
            if line.startswith('LINK-'):
                found_links = True
                # Example line: LINK-00007      FEATURE-001     -> EPIC-005        FeatureContains (Feature Contains)
                # We need to parse this.
                parts = line.split()
                if len(parts) >= 5:
                    link_id = parts[0]
                    source = parts[1]
                    # The target might be after '->'
                    # Let's find the index of '->'
                    try:
                        arrow_index = parts.index('->')
                        target = parts[arrow_index + 1]
                        # The rest is Type and Role
                        # Type might be multiple words if it's not just one word before the parenthesis
                        # But based on the example: FeatureContains (Feature Contains)
                        # parts[arrow_index + 2] is Type
                        # parts[arrow_index + 3:] is Role
                        link_type = parts[arrow_index + 2]
                        role = " ".join(parts[arrow_index + 3:])
                        
                        print(f"{ticket_id:<15} | {link_id:<12} | {source:<15} | {target:<15} | {link_type:<15} | {role}")
                    except (ValueError, IndexError):
                        # Fallback if parsing fails
                        print(f"{ticket_id:<15} | {line}")
            elif found_links and not line.startswith('---') and not line.startswith('Link ID'):
                # This might be a continuation or something else, but let's stick to LINK- lines for now
                pass

if __name__ == "__main__":
    tickets = [
        "EPIC-005", "EPIC-006", "EPIC-007", "EPIC-008", 
        "DEV-STORY-001", "DEV-STORY-002", "DEV-STORY-003", "DEV-STORY-004", 
        "DEV-STORY-005", "DEV-STORY-006", "DEV-STORY-007", "DEV-STORY-008", 
        "DEV-STORY-009", "DEV-STORY-010", "DEV-STORY-011", "DEV-STORY-012", 
        "DEV-STORY-013", "DEV-STORY-014", "DEV-STORY-015", "DEV-STORY-016", 
        "DEV-STORY-017", "DEV-STORY-018", "DEV-STORY-019", "DEV-STORY-020", 
        "DEV-STORY-021", "DEV-STORY-022", "DEV-STORY-023"
    ]
    list_links_for_tickets(tickets)
