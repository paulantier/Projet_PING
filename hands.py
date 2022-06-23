#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:29:41 2022

@author: nicolasnicolas
"""
import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

# fname = 'Mains/imag.png'
# image = Image.open(fname).convert("L")
# arr = np.asarray(image)
# plt.imshow(arr, cmap='pink_r', vmin=0, vmax=255)
# plt.axis('off')
# plt.savefig('test.png', bbox_inches='tight')
# plt.show()
im_gray = cv2.imread("imag.png", cv2.IMREAD_GRAYSCALE)
im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_PINK)
cv2.imshow('test.png', im_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('test.png', im_color)

# For static images:
IMAGE_FILES = ["test.png"]
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.imread(file)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
  all_x, all_y = [], [] # store all x and y points in list
  for hnd in mp_hands.HandLandmark:
      all_x.append(int(hand_landmarks.landmark[hnd].x * image.shape[1])) # multiply x by image width
      all_y.append(int(hand_landmarks.landmark[hnd].y * image.shape[0])) # multiply y by image height
  tab = [all_x,all_y]
  dist = np.sqrt((all_x[1]-all_x[0])**2+(all_y[1]-all_y[0])**2)
  print(tab)
  print(dist)

