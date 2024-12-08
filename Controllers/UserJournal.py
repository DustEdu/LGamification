from App import api, logger
from Services.funcs import check_session, edit_model_fields

from flask import request, make_response as resp, jsonify, Response, abort
from flask_restx import Resource as Controller, Namespace, fields
from Facades.Journal import JournalFacade

ns = Namespace("user/<int:userID>/journal")


# ToDo test endpoints


@ns.route("/")
class Journal(Controller):
    @api.marshal_list_with(JournalFacade.dto)
    def get(self, userID: int) -> tuple[JournalFacade.model]:
        check_session(userID)

        res = JournalFacade.get_by_user(userID)
        logger.debug(res[0].__dict__)
        return res


@ns.route("/<int:entryID>")
class Journal(Controller):
    @api.marshal_list_with(JournalFacade.dto)
    def get(self, userID: int, entryID) -> tuple[JournalFacade.model]:
        check_session(userID)

        return JournalFacade.get(entryID).entry

    journalput_dict = {
        "title": fields.String(required=False),
        "date": fields.DateTime(required=False),
        "xp":   fields.Integer(required=False),
        "cash": fields.Integer(required=False),
        "hp":   fields.Integer(required=False),
        "sp":   fields.Integer(required=False),
    }
    journalput_dto = ns.model("Journaledit", journalput_dict)

    @ns.expect(journalput_dto)
    @api.marshal_list_with(JournalFacade.dto)
    def put(self, userID: int, entryID) -> JournalFacade.model:
        check_session(userID)

        return edit_model_fields(
            facade=JournalFacade.get(entryID),
            field_names=list(self.journalput_dict.keys()),
            data=request.json
        ).entry

    def delete(self, userID: int, entryID):
        check_session(userID)

        JournalFacade.get(entryID).delete()
