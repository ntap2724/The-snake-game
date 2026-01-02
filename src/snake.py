"""Snake class for the game"""

class Snake:
    """Represents the snake in the game"""
    
    def __init__(self, initial_position, length=3):
        """
        Initialize snake with starting position and length
        
        Args:
            initial_position: Tuple (x, y) for head position
            length: Initial snake body length
        """
        self.direction = 'DOWN'
        self.body = []
        
        # Body extends downward from initial position
        for i in range(length):
            self.body.append((initial_position[0], initial_position[1] + i))
    
    def move(self, direction):
        """Move the snake in the given direction"""
        self.direction = direction
        
        # Calculate new head position based on direction
        head_x, head_y = self.body[0]
        
        if direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif direction == 'RIGHT':
            new_head = (head_x + 1, head_y)
        else:
            new_head = (head_x, head_y)
        
        # Add new head to front of body
        self.body.insert(0, new_head)
        
        # Remove tail (snake moves, doesn't grow)
        self.body.pop()
    
    def grow(self):
        """Grow the snake by one segment"""
        # Get current tail position
        tail_position = self.body[-1]
        
        # Add a new segment at the tail position (no removal, so snake grows)
        self.body.append(tail_position)
    
    def check_self_collision(self):
        """Check if snake collided with itself"""
        # Check if head position exists in body[1:] (excluding head itself)
        head_position = self.body[0]
        return head_position in self.body[1:]
    
    def get_head_position(self):
        """Return the position of the snake's head"""
        return self.body[0]
    
    def get_body(self):
        """Return the entire snake body as list of positions"""
        return self.body
