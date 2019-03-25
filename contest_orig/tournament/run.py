import sys
import time
import random
import csv
import glob
import os
import shutil
import importlib
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
from collections import namedtuple


def read_log():
    logs = glob.glob('/root/userspace/private/public/FightingICE/log/point/*.csv')
    if logs:
        latest = max(logs, key=os.path.getctime)
        #print(f'Found: {latest}')
    else:
        raise RuntimeError(f'No log files found.')
    
    with open(latest, mode='r') as csv_file:
        # Read CSV
        csv_reader = csv.DictReader(csv_file,
                                    fieldnames=['round', 'hp1', 'hp2', 'time'])
        # Calculate wins
        p1_wins = 0
        p2_wins = 0
        for row in csv_reader:
            hp1 = int(row['hp1'])
            hp2 = int(row['hp2'])
            if hp1 == hp2:
                # Draw, nobody wins
                pass
            elif hp1 > hp2:
                p1_wins += 1
            else:
                p2_wins += 1
        # Check winner
        if p1_wins == p2_wins:
            return random.choice([1, 2])
        else:
            return 1 if p1_wins > p2_wins else 2

        
def import_from(module, name):
    importlib.invalidate_caches()
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def run_game(t1, t2):
    gateway = JavaGateway(gateway_parameters=GatewayParameters(port=4242),
                          callback_server_parameters=CallbackServerParameters())
    manager = gateway.entry_point

    # Import python classes from subdirectories
    
    # Save
    cwd = os.getcwd()
    original_path = sys.path[:]
    
    if t1.classname == "Mutagen":
        agent1 = "Mutagen"
        character1 = "LUD"
    else:
        # Load module/class 1
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), f'teams/{t1.id}/agent/'))
        t1_class = import_from(t1.classname, t1.classname)
        
        # Create object 1
        # NOTE Need to change the cwd, BasicBot complains about BasicBot.pt
        os.chdir(os.path.join(os.path.dirname(__file__), f'teams/{t1.id}/agent/'))
        p1 = t1_class(gateway)
        
        # Restore
        os.chdir(cwd)
        sys.path = original_path[:]

        # Register AIs
        manager.registerAI(t1.id, p1)
        agent1 = t1.id
        character1 = p1.getCharacter()

    if t2.classname == "Mutagen":
        agent2 = "Mutagen"
        character2 = "LUD"
    else:
        # Load module/class 2
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), f'teams/{t2.id}/agent/'))
        t2_class = import_from(t2.classname, t2.classname)
    
        # Create object 2
        #os.chdir(os.path.join(os.path.dirname(__file__), f'teams/{t1.id}/agent/'))
        os.chdir(os.path.join(os.path.dirname(__file__), f'teams/{t2.id}/agent/'))
        p2 = t2_class(gateway)
     
        # Restore
        os.chdir(cwd)
        sys.path = original_path[:]
    
        # Register AIs
        manager.registerAI(t2.id, p2)
        agent2 = t2.id
        character2 = p2.getCharacter()
   
    #print("Starting game")
    game = manager.createGame(character1,
                              character2,
                              agent1,
                              agent2,
                              1)
    manager.runGame(game)
    #print("After game")
    
    sys.stdout.flush()
    gateway.close_callback_server()
    gateway.close()
    # Wait for connection to actually close
    time.sleep(5)		

    
def get_winner(t1, t2):
    print(f'{t1.id} ({t1.classname}) vs {t2.id} ({t2.classname})')
    run_game(t1, t2)
    winner = read_log()
    return t1 if winner == 1 else t2

Team = namedtuple('Team', field_names=['id', 'username', 'classname'])

def main():
    # Create team IDs (A1, A2, ..., D4)
    # TODO replace each "foo" with the actual ilect username of each team "captain"
    # TODO replace each "BasicBot" with the actual name of the file to use
    teams = [
        Team('C4', 'foo', 'MyBasicBot4'),
        Team('B3', 'foo', 'BasicBotMzk'),
        Team('D3', 'foo', 'Mutagen'),
        Team('D1', 'foo', 'BasicBotD1'),
        Team('B2', 'foo', 'BasicBotB2'),
        Team('D2', 'foo', 'SandBag'),
        Team('B1', 'foo', 'BasicBotB1'),
        Team('B4', 'foo', 'Human'),
        Team('A2', 'foo', 'BasicBot3rd'),
        Team('D4', 'foo', 'Human'),
        Team('A3', 'foo', 'BasicBotA3'),
        Team('C1', 'foo', 'BasicBotC1'),
        Team('C3', 'foo', 'BasicBotC3'),
        Team('C2', 'foo', 'SandBag'),
        Team('A1', 'foo', 'BasicBotA1'),
        Team('A4', 'foo', 'SandBag'),
        
    ]
    
    if len(sys.argv) != 2:
        print(f'*** Needs an argument. Options are [copy, competition]')
        return
        
    if sys.argv[1] == 'copy':
        # Copy files from students to local "teams/XX" folder
        base_path = '/root/userspace/private/private/users/'
        
        # TODO Change 'something.tar.gz' with the actual predetermined file name
        file_name = 'something.tar.gz' 

        for team in teams:
            os.makedirs(f'{team.id}', exist_ok=True)
            from_path = os.path.join(base_path, team.username, file_name)
            to_path = os.path.join(os.getcwd(), f'teams/{team.id}')
            print(f'Copying {from_path} to {to_path}')
            shutil.copy2(from_path, to_path)
            print(f'Unpacking {os.path.join(to_path, file_name)}')
            shutil.unpack_archive(f'{os.path.join(to_path, file_name)}', to_path)
            
        print(f'*** You can now verify everything is in order before running the competition.')

    elif sys.argv[1] == 'competition':
        # Round names
        rounds = ['Eights', 'Quarters', 'Semifinals', 'Final']

        # Create inital matches
        matches = zip(teams[0::2], teams[1::2])

        for round in rounds:
            print('*' * 80)
            print(round)
            print('*' * 80)

            winners = []

            for t1, t2 in matches:
                winner = get_winner(t1, t2)
                winners.append(winner)

                print('=' * 80)
                print(f'The winner of "{t1.id} vs {t2.id}" is... {winner.id} ({winner.classname})!!')
                print('=' * 80)

            matches = zip(winners[0::2], winners[1::2])
    
    print(f'Done')


if __name__ == '__main__':
    main()
