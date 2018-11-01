def reformat(groups, results):
  output = []
  for key in results:
    fields = key.split('.')
    entry = {}
    for (field, group) in zip(fields, groups):
      entry[group] = field 
    output.append((entry, results[key]))
  return output

def query(groups, where, f, init = lambda: None):
  def run(data):
    results = {}
    for entry in data:
      if not where(entry):
        continue
      name = '.'.join([ entry[group].strip() for group in groups ])
      if name not in results:
        results[name] = init()
      results[name] = f(results[name], entry) 
    return reformat(groups, results)
  return run

def dictToString(dictObj, hidden):
  return ','.join([ str(key) + '=' + str(dictObj[key]) for key in dictObj if key not in hidden ])

def influxString(prefix, value, hidden = []):
  return prefix + ',' +  dictToString(value[0], hidden) + ' ' + dictToString(value[1], hidden) 
