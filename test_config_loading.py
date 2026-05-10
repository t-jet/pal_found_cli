import yaml
import sys
from pathlib import Path

config_dir = Path('.ept/tracker/.config')
workflow_file = config_dir / '.workflow.yaml'

try:
    # Load main workflow
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)
    print(f'✓ Loaded main workflow file')
    
    # Resolve ticket type refs (mimicking config.py logic)
    ticket_types_raw = workflow.get('ticket_types', [])
    resolved = []
    
    for i, item in enumerate(ticket_types_raw):
        if not isinstance(item, dict):
            print(f'Warning: ticket_types[{i}] is not a dict')
            continue
            
        ref_path = item.get('$ref')
        if ref_path is not None:
            abs_path = config_dir / ref_path
            print(f'Loading {abs_path.name}...', end=' ')
            try:
                with open(abs_path, 'r', encoding='utf-8') as fh:
                    loaded = yaml.safe_load(fh)
                print('✓')
                resolved.append(loaded)
            except Exception as exc:
                print(f'✗ Error: {exc}')
                sys.exit(1)
        else:
            resolved.append(item)
    
    print(f'\n✓ Successfully loaded {len(resolved)} ticket types')
    
except Exception as e:
    print(f'\n✗ Fatal error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
