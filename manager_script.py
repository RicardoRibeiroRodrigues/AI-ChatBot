import argparse
import os

# Run this script with python manager_script.py <setup | cleanup>
parser = argparse.ArgumentParser(description='Perform setup or cleanup operation.')
parser.add_argument('mode', choices=['setup', 'cleanup'], help='select operation mode')

args = parser.parse_args()

if args.mode == 'setup':
    print('Running setup...')
    import nltk
    nltk.download('wordnet')
elif args.mode == 'cleanup':
    print('Running cleanup...')
    # Delete all Docs files, data/index.json, data/urls.pickle and data/contents.pickle
    for file in os.listdir('data/Docs'):
        os.remove(os.path.join('data/Docs', file))
    if os.path.exists('data/index.json'):
        os.remove('data/index.json')
    if os.path.exists('data/urls.pickle'):
        os.remove('data/urls.pickle')
    if os.path.exists('data/contents.pickle'):
        os.remove('data/contents.pickle')

