import os
import re

# Strict .htm pattern (ignores .html)
FILE_PATTERN = re.compile(r'.*\.htm$', re.IGNORECASE)
AD_COMMENT_PATTERN = re.compile(r'<!--#+.*?#+-->', re.DOTALL)

def sanitize_archives():
    source_dir = os.getcwd()
    total_files_processed = 0

    print(f"Scanning for .htm files in: {source_dir}")

    for filename in os.listdir(source_dir):
        if FILE_PATTERN.match(filename):
            file_path = os.path.join(source_dir, filename)
            
            # Reset counter to 1 for every new file
            file_ad_count = 0

            def ad_replacer(match):
                nonlocal file_ad_count
                file_ad_count += 1
                return f"<!--######ADVERTSING-BLOCK-No.#{file_ad_count:02d}########-->"

            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()

            sanitized_content = AD_COMMENT_PATTERN.sub(ad_replacer, content)

            with open(file_path, 'w', encoding='latin-1') as f:
                f.write(sanitized_content)
            
            total_files_processed += 1
            print(f"Sanitized: {filename} ({file_ad_count} blocks replaced)")

    print(f"\nProcessing complete. Total .htm files handled: {total_files_processed}")

if __name__ == "__main__":
    sanitize_archives()
