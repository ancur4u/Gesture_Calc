import cv2

class Button:
    def __init__(self, pos, width, height, text):
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text
        self.hover_counter = 0
        self.pressed = False

    def draw(self, img):
        x, y = self.pos

        # Hover glow effect
        color = (255, 0, 255)
        if self.hover_counter > 0:
            glow_intensity = min(255, 100 + self.hover_counter * 10)
            color = (0, glow_intensity, 255)

        # Shadow rectangle
        cv2.rectangle(img, (x + 5, y + 5), (x + self.width + 5, y + self.height + 5), (30, 30, 30), -1)

        # Main button
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), color, cv2.FILLED)

        # Button text
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, 4, 4)[0]
        text_x = x + (self.width - text_size[0]) // 2
        text_y = y + (self.height + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        # Outline
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), (200, 200, 200), 2)

        return img

    def is_hover(self, x, y):
        return self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height