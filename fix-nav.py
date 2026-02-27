import re

files_to_fix = {
    'admin.html': 'admin',
    'ideas.html': 'ideas',
    'ads.html': 'ads',
    'prompts.html': 'prompts',
    'docs.html': 'docs',
    'apps.html': 'apps'
}

for filename, active_page in files_to_fix.items():
    with open(filename, 'r') as f:
        content = f.read()
    
    # Fix 2: Add <cc-app-topnav> before <cc-user-auth> (if not already present)
    if '<cc-app-topnav' not in content:
        topnav = f'''<cc-app-topnav app="cc-architecture" title="Architecture Viewer" links='[{{"href":"/admin.html","label":"Admin"}},{{"href":"/apps.html","label":"Apps"}},{{"href":"/ideas.html","label":"Ideas"}},{{"href":"/ads.html","label":"Ads"}},{{"href":"/prompts.html","label":"Prompts"}},{{"href":"/docs.html","label":"Docs"}}]' active="{active_page}"></cc-app-topnav>'''
        # Insert topnav right after <body>
        content = content.replace('<body>\n', f'<body>\n{topnav}\n')
    
    # Fix 3: Add position="bottom" to <cc-app-nav> if not already present
    if 'position="bottom"' not in content:
        content = re.sub(
            r'(<cc-app-nav[^>]*)(>)',
            r'\1 position="bottom"\2',
            content
        )
    
    # Move cc-app-nav to after cc-user-auth if it's before
    lines = content.split('\n')
    nav_line_idx = None
    auth_line_idx = None
    
    for i, line in enumerate(lines):
        if '<cc-app-nav' in line:
            nav_line_idx = i
        if '<cc-user-auth' in line:
            auth_line_idx = i
    
    # If nav comes before auth, move it
    if nav_line_idx is not None and auth_line_idx is not None and nav_line_idx < auth_line_idx:
        nav_line = lines[nav_line_idx]
        lines.pop(nav_line_idx)
        # Find auth line again (index shifted)
        for i, line in enumerate(lines):
            if '<cc-user-auth' in line:
                lines.insert(i + 1, nav_line)
                break
        content = '\n'.join(lines)
    
    with open(filename, 'w') as f:
        f.write(content)

print("✅ Fixed all 6 files")
