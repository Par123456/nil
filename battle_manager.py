from typing import Dict, List
import hashlib
from time import sleep
from config import Config
from logger import Logger

class BattleManager:
    def __init__(self, api_client):
        self.api_client = api_client
        self.attack_stats = {
            'wins': 0,
            'losses': 0,
            'xp': 0,
            'doon': 0
        }
        self.logger = Logger()

    def battle(self, opponent_id: str, q: str, cards: List[str], 
               attacks_today: int, hero_id: Optional[str] = None) -> Dict:
        check = hashlib.md5(str(q).encode()).hexdigest()
        data = {
            'opponent_id': opponent_id,
            'check': check,
            'cards': str(cards).replace(' ', ''),
            'attacks_in_today': attacks_today
        }
        
        if hero_id:
            data['hero_id'] = hero_id

        while True:
            try:
                return self.api_client.post('battle/battle', data)
            except Exception as e:
                self.logger.error(f"Battle error: {e}")
                sleep(30)

    async def attack_player(self, player: Dict, cards: List[str], q: str) -> Dict:
        self.logger.info(f"Attacking player {player['id']} (Level {player['level']})")
        
        for _ in range(Config.GAME_CONFIG['attacks_per_player']):
            try:
                result = self.battle(
                    player['id'],
                    q,
                    cards,
                    self.attack_stats['wins']
                )
                
                if result['data'].get('xp_added', 0) > 0:
                    self.attack_stats['wins'] += 1
                    self.attack_stats['xp'] += result['data']['xp_added']
                    self.attack_stats['doon'] = result['data'].get('weekly_score', 0)
                else:
                    self.attack_stats['losses'] += 1
                    break

                sleep(Config.GAME_CONFIG['attack_delay'])
            except Exception as e:
                self.logger.error(f"Attack failed: {e}")
                break

        return self.attack_stats