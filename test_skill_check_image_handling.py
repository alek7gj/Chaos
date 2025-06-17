import os
import shutil
import subprocess
import time
import pyautogui
import pytest
from PIL import Image, ImageChops
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

task_name = "Skill Check"
INPUT = "input"
OUTPUT = "output"
IMAGE_1 = os.path.join(INPUT, "IMAGE_1.png")
IMAGE_2 = os.path.join(INPUT, "IMAGE_2.png")  # ← Renamed from MAGE
NEW_IMAGE = os.path.join(OUTPUT, "NEW.png")
EXPORT_JPG = os.path.join(OUTPUT, "EXPORT.jpg")
DIFF_IMAGE = os.path.join(OUTPUT, "diff.png")

PAINTNET_EXE = r"C:\Program Files\paint.net\PaintDotNet.exe"

@pytest.fixture(scope="session", autouse=True)
def setup_folders():
    os.makedirs(INPUT, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)
    generate_sample_images()
    yield

def generate_sample_images():
    if not os.path.exists(IMAGE_1):
        raise FileNotFoundError(f"input/IMAGE_1.png is missing at: {IMAGE_1}")
    if not os.path.exists(IMAGE_2):
        raise FileNotFoundError(f"input/IMAGE_2.png is missing at: {IMAGE_2}")

def open_paintnet_with_image(image_path):
    subprocess.Popen([PAINTNET_EXE, os.path.abspath(image_path)])
    time.sleep(5)

def save_file_as(path, filetype="PNG"):
    pyautogui.hotkey("ctrl", "shift", "s")
    time.sleep(2)
    pyautogui.write(os.path.abspath(path))
    time.sleep(1)

    if filetype.upper() == "JPG":
        pyautogui.press("tab", presses=2)
        pyautogui.press("down", presses=1)
        time.sleep(1)

    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)

def close_paintnet():
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    pyautogui.press("right")
    pyautogui.press("enter")
    time.sleep(2)

def images_are_equal(img1_path, img2_path):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    return ImageChops.difference(img1, img2).getbbox() is None

def compare_images_ssim(img1_path, img2_path, diff_output=None):
    imageA = cv2.imread(img1_path)
    imageB = cv2.imread(img2_path)

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    score, diff = ssim(grayA, grayB, full=True)
    if diff_output:
        diff = (diff * 255).astype("uint8")
        cv2.imwrite(diff_output, diff)
    return score

def test_paintnet_image_handling():
    print(f"Starting '{task_name}'...")
    open_paintnet_with_image(IMAGE_1)

    save_file_as(NEW_IMAGE, "PNG")

    assert images_are_equal(IMAGE_1, NEW_IMAGE), "❌ Baseline comparison failed."

    save_file_as(EXPORT_JPG, "JPG")

    assert os.path.exists(EXPORT_JPG), "❌ Exported JPG does not exist."


    similarity = compare_images_ssim(EXPORT_JPG, IMAGE_2, diff_output=DIFF_IMAGE)
    assert similarity < 0.99, f"❌ Unexpected match (SSIM: {similarity:.4f})"

    close_paintnet()
    print(f"'{task_name}' completed successfully.")