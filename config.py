from typing import Dict, List

class Config:
    GAME_CONFIG = {
        'min_level': 8,
        'max_level': 100,
        'doon_limit': 5000,
        'attacks_per_player': 3,
        'attack_delay': 0.3,
        'search_delay': 1.0,
        'secondary_search_delay': 2.0,
        'target_suspended': False,
        'weak_card_power_threshold': 100,
        'min_weak_cards': 20,
        'fruit_pass_enabled': True,
        'database_update_interval': 300,
        'gold_threshold': 500000000000,
        'league_db_enabled': True,
        'user_agent_rotation': True,
        'max_retries': 3,
        'xp_target': 1000,
        'gold_target': 1000000
    }

    USER_AGENTS = [
        'Dalvik/2.1.0 (Linux; U; Android 10; PO-X1100 Build/RP1A.200320.012)',
        'Dalvik/2.1.0 (Linux; U; Android 9; SM-A505F Build/PPR1.180610.011)'
    ]

    API_ENDPOINTS = {
        'base': 'http://iran.fruitcraft.ir/',
        'secure_base': 'https://iran.fruitcraft.ir/',
        'load': 'player/load',
        'battle': 'battle/battle',
        'opponents': 'battle/getopponents'
    }