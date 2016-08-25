import re
import urllib

asset_url = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
asset_filename = re.compile('([^/\\&\?]+\.\w{3,4}(?=([\?&].*$|$)))')

def clean_line(line):
  url_matches = re.finditer(asset_url, line)
  return_obj = { 'files': [] }
  for url_match in url_matches:
    url = url_match.group(1)
    filename_match = asset_filename.search(url)
    if filename_match:
      filename = filename_match.group(1)
      line = line.replace(url, './assets/' + filename)
      return_obj['files'].append({
        'filename': filename,
        'url': url
      })
      urllib.urlretrieve(url, './assets/' + filename)
  return_obj['line'] = line
  if len(return_obj['files']) > 0:
    print return_obj['files']
  return return_obj

css_files = []
with open('raw_index.html', 'r') as raw_file:
  with open('index.html', 'w') as clean_file:
    for line in raw_file:
      cleaned_obj = clean_line(line)
      cleaned_line = cleaned_obj['line']
      clean_file.write(cleaned_line)
      

