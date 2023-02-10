# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import openai
import replicate
import urllib.request
import schedule
from datetime import datetime

def download_image(url, file_path, file_name):
    print(url)
    full_path = file_path + file_name + '.jpg'
    print(full_path)
    urllib.request.urlretrieve(url, full_path)


def drawing():
    print("start drawing at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    openai.api_key = "YOUR_API_KEY_HERE"
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt="give a random description of a picture",
    )
    print(completion.choices[0].text)
    rc = replicate.Client(api_token='YOU_API_TOKEN_HERE')
    model = rc.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")

    # https://replicate.com/stability-ai/stable-diffusion/versions/f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1#input
    inputs = {
        # Input prompt
        'prompt': completion.choices[0].text,

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Width of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'width': 1024,

        # Height of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'height': 768,

        # Prompt strength when using init image. 1.0 corresponds to full
        # destruction of information in init image
        'prompt_strength': 0.8,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 300,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }

    # https://replicate.com/stability-ai/stable-diffusion/versions/f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1#output-schema
    output = version.predict(**inputs)
    current_date = datetime.now()
    download_image(output[0], 'images/', current_date.year + current_date.month + current_date.day)


schedule.every(2).minutes.do(drawing)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
