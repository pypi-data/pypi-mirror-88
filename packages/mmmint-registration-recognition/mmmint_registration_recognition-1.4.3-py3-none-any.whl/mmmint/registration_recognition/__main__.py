import os
import time

from sdk import Client, Status


def main():
    apikey = os.environ.get("API_KEY", "")

    # Create an Endpoint with your Credentials
    client = Client(apikey)

    # Post Fahrzeugschein from local Image
    #image_path = "4.jpg"
    # client.post_image(image_path)
    # print(client.session)

    # Post Fahrzeugschein from URL
    image_url = "https://deinautoguide.de/wp-content/uploads/2020/06/Fahrzeugschein-Aventador.jpg"
    # client.new_fahrzeugschein_url(image_url)
    client.session = '28ea1770c52c9c5d508b7c4e3c715fae739c97d4dfa615ff847822aebf1804d2'
    print(client.session)

    # Get Status of Calculation
    while client.status == Status.STARTED.value:
        client.get_fahrzeugschein_status()
        time.sleep(2)

    # Get Results of Fahrzeugschein
    if client.status == Status.FINISHED.value:
        client.get_fahrzeugschein()

        for i in client.fahrzeugschein:
            print(i, ": ", client.fahrzeugschein[i])

        bb = client.get_detection_bounding_boxes()
        di = client.get_detection_image()
        ci = client.get_detection_cropped_image()
        print(bb)
        print(di)
        print(ci)

    # TODO: client.edit_fahrzeugschein()


if __name__ == "__main__":
    # execute only if run as a script
    main()
