import pdfplumber
import pandas as pd
import os
from collections import defaultdict

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            chars = page.chars
            words = []
            current_word = []
            for char in chars:
                if current_word and _is_new_word(char, current_word[-1]):
                    words.append(current_word)
                    current_word = []
                current_word.append(char)
            if current_word:
                words.append(current_word)
            
            word_objects = []
            for word in words:
                text = ''.join([c['text'] for c in word])
                x0 = min(c['x0'] for c in word)
                x1 = max(c['x1'] for c in word)
                top = min(c['top'] for c in word)
                bottom = max(c['bottom'] for c in word)
                word_objects.append({'text': text, 'x0': x0, 'x1': x1, 'top': top, 'bottom': bottom})
            
            rows = defaultdict(list)
            for word in word_objects:
                row_key = round(word['top'])
                rows[row_key].append(word)
            
            sorted_rows = sorted(rows.items(), key=lambda x: x[0])
            column_boundaries = set()
            for row in sorted_rows:
                for word in row[1]:
                    column_boundaries.add(word['x0'])
                    column_boundaries.add(word['x1'])
            sorted_columns = sorted(column_boundaries)
            
            table = []
            for row_key, words in sorted_rows:
                row_dict = {}
                for word in words:
                    col_start = max([c for c in sorted_columns if c <= word['x0']], default=sorted_columns[0])
                    col_end = min([c for c in sorted_columns if c >= word['x1']], default=sorted_columns[-1])
                    col_index = sorted_columns.index(col_start)
                    row_dict[col_index] = word['text']
                max_col = max(row_dict.keys()) if row_dict else 0
                row_data = [row_dict.get(i, '') for i in range(max_col+1)]
                table.append(row_data)
            
            if table:
                tables.append((f"Page_{page_num+1}", table))
    
    return tables

def _is_new_word(new_char, prev_char):
    return (new_char['x0'] - prev_char['x1'] > 3 or new_char['top'] - prev_char['top'] > 5)

def save_to_excel(tables, output_path):
    with pd.ExcelWriter(output_path) as writer:
        for name, table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            df.to_excel(writer, sheet_name=name, index=False)