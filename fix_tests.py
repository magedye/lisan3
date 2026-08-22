import glob
import re

test_files = glob.glob('tests/test_*.py')

for filepath in test_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if app.dependency_overrides is defined globally
    if re.search(r'^app\.dependency_overrides\[get_db\] = override_get_db', content, flags=re.MULTILINE):
        # We replace the global override with setting it inside the test_db fixture
        content = re.sub(
            r'^app\.dependency_overrides\[get_db\] = override_get_db\n', 
            '', 
            content, 
            flags=re.MULTILINE
        )
        
        # Now find the test_db fixture
        fixture_pattern = r'(@pytest\.fixture(?:\(.*?\))?\s*def test_db\(\s*\):.*?)(?=\n@|\ndef|\Z)'
        
        def insert_override(match):
            fixture_body = match.group(1)
            # Insert `app.dependency_overrides[get_db] = override_get_db` inside the fixture
            # but we need to do it at the start of the function body
            # find the line after `def test_db():`
            lines = fixture_body.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('def test_db'):
                    lines.insert(i+1, '    app.dependency_overrides[get_db] = override_get_db')
                    break
            return '\n'.join(lines)
            
        content = re.sub(fixture_pattern, insert_override, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
