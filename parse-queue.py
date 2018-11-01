import fileinput
from query import query, influxString
from parse import parse

makeCounts = query(
  ['account', 'partition', 'state'], 
  lambda _: True,
  lambda val, entry: { 
    'cpus': val['cpus'] + entry['cpus'], 
    'nodes': len(set(entry['reason'].split(',')).union(val['reasons'])),
    'reasons': set(entry['reason'].split(',')).union(val['reasons'])  
  }, 
  lambda: { 'cpus': 0, 'nodes': 0, 'reasons': [] })
counts = makeCounts(map(parse, fileinput.input()))
for count in counts:
  print(influxString('queue', count, ['reasons']))
