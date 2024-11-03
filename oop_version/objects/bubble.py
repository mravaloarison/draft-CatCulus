class Bublle:
    """
        if current_time - message_change_timer > message_change_interval:
            if len(generated_quiz) > 1 and len(generated_quiz) < count:
                index = (index + 1) % len(generated_quiz)

            else:
                generated_quiz = generate_quiz()
                index = 0

            quiz = Quiz(generated_quiz[index])
            message_change_timer = current_time

        text_surface = font.render(instructions, True, (0, 0, 0))
        bubble_width = text_surface.get_width() + bubble_padding * 2

        bubble_surface = pygame.Surface((bubble_width, bubble_height))
        bubble_surface.fill((255, 255, 255))
        bubble_surface.set_alpha(230)
        
        bubble_rect = pygame.Rect(
            (WIDTH - bubble_width) // 2,
            (HEIGHT - bubble_height) //2,
            bubble_width,
            bubble_height,
        )

        screen.blit(bubble_surface, bubble_rect.topleft)
        text_x = bubble_rect.x + bubble_padding
        text_y = bubble_rect.y + (bubble_height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
    
    """

    def __init__(self, current_time, message_change_timer, pygame, message_change_interval, generated_quiz, count, index, quiz, font, instructions, WIDTH, HEIGHT, bubble_padding, bubble_height, new_quiz):
        self.current_time = current_time
        self.message_change_timer = message_change_timer
        self.message_change_interval = message_change_interval
        self.generated_quiz = generated_quiz
        self.count = count
        self.index = index
        self.quiz = quiz
        self.pygame = pygame
        self.new_quiz = new_quiz
        self.font = font
        self.instructions = instructions
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.bubble_padding = bubble_padding
        self.bubble_height = bubble_height

    def change_message(self):
        if self.current_time - self.message_change_timer > self.message_change_interval:
            if len(self.generated_quiz) > 1 and len(self.generated_quiz) < self.count:
                self.index = (self.index + 1) % len(self.generated_quiz)

            else:
                self.generated_quiz = self.new_quiz()
                self.index = 0

            self.quiz = self.new_quiz
            self.message_change_timer = self.current_time

        text_surface = self.font.render(self.instructions, True, (0, 0, 0))
        bubble_width = text_surface.get_width() + self.bubble_padding * 2

        bubble_surface = self.pygame.Surface((bubble_width, self.bubble_height))
        bubble_surface.fill((255, 255, 255))
        bubble_surface.set_alpha(230)

        bubble_rect = self.pygame.Rect(
            (self.WIDTH - bubble_width) // 2,
            (self.HEIGHT - self.bubble_height) // 2,
            bubble_width,
            self.bubble_height,
        )

        self.pygame.screen.blit(bubble_surface, bubble_rect.topleft)
        text_x = bubble_rect.x + self.bubble_padding
        text_y = bubble_rect.y + (self.bubble_height - text_surface.get_height()) // 2

        self.pygame.screen.blit(text_surface, (text_x, text_y))
        return self.pygame.screen