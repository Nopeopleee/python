from flask import Flask, request, send_file, jsonify
from io import BytesIO
import torch
from diffusers import StableDiffusionPipeline
import time

app = Flask(__name__)

# 載入模型
model_id = "hakurei/waifu-diffusion"
device = "cpu"

# 使用模型
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, revision="fp32", torch_dtype=torch.float32
)
pipe = pipe.to(device)


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # 進行生成
    start = time.time()
    image = pipe(prompt).images[0]
    end = time.time()
    print(f"Time: {end - start}")

    # 將生成的圖片轉為 BytesIO
    image_byte_array = BytesIO()
    image.save(image_byte_array, format="PNG")
    image_byte_array.seek(0)

    return send_file(image_byte_array, mimetype="image/png")


if __name__ == "__main__":
    # 運行於 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000)
