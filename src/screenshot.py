import cv2
import os
from datetime import datetime


class Screenshot:

    def __init__(self):

        self.folder = "screenshots"

        # Agar folder nahi hai to create karo
        if not os.path.isdir(self.folder):

            # Agar same naam ki file hai to hata do
            if os.path.exists(self.folder):
                os.remove(self.folder)

            os.mkdir(self.folder)

    def save(self, frame):

        filename = datetime.now().strftime(
            "portal_%Y%m%d_%H%M%S.png"
        )

        path = os.path.join(
            self.folder,
            filename
        )

        cv2.imwrite(path, frame)

        print(f"Screenshot Saved: {path}")