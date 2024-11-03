class Ghost:
    """
    ghost_sprite_sheet = pygame.image.load("assets/ghost/Ghost_Idle.png").convert_alpha()
    ghost_death_sprite_sheet = pygame.image.load("assets/ghost/Ghost_Death.png").convert_alpha()
    """
    def __init__(self, pygame):
        self.pygame = pygame
        self.ghost_sprite_sheet = self.pygame.image.load("assets/ghost/Ghost_Idle.png").convert_alpha()
        self.ghost_death_sprite_sheet = self.pygame.image.load("assets/ghost/Ghost_Death.png").convert_alpha()
        self.ghost_sprite_height = 48
        self.ghost_scale_factor = 3
        self.ghost_scaled_width = self.ghost_sprite_width * self.ghost_scale_factor
        self.ghost_scaled_height = self.ghost_sprite_height * self.ghost_scale_factor
        self.num_frames_ghost_idle = 4
        self.num_frames_ghost_death = 6
        # ghost_speed = 2  # Speed of ghost movement
        # ghost_stop_distance = 9  
        self.ghost_frames = []
        self.ghost_death_frames = []
        self.ghosts = []
        self.ghost_speed = 2
        self.ghost_stop_distance = 9

    def display_ghost(self, WIDTH, HEIGHT):
        ...