"""
Configuration for the TalentParse Engine (Resume Intelligence Pipeline).
Contains sample skill dictionary and thresholds; product owners can update this.
"""

SKILL_DICTIONARY = {
    'React': ['react', 'react.js', 'reactjs'],
    'JavaScript': ['javascript', 'js'],
    'TypeScript': ['typescript', 'ts'],
    'Docker': ['docker', 'containers'],
    'AWS': ['aws', 'amazon web services'],
}

FUZZY_THRESHOLD = 0.85

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
