# ecc/stats_tracker.py
stats = {
    'Hamming': {'tested': 0, 'corrected': 0},
    'Reed-Solomon': {'tested': 0, 'corrected': 0},
    'Convolutional': {'tested': 0, 'corrected': 0}
}

def update_stats(ecc_type, corrected):
    stats[ecc_type]['tested'] += 1
    if corrected:
        stats[ecc_type]['corrected'] += 1

def get_success_rates():
    return {
        ecc: (val['corrected'] / val['tested'] * 100 if val['tested'] else 0)
        for ecc, val in stats.items()
    }

def get_raw_stats():
    return stats
