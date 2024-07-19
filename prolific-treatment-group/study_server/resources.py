import falcon
from dacite import from_dict, DaciteError
from falcon import Request, Response
import pendulum
import json
from study_server.expected import ConsentGet, StudyPost, CompleteGet, TutorialGet, TutorialPost, TutorialPost2, TutorialGet2, FormPost
from study_server.db_definitions import Participant, FormData

import io
class ConsentResource:
    consent_path: str

    def __init__(self, consent_path):
        self.consent_path = consent_path

    def on_get(self, req: Request, resp: Response):  # noqa
        try:
            request: ConsentGet = from_dict(ConsentGet, req.params)  # noqa
            session = req.env["beaker.session"]

            # check if the file exists and return a 404 if it doesn't
            try:
                with open(self.consent_path, "rb") as file:
                    # read the contents of the file and replace the placeholders
                    contents = file.read()
                    contents = contents.replace(b"#PROLIFIC_ID#", request.prolific_id.encode())
                    contents = contents.replace(b"#SESSION_ID#", session.id.encode())
                    # provide the HTML response
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_OK
                    resp.text = contents
            except FileNotFoundError:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_NOT_FOUND
                resp.text = "file not found"
        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"


class StudyResource:
    study_path: str

    def __init__(self, study_path):
        self.study_path = study_path

    def on_post(self, req: Request, resp: Response):  # noqa
        try:
            request: StudyPost = from_dict(StudyPost, req.media)  # noqa
            print('request',request)
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that request.consent_for matches session.id
            if request.consent_for != session.id:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to start the study"
                return

            # # store the information in the database using an upsert
            # participant = Participant(
            #     id=session.id,
            #     prolific_id=request.prolific_id,
            #     start=pendulum.now()
            # )
            # db.merge(participant)
            #
            # db.commit()
            print('finished')
            # redirect to the GET endpoint
            raise falcon.HTTPSeeOther(f"/study")

        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"

    def on_get(self, req: Request, resp: Response):  # noqa
        try:
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that the user has given consent and fetch the user's prolific ID
            participant = db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).one_or_none()

            if participant is None:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to start the study"
                return

            # if the 'extra' column is not null redirect to the survey endpoint
            if participant.extra is not None:
                raise falcon.HTTPSeeOther(f"/survey")

            # check if the file exists and return a 404 if it doesn't
            try:
                with open(self.study_path, "rb") as file:
                    # read the contents of the file and replace the placeholders
                    contents = file.read()
                    contents = contents.replace(b"#PROLIFIC_ID#", participant.prolific_id.encode())
                    contents = contents.replace(b"#SESSION_ID#", session.id.encode())
                    # provide the HTML response
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_OK
                    resp.text = contents
            except FileNotFoundError:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_NOT_FOUND
                resp.text = "file not found"
        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"


class SurveyResource:
    survey_path: str

    def __init__(self, survey_path):
        self.survey_path = survey_path

    def on_post(self, req: Request, resp: Response):  # noqa
        try:
            session = req.env["beaker.session"]
            db = req.context.session

            # update the database by setting 'extra' to req.media for the user with 'id' set to session.id
            # only allow this to happen *once*, so check if that extra column is still null

            db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).filter(
                Participant.extra.is_(None)
            ).update(
                {Participant.extra: req.media}
            )

            db.commit()

            # redirect to the GET endpoint
            raise falcon.HTTPSeeOther(f"/survey")

        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"

    def on_get(self, req: Request, resp: Response):  # noqa
        try:
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that the user has given consent and fetch the user's prolific ID
            participant = db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).one_or_none()

            if participant is None:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to participate in the the study"
                return

            # if the 'survey' column is not null redirect to the survey endpoint
            if participant.survey is not None:
                raise falcon.HTTPSeeOther(f"/complete")

            # check if the file exists and return a 404 if it doesn't
            try:
                with open(self.survey_path, "rb") as file:
                    # read the contents of the file and replace the placeholders
                    contents = file.read()
                    contents = contents.replace(b"#PROLIFIC_ID#", participant.prolific_id.encode())
                    contents = contents.replace(b"#SESSION_ID#", session.id.encode())
                    # provide the HTML response
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_OK
                    resp.text = contents
            except FileNotFoundError:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_NOT_FOUND
                resp.text = "file not found"
        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"


class CompleteResource:
    complete_path: str

    def __init__(self, complete_path):
        self.complete_path = complete_path

    def on_post(self, req: Request, resp: Response):  # noqa
        try:
            session = req.env["beaker.session"]
            db = req.context.session

            # update the database by setting 'survey' to req.media for the user with 'id' set to session.id
            # only allow this to happen *once*, so check if that extra column is still null

            participant = db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).filter(
                Participant.survey.is_(None)
            ).one_or_none()

            if participant is None:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to participate in the study"
                return

            participant.survey = req.media
            participant.end = pendulum.now()

            db.commit()

            # redirect to the GET endpoint
            raise falcon.HTTPSeeOther(f"/complete")

        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"

    def on_get(self, req: Request, resp: Response):  # noqa
        try:
            request: CompleteGet = from_dict(CompleteGet, req.params)  # noqa
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that the user has given consent and fetch the user's prolific ID
            participant = db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).one_or_none()

            if participant is None:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to participate in the study"
                return

            # check if this is a second call to the page with a 'check' parameter
            if request.check is not None:
                # verify that check is set to the prolific ID or show an error
                if request.check != participant.prolific_id:
                    resp.content_type = falcon.MEDIA_TEXT
                    resp.status = falcon.HTTP_BAD_REQUEST
                    resp.text = "the verification check for completing the survey failed"
                    return

                # redirect the user back to Prolific
                raise falcon.HTTPSeeOther(f"https://app.prolific.com/submissions/complete?cc={'submission_ok'}")  # noqa

                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_OK
                resp.text = "redirecting user to Prolific ..."
                return

            # check if the file exists and return a 404 if it doesn't
            try:
                with open(self.complete_path, "rb") as file:
                    # read the contents of the file and replace the placeholders
                    contents = file.read()
                    contents = contents.replace(b"#VERIFY_ID#", participant.prolific_id.encode())
                    # provide the HTML response
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_OK
                    resp.text = contents
            except FileNotFoundError:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_NOT_FOUND
                resp.text = "file not found"
        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"



class TutorialResource:
    tutorial_path: str

    def __init__(self, tutorial_path):
        self.tutorial_path = tutorial_path

    def on_post(self, req: Request, resp: Response):  # noqa
        try:
            request: TutorialPost = from_dict(TutorialPost, req.media)  # noqa
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that request.consent_for matches session.id
            if request.consent_for != session.id:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to start the study"
                return

            # store the information in the database using an upsert
            participant = Participant(
                id=session.id,
                prolific_id=request.prolific_id,
                start=pendulum.now()
            )
            db.merge(participant)
            db.commit()

            # redirect to the GET endpoint
            raise falcon.HTTPSeeOther(f"/tutorial")

        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"

    def on_get(self, req: Request, resp: Response):  # noqa
        try:
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that the user has given consent and fetch the user's prolific ID
            participant = db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).one_or_none()

            if participant is None:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to start the study"
                return

            # if the 'extra' column is not null redirect to the survey endpoint
            if participant.extra is not None:
                raise falcon.HTTPSeeOther(f"/survey")

            # check if the file exists and return a 404 if it doesn't
            try:
                with open(self.tutorial_path, "rb") as file:
                    # read the contents of the file and replace the placeholders
                    contents = file.read()
                    contents = contents.replace(b"#PROLIFIC_ID#", participant.prolific_id.encode())
                    contents = contents.replace(b"#SESSION_ID#", session.id.encode())
                    # provide the HTML response
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_OK
                    resp.text = contents
            except FileNotFoundError:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_NOT_FOUND
                resp.text = "file not found"
        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"


class TutorialResource2:
    tutorial_path2: str

    def __init__(self, tutorial_path2):
        self.tutorial_path2 = tutorial_path2

    def on_post(self, req: Request, resp: Response):  # noqa
        try:
            request: TutorialPost2 = from_dict(TutorialPost2, req.media)  # noqa
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that request.consent_for matches session.id
            if request.consent_for != session.id:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to start the study"
                return

            # store the information in the database using an upsert
            # participant = Participant(
            #     id=session.id,
            #     prolific_id=request.prolific_id,
            #     start=pendulum.now()
            # )
            # db.merge(participant)
            # db.commit()

            # redirect to the GET endpoint
            raise falcon.HTTPSeeOther(f"/tutorial2")

        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"

    def on_get(self, req: Request, resp: Response):  # noqa
        try:
            session = req.env["beaker.session"]
            db = req.context.session

            # verify that the user has given consent and fetch the user's prolific ID
            participant = db.query(
                Participant
            ).filter(
                Participant.id == session.id
            ).one_or_none()

            if participant is None:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.text = "consent was not given to start the study"
                return

            # if the 'extra' column is not null redirect to the survey endpoint
            if participant.extra is not None:
                raise falcon.HTTPSeeOther(f"/survey")

            # check if the file exists and return a 404 if it doesn't
            try:
                with open(self.tutorial_path2, "rb") as file:
                    # read the contents of the file and replace the placeholders
                    contents = file.read()
                    contents = contents.replace(b"#PROLIFIC_ID#", participant.prolific_id.encode())
                    contents = contents.replace(b"#SESSION_ID#", session.id.encode())
                    # provide the HTML response
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_OK
                    resp.text = contents
            except FileNotFoundError:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_NOT_FOUND
                resp.text = "file not found"
        except DaciteError as err:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.text = f"one or more of the parameters was not understood\n{err}"




# save user interaction's data(radio button selection)
class RecordResource:
     def on_post(self, req, resp):
         try:
            session = req.env["beaker.session"]
            db = req.context.session
            form_data_dict = req.media
            print('form_data_dict',form_data_dict)
            form_data = FormData(
                id=session.id,
                prolific_id=form_data_dict['prolificId'],
                round_number=form_data_dict['round'],
                first_form_value=form_data_dict['firstFormValue'],
                second_form_value=form_data_dict['secondFormValue'],

            )
            # Implement your logic to save form_data into your database
            db.add(form_data)
            db.commit()

            resp.status = falcon.HTTP_200
            resp.media = {'message': 'Form data saved successfully'}

         except DaciteError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.media = {'error': str(e)}












