class Cat:
    def __init__(self, x, y, width, height, speed, cat_frames):
        ...
    
    def move(self):
        """
            cat_frames = []
            for i in rande (number of frames):
                frame = cat_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
                scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
                cat_frames.append(scaled_frame)
        """