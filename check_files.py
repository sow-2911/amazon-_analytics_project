# find_files.py
import os
import glob

print("🔍 Searching for ALL files in your project...")
print("=" * 50)

# Get all files in current directory
all_files = glob.glob("*")
print("📁 ALL FILES IN PROJECT FOLDER:")
for file in all_files:
    if os.path.isfile(file):
        file_size = os.path.getsize(file)
        print(f"  - {file} ({file_size} bytes)")

print("\n📊 Looking for data files...")
# Look for any data files with common extensions
data_extensions = ['*.csv', '*.xlsx', '*.xls', '*.json', '*.txt']
data_files = []

for ext in data_extensions:
    data_files.extend(glob.glob(ext))

print("📈 DATA FILES FOUND:")
for file in data_files:
    file_size = os.path.getsize(file)
    print(f"  - {file} ({file_size} bytes)")

print("\n📁 Checking subdirectories...")
subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
for subdir in subdirs:
    print(f"  📂 {subdir}/")
    subdir_files = glob.glob(f"{subdir}/*")
    for file in subdir_files:
        if os.path.isfile(file):
            file_size = os.path.getsize(file)
            print(f"    - {file} ({file_size} bytes)")

print("=" * 50)
input("Press Enter to see the results...")