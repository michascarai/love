import math
import turtle

screen = turtle.Screen()
screen.setup(800, 800)
screen.bgcolor("black")
screen.setworldcoordinates(-220, -220, 220, 220)
screen.tracer(0)

heart = turtle.Turtle()
heart.hideturtle()
heart.penup()


def prepare_love_layer(scale, color, font_size):
    points = []
    for angle in range(361):
        theta = math.radians(angle)
        x = 16 * math.sin(theta) ** 3
        y = (
            13 * math.cos(theta)
            - 5 * math.cos(2 * theta)
            - 2 * math.cos(3 * theta)
            - math.cos(4 * theta)
        )
        points.append((x * scale, y * scale))

    distances = [0]
    for previous, current in zip(points, points[1:]):
        distances.append(
            distances[-1] + math.dist(previous, current)
        )

    perimeter = distances[-1]
    word_count = max(1, round(perimeter / 34))
    words = []
    segment_index = 0

    for index in range(word_count):
        target_distance = index * perimeter / word_count
        while distances[segment_index + 1] < target_distance:
            segment_index += 1

        start = points[segment_index]
        end = points[segment_index + 1]
        segment_length = distances[segment_index + 1] - distances[segment_index]
        fraction = (target_distance - distances[segment_index]) / segment_length
        x = start[0] + (end[0] - start[0]) * fraction
        y = start[1] + (end[1] - start[1]) * fraction

        heading = math.degrees(math.atan2(end[1] - start[1], end[0] - start[0]))
        if heading > 90 or heading < -90:
            heading += 180

        words.append((x, y, heading))

    return color, font_size, words


layer_settings = [
    (5.2, "#ff4d8d", 9),
    (6.4, "#ff80ab", 10),
    (7.6, "#ffb6c1", 11),
    (8.8, "#ffe0e8", 12),
]

layers = [prepare_love_layer(*settings) for settings in layer_settings]
frame = 0


def shade_color(color, brightness):
    red = int(int(color[1:3], 16) * brightness)
    green = int(int(color[3:5], 16) * brightness)
    blue = int(int(color[5:7], 16) * brightness)
    return f"#{red:02x}{green:02x}{blue:02x}"


def animate_heart():
    global frame

    heart.clear()
    elapsed = frame * 0.08

    for layer_index, (color, font_size, words) in enumerate(layers):
        for word_index, (x, y, heading) in enumerate(words):
            phase = (elapsed + word_index * 0.045 + layer_index * 0.2) % 2.4
            if phase >= 1.2:
                continue

            fade = min(phase / 0.25, (1.2 - phase) / 0.3, 1)
            heart.color(shade_color(color, 0.35 + 0.65 * fade))
            heart.goto(x, y)
            heart.setheading(heading)
            heart.write("love", align="center", font=("Arial", font_size, "bold"))

    frame += 1
    screen.update()
    screen.ontimer(animate_heart, 80)


animate_heart()
screen.mainloop()
