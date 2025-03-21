from flask import (
    Flask,
    request,
    send_file,
    jsonify,
)
from io import BytesIO
import torch
from diffusers import StableDiffusionPipeline
import time
import os

app = Flask(__name__)

print("CUDA available:", torch.cuda.is_available())

# 載入模型
model_id = "hakurei/waifu-diffusion"
device = "cuda" if torch.cuda.is_available() else "cpu"

torch_dtype = torch.float16 if device == "cuda" else torch.float32

# 使用模型
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    use_safetensors=True,
    torch_dtype=torch_dtype,
    add_watermarker=False,
    safety_checker=None,
)
pipe.enable_attention_slicing()
pipe = pipe.to(device)


@app.route("/generate", methods=["POST"])
def generate():
    print(f"使用設備: {device}")
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    negative_prompt = data.get("negative_prompt")
    if not negative_prompt:
        negative_prompt = ""

    width = data.get("width", 512)
    height = data.get("height", 512)
    steps = data.get("steps", 28)

    # 進行生成
    start = time.time()
    # 使用較大的批量大小和較高的步數
    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        guidance_scale=5,
        num_inference_steps=steps,
    ).images[0]
    end = time.time()
    print(f"生成時間: {end - start} 秒")

    # 將生成的圖片轉為 BytesIO
    image_byte_array = BytesIO()
    image.save(image_byte_array, format="PNG")
    image_byte_array.seek(0)

    folder = f"images/{time.strftime('%Y-%m-%d')}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 將生成的圖片儲存
    image.save(f"{folder}/{time.time()}.png")

    # 回傳圖片
    return send_file(image_byte_array, mimetype="image/png")


if __name__ == "__main__":
    # 運行於 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000)
