import sqlite3
from typing import Dict, List
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_files: Dict[str, str]):
        self.connections = {}
        self.initialize_databases(db_files)

    def initialize_databases(self, db_files: Dict[str, str]):
        for key, file in db_files.items():
            db_path = os.path.join('data', file)
            os.makedirs('data', exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id TEXT PRIMARY KEY,
                    power INTEGER,
                    level INTEGER,
                    league INTEGER,
                    gold INTEGER,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            self.connections[key] = conn

    def update_player(self, db_key: str, player: Dict):
        conn = self.connections[db_key]
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO players (id, power, level, league, gold, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            player['id'],
            player['def_power'],
            player['level'],
            player['league_id'],
            player['gold'],
            datetime.now().isoformat()
        ))
        
        conn.commit()

    def get_target_players(self, db_key: str, criteria: Dict) -> List[Dict]:
        conn = self.connections[db_key]
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM players 
            WHERE level >= ? 
            AND level <= ? 
            AND power <= ?
            ORDER BY last_updated DESC
        ''', (
            criteria['min_level'],
            criteria['max_level'],
            criteria['max_power']
        ))
        
        return [
            {
                'id': row[0],
                'power': row[1],
                'level': row[2],
                'league': row[3],
                'gold': row[4]
            }
            for row in cursor.fetchall()
        ]

    def close(self):
        for conn in self.connections.values():
            conn.close()