from flask import Flask, request, send_file, jsonify
from io import BytesIO
import torch
from diffusers import StableDiffusion3Pipeline
import time

app = Flask(__name__)

# 選擇運行裝置，如果有 GPU 建議使用 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-medium",
    torch_dtype=torch.float32 if device == "cpu" else torch.float16,
    revision="fp16" if device == "cuda" else None,
)
pipe = pipe.to(device)


@app.route("/generate", methods=["POST"])
def generate():
    timer = time.time()
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # 產生圖片
    image = pipe(prompt).images[0]

    # 將圖片存入記憶體的 buffer 並輸出為 PNG
    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    print(f"Time: {time.time() - timer}")
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    # 運行於 0.0.0.0:5000，供外部存取，或改為 127.0.0.1
    app.run(host="0.0.0.0", port=5000)
