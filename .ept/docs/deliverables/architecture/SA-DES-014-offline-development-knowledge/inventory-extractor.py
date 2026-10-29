import ast, collections, hashlib, io, json, pathlib, re, subprocess, tarfile
repo=pathlib.Path('.ept/docs/customer_input/foundry-platform-python')
dest=pathlib.Path('.ept/docs/deliverables/architecture/SA-DES-014-offline-development-knowledge/sdk-inventory')
dest.mkdir(parents=True, exist_ok=True)
summaries={}
for tag in ('1.79.0','1.101.0'):
    archive=subprocess.check_output(['git','-C',str(repo),'archive',tag])
    with tarfile.open(fileobj=io.BytesIO(archive)) as t:
        files={m.name:t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    ops=[]; services=collections.defaultdict(list); model_files={}; error_files={}; symbols={}; imports={}; source_trees={}
    for path,data in files.items():
        if not path.startswith('foundry_sdk/v') or not path.endswith('.py'):continue
        tree=ast.parse(data);source_trees[path]=tree
        module=path[:-3].replace('/','.')
        imports[module]={}
        for node in tree.body:
            if isinstance(node,ast.ImportFrom):
                for item in node.names:imports[module][item.asname or item.name]=(node.module or '')+'.'+item.name
            if path.endswith(('/models.py','/errors.py')) or '/models/' in path or '/errors/' in path:
                names=[node.name] if isinstance(node,ast.ClassDef) else [t.id for t in node.targets if isinstance(t,ast.Name)] if isinstance(node,ast.Assign) else [node.target.id] if isinstance(node,ast.AnnAssign) and isinstance(node.target,ast.Name) else []
                for name in names:
                    if not name.startswith('_'):symbols[module+'.'+name]=(module,node,path)
    def refs(node,module):
        out=set()
        for n in ast.walk(node):
            candidate=None
            if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name): candidate=imports[module].get(n.value.id,'')+'.'+n.attr
            elif isinstance(n,ast.Name):candidate=imports[module].get(n.id,module+'.'+n.id)
            elif isinstance(n,ast.Constant) and isinstance(n.value,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',n.value):candidate=module+'.'+n.value
            if candidate in symbols:out.add(candidate)
        return out
    edges={key:refs(node,module)-{key} for key,(module,node,path) in symbols.items()}
    for path,data in files.items():
        if not path.startswith('foundry_sdk/v') or not path.endswith('.py'): continue
        bits=path.split('/'); version,service=bits[1:3]
        if ('/models/' in path or path.endswith('/models.py')) and not path.endswith('__init__.py'): model_files[path]=hashlib.sha256(data).hexdigest()
        if ('/errors/' in path or path.endswith('/errors.py')) and not path.endswith('__init__.py'): error_files[path]=hashlib.sha256(data).hexdigest()
        if len(bits)!=4 or bits[-1].startswith('_') or bits[-1] in ('client.py','cli.py'): continue
        tree=ast.parse(data)
        for cls in tree.body:
            if not isinstance(cls,ast.ClassDef) or not cls.name.endswith('Client') or cls.name.startswith(('_','Async')):continue
            for method in cls.body:
                if not isinstance(method,ast.FunctionDef) or method.name.startswith('_'):continue
                requests=[n for n in ast.walk(method) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='RequestInfo']
                if not requests:continue
                kv={k.arg:ast.literal_eval(k.value) for k in requests[0].keywords if k.arg in ('method','resource_path')}
                opid=f'{version}.{service}.{cls.name.removesuffix("Client")}.{method.name}'
                docpath=next((p for p in files if p.startswith(f'docs/{version}/') and p.endswith('/'+cls.name.removesuffix('Client')+'.md') and f'/{service.replace("_", "").lower()}/' in p.lower().replace('_','')),None)
                stage='UNRESOLVED'
                if docpath:
                    match=re.search(r'\[\*\*'+re.escape(method.name)+r'\*\*\][^\r\n]*?\|[^\r\n]*?\|\s*([^|\r\n]+)\s*\|',files[docpath].decode())
                    if match:stage=match.group(1).strip()
                args=ast.unparse(method.args)
                seeds=set()
                for related in ast.walk(tree):
                    if isinstance(related,(ast.FunctionDef,ast.AsyncFunctionDef)) and related.name==method.name:seeds.update(refs(related,path[:-3].replace('/','.')))
                closure=set(seeds);pending=list(seeds)
                while pending:
                    for dependency in edges[pending.pop()]-closure:closure.add(dependency);pending.append(dependency)
                record={'id':opid,'http':kv,'stage':stage,'signature':args,'returns':ast.unparse(method.returns) if method.returns else None,'source':path,'source_sha256':hashlib.sha256(data).hexdigest(),'docs':docpath,'doc_sha256':hashlib.sha256(files[docpath]).hexdigest() if docpath else None,'contract_symbol_seeds':sorted(seeds),'transitive_contract_symbols':sorted(closure)}
                ops.append(record);services[f'{version}.{service}'].append(record)
    target=dest/tag;target.mkdir(exist_ok=True)
    for key,rows in sorted(services.items()):
        (target/(key+'.jsonl')).write_text('\n'.join(json.dumps(r,sort_keys=True) for r in sorted(rows,key=lambda r:r['id']))+'\n',encoding='utf-8')
    symbolrows=[{'id':key,'source':path,'source_sha256':hashlib.sha256(files[path]).hexdigest(),'definition_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest(),'dependencies':sorted(edges[key])} for key,(module,node,path) in sorted(symbols.items())]
    for i in range(0,len(symbolrows),250):(target/f'contract-symbols-{i//250+1:02}.jsonl').write_text('\n'.join(json.dumps(r,sort_keys=True) for r in symbolrows[i:i+250])+'\n',encoding='utf-8')
    for label,records in [('models',model_files),('errors',error_files)]:
        rows=sorted(records.items())
        for i in range(0,len(rows),250):
            (target/f'{label}-{i//250+1:02}.tsv').write_text('source\tsha256\n'+'\n'.join(p+'\t'+h for p,h in rows[i:i+250])+'\n',encoding='utf-8')
    summaries[tag]={'commit':subprocess.check_output(['git','-C',str(repo),'rev-parse',tag+'^{commit}'],text=True).strip(),'operation_count':len(ops),'service_count':len(services),'resource_count':len(set('.'.join(r['id'].split('.')[:-1]) for r in ops)),'models_source_count':len(model_files),'errors_source_count':len(error_files),'stages':dict(collections.Counter(r['stage'] for r in ops)),'services':{k:len(v) for k,v in sorted(services.items())},'operation_ids_sha256':hashlib.sha256('\n'.join(sorted(r['id'] for r in ops)).encode()).hexdigest()}
    reachable=set().union(*(set(r['transitive_contract_symbols']) for r in ops))
    summaries[tag]['contract_symbols_defined']=len(symbols)
    summaries[tag]['contract_symbols_reachable']=len(reachable)
    summaries[tag]['reachable_models']=sum(x.rsplit('.',1)[0].endswith('.models') for x in reachable)
    summaries[tag]['reachable_error_symbols']=sum(x.rsplit('.',1)[0].endswith('.errors') for x in reachable)
    print(tag,json.dumps(summaries[tag],indent=2))
(dest/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n',encoding='utf-8')
