from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from typing import List
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()


# Serve images from directories './a' and './b'
os.makedirs('/home/wg25r/fastdata/frames/tmp', exist_ok=True)

app.mount("/a", StaticFiles(directory="/home/wg25r/fastdata/frames/tmp"), name="a")
app.mount("/b", StaticFiles(directory="/home/wg25r/fakedata/Gas-DB/visual_labels/"), name="b")

# Data structures to hold state
class ImagePair(BaseModel):
    id: int
    a_image: str  # URL to image in /a
    b_image: str  # URL to image in /b

class UserResponse(BaseModel):
    pair_id: str
    key: str  # 'left' or 'right'

image_pairs: List[ImagePair] = []
current_index = 0


import cv2
# On startup, load the image pairs
@app.on_event("startup")
def load_image_pairs():
    global image_pairs
    a_images = [i for i in sorted(os.listdir('/home/wg25r/fastdata/frames/images')) if not "_" in i]
    b_images = [i for i in sorted(os.listdir('/home/wg25r/fastdata/frames/labels')) if not "_" in i]
    if os.listdir('/home/wg25r/fastdata/frames/tmp') == []:
        for i in a_images:
            img = cv2.imread(f"/home/wg25r/fastdata/frames/images/{i}", cv2.IMREAD_UNCHANGED)
            alpha = img[:, :, 3]
            cv2.imwrite(f"/home/wg25r/fastdata/frames/tmp/{i}", alpha)
        a_images = [i for i in sorted(os.listdir('/home/wg25r/fastdata/frames/tmp')) if not "_" in i]


    # Assuming images have matching filenames
    common_images = set(a_images).intersection(b_images)
    image_pairs = []
    for idx, filename in enumerate(sorted(common_images)):
        a_image_url = f"/a/{filename}"
        b_image_url = f"/b/{filename}"
        image_pairs.append(ImagePair(id=idx, a_image=a_image_url, b_image=b_image_url))
    print(f"Loaded {len(image_pairs)} image pairs.")

# Endpoint to get the next image pair
@app.get("/next_pair")
def get_next_pair():
    global current_index
    if current_index >= len(image_pairs):
        raise HTTPException(status_code=404, detail="No more image pairs.")
    pair = image_pairs[current_index]
    return pair
 

@app.get("/last_pair")
def get_last_pair():
    global current_index
    current_index -= 1
    if current_index == 0:
        raise HTTPException(status_code=404, detail="No more image pairs.")
    pair = image_pairs[current_index]
    return pair

# Endpoint to record user's key press
@app.post("/record_response")
def record_response(response: UserResponse):
    global current_index
    current_index += 1
    # For simplicity, just print the response
    print(f"Received response: {response}")
    # You may want to save this to a file or database
    # to a file 
    with open("responses.txt", "a") as f:
        f.write(f"Received response: {response}\n")
    return {"status": "success"}
