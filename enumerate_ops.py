import os, re

base = r'e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\customer_input\foundry-platform-python\foundry_sdk\v2'
results = []
for ns in sorted(os.listdir(base)):
    ns_path = os.path.join(base, ns)
    if not os.path.isdir(ns_path) or ns.startswith('_'):
        continue
    for fname in sorted(os.listdir(ns_path)):
        if not fname.endswith('.py') or fname.startswith('_') or fname in ('models.py', 'errors.py'):
            continue
        className = fname[:-3]
        fpath = os.path.join(ns_path, fname)
        content = open(fpath).read()
        methods = re.findall(r'^    def ([a-z][a-z0-9_]+)\(', content, re.MULTILINE)
        for m in methods:
            results.append(f'{ns}.{className}.{m}')

seen = set()
unique = []
for r in sorted(results):
    if r not in seen:
        seen.add(r)
        unique.append(r)

for r in unique:
    print(r)

print(f"\nTotal: {len(unique)} operations")
