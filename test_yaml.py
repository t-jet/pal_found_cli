import yaml
import sys

try:
    with open('.ept/tracker/.config/.workflow.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print('✓ Main workflow file parses successfully')
    print(f'Found {len(data.get("ticket_types", []))} ticket type references')
except Exception as e:
    print(f'✗ Error: {e}')
    sys.exit(1)
