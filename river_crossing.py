from typing import Optional, Dict, List, Set
from dataclasses import dataclass
from enum import Enum, auto
import time

class Bank(Enum):
    LEFT = auto()
    RIGHT = auto()
    
    def opposite(self) -> 'Bank':
        return Bank.RIGHT if self == Bank.LEFT else Bank.LEFT
    
    def __str__(self) -> str:
        return self.name.lower()

@dataclass
class GameState:
    positions: Dict[str, Bank]
    history: List[tuple[str, Bank]]
    
    def copy(self) -> 'GameState':
        return GameState(
            positions=self.positions.copy(),
            history=self.history.copy()
        )

class RiverCrossingGame:
    def __init__(self):
        """Initialize the game with all items on the left bank."""
        self.state = GameState(
            positions={
                'Farmer': Bank.LEFT,
                'Fox': Bank.LEFT,
                'Chicken': Bank.LEFT,
                'Grain': Bank.LEFT
            },
            history=[]
        )
        self.move_count = 0
        self._cached_solutions: Optional[Set[tuple[str, Bank]]] = None

    def get_items_at_bank(self, bank: Bank) -> List[str]:
        """Get all items at the specified bank."""
        return [item for item, pos in self.state.positions.items() if pos == bank]

    def is_valid_state(self) -> bool:
        """Check if the current state is valid based on game rules."""
        farmer_bank = self.state.positions['Farmer']
        
        # Check dangerous combinations on the bank opposite to farmer
        opposite_bank = farmer_bank.opposite()
        items_without_farmer = self.get_items_at_bank(opposite_bank)
        
        if 'Fox' in items_without_farmer and 'Chicken' in items_without_farmer:
            print("\n🦊 The fox ate the chicken! 🐔")
            return False
            
        if 'Chicken' in items_without_farmer and 'Grain' in items_without_farmer:
            print("\n🐔 The chicken ate the grain! 🌾")
            return False
            
        return True

    def is_won(self) -> bool:
        """Check if all items have been moved to the right bank."""
        return all(pos == Bank.RIGHT for pos in self.state.positions.values())

    def make_move(self, item: Optional[str]) -> bool:
        """
        Attempt to move the farmer and optionally one item.
        Returns True if the move was valid and successful.
        """
        if item and item not in self.state.positions:
            print(f"\n❌ Invalid item: {item}")
            return False

        current_bank = self.state.positions['Farmer']
        if item and self.state.positions[item] != current_bank:
            print(f"\n❌ Cannot move {item} - not on same bank as farmer")
            return False

        # Make the move
        next_bank = current_bank.opposite()
        self.state.positions['Farmer'] = next_bank
        if item:
            self.state.positions[item] = next_bank
            self.state.history.append((item, next_bank))
        else:
            self.state.history.append(('Farmer', next_bank))
            
        self.move_count += 1
        return True

    def display_state(self):
        """Display the current game state with ASCII art."""
        left_items = self.get_items_at_bank(Bank.LEFT)
        right_items = self.get_items_at_bank(Bank.RIGHT)
        
        print("\n" + "=" * 60)
        print(f"Move {self.move_count}")
        print("-" * 60)
        
        # Display items with emoji
        emoji_map = {
            'Farmer': '👨‍🌾',
            'Fox': '🦊',
            'Chicken': '🐔',
            'Grain': '🌾'
        }
        
        left_str = ' '.join(emoji_map[item] for item in left_items)
        right_str = ' '.join(emoji_map[item] for item in right_items)
        
        print(f"Left bank:  {left_str}")
        print("          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"Right bank: {right_str}")
        print("=" * 60)

    def solve(self) -> Optional[List[tuple[str, Bank]]]:
        """Find a solution using depth-first search."""
        if self._cached_solutions:
            return list(self._cached_solutions)

        def dfs(state: GameState, visited: Set[frozenset]) -> Optional[List[tuple[str, Bank]]]:
            if all(pos == Bank.RIGHT for pos in state.positions.values()):
                return state.history

            # Create a frozen set of current positions for visited checking
            state_key = frozenset((item, pos) for item, pos in state.positions.items())
            if state_key in visited:
                return None
            visited.add(state_key)

            farmer_bank = state.positions['Farmer']
            items_with_farmer = [item for item, pos in state.positions.items() 
                               if pos == farmer_bank and item != 'Farmer']
            
            # Try moving farmer alone
            next_state = state.copy()
            next_state.positions['Farmer'] = farmer_bank.opposite()
            next_state.history.append(('Farmer', farmer_bank.opposite()))
            
            # Check if next state is valid
            if self._is_valid_state(next_state.positions):
                result = dfs(next_state, visited)
                if result:
                    return result

            # Try moving farmer with each possible item
            for item in items_with_farmer:
                next_state = state.copy()
                next_state.positions['Farmer'] = farmer_bank.opposite()
                next_state.positions[item] = farmer_bank.opposite()
                next_state.history.append((item, farmer_bank.opposite()))
                
                if self._is_valid_state(next_state.positions):
                    result = dfs(next_state, visited)
                    if result:
                        return result
            
            return None

        solution = dfs(self.state, set())
        if solution:
            self._cached_solutions = set(solution)
        return solution

    @staticmethod
    def _is_valid_state(positions: Dict[str, Bank]) -> bool:
        """Helper method to check if a position dictionary represents a valid state."""
        farmer_bank = positions['Farmer']
        opposite_bank = Bank.RIGHT if farmer_bank == Bank.LEFT else Bank.LEFT
        
        items_without_farmer = [item for item, pos in positions.items() 
                              if pos == opposite_bank and item != 'Farmer']
        
        if 'Fox' in items_without_farmer and 'Chicken' in items_without_farmer:
            return False
        if 'Chicken' in items_without_farmer and 'Grain' in items_without_farmer:
            return False
        return True

    def play(self):
        """Main game loop with interactive gameplay."""
        print("\n🎮 Welcome to the River Crossing Puzzle! 🚣‍♂️")
        print("\nHelp the farmer transport everyone across the river safely!")
        print("Rules:")
        print("- The boat can only carry the farmer and one item")
        print("- The fox will eat the chicken if left alone")
        print("- The chicken will eat the grain if left alone")
        print("- Type 'help' for commands, 'hint' for a hint, or 'quit' to exit")
        
        while True:
            self.display_state()
            
            if not self.is_valid_state():
                print("\n💀 Game Over!")
                return
                
            if self.is_won():
                print("\n🎉 Congratulations! You've solved the puzzle!")
                print(f"You completed it in {self.move_count} moves!")
                return
            
            command = input("\nWhat would you like to move? ").strip().lower()
            
            if command == 'quit':
                print("\n👋 Thanks for playing!")
                return
            elif command == 'help':
                print("\nCommands:")
                print("- fox, chicken, grain: move with item")
                print("- none: move farmer alone")
                print("- hint: get a hint")
                print("- quit: exit game")
                continue
            elif command == 'hint':
                solution = self.solve()
                if solution:
                    next_move = solution[len(self.state.history)]
                    print(f"\n💡 Hint: Consider moving the {next_move[0].lower()}")
                continue
                
            # Process move
            item = None if command == 'none' else command.capitalize()
            if item and item not in ['Fox', 'Chicken', 'Grain', None]:
                print("\n❌ Invalid input. Type 'help' for commands.")
                continue
                
            if not self.make_move(item):
                continue

if __name__ == "__main__":
    game = RiverCrossingGame()
    game.play()