# -*- coding: utf-8 -*-
"""Video_Describer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11F2DwDmZxd4CXpQb1pEoPF3szyiS79oS
"""

pip install torch torchvision torchaudio

import cv2
import torch
from transformers import SwinModel, AutoImageProcessor, GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image
import os

# Step 1: Upload video
video_path = input("Please provide the path to the video: ")

# Step 2: Extract every Nth frame from the video
def extract_frames(video_path, interval=30):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frames = []
    while success:
        if count % interval == 0:
            frame_path = f"frame{count}.jpg"
            cv2.imwrite(frame_path, image)
            frames.append(frame_path)
        success, image = vidcap.read()
        count += 1
    return frames

# Step 3: Extract features from frames
def extract_features(frames, feature_extractor, model):
    features = []
    for frame_path in frames:
        frame = Image.open(frame_path)
        inputs = feature_extractor(images=frame, return_tensors="pt")
        outputs = model(**inputs)
        features.append(outputs.last_hidden_state)
    return features

# Step 4: Generate descriptions
def generate_description(features, tokenizer, gpt2_model):
    descriptions = []
    for feature in features:
        input_ids = tokenizer.encode("Describe the following scene: ", return_tensors="pt")
        outputs = gpt2_model.generate(input_ids, max_length=150, num_return_sequences=1)
        description = tokenizer.decode(outputs[0], skip_special_tokens=True)
        descriptions.append(description)
    return descriptions

# Load models
feature_extractor = AutoImageProcessor.from_pretrained("microsoft/swin-tiny-patch4-window7-224")
swin_model = SwinModel.from_pretrained("microsoft/swin-tiny-patch4-window7-224")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

# Process video
frames = extract_frames(video_path, interval=30)  # Extract every 30th frame
features = extract_features(frames, feature_extractor, swin_model)
descriptions = generate_description(features, tokenizer, gpt2_model)

# Combine descriptions
video_description = " ".join(descriptions)
print("Video Description:")
print(video_description)

# Clean up frame files
for frame in frames:
    os.remove(frame)

# Step 1: Upload video
video_path = "/content/puzzle.mp4"

# Step 2: Extract frames from video
def extract_frames(video_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frames = []
    while success:
        frame_path = f"frame{count}.jpg"
        cv2.imwrite(frame_path, image)
        frames.append(frame_path)
        success, image = vidcap.read()
        count += 1
    return frames

# Step 3: Extract features from frames
def extract_features(frames, feature_extractor, model):
    features = []
    for frame_path in frames:
        frame = Image.open(frame_path)
        inputs = feature_extractor(images=frame, return_tensors="pt")
        outputs = model(**inputs)
        features.append(outputs.last_hidden_state)
    return features

# Step 4: Generate descriptions
def generate_description(features, tokenizer, gpt2_model):
    descriptions = []
    for feature in features:
        input_ids = tokenizer.encode("Describe the following scene: ", return_tensors="pt")
        outputs = gpt2_model.generate(input_ids, max_length=150, num_return_sequences=1)
        description = tokenizer.decode(outputs[0], skip_special_tokens=True)
        descriptions.append(description)
    return descriptions

# Load models
feature_extractor = AutoImageProcessor.from_pretrained("microsoft/swin-tiny-patch4-window7-224")
swin_model = SwinModel.from_pretrained("microsoft/swin-tiny-patch4-window7-224")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

# Process video
frames = extract_frames(video_path)
features = extract_features(frames, feature_extractor, swin_model)
descriptions = generate_description(features, tokenizer, gpt2_model)

# Combine descriptions
video_description = " ".join(descriptions)
print("Video Description:")
print(video_description)

# Clean up frame files
for frame in frames:
    os.remove(frame)