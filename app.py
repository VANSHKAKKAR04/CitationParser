from flask import Flask, request, jsonify, render_template
import bibtexparser
import re
import rispy

app = Flask(__name__)

def extract_plain_text_details(plaintext_entry):
    # author_regex = r"^(.*?)\,\s\""
    # title_regex = r"\,\s\"(.*?)\,\"\s"
    # year_regex = r"\,\s.*?\.\s(\d{4})\,\s"
    # journal_regex = r",\"\sin\s(.*?)\,\s"
    # volume_regex = r"\,\svol.\s(\d+)\,\s"
    # number_regex = r"\,\sno.\(\d+)\,\s"
    # pages_regex = r"\,\spp.\s(\d+.*?)\,\s"
    # doi_regex = r"\,\sdoi:\s(.*?)\.\s"

    author_regex = r"^(.*?)\,\s\""
    title_regex = r"\"(.*?)\,\"\sin\s"
    journal_regex = r",\"\sin\s(.*?)\,\s"
    volume_regex = r"\,\svol.\s(\d+)\,\s"
    number_regex = r"\,\sno.\s(\d+)\,\s"
    pages_regex = r"\,\spp.\s(\d+.*?)\,\s"
    year_regex = r"\,\s.*?\.\s(\d{4})\,\s"
    doi_regex = r"\,\sdoi:\s(.*?)\.\s"

    details = {}

    author_match = re.search(author_regex, plaintext_entry)
    title_match = re.search(title_regex, plaintext_entry)
    year_match = re.search(year_regex, plaintext_entry)
    journal_match = re.search(journal_regex, plaintext_entry)
    volume_match = re.search(volume_regex, plaintext_entry)
    number_match = re.search(number_regex, plaintext_entry)
    pages_match = re.search(pages_regex, plaintext_entry)
    doi_match = re.search(doi_regex, plaintext_entry)

    if author_match:
        details['author'] = author_match.group(1)
    if title_match:
        details['title'] = title_match.group(1)
    if year_match:
        details['year'] = year_match.group(1)
    if journal_match:
        details['journal'] = journal_match.group(1)
    if volume_match:
        details['volume'] = volume_match.group(1)
    if number_match:
        details['number'] = number_match.group(1)
    if pages_match:
        details['pages'] = pages_match.group(1)
    if doi_match:
        details['doi'] = doi_match.group(1)

    return details


def extract_ris_details(ris_entry):
    entries = rispy.loads(ris_entry)
    entry = entries[0]  # assuming single entry for simplicity
    
    details = {
        'author': ' and '.join(entry.get('authors', [])),
        'title': entry.get('title', ''),
        'year': entry.get('year', ''),
        'journal': entry.get('journal_name', ''),
        'volume': entry.get('volume', ''),
        'number': entry.get('number', ''),
        'pages': entry.get('start_page', '') + '-' + entry.get('end_page', ''),
        'publisher': entry.get('publisher', ''),
        'doi': entry.get('doi', ''),
        'url': entry.get('urls', ''),
    }
    return details

def extract_bibtex_details(bibtex_entry):
    parser = bibtexparser.loads(bibtex_entry)
    entry = parser.entries[0]  # assuming single entry for simplicity

    details = {
        'author': entry.get('author', ''),
        'title': entry.get('title', ''),
        'year': entry.get('year', ''),
        'journal': entry.get('journal', ''),
        'volume': entry.get('volume', ''),
        'number': entry.get('number', ''),
        'pages': entry.get('pages', ''),
        'publisher': entry.get('publisher', ''),
        'doi': entry.get('doi', ''),    
        'url': entry.get('url', ''),
    }
    return details

def extract_apa_details(apa_entry):
    author_regex = r"^(.*?)\.\s\(\d{4}\)"
    title_regex = r"\)\.\s(.*?)\."
    year_regex = r"\((\d{4})\)"
    journal_regex = r"\.*[a-z]\.\s([A-Z].*?)\,"
    volume_regex = r"\,\s(\d+).*?\,"
    number_regex = r"\((\d+)\)\,"   
    pages_regex = r"\d+.*?\,\s(\d+.*?)\."
    doi_regex = r"https://doi.org/(.+)"

    details = {}
    
    author_match = re.search(author_regex, apa_entry)
    title_match = re.search(title_regex, apa_entry)
    year_match = re.search(year_regex, apa_entry)
    journal_match = re.search(journal_regex, apa_entry)
    volume_match = re.search(volume_regex, apa_entry)
    number_match = re.search(number_regex, apa_entry)
    pages_match = re.search(pages_regex, apa_entry)
    doi_match = re.search(doi_regex, apa_entry)

    if author_match:
        details['author'] = author_match.group(1)
    if title_match:
        details['title'] = title_match.group(1)
    if year_match:
        details['year'] = year_match.group(1)
    if journal_match:
        details['journal'] = journal_match.group(1)
    if volume_match:
        details['volume'] = volume_match.group(1)
    if number_match:
        details['number'] = number_match.group(1)
    if pages_match:
        details['pages'] = pages_match.group(1)
    if doi_match:
        details['doi'] = doi_match.group(1)

    return details

def extract_mla_details(mla_entry):
    author_regex = r"^(.*?)\."
    title_regex = r"\.\s\"(.*?)\.\""
    journal_regex = r"\.\"\s(.*?)\s(\d+)"
    volume_regex = r"\s(\d+)(.*?)\."
    number_regex = r"\.(\d+)\s"
    year_regex = r"\s\((\d{4})\)\:"
    pages_regex = r"\:\s(\d+.*?)\."
    doi_regex = r"\.\sdoi\:\s(.+)"
    
    details = {}
    
    author_match = re.search(author_regex, mla_entry)
    title_match = re.search(title_regex, mla_entry)
    journal_match = re.search(journal_regex, mla_entry)
    volume_match = re.search(volume_regex, mla_entry)
    number_match = re.search(number_regex, mla_entry)
    year_match = re.search(year_regex, mla_entry)
    pages_match = re.search(pages_regex, mla_entry)
    doi_match = re.search(doi_regex, mla_entry)
    
    if author_match:
        details['author'] = author_match.group(1)
    if title_match:
        details['title'] = title_match.group(1)
    if journal_match:
        details['journal'] = journal_match.group(1)
    if volume_match:
        details['volume'] = volume_match.group(1)
    if number_match:
        details['number'] = number_match.group(1)
    if year_match:
        details['year'] = year_match.group(1)
    if pages_match:
        details['pages'] = pages_match.group(1)
    if doi_match:
        details['doi'] = doi_match.group(1)

    return details

def extract_chicago_details(chicago_entry):
    author_regex = r"^(.*?)\."
    title_regex = r"\"(.*?)\""
    journal_regex = r"\.\s(.*?)\s"
    volume_regex = r"\s(\d+)\,"
    number_regex =  r"no\.\s(\d+)\s"
    year_regex = r"\((\d{4})\)"
    pages_regex = r"\s(\d+.*?)\."
    doi_regex = r"doi:(.+)"

    details = {}
    
    author_match = re.search(author_regex, chicago_entry)
    title_match = re.search(title_regex, chicago_entry)
    journal_match = re.search(journal_regex, chicago_entry)
    volume_match = re.search(volume_regex, chicago_entry)
    number_match = re.search(number_regex, chicago_entry)
    year_match = re.search(year_regex, chicago_entry)
    pages_match = re.search(pages_regex, chicago_entry)
    doi_match = re.search(doi_regex, chicago_entry)

    if author_match:
        details['author'] = author_match.group(1).strip()
    if title_match:
        details['title'] = title_match.group(1).strip()
    if journal_match:
        details['journal'] = journal_match.group(1).strip()
    if volume_match:
        details['volume'] = volume_match.group(1).strip()
    if number_match:
        details['number'] = number_match.group(1).strip()
    if year_match:
        details['year'] = year_match.group(0).strip()
    if pages_match:
        details['pages'] = pages_match.group(1).strip()
    if doi_match:
        details['doi'] = doi_match.group(1).strip()

    return details

def extract_vancouver_details(vancouver_entry):
    author_regex = r"^(.*?)\.\s"
    title_regex = r"\.\s(.*?)\.\s"
    journal_regex = r"[a-z]\.\s(.*?)\."
    year_regex = r"\.\s(\d{4})\s"
    volume_regex = r"\;(\d+).*?\:"
    number_regex = r"\((\d+)\)\:"
    pages_regex = r"\:(\d+.*?)\."
    doi_regex = r"doi\:(.+)"

    details = {}
    
    author_match = re.search(author_regex, vancouver_entry)
    title_match = re.search(title_regex, vancouver_entry)
    journal_match = re.search(journal_regex, vancouver_entry)
    year_match = re.search(year_regex, vancouver_entry)
    volume_match = re.search(volume_regex, vancouver_entry)
    number_match = re.search(number_regex, vancouver_entry)
    pages_match = re.search(pages_regex, vancouver_entry)
    doi_match = re.search(doi_regex, vancouver_entry)

    if author_match:
        details['author'] = author_match.group(1)
    if title_match:
        details['title'] = title_match.group(1)
    if journal_match:
        details['journal'] = journal_match.group(1)
    if year_match:
        details['year'] = year_match.group(1)
    if volume_match:
        details['volume'] = volume_match.group(1)
    if number_match:
        details['number'] = number_match.group(1)
    if pages_match:
        details['pages'] = pages_match.group(1)
    if doi_match:
        details['doi'] = doi_match.group(1)

    return details

def extract_harvard_details(harvard_entry):
    #Define regular expressions for each component
    author_regex = r"^(.*?),\s\d{4}\."
    year_regex = r"\s(\d{4})\."
    title_regex = r"\d{4}\.\s(.*?)\."
    journal_regex = r"\.*[a-z]\.\s([A-Z].*?)\,"
    volume_regex = r"\,\s(\d+)\("
    number_regex = r"\((\d+)\)\,"
    pages_regex = r",\spp\.(\d+.*?)"
    
    details = {}
    
    # Perform regex searches to extract each detail
    author_match = re.search(author_regex, harvard_entry)
    year_match = re.search(year_regex, harvard_entry)
    title_match = re.search(title_regex, harvard_entry)
    journal_match = re.search(journal_regex, harvard_entry)
    volume_match = re.search(volume_regex, harvard_entry)
    number_match=re.search(number_regex, harvard_entry)
    pages_match = re.search(pages_regex, harvard_entry)
    
    # Populate the details dictionary with the matched groups
    if author_match:
        details['author'] = author_match.group(1)
    if year_match:
        details['year'] = year_match.group(1)
    if title_match:
        details['title'] = title_match.group(1)
    if journal_match:
        details['journal'] = journal_match.group(1)
    if volume_match:
        details['volume'] = volume_match.group(1)
    if number_match :
        details['number'] = number_match.group(1)
    if pages_match:
        details['pages'] = pages_match.group(1)

    return details



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file_type = request.form.get('fileType')
    content = request.form.get('content')
    file = request.files.get('file')
    
    if not file and not content:
        return jsonify({'error': 'No content or file provided'}), 400
    
    if file:
        file_content = file.read().decode('utf-8').strip()
    else:
        file_content = content.strip()
    
    if file_type == 'bibtex':
        details = extract_bibtex_details(file_content)
    elif file_type == 'apa':
        details = extract_apa_details(file_content)
    elif file_type == 'mla':
        details = extract_mla_details(file_content)
    elif file_type == 'chicago':
        details = extract_chicago_details(file_content)
    elif file_type == 'vancouver':
        details = extract_vancouver_details(file_content)
    elif file_type == 'harvard':
        details = extract_harvard_details(file_content)
    elif file_type == 'ris':
        details = extract_ris_details(file_content)
    elif file_type == 'plaintext':
        details = extract_plain_text_details(file_content)
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True)

