 
import turtle
import random

# =========================================================
# GAME WINDOW
# =========================================================

screen = turtle.Screen()
screen.title("SPACE SHOOTER")
screen.bgcolor("#02020f")
screen.setup(width=800, height=600)


# =========================================================
# GAME VARIABLES
# =========================================================

score = 0
lives = 3
level = 1

enemy_speed = 2

game_over = False
shield_active = False
triple_shot = False

boss_active = False
boss_defeated = False
boss_health = 30

enemies = []


# =========================================================
# STARS
# =========================================================

stars = []

for i in range(70):

    star = turtle.Turtle()
    star.shape("circle")
    star.color("white")
    star.shapesize(0.08)
    star.penup()

    star.goto(
        random.randint(-390, 390),
        random.randint(-280, 280)
    )

    stars.append(star)


# =========================================================
# SCORE DISPLAY
# =========================================================

score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-380, 260)

score_display.write(
    "SCORE: 0",
    font=("Arial", 15, "bold")
)


# =========================================================
# LIVES DISPLAY
# =========================================================

lives_display = turtle.Turtle()
lives_display.hideturtle()
lives_display.color("#00ff66")
lives_display.penup()
lives_display.goto(180, 260)

lives_display.write(
    "LIVES: 3",
    font=("Arial", 15, "bold")
)


# =========================================================
# LEVEL DISPLAY
# =========================================================

level_display = turtle.Turtle()
level_display.hideturtle()
level_display.color("#00ccff")
level_display.penup()
level_display.goto(-70, 260)

level_display.write(
    "LEVEL: 1",
    font=("Arial", 15, "bold")
)


# =========================================================
# POWER-UP DISPLAY
# =========================================================

power_display = turtle.Turtle()
power_display.hideturtle()
power_display.color("yellow")
power_display.penup()
power_display.goto(-100, 220)


# =========================================================
# PLAYER SPACE SHIP
# =========================================================

player = turtle.Turtle()

player.shape("triangle")
player.color("#00ffff")

player.shapesize(
    stretch_wid=1.8,
    stretch_len=1.8
)

player.penup()
player.goto(0, -230)
player.setheading(90)


# =========================================================
# ENEMIES
# =========================================================

enemy_colors = [
    "#ff3030",
    "#ff00ff",
    "#ff6600",
    "#9900ff"
]

for i in range(8):

    enemy = turtle.Turtle()

    enemy.shape("square")
    enemy.color(
        random.choice(enemy_colors)
    )

    enemy.shapesize(
        stretch_wid=1.2,
        stretch_len=1.5
    )

    enemy.penup()

    enemy.goto(
        random.randint(-350, 350),
        random.randint(50, 280)
    )

    enemies.append(enemy)


# =========================================================
# BOSS
# =========================================================

boss = turtle.Turtle()

boss.shape("square")
boss.color("#ff0000")

boss.shapesize(
    stretch_wid=3,
    stretch_len=5
)

boss.penup()
boss.goto(0, 230)
boss.hideturtle()


boss_health_display = turtle.Turtle()
boss_health_display.hideturtle()
boss_health_display.color("red")
boss_health_display.penup()
boss_health_display.goto(-100, 190)


# =========================================================
# PLAYER MOVEMENT
# =========================================================

def move_left():

    if game_over:
        return

    if player.xcor() > -370:
        player.setx(
            player.xcor() - 25
        )


def move_right():

    if game_over:
        return

    if player.xcor() < 370:
        player.setx(
            player.xcor() + 25
        )


# =========================================================
# EXPLOSION
# =========================================================

def explosion(x, y):

    boom = turtle.Turtle()

    boom.shape("circle")
    boom.color("orange")
    boom.shapesize(1.8)
    boom.penup()
    boom.goto(x, y)

    screen.ontimer(
        boom.hideturtle,
        180
    )


# =========================================================
# POWER-UP
# =========================================================

def create_powerup(x, y):

    if random.randint(1, 100) > 30:
        return

    power = turtle.Turtle()

    power.shape("circle")
    power.shapesize(0.9)
    power.penup()

    power_type = random.choice(
        ["life", "shield", "triple"]
    )

    if power_type == "life":
        power.color("lime")

    elif power_type == "shield":
        power.color("blue")

    else:
        power.color("yellow")

    power.power_type = power_type

    power.goto(x, y)

    move_powerup(power)


def move_powerup(power):

    if game_over:

        power.hideturtle()
        return

    power.sety(
        power.ycor() - 4
    )

    if power.distance(player) < 30:

        activate_powerup(
            power.power_type
        )

        power.hideturtle()
        return

    if power.ycor() < -300:

        power.hideturtle()
        return

    screen.ontimer(
        lambda: move_powerup(power),
        30
    )


# =========================================================
# ACTIVATE POWER-UP
# =========================================================

def activate_powerup(power_type):

    global lives
    global shield_active
    global triple_shot

    if power_type == "life":

        if lives < 5:
            lives += 1

        lives_display.clear()

        lives_display.write(
            "LIVES: " + str(lives),
            font=("Arial", 15, "bold")
        )

        power_display.clear()

        power_display.write(
            "+1 LIFE",
            font=("Arial", 15, "bold")
        )

    elif power_type == "shield":

        shield_active = True

        power_display.clear()

        power_display.write(
            "SHIELD ACTIVE!",
            font=("Arial", 15, "bold")
        )

        screen.ontimer(
            remove_shield,
            6000
        )

    elif power_type == "triple":

        triple_shot = True

        power_display.clear()

        power_display.write(
            "TRIPLE SHOT!",
            font=("Arial", 15, "bold")
        )

        screen.ontimer(
            remove_triple_shot,
            8000
        )


def remove_shield():

    global shield_active

    shield_active = False
    power_display.clear()


def remove_triple_shot():

    global triple_shot

    triple_shot = False
    power_display.clear()


# =========================================================
# PLAYER SHOOTING
# =========================================================

def shoot():

    if game_over:
        return

    if triple_shot:

        create_bullet(-18)
        create_bullet(0)
        create_bullet(18)

    else:

        create_bullet(0)


def create_bullet(offset):

    bullet = turtle.Turtle()

    bullet.shape("circle")
    bullet.color("yellow")
    bullet.shapesize(0.5)
    bullet.penup()

    bullet.goto(
        player.xcor() + offset,
        player.ycor() + 20
    )

    move_player_bullet(bullet)


# =========================================================
# PLAYER BULLET MOVEMENT
# =========================================================

def move_player_bullet(bullet):

    global score
    global enemy_speed
    global boss_health

    if game_over:

        bullet.hideturtle()
        return

    bullet.sety(
        bullet.ycor() + 12
    )

    # Hit boss
    if boss_active and not boss_defeated:

        if bullet.distance(boss) < 70:

            bullet.hideturtle()

            boss_health -= 1

            explosion(
                boss.xcor(),
                boss.ycor()
            )

            boss_health_display.clear()

            boss_health_display.write(
                "BOSS HP: " + str(boss_health),
                font=("Arial", 15, "bold")
            )

            if boss_health <= 0:
                defeat_boss()

            return

    # Hit enemies
    for enemy in enemies:

        if bullet.distance(enemy) < 25:

            x = enemy.xcor()
            y = enemy.ycor()

            bullet.hideturtle()

            explosion(x, y)
            create_powerup(x, y)

            enemy.goto(
                random.randint(-350, 350),
                random.randint(180, 300)
            )

            score += 10
            enemy_speed += 0.1

            update_score()
            check_level()

            return

    if bullet.ycor() > 300:

        bullet.hideturtle()
        return

    screen.ontimer(
        lambda: move_player_bullet(bullet),
        20
    )


# =========================================================
# SCORE
# =========================================================

def update_score():

    score_display.clear()

    score_display.write(
        "SCORE: " + str(score),
        font=("Arial", 15, "bold")
    )


# =========================================================
# LEVEL
# =========================================================

def check_level():

    global level
    global enemy_speed

    new_level = (score // 100) + 1

    if new_level > level:

        level = new_level
        enemy_speed += 0.5

        level_display.clear()

        level_display.write(
            "LEVEL: " + str(level),
            font=("Arial", 15, "bold")
        )

    if score >= 500 and not boss_active and not boss_defeated:

        start_boss()


# =========================================================
# ENEMY MOVEMENT
# =========================================================

def move_enemies():

    if game_over:
        return

    for enemy in enemies:

        enemy.sety(
            enemy.ycor() - enemy_speed
        )

        if enemy.ycor() < -280:

            enemy.goto(
                random.randint(-350, 350),
                random.randint(180, 300)
            )

    screen.ontimer(
        move_enemies,
        30
    )


# =========================================================
# 🔴 ENEMY SHOOTING
# =========================================================

def enemy_shoot():

    if game_over:
        return

    # Pick a random enemy
    enemy = random.choice(enemies)

    # Create red enemy bullet
    bullet = turtle.Turtle()

    bullet.shape("circle")
    bullet.color("#ff2222")

    bullet.shapesize(
        stretch_wid=0.6,
        stretch_len=0.6
    )

    bullet.penup()

    # Bullet starts directly underneath enemy
    bullet.goto(
        enemy.xcor(),
        enemy.ycor() - 20
    )

    # Move the bullet toward the player
    move_enemy_bullet(bullet)

    # Another enemy shoots after a short delay
    screen.ontimer(
        enemy_shoot,
        random.randint(500, 1000)
    )


# =========================================================
# 🔴 ENEMY BULLET MOVEMENT
# =========================================================

def move_enemy_bullet(bullet):

    global lives

    if game_over:

        bullet.hideturtle()
        return

    # Move red bullet DOWN
    bullet.sety(
        bullet.ycor() - 9
    )

    # Hit spaceship
    if bullet.distance(player) < 25:

        bullet.hideturtle()

        # Shield protects spaceship
        if shield_active:

            power_display.clear()

            power_display.write(
                "SHIELD BLOCKED!",
                font=("Arial", 15, "bold")
            )

            return

        # Lose one life
        lives -= 1

        lives_display.clear()

        lives_display.write(
            "LIVES: " + str(lives),
            font=("Arial", 15, "bold")
        )

        # Game over
        if lives <= 0:

            end_game()

        return

    # Bullet leaves screen
    if bullet.ycor() < -300:

        bullet.hideturtle()
        return

    # Continue moving bullet
    screen.ontimer(
        lambda: move_enemy_bullet(bullet),
        20
    )


# =========================================================
# BOSS
# =========================================================

def start_boss():

    global boss_active
    global boss_health

    boss_active = True
    boss_health = 30

    boss.goto(0, 230)
    boss.showturtle()

    boss_health_display.clear()

    boss_health_display.write(
        "BOSS HP: 30",
        font=("Arial", 15, "bold")
    )

    power_display.clear()

    power_display.write(
        "BOSS INCOMING!",
        font=("Arial", 15, "bold")
    )

    move_boss()
    boss_shoot()


def move_boss():

    if game_over or not boss_active:
        return

    if boss.xcor() >= 300:
        boss.setheading(180)

    elif boss.xcor() <= -300:
        boss.setheading(0)

    boss.forward(4)

    screen.ontimer(
        move_boss,
        30
    )


# =========================================================
# BOSS SHOOTING
# =========================================================

def boss_shoot():

    if game_over or not boss_active:
        return

    for offset in [-30, 0, 30]:

        bullet = turtle.Turtle()

        bullet.shape("circle")
        bullet.color("#ff00ff")
        bullet.shapesize(0.7)
        bullet.penup()

        bullet.goto(
            boss.xcor() + offset,
            boss.ycor() - 50
        )

        move_enemy_bullet(bullet)

    screen.ontimer(
        boss_shoot,
        1200
    )


# =========================================================
# DEFEAT BOSS
# =========================================================

def defeat_boss():

    global boss_active
    global boss_defeated
    global score

    boss_active = False
    boss_defeated = True

    explosion(
        boss.xcor(),
        boss.ycor()
    )

    boss.hideturtle()

    boss_health_display.clear()

    power_display.clear()

    power_display.write(
        "BOSS DESTROYED! +500",
        font=("Arial", 15, "bold")
    )

    score += 500

    update_score()


# =========================================================
# GAME OVER
# =========================================================

game_over_text = turtle.Turtle()

game_over_text.hideturtle()
game_over_text.penup()


def end_game():

    global game_over

    game_over = True

    game_over_text.color("red")

    game_over_text.goto(
        0,
        60
    )

    game_over_text.write(
        "GAME OVER",
        align="center",
        font=("Arial", 38, "bold")
    )

    game_over_text.goto(
        0,
        10
    )

    game_over_text.color("white")

    game_over_text.write(
        "FINAL SCORE: " + str(score),
        align="center",
        font=("Arial", 20, "bold")
    )

    game_over_text.goto(
        0,
        -40
    )

    game_over_text.write(
        "Press R to Restart",
        align="center",
        font=("Arial", 16, "normal")
    )


# =========================================================
# RESTART
# =========================================================

def restart():

    global score
    global lives
    global level
    global enemy_speed
    global game_over
    global shield_active
    global triple_shot
    global boss_active
    global boss_defeated
    global boss_health

    if not game_over:
        return

    score = 0
    lives = 3
    level = 1
    enemy_speed = 2

    game_over = False
    shield_active = False
    triple_shot = False

    boss_active = False
    boss_defeated = False
    boss_health = 30

    game_over_text.clear()

    boss.hideturtle()
    boss_health_display.clear()
    power_display.clear()

    score_display.clear()

    score_display.write(
        "SCORE: 0",
        font=("Arial", 15, "bold")
    )

    lives_display.clear()

    lives_display.write(
        "LIVES: 3",
        font=("Arial", 15, "bold")
    )

    level_display.clear()

    level_display.write(
        "LEVEL: 1",
        font=("Arial", 15, "bold")
    )

    player.goto(
        0,
        -230
    )

    for enemy in enemies:

        enemy.showturtle()

        enemy.goto(
            random.randint(-350, 350),
            random.randint(50, 280)
        )

    move_enemies()


# =========================================================
# CONTROLS
# =========================================================

screen.listen()

screen.onkeypress(
    move_left,
    "Left"
)

screen.onkeypress(
    move_right,
    "Right"
)

screen.onkeypress(
    shoot,
    "space"
)

screen.onkeypress(
    restart,
    "r"
)


# =========================================================
# START GAME
# =========================================================

move_enemies()

enemy_shoot()

turtle.mainloop()