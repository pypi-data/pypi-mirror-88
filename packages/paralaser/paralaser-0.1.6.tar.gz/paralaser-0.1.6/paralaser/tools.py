from pathlib import Path
from .lib.romanize_lc import script_path as roman_lc_path

home = Path.home()
laser_dir = home / ".local" / "share" / "paralaser"
tools_dir = Path(__file__).parent / "tools-external"
moses_dir = tools_dir / "moses-tokenizer" / "tokenizer"

FASTBPE = f'{tools_dir / "fast"}'
MOSES_TOKENIZER = f'perl {moses_dir / "tokenizer.perl"} -q -no-escape -threads 20 -l '
MOSES_LC = f'perl {moses_dir / "lowercase.perl"}'
NORM_PUNC = f'perl {moses_dir / "normalize-punctuation.perl"} -l '
DESCAPE = f'perl {moses_dir / "descape-special-chars.perl"}'
REM_NON_PRINT_CHAR = f'perl {moses_dir / "remove-non-printing-char.perl"}'

# Romanization (Greek only)
ROMAN_LC = f"python3 {roman_lc_path} -l "

# Mecab tokenizer for Japanese
MECAB = f'{tools_dir / "mecab"}'
