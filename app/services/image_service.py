import requests


class ImageService:
    @staticmethod
    def upload_images_to_imgbb(image_files):
        url = 'https://api.imgbb.com/1/upload'
        payload = {
            'key': "6767332c505eef11068e4bfd1629b11c"  # your ImgBB API key
        }

        image_urls = []

        for image_file in image_files:
            files = {'image': image_file}

            try:
                response = requests.post(url, data=payload, files=files)
                response_data = response.json()

                print("Response Data:", response_data)

                if "data" in response_data and "display_url" in response_data["data"]:
                    image_urls.append(response_data["data"]["display_url"])
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

        return image_urls  # ✅ Always return as list
