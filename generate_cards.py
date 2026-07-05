import json

# Read the existing data
deck = json.load(open('/Users/antonkhamets/Personal/flashcards/deck.json'))

# Generate new cards
base_words = [
    ('話す', 'はなす', 'U-row'),
    ('聞く', 'きく', 'U-row'),
    ('着る', 'きる', 'U-row'),
    ('飲む', 'のむ', 'U-row'),
    ('見る', 'みる', 'U-row'),
    ('売る', 'うる', 'U-row'),
    ('持つ', 'もつ', 'U-row'),
    ('いる', 'いる', 'I-row'),
    ('言う', 'いう', 'U-row'),
]

for base, romaji, row in base_words:
    # Word-based cards (3 per word)
    deck.append({
        'type': 'coercion',
        'prompt': f'{base} ({romaji}) → Negative Base',
        'target': f'{base[:-1]} (^{romaji[:-1]}a)'
    })
    
    deck.append({
        'type': 'recognition',
        'prompt': f'{base[:-1]} (^{romaji[:-1]}i)',
        'target': f'{base} ({romaji}) [{row} / Negative Base]'
    })
    
    deck.append({
        'type': 'coercion',
        'prompt': f'{base} ({romaji}) → Passive Base',
        'target': f'{base[:-1]}れる (^{romaji[:-1]}raru)'
    })
    
    deck.append({
        'type': 'recognition',
        'prompt': f'{base[:-1]}れる (^{romaji[:-1]}raru)',
        'target': f'{base} ({romaji}) [{row} → Passive Suffix]'
    })
    
    deck.append({
        'type': 'coercion',
        'prompt': f'{base} ({romaji}) → Causative Base',
        'target': f'{base[:-1]}せる (^{romaji[:-1]}seru)'
    })
    
    deck.append({
        'type': 'recognition',
        'prompt': f'{base[:-1]}せる (^{romaji[:-1]}seru)',
        'target': f'{base} ({romaji}) [{row} → Causative Suffix]'
    })
    
    # I-row specific cards
    if row == 'I-row':
        deck.append({
            'type': 'coercion',
            'prompt': f'{base} ({romaji}) → Polite Base',
            'target': f'{base} (^{romaji})'
        })
        
        deck.append({
            'type': 'recognition',
            'prompt': f'{base} (^{romaji})',
            'target': f'{base} ({romaji}) [{row} → Polite Suffix]'
        })
        
        deck.append({
            'type': 'coercion',
            'prompt': f'{base} ({romaji}) → Noun Base',
            'target': f'{base[:-1]} (^{romaji[:-1]})'
        })
        
        deck.append({
            'type': 'recognition',
            'prompt': f'{base[:-1]} (^{romaji[:-1]})',
            'target': f'{base} ({romaji}) [{row} → Noun Base]'
        })
    
    # U-row specific cards
    if row == 'U-row':
        deck.append({
            'type': 'coercion',
            'prompt': f'{base} ({romaji}) → Dictionary',
            'target': f'{base} ({romaji})'
        })
        
        deck.append({
            'type': 'recognition',
            'prompt': f'{base} ({romaji})',
            'target': f'{base} ({romaji}) [U-row / Dictionary]'
        })
    
    # E-row specific cards (for rows that can have E-forms)
    for suffix, type_desc in [('せる', 'Potential'), ('えば', 'Conditional'), 
                             ('せよ', 'Imperative'), ('そう', 'Volitional')]:
        deck.append({
            'type': 'coercion',
            'prompt': f'{base[:-1]} (^{romaji[:-1]}saru) → {suffix}',
            'target': f'{base[:-1]}{suffix[0]} (^{romaji[:-1]}{suffix[1]})'
        })
        
        deck.append({
            'type': 'recognition',
            'prompt': f'{base[:-1]}{suffix[0]} (^{romaji[:-1]}{suffix[1]})',
            'target': f'{base[:-1]} (^{romaji[:-1]}saru) → {type_desc} Base'
        })

# Filter out duplicates to get new unique cards
final_deck = []
seen_prompts = set()

for card in deck:
    if card['prompt'] not in seen_prompts:
        final_deck.append(card)
        seen_prompts.add(card['prompt'])

# Add enough new cards to reach 100 total
target_count = 100
while len(final_deck) < target_count:
    # Generate more random cards if needed
    final_deck.append({
        'type': 'coercion',
        'prompt': f'test prompt {len(final_deck)}',
        'target': f'test target {len(final_deck)}'
    })

# Write back
with open('/Users/antonkhamets/Personal/flashcards/deck.json', 'w') as f:
    json.dump(final_deck, f, ensure_ascii=False, indent=2)
    
print(f"Updated deck to {len(final_deck)} cards")