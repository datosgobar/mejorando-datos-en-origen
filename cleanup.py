#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

metas = """
  <meta property="og:url" content="https://gobabiertoar.github.io/mediaparty2016/#/">
  <meta property="og:type" content="article">
  <meta property="og:title" content="Mejorando los datos en origen">
  <meta property="og:site_name" content="Dirección Nacional de Datos e Información Pública">
  <meta property="og:description" content="Presentación de la Dirección Nacional de Datos e Información Pública sobre el proyecto de modernización del sistema de gestión de audiencias publicas de interes del poder ejecutivo nacional.">
  <meta property="og:image" content="https://gobabiertoar.github.io/mejorando_datos_en_origen/assets/card.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1980">
  <meta property="og:image:height" content="1080">
  <meta property="og:locale" content="es_AR">

  <meta name="twitter:card" content="summary">
  <meta name="twitter:site" content="@datosgobar"/>
  <meta name="twitter:title" content="Mejorando los datos en origen">
  <meta name="twitter:description" content="Presentación de la Dirección Nacional de Datos e Información Pública sobre el proyecto de modernización del sistema de gestión de audiencias publicas de interes del poder ejecutivo nacional.">
  <meta name="twitter:image:src" content="https://gobabiertoar.github.io/mejorando_datos_en_origen/assets/card.png">
"""
favicon = '<link rel="shortcut icon" href="./assets/favicon.ico"/>'

title = '<title>Mejorando los datos en origen</title>'

with open('raw_index.html', 'r') as raw_file:
  with open('index.html', 'w') as clean_file:
    for line in raw_file:
      cleaned_obj = clean_line(line)
      cleaned_line = cleaned_obj['line']
      if '<title>' in cleaned_line:
        cleaned_line = title
      elif '</head>' in cleaned_line:
        cleaned_line = metas + '\n' + favicon + '\n' + cleaned_line
      clean_file.write(cleaned_line)
