import pygame, sys, random

# Game settings
speed = 12
frame_size_x = 750
frame_size_y = 450

pygame.init()
pygame.display.set_caption("Catch the Clown")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (50, 50, 255)
highlight_color = (0, 255, 255)  

fps_controller = pygame.time.Clock()
square_size = 20

bodyguard = ["💂🏻‍♀️"]

# Load images for backgrounds
main_menu_bg = pygame.image.load("clown.jpg") 
main_menu_bg = pygame.transform.scale(main_menu_bg, (frame_size_x, frame_size_y))

game_bg = pygame.image.load("London.jpg") 
game_bg = pygame.transform.scale(game_bg, (frame_size_x, frame_size_y))

# Initialize variables
def init_vars():
    global head_pos, bodyguard_body, food_pos, food_spawn, score, direction, change_to, bombs, police_girl_pos, police_girl_active
    direction = "RIGHT"
    change_to = direction
    head_pos = [120, 60]
    bodyguard_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True
    bombs = []
    police_girl_active = False
    police_girl_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                        random.randrange(1, (frame_size_y // square_size)) * square_size]
    score = 0

# Display score
def show_score():
    font = pygame.font.SysFont('consolas', 20)
    score_surface = font.render(f"Score: {score}", True, white)
    game_window.blit(score_surface, (10, 10))

# Draw emoji
def draw_emoji(text, position):
    font = pygame.font.SysFont('segoeuiemoji', square_size)
    surface = font.render(text, True, white)
    game_window.blit(surface, position)

# Show top scores
def show_top_scores(top_scores):
    font = pygame.font.SysFont('consolas', 20)
    y_pos = 100
    for score in top_scores:
        score_text = font.render(f"Score: {score}", True, white)
        game_window.blit(score_text, (frame_size_x // 3, y_pos))
        y_pos += 30

# Main menu
def show_main_menu(selected_option, top_scores):
    font_title = pygame.font.SysFont('consolas', 50)
    font_button = pygame.font.SysFont('consolas', 40)
    
    title_text = font_title.render("Catch the Clown", True, white)
    start_text = font_button.render("Start Game", True, white)
    top_scores_text = font_button.render("Top Scores", True, white)

    # Fill background with gradient
    game_window.fill(black)
    game_window.blit(main_menu_bg, (0, 0)) 

    # Title at the top of the screen
    game_window.blit(title_text, (frame_size_x // 4, frame_size_y // 4))
    
    # Draw buttons with highlights
    game_window.blit(start_text, (frame_size_x // 4, frame_size_y // 2))
    game_window.blit(top_scores_text, (frame_size_x // 4, frame_size_y // 1.5))

    # Highlight selected option
    if selected_option == 0:
        pygame.draw.rect(game_window, highlight_color, (frame_size_x // 4 - 10, frame_size_y // 2 - 10, 350, 50), 3)
    elif selected_option == 1:
        pygame.draw.rect(game_window, highlight_color, (frame_size_x // 4 - 10, frame_size_y // 1.5 - 10, 350, 50), 3)

    pygame.display.update()

# Show game over screen with option to save score and show top scores
def game_over_with_scores(top_scores):
    font = pygame.font.SysFont('consolas', 50)
    game_over_text = font.render("GAME OVER", True, green)
    game_window.blit(game_over_text, (frame_size_x // 3, frame_size_y // 3))
    pygame.display.update()
    pygame.time.delay(2000)

    if score >= 10:
        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:5]  # Keep only top 5 scores
    return top_scores

# Check collision with the bodyguard’s own body or the edges
def check_collision():
    for segment in bodyguard_body[1:]:
        if head_pos == segment:
            return True
    return False

# Load top scores from file
def load_top_scores():
    try:
        with open("top_scores.txt", "r") as file:
            return [int(score.strip()) for score in file.readlines()]
    except FileNotFoundError:
        return []

# Save top scores to file
def save_top_scores(top_scores):
    with open("top_scores.txt", "w") as file:
        for score in top_scores:
            file.write(f"{score}\n")

# Function to move the police girl towards the bodyguard, but slower
def move_police_girl():
    global police_girl_pos
    diff_x = head_pos[0] - police_girl_pos[0]
    diff_y = head_pos[1] - police_girl_pos[1]
    
    # Slow down the movement by moving in smaller steps
    if abs(diff_x) > abs(diff_y):
        if diff_x > 0:
            police_girl_pos[0] += square_size // 2
        elif diff_x < 0:
            police_girl_pos[0] -= square_size // 2
    else:
        if diff_y > 0:
            police_girl_pos[1] += square_size // 2
        elif diff_y < 0:
            police_girl_pos[1] -= square_size // 2

# Main game loop
top_scores = load_top_scores()
game_running = False
selected_option = 0  # 0 = Start Game, 1 = Top Scores
game_over = False  # Флаг для проверки завершения игры

while True:
    if not game_running:
        show_main_menu(selected_option, top_scores)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game or show top scores
                    if selected_option == 0:  # Start game
                        init_vars()
                        game_running = True
                    elif selected_option == 1:  # Show top scores
                        game_window.fill(black)
                        show_top_scores(top_scores)
                        pygame.display.update()
                        pygame.time.delay(3000)  # Show top scores for 3 seconds
                elif event.key == pygame.K_UP:  # Navigate up
                    selected_option = (selected_option - 1) % 2
                elif event.key == pygame.K_DOWN:  # Navigate down
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_ESCAPE:  # Exit to main menu
                    game_running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, ord("w")]:
                    change_to = "UP"
                elif event.key in [pygame.K_DOWN, ord("s")]:
                    change_to = "DOWN"
                elif event.key in [pygame.K_LEFT, ord("a")]:
                    change_to = "LEFT"
                elif event.key in [pygame.K_RIGHT, ord("d")]:
                    change_to = "RIGHT"
        
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        elif change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        elif change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        elif change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
        
        # Bodyguard's movement
        if direction == "UP":
            head_pos[1] -= square_size
        elif direction == "DOWN":
            head_pos[1] += square_size
        elif direction == "LEFT":
            head_pos[0] -= square_size
        else:
            head_pos[0] += square_size
        
        if head_pos[0] < 0:
            head_pos[0] = frame_size_x - square_size
        elif head_pos[0] > frame_size_x - square_size:
            head_pos[0] = 0
        elif head_pos[1] < 0:
            head_pos[1] = frame_size_y - square_size
        elif head_pos[1] > frame_size_y - square_size:
            head_pos[1] = 0
        
        bodyguard_body.insert(0, list(head_pos))
        
        # Check for food and update game state
        if abs(head_pos[0] - food_pos[0]) < square_size and abs(head_pos[1] - food_pos[1]) < square_size:
            score += 1
            food_spawn = False

            # Bomb logic
            if score >= 3 and len(bombs) < 1:
                bombs.append([random.randrange(1, (frame_size_x // square_size)) * square_size,
                            random.randrange(1, (frame_size_y // square_size)) * square_size])
            elif score >= 7 and len(bombs) < 2:
                bombs.append([random.randrange(1, (frame_size_x // square_size)) * square_size,
                            random.randrange(1, (frame_size_y // square_size)) * square_size])
            elif score >= 10 and len(bombs) < 3:
                bombs.append([random.randrange(1, (frame_size_x // square_size)) * square_size,
                            random.randrange(1, (frame_size_y // square_size)) * square_size])

            if score >= 7 and not police_girl_active:
                police_girl_active = True

            if score < len(bodyguard):
                bodyguard_body.append(bodyguard_body[-1])
        else:
            bodyguard_body.pop()

        # Spawn food
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                        random.randrange(1, (frame_size_y // square_size)) * square_size]
            food_spawn = True

        # Fill window with game background
        game_window.fill(black)
        game_window.blit(game_bg, (0, 0))  # Фон игры
        
        for i, pos in enumerate(bodyguard_body):
            draw_emoji(bodyguard[min(i, len(bodyguard) - 1)], pos)
        
        draw_emoji("🤡", food_pos)
        
        # Police girl moves towards the bodyguard
        if police_girl_active:
            move_police_girl()
            draw_emoji("👮‍♀️", police_girl_pos)
            if head_pos == police_girl_pos:
                game_over = True  # Set game over flag when colliding with police girl
                break
        
        # Draw bombs
        for bomb in bombs:
            draw_emoji("💣", bomb)
            if head_pos == bomb:  
                game_over = True  # Set game over flag when colliding with bomb
                break
        
        # Check collision with body (Game Over condition)
        if check_collision():
            game_over = True  # Set game over flag when colliding with body
            break
        
        show_score()
        pygame.display.update()
        fps_controller.tick(speed)

    if game_over:
        top_scores = game_over_with_scores(top_scores)
        save_top_scores(top_scores)  # Save top scores
        game_running = False  # Reset game running flag
        game_over = False  # Reset game over flag
