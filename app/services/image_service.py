import requests
from app.config import Config

class ImageService:
    @staticmethod
    def upload_image_to_imgbb(image_file):
        url = 'https://api.imgbb.com/1/upload'
        
        # Prepare the payload with your API key
        payload = {
            'key': "6767332c505eef11068e4bfd1629b11c"  # your ImgBB API key
        }
        
        # Prepare the files part with the image file
        files = {'image': image_file}
        
        try:
            # Send the POST request with payload and image
            response = requests.post(url, data=payload, files=files)
            
            # Parse the response JSON
            response_data = response.json()
            if not response_data:
                return {"error": "Failed to upload image"}, 500
            
            url = response_data['data']['display_url']
            return url
                
        except requests.RequestException as e:
            # Return an error message in case of a request exception
            return {"error": f"Error uploading image: {str(e)}"}, 500