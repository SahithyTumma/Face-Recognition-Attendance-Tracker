import cv2
import io
import json
import sys
import time
from PIL import ImageFont
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, QualityForRecognition

credential = json.load(open('apps/home/AzureCloudKeys.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']


face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        if(success):
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
            return jpeg.tobytes(), success
        else:
            self.video.release()
            cv2.destroyAllWindows()
            return "NONE", success

    def recognize(self, persongroupid):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        image1 = jpeg.tobytes()
        image1 = io.BytesIO(image1)
        face_ids = []
        faces = face_client.face.detect_with_stream(
            image=image1, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
        for face in faces:
            if face.face_attributes.quality_for_recognition == QualityForRecognition.high or face.face_attributes.quality_for_recognition == QualityForRecognition.medium:
                face_ids.append(face.face_id)
        if(len(face_ids)):
            results = face_client.face.identify(
                face_ids, person_group_id=persongroupid)
            if not results:
                self.video.release()
                cv2.destroyAllWindows()
                return 'Please keep your face in front of camera'
            font = ImageFont.truetype(
                'C:\\Users\\sahit\\Desktop\\Open_Sans\\static\\OpenSans\\OpenSans-Bold.ttf', 25)
            for person in results:
                if len(person.candidates) > 0:
                    a = face_client.person_group_person.get(
                        person_group_id=persongroupid, person_id=person.candidates[0].person_id)
                    # print('Person {} for face ID {} is identified with a confidence of {}.'.format(
                    #     a.name, person.face_id, person.candidates[0].confidence))
                    self.video.release()
                    cv2.destroyAllWindows()
                    return str(a.name)
                else:
                    self.video.release()
                    cv2.destroyAllWindows()
                    return 'No person identified'
        else:
            self.video.release()
            cv2.destroyAllWindows()
            return "Bad Argument"

    def capture(self, person_id, persongroupid):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        image2 = jpeg.tobytes()
        image1 = io.BytesIO(image2)
        sufficientQuality = True
        detected_faces = face_client.face.detect_with_stream(
            image=image1, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
        if(len(detected_faces)):
            for face in detected_faces:
                if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
                    sufficientQuality = False
                    return False
            face_client.person_group_person.add_face_from_stream(persongroupid, person_id, io.BytesIO(image2))
            face_client.person_group.train(person_group_id=persongroupid)
            while (True):
                training_status = face_client.person_group.get_training_status(
                    person_group_id=persongroupid)
                if (training_status.status is TrainingStatusType.succeeded):
                    break
                elif (training_status.status is TrainingStatusType.failed):
                    sys.exit('Training the person group has failed.')
                time.sleep(5)
            return True
        else:
            return False
