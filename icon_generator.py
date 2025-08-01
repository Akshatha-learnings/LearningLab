import base64
import boto3
import json
import os
import random
import logging
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import Optional

# Assuming these imports exist in your project
# from your_app.database import get_db
# from your_app.models import Icon

logger = logging.getLogger(__name__)

def generate_icon_image(description: str) -> bytes:
    """Generate an icon image using AWS Bedrock Stable Diffusion."""
    try:
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.environ.get("AWS_REGION"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
        )
        
        # Set the model ID for Stable Diffusion XL
        model_id = "stability.stable-diffusion-xl-v1"

        # Generate a random seed
        seed = random.randint(0, 4294967295)

        # Format the request payload using the model's native structure
        native_request = {
            "text_prompts": [{"text": f"Professional icon for {description}, simple, clean, modern design"}],
            "style_preset": "photographic",
            "seed": seed,
            "cfg_scale": 10,
            "steps": 30,
            "width": 512,  # Added for better icon dimensions
            "height": 512,
        }

        # Convert the native request to JSON
        request = json.dumps(native_request)

        # Invoke the model with the request
        response = client.invoke_model(modelId=model_id, body=request)

        # Decode the response body
        model_response = json.loads(response["body"].read())

        # Extract the image data
        base64_image_data = model_response["artifacts"][0]["base64"]
        
        return base64.b64decode(base64_image_data)
    
    except Exception as e:
        logger.error(f"Error generating icon image: {str(e)}")
        raise HTTPException(status_code=500, f"Failed to generate icon: {str(e)}")


class IconDBController:
    @staticmethod
    def save_generated_icon(image_bytes: bytes, db: Session) -> 'Icon':
        """Save generated icon to database."""
        try:
            # Assuming Icon model exists with icon_bytes field
            icon = Icon(icon_bytes=image_bytes)
            db.add(icon)
            db.commit()
            db.refresh(icon)
            logger.info(f"Successfully saved icon with ID: {icon.id}")
            return icon
        except Exception as e:
            logger.error(f"Error saving generated icon: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to save icon: {str(e)}")


def create_agent_with_icon(description: Optional[str], icon_id: Optional[int], db: Session) -> int:
    """Logic for creating agent with icon generation if needed."""
    if not icon_id and description:
        try:
            # Generate icon image
            image_bytes = generate_icon_image(description)
            
            # Save to database
            icon_obj = IconDBController.save_generated_icon(image_bytes=image_bytes, db=db)
            icon_id = icon_obj.id
            
            logger.info(f"Generated and saved new icon with ID: {icon_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate icon for agent: {str(e)}")
            # Depending on requirements, you might want to:
            # 1. Continue without icon (icon_id remains None)
            # 2. Use a default icon
            # 3. Raise the exception to fail agent creation
            raise
    
    return icon_id