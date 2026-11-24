import time, pandas as pd
from textblob import TextBlob
from colorama import init, Fore

# Init colors
init(autoreset=True)

# Load CSV (same error output)
try: df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Error: The file 'imdb_top_1000.csv' was not found."); raise SystemExit

# Unique genres
genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(", ") for g in xs})

def dots():
    """Prints ... with delay (AI thinking effect)."""
    for _ in range(3): print(Fore.YELLOW + ".", end="", flush=True); time.sleep(0.5)

def senti(p):
    """Polarity -> label."""
    return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"

def recommend(genre=None, mood=None, rating=None, n=5):
    """Filter by genre/rating, shuffle, analyze Overview polarity, return n (title, polarity) or message."""
    d = df
    if genre: d = d[d["Genre"].str.contains(genre, case=False, na=False)]
    if rating is not None: d = d[d["IMDB_Rating"] >= rating]
    if d.empty: return "No suitable movie reccomendations found."
    d, need_nonneg, out = d.sample(frac=1).reset_index(drop=True), bool(mood), []
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov): continue
        pol = TextBlob(ov).sentiment.polarity
        if (not need_nonneg) or pol >= 0:
            out.append((r["Series_Title"], pol))
            if len(out) == n: break
    return out if out else "No suitable movie recemmondations found."
    pass

def show(recs, name):
    """Print in same format: header + numbered 🎥 lines with polarity + senti()."""
    print(Fore.YELLOW + f"\n🍿 AI-Analyzed Movie Reccomendations for {name}:")
    for i, (t, p) in enumerate(recs, 1):
        print(f"{Fore.CYAN}{i}. 🎥 {t} (Polarity: {p:.2f}, {senti(p)})")
    pass

def get_genre():
    """Print genres, then ask: Enter genre number or name: (repeat until valid)."""
    print(Fore.GREEN + "Available Genres: ", end="")
    for i, g in enumerate(genres, 1): print(f"{Fore.CYAN}{i}. {g}")
    print()
    while True:
        x = input(Fore.YELLOW + "Enter genre number or name: ").strip()
        if x.isdigit() and 1 <= int(x) <= len(genres): return genres[int(x) - 1]
        x = x.title()
        if x in genres: return x
        print(Fore.RED + "Invalid input. Try again.\n")
    pass

def get_rating():
    """Ask rating or 'skip' (repeat until valid)."""
    while True:
        x = input(Fore.YELLOW + "Enter minimum IMDB rating (7.6-9.3) or 'skip': ").strip()
        if x.lower() == "skip": return None
        try:
            r = float(x)
            if 7.6 <= r <= 9.3: return r
            print(Fore.RED + "Rating out of range. Try again.\n")
        except ValueError:
            print(Fore.RED + "Invalid input. Try again.\n")

print(Fore.BLUE + "🎥 Welcome to your Personal Movie Recommendation Assistant! 🎥\n")
name = input(Fore.YELLOW + "What's your name? ").strip()
    pass

# MAIN (students write)
# 1) Print welcome + ask name + greet
# 2) Print 🔍 line
# 3) genre = get_genre(); mood input
# 4) Print "Analyzing mood" + dots(); compute mood polarity + print mood line
# 5) rating = get_rating()
# 6) Print "Finding movies for {name}" + dots()
# 7) recs = recommend(...); if str print red else show()
# 8) Loop ask "Would you like more recommendations? (yes/no):"
#    - no -> print enjoy line + break
#    - yes -> recommend again + show
#    - else -> invalid choice line
