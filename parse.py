def parseFields(fields, output):
  """ Take a string of fields encoded as
  key1=value1,key2=value2,...
  and add the keys and values to the output dict"""
  for field in fields.split('|'):
    key, value = field.split('=')
    try:
      value = int(value)
    except:
      pass
    output[key] = value
  return output

def parse(line):
  output = {}
  parseFields(line, output)
  return output
