#!/bin/bash

# Diretório onde os arquivos SVG estão localizados
input_dir="./img"

# Iterar por todos os arquivos .svg no diretório
for svg_file in "$input_dir"/*.svg; do
    # Nome do arquivo sem extensão
    filename=$(basename "$svg_file" .svg)

    # Converter o SVG para PNG
    inkscape -w 1024 -h 1024 "$svg_file" -o "$input_dir/$filename.png"
done
