#!/usr/bin/env python3
"""
Generate an HTML overview page for all T.35 manufacturer codes.
Reads all CSV files from the data/ directory and creates a searchable, interactive page.
"""

import csv
import json
from pathlib import Path
from datetime import datetime

def read_csv_file(csv_path):
    """Read a CSV file and return list of dictionaries."""
    codes = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codes.append(row)
    return codes

def get_country_name(filename):
    """Extract country name from filename (e.g., t35_usa.csv -> USA)."""
    name = filename.stem.replace('t35_', '')
    return name.upper()

def generate_html(data_by_country):
    """Generate complete HTML page with all T.35 codes."""

    # Calculate total codes
    total_codes = sum(len(codes) for codes in data_by_country.values())

    # Prepare JSON data for JavaScript
    json_data = json.dumps(data_by_country, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ITU-T T.35 Manufacturer Codes - Overview</title>
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --background: #ffffff;
            --surface: #f8fafc;
            --border: #e2e8f0;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --hover-bg: #f1f5f9;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: var(--background);
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: var(--surface);
            border-radius: 12px;
            border: 1px solid var(--border);
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 10px;
        }}

        .warning {{
            background: #fef3c7;
            border: 2px solid #fbbf24;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: 500;
            color: #92400e;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat {{
            background: white;
            padding: 15px 30px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary-color);
        }}

        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .controls {{
            background: var(--surface);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 1px solid var(--border);
        }}

        .search-box {{
            width: 100%;
            padding: 12px 20px;
            font-size: 1rem;
            border: 2px solid var(--border);
            border-radius: 8px;
            margin-bottom: 15px;
            transition: border-color 0.2s;
        }}

        .search-box:focus {{
            outline: none;
            border-color: var(--primary-color);
        }}

        .filter-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid var(--border);
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.95rem;
            transition: all 0.2s;
        }}

        .filter-btn:hover {{
            border-color: var(--primary-color);
            background: var(--hover-bg);
        }}

        .filter-btn.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}

        .country-section {{
            margin-bottom: 40px;
            background: white;
            border-radius: 8px;
            border: 1px solid var(--border);
            overflow: hidden;
        }}

        .country-header {{
            background: var(--surface);
            padding: 20px;
            border-bottom: 1px solid var(--border);
        }}

        .country-name {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .country-code {{
            display: inline-block;
            background: var(--primary-color);
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            margin-left: 10px;
        }}

        .code-count {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-top: 5px;
        }}

        .table-container {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        thead {{
            background: var(--surface);
            border-bottom: 2px solid var(--border);
        }}

        th {{
            padding: 12px 20px;
            text-align: left;
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px 20px;
            border-bottom: 1px solid var(--border);
        }}

        tbody tr:hover {{
            background: var(--hover-bg);
        }}

        .code {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: var(--primary-color);
        }}

        .no-results {{
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            color: var(--text-secondary);
            border-top: 1px solid var(--border);
        }}

        footer a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        .hidden {{
            display: none;
        }}

        .github-button {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: white;
            color: #1f2937;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .github-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}

        .github-logo {{
            width: 24px;
            height: 24px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ITU-T T.35 Manufacturer Codes</h1>
            <p class="subtitle">Community-maintained collection of T.35 codes</p>
            
            <div class="contribution-box">
                <p>If you don't see what you're looking for, open a PR!</p>
                <a href="https://github.com/podborski/ITU-T-T35-Codes" target="_blank" class="github-button">
                    <svg class="github-logo" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                    View on GitHub & Submit a PR
                </a>
            </div>

            <div class="warning">
                ⚠️ This is not an official document
            </div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{total_codes}</div>
                    <div class="stat-label">Total Codes</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(data_by_country)}</div>
                    <div class="stat-label">Countries</div>
                </div>
            </div>
        </header>

        <div class="controls">
            <input type="text" id="searchBox" class="search-box" placeholder="Search by manufacturer name or code...">
            <div class="filter-buttons">
                <button class="filter-btn active" data-country="all">All Countries</button>
                {''.join(f'<button class="filter-btn" data-country="{country.lower()}">{country}</button>' for country in sorted(data_by_country.keys()))}
            </div>
        </div>

        <div id="content">
            <!-- Tables will be generated here by JavaScript -->
        </div>

        <footer>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
            <p>Source: <a href="https://github.com/podborski/ITU-T-T35-Codes" target="_blank">github.com/podborski/ITU-T-T35-Codes</a></p>
            <p>Official ITU-T T.35 Specification: <a href="https://www.itu.int/rec/T-REC-T.35/en" target="_blank">itu.int/rec/T-REC-T.35</a></p>
        </footer>
    </div>

    <script>
        const data = {json_data};

        function renderTable(country, codes) {{
            const countryCode = codes[0]['Country Code'];
            const html = `
                <div class="country-section" data-country="${{country.toLowerCase()}}">
                    <div class="country-header">
                        <h2 class="country-name">
                            ${{country}}
                            <span class="country-code">${{countryCode}}</span>
                        </h2>
                        <div class="code-count">${{codes.length}} manufacturer codes</div>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Country Code</th>
                                    <th>First Byte</th>
                                    <th>Second Byte</th>
                                    <th>Manufacturer</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${{codes.map(code => `
                                    <tr>
                                        <td class="code">${{code['Country Code']}}</td>
                                        <td class="code">${{code['First Byte']}}</td>
                                        <td class="code">${{code['Second Byte'] || 'N/A'}}</td>
                                        <td>${{code['Manufacturer']}}</td>
                                    </tr>
                                `).join('')}}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
            return html;
        }}

        function renderAll() {{
            const content = document.getElementById('content');
            let html = '';

            // Sort countries alphabetically
            const sortedCountries = Object.keys(data).sort();

            for (const country of sortedCountries) {{
                html += renderTable(country, data[country]);
            }}

            content.innerHTML = html;
        }}

        function filterByCountry(country) {{
            const sections = document.querySelectorAll('.country-section');
            sections.forEach(section => {{
                if (country === 'all' || section.dataset.country === country) {{
                    section.classList.remove('hidden');
                }} else {{
                    section.classList.add('hidden');
                }}
            }});
        }}

        function search(query) {{
            const sections = document.querySelectorAll('.country-section');
            const lowerQuery = query.toLowerCase();

            sections.forEach(section => {{
                const rows = section.querySelectorAll('tbody tr');
                let hasVisibleRows = false;

                rows.forEach(row => {{
                    const text = row.textContent.toLowerCase();
                    if (text.includes(lowerQuery)) {{
                        row.classList.remove('hidden');
                        hasVisibleRows = true;
                    }} else {{
                        row.classList.add('hidden');
                    }}
                }});

                // Hide section if no matching rows
                if (hasVisibleRows) {{
                    section.classList.remove('hidden');
                }} else {{
                    section.classList.add('hidden');
                }}
            }});
        }}

        // Initialize
        renderAll();

        // Search functionality
        const searchBox = document.getElementById('searchBox');
        searchBox.addEventListener('input', (e) => {{
            search(e.target.value);
        }});

        // Filter buttons
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {{
            btn.addEventListener('click', () => {{
                // Update active state
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Reset search
                searchBox.value = '';

                // Render filtered content
                filterByCountry(btn.dataset.country);
            }});
        }});
    </script>
</body>
</html>"""

    return html

def main():
    """Main function to generate the overview page."""
    # Get data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir / 'data'

    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        return

    # Read all CSV files
    data_by_country = {}
    csv_files = sorted(data_dir.glob('t35_*.csv'))

    if not csv_files:
        print(f"Error: No CSV files found in {data_dir}")
        return

    print(f"Found {len(csv_files)} CSV files:")
    for csv_file in csv_files:
        country = get_country_name(csv_file)
        codes = read_csv_file(csv_file)
        data_by_country[country] = codes
        print(f"  - {csv_file.name}: {len(codes)} codes")

    # Generate HTML
    html_content = generate_html(data_by_country)

    # Write to index.html
    output_file = script_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nGenerated: {output_file}")
    print(f"Total codes: {sum(len(codes) for codes in data_by_country.values())}")

if __name__ == '__main__':
    main()
