import asyncio
from config import Config
from database_manager import DatabaseManager
from battle_manager import BattleManager
from api_client import ApiClient
from logger import Logger
import os

async def main():
    logger = Logger()
    
    restore_key = input('Enter your restore key: ')
    api_client = ApiClient(restore_key)
    load_response = api_client.initialize()

    if not load_response['status']:
        logger.error('Failed to connect. Check your restore key.')
        return

    account_info = load_response['data']
    logger.success(
        f"Connected successfully!\n"
        f"Account: {account_info['name']}\n"
        f"Level: {account_info['level']}\n"
        f"Gold: {account_info['gold']}\n"
        f"Tribe: {account_info['tribe']['name']}"
    )

    # Get user configuration
    max_power = int(input('Your power: '))
    min_level = int(input('Level Up to attack: '))
    min_level_for_storage = int(input('Level up To Save Database: '))
    max_attempts_per_player = int(input('Number of Attacks to Enemy: '))

    # Initialize databases
    db_files = {
        'regular': 'players.db',
        'league': f'league_{account_info["league_id"]}.db',
        'high_value': 'rich_players.db',
        'suspended': 'suspended.db'
    }

    db_manager = DatabaseManager(db_files)
    battle_manager = BattleManager(api_client)

    # Get weak cards
    cards = [
        card['id'] 
        for card in account_info['cards'] 
        if card['power'] < Config.GAME_CONFIG['weak_card_power_threshold']
    ]

    if len(cards) < Config.GAME_CONFIG['min_weak_cards']:
        logger.error(f"Not enough weak cards! Need at least {Config.GAME_CONFIG['min_weak_cards']}")
        return

    try:
        while True:
            players = api_client.get_opponents()
            
            for player in players:
                if (player['level'] >= min_level and 
                    player['level'] <= Config.GAME_CONFIG['max_level']):
                    
                    db_manager.update_player('regular', player)
                    
                    if player['gold'] >= Config.GAME_CONFIG['gold_threshold']:
                        db_manager.update_player('high_value', player)

                    stats = await battle_manager.attack_player(
                        player,
                        cards,
                        account_info['q']
                    )

                    logger.info(
                        f"Stats - Wins: {stats['wins']}, "
                        f"XP: {stats['xp']}, "
                        f"Doon: {stats['doon']}"
                    )

                    if stats['doon'] >= Config.GAME_CONFIG['doon_limit']:
                        logger.success('Reached doon limit. Stopping...')
                        return

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error("Bot error", e)
    finally:
        db_manager.close()

if __name__ == "__main__":
    os.system('clear')
    asyncio.run(main())