import io
import os
from dotenv import load_dotenv
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Load API Key
load_dotenv(dotenv_path='../Data/.env')
DREAMSTUDIO = os.getenv('DREAMSTUDIO_API')

def generate_image(text):
    stability_api = client.StabilityInference(
        key=DREAMSTUDIO,
        verbose=True,
        engine="stable-diffusion-xl-1024-v1-0"  # Required engine
    )

    # Generate image
    answers = stability_api.generate(
        prompt=text,
        seed=95456  # Makes results deterministic
    )

    # Iterate over the response
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("WARNING: Request blocked due to safety filters. Modify prompt and try again.")
                return
            elif artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))  # Ensure correct attribute
                img.show()

