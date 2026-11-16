from pathlib import Path
import collections, csv, datetime, difflib, hashlib, io, json, os, re, subprocess, tarfile
import yaml

root = Path.cwd()
candidate = root / '.ept/tmp/feature015_parent_tracker_data'
out = root / '.ept/tmp/feature015_capture_independent_qa_20261116'
out.mkdir(exist_ok=True)
capture = root / '.ept/tmp/feature015_git_capture_20261116'
manifest_path = '.ept/docs/deliverables/qa/FEATURE-015-tracker-capture-2026-11-16.json'
manifest_bytes = (candidate / manifest_path).read_bytes()
m = json.loads(manifest_bytes)
checks = []
def check(name, condition, details=None):
    checks.append({'name': name, 'passed': bool(condition), 'details': details})
def git(repo, *args, env=None):
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)
def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def tree_map(repo, tree, prefix):
    rows = git(repo, 'ls-tree', '-rz', tree, '--', prefix).split(b'\0')
    return {r.split(b'\t',1)[1].decode(): r.split(b'\t',1)[0].decode().split()[2] for r in rows if r}
def tar_map(data, prefix='.ept/tracker/'):
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        return {p.name[len(prefix):]: t.extractfile(p).read() for p in t.getmembers() if p.isfile() and p.name.startswith(prefix)}
def rows(data): return list(csv.DictReader(io.StringIO(data.decode(), newline=None)))

# Git reads published source objects; only this private index is changed.
env = os.environ.copy()
env['GIT_INDEX_FILE'] = str(out / 'candidate.index')
head = git(candidate, 'rev-parse', 'HEAD').decode().strip()
git(candidate, 'read-tree', head, env=env)
git(candidate, 'add', '-A', '--', '.ept/tracker', manifest_path,
    '.ept/docs/legacy_codereview_002_unindexed.md', '.ept/tools/tracker', env=env)
candidate_tree = git(candidate, 'write-tree', env=env).decode().strip()
candidate_tracker_tree = git(candidate, 'rev-parse', candidate_tree+':.ept/tracker').decode().strip()
raw_tar = (capture / 'raw-tracker.tar').read_bytes()
raw = tar_map(raw_tar)
published = tar_map(git(candidate, 'archive', candidate_tree, '.ept/tracker'))
raw_objects = tree_map(root, m['raw_root_tree_before'], '.ept/tracker')
published_objects = tree_map(candidate, candidate_tree, '.ept/tracker')
check('candidate_parent', head == m['snapshot_parent_commit'])
check('capture_root_stability', m['raw_root_tree_before'] == m['raw_root_tree_after'])
check('raw_tracker_tree_binding', git(root, 'rev-parse', m['raw_root_tree_before']+':.ept/tracker').decode().strip() == m['raw_tracker_tree'])
check('raw_tar_hash', sha(raw_tar) == m['raw_export_tar_sha256'])
check('every_raw_tar_file_matches_git_object', {'.ept/tracker/'+p:blob(b) for p,b in raw.items()} == raw_objects)
check('every_candidate_export_matches_git_object', {'.ept/tracker/'+p:blob(b) for p,b in published.items()} == published_objects)
raw_hashes = {p:sha(b) for p,b in raw.items()}
pub_hashes = {p:sha(b) for p,b in published.items()}
check('raw_manifest_all_file_hashes', raw_hashes == m['raw_file_sha256'])
check('candidate_manifest_all_file_hashes', pub_hashes == m['capture_file_sha256'])
changed = sorted(p for p in raw.keys() & published.keys() if raw[p] != published[p])
missing, extra = sorted(raw.keys()-published.keys()), sorted(published.keys()-raw.keys())
check('only_reviewed_source_changes', changed == m['changed_source_paths'] == ['.config/.link-index.csv'] and missing == m['missing_source_paths'] == ['CODEREVIEW-002/ticket.md'] and extra == m['capture_only_paths'] == [])
check('file_and_comment_counts', len(raw) == m['source_files'] == 12627 and len(published) == m['capture_files'] == 12626 and sum('/comments/' in p for p in raw) == m['comments_source'] == 11542)
check('ticket_counts', sum(p.endswith('/ticket.md') for p in raw) == m['tickets_source'] == 1052 and sum(p.endswith('/ticket.md') for p in published) == m['active_ticket_files'] == 1051)
link = '.config/.link-index.csv'
base_bytes = git(candidate, 'show', head+':.ept/tracker/'+link)
base_links = {r['link_id']:r for r in rows(base_bytes)}
raw_links = rows(raw[link]); links = rows(published[link]); by_link = {r['link_id']:r for r in links}
repair = m['repair_baseline']
check('repair_hash_bindings', sha(base_bytes) == repair['link_index_sha256'] and sha(raw[link]) == repair['raw_link_index_sha256'] and sha(published[link]) == repair['repaired_link_index_sha256'])
check('six_reviewed_repairs_equal_baseline', all(by_link[k] == base_links[k] for k in ['LINK-01027','LINK-01028','LINK-01278','LINK-01612','LINK-01981','LINK-01982']))
check('lost_history_not_reconstructed', 'LINK-01279' not in by_link)
check('remapped_collision', any(r['link_id']=='LINK-01612' and r['source_ticket']=='FEATURE-015' and r['target_ticket']=='DEV-STORY-092' for r in raw_links) and by_link['LINK-01981']['source_ticket']=='FEATURE-015' and by_link['LINK-01981']['target_ticket']=='DEV-STORY-092')
check('six_repairs_only_semantic_changes', all(r == by_link[r['link_id']] for r in raw_links if re.fullmatch(r'LINK-\d{5}',r['link_id']) and r['link_id'] not in ['LINK-01027','LINK-01028','LINK-01278','LINK-01612','LINK-01982']))
fragments = sorted(r['link_id'] for r in raw_links if not re.fullmatch(r'LINK-\d{5}',r['link_id']))
check('removed_fragments_match_declaration', fragments == repair['removed_corrupt_fragment_ids'])
diff = ''.join(difflib.unified_diff(raw[link].decode().splitlines(True), published[link].decode().splitlines(True), fromfile='raw-export', tofile='repaired-capture'))
display_diff = io.StringIO(diff.replace('\n','\r\n'),newline=None).read()
check('embedded_repair_diff_matches_windows_text_serialization', display_diff == m['repair_diff_raw_to_capture'], 'Display diff went through Windows write_text and universal-newline read_text. Embedded diff is presentation evidence, not a byte-preserving patch; per-file SHA256 checks validate exact source bytes.')
archive_path = m['CODEREVIEW002']['historical_archive_path']
archive = git(candidate,'show',candidate_tree+':'+archive_path)
check('legacy_archive_exact_git_blob', archive == raw['CODEREVIEW-002/ticket.md'] == git(candidate,'show',head+':'+archive_path) and blob(archive) == m['CODEREVIEW002']['historical_root_archive_git_blob'] and sha(archive)==m['CODEREVIEW002']['historical_root_archive_sha256'])
check('canonical_nested_ticket_preserved', published['DEV-STORY-002/CODEREVIEW-002/ticket.md'] == raw['DEV-STORY-002/CODEREVIEW-002/ticket.md'])
for proof in m['CODEREVIEW002']['raw_paths']:
    check('CODE002_proof_'+proof['path'], raw_hashes[proof['path']]==proof['raw_sha256'] and pub_hashes.get(proof['path'])==proof['capture_sha256'] and blob(raw[proof['path']])==proof['raw_git_blob'])

index = rows(published['.config/.index.csv']); ids = [r['id'] for r in index]; idset = set(ids)
ticket_paths = {p for p in published if p.endswith('/ticket.md')}
check('unique_ticket_csv_ids', len(ids)==len(idset)==1051)
check('csv_paths_cover_all_active_ticket_files', {r['path']+'/ticket.md' for r in index}==ticket_paths)
fm = {p:yaml.safe_load(b.decode().split('---',2)[1]) for p,b in published.items() if p in ticket_paths}
check('csv_ticket_id_and_type_match', all(fm[r['path']+'/ticket.md']['id']==r['id'] and fm[r['path']+'/ticket.md']['type']==r['type'] for r in index))
status_drift = [{'id':r['id'],'csv':r['status'],'ticket':fm[r['path']+'/ticket.md']['status']} for r in index if r['status'] != fm[r['path']+'/ticket.md']['status']]
check('csv_statuses_match_canonical', not status_drift, status_drift)
check('parent_references_exist', all(not r['parent'] or r['parent'] in idset for r in index))
check('unique_well_formed_links', len(links)==len(by_link)==m['links_after_repair']==1589 and all(re.fullmatch(r'LINK-\d{5}',r['link_id']) and None not in r and all(v is not None for v in r.values()) for r in links))
check('link_endpoints_exist', all(r['source_ticket'] in idset and r['target_ticket'] in idset for r in links))
help_cmd = ['python','.ept/tools/tracker/tracker_cli.py','--help-toon']
help_result = subprocess.run(help_cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'help-toon.cli.txt').write_bytes(help_result.stdout)
check('current_CLI_config_read_succeeded',help_result.returncode==0,{'command':help_cmd,'exit_code':help_result.returncode,'stdout_sha256':sha(help_result.stdout)})
help_text = help_result.stdout.decode()
valid_link_types = re.search(r'values\[9\]: ([^\r\n]+)',help_text).group(1).split(',')
check('published_link_types_allowed_by_CLI',all(r['link_type'] in valid_link_types for r in links),valid_link_types)
check('published_types_and_statuses_allowed_by_CLI',all(re.search(r'^\s+'+re.escape(r['type'])+r'\[\d+\]: ([^\r\n]+)',help_text,re.M) and r['status'] in re.search(r'^\s+'+re.escape(r['type'])+r'\[\d+\]: ([^\r\n]+)',help_text,re.M).group(1).split(',') for r in index))
relation_counts = collections.Counter((r['source_ticket'],r['target_ticket'],r['link_type']) for r in links)
relation_duplicates = [{'relation':list(k),'count':v} for k,v in relation_counts.items() if v>1]
check('no_duplicate_link_relations',not relation_duplicates,relation_duplicates)
counter = yaml.safe_load(published['.config/.id-counters.yaml'])['counters']
maxima = {typ:max(int(r['id'].rsplit('-',1)[1]) for r in index if r['type']==typ) for typ in {r['type'] for r in index}}
maxima['link']=max(int(r['link_id'].rsplit('-',1)[1]) for r in links)
check('counters_at_least_all_published_ids', all(counter[k]>=v for k,v in maxima.items()), {'counters':counter,'maxima':maxima})
engine = m['engine_continuity']
eng_map = tree_map(candidate,candidate_tree,'.ept/tools/tracker')
check('engine_45_files_unchanged', len(eng_map)==45 and eng_map == tree_map(candidate,head,'.ept/tools/tracker') and git(candidate,'rev-parse',candidate_tree+':.ept/tools/tracker').decode().strip()==engine['tree'] and engine['new_test_run'] is False)
for key,text in m['cli'].items():
    check('CLI_binding_'+key, (capture/(key+'.cli.txt')).read_bytes().decode()==text)
cli_rows = [s for s in m['cli']['all-tickets'].splitlines() if re.match(r'^[A-Z][A-Z-]*-\d+\s',s)]
check('every_captured_CLI_status_matches_frozen_csv',len(cli_rows)==len(index) and all(any(re.match('^'+re.escape(r['id'])+r'\s+'+re.escape(r['status'])+r'\s+'+re.escape(r['priority'])+r'\s+',s) for s in cli_rows) for r in index))
check('CLI_count_matches_snapshot', 'Found 1051 ticket(s)' in m['cli']['all-tickets'])
check('post_capture_canonical_path_separate', 'post-capture' in m['post_capture_cli_observations']['scope'].lower() and 'DEV-STORY-002/CODEREVIEW-002' in m['post_capture_cli_observations']['CODEREVIEW-002'])
report = {'result':'PASS' if all(c['passed'] for c in checks) else 'FAIL', 'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope':'Frozen as-of source publication only. Later live workflow changes excluded. No new engine test result or feature acceptance.', 'candidate_parent':head,'candidate_root_tree':candidate_tree,'candidate_tracker_tree':candidate_tracker_tree,'raw_root_tree':m['raw_root_tree_before'],'raw_tracker_tree':m['raw_tracker_tree'],'manifest_sha256':sha(manifest_bytes),'manifest_git_blob':blob(manifest_bytes),'archive_git_blob':blob(archive),'raw_tar_sha256':sha(raw_tar),'observations':['Embedded repair diff preserves the capture author Windows text serialization, which adds blank presentation lines. It is not a byte-preserving executable patch. Exact source and candidate bytes were independently checked by Git blob IDs and SHA256 for every file.'],'checks':checks}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
print('CHECKS',len(checks),'FAILED',json.dumps([c for c in checks if not c['passed']],indent=2))
