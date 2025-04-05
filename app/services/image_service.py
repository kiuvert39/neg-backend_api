import requests


class ImageService:
    @staticmethod
    def upload_images_to_imgbb(image_files):
        url = 'https://api.imgbb.com/1/upload'
        payload = {
            'key': "6767332c505eef11068e4bfd1629b11c"  # your ImgBB API key
        }

        image_urls = []  # List to store the URLs of uploaded images

        for image_file in image_files:
            files = {'image': image_file}

            try:
                response = requests.post(url, data=payload, files=files)
                response_data = response.json()

                print("Response Data:", response_data)  # Debugging: print the response

                # Check if 'data' and 'display_url' exist in the response
                if "data" in response_data and "display_url" in response_data["data"]:
                    image_urls.append(response_data["data"]["display_url"])  # Add the image URL to the list
                else:
                    print("⚠️ ImgBB Upload Failed:", response_data)
                    image_urls.append({
                        "error": "Failed to upload image",
                        "details": response_data.get("error", response_data)
                    })

            except requests.RequestException as e:
                image_urls.append({
                    "error": f"Error uploading image: {str(e)}"
                })

        if len(image_urls) == 1:
            return image_urls[0]  # Return the first image URL for a single image
        return image_urls  # Return the list of image URLs or error details
