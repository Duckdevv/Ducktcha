import io
import os
import random
import string
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class CaptchaGenerator:

  def __init__(
      self, width=350, height=150, font_path='font.ttf', font_size=80
  ):
    self.width = width
    self.height = height

    base_dir = os.path.dirname(os.path.abspath(__file__))
    self.font_path = os.path.join(base_dir, font_path)
    self.font_size = font_size

  def generate_code(self, length=5):
    chars = string.ascii_uppercase.replace('O', '').replace('I', '') + '23456789'
    return ''.join(random.choices(chars, k=length))

  def create_image(self):
    text = self.generate_code()
    num_frames = 3

    mask_img = Image.new('L', (self.width, self.height), 0)
    draw = ImageDraw.Draw(mask_img)

    try:
      font = ImageFont.truetype(self.font_path, self.font_size)
    except OSError:
      try:
        font = ImageFont.load_default(size=self.font_size)
      except TypeError:
        font = ImageFont.load_default()

    center_x = self.width // 2
    center_y = self.height // 2
    draw.text((center_x, center_y), text, fill=255, font=font, anchor='mm')

    text_mask = np.array(mask_img) > 10

    bg_noise = np.random.choice(
        [0, 255], size=(self.height, self.width)
    ).astype(np.uint8)
    text_noise = np.random.choice(
        [0, 255], size=(self.height, self.width)
    ).astype(np.uint8)

    frames = []
    for i in range(num_frames):
      shifted_bg = np.roll(bg_noise, shift=i, axis=0)
      shifted_text = np.roll(text_noise, shift=-i, axis=0)
      frame_data = np.where(text_mask, shifted_text, shifted_bg)
      frames.append(Image.fromarray(frame_data, mode='L'))

    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
    )
    buffer.seek(0)

    return text, buffer
