from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func, or_, extract, and_
import flask_praetorian
from webargs.flaskparser import use_args
from webargs import fields
from app.schemas.ClassroomSchema import TicketSchema
# from app.schemas.TicketSchema import GetTicketSchema
from app.schemas.TicketLogsSchema import TicketLogsSchema
# from app.schemas.TicketSchema import EditTicketSchema
from app.models.Ticket import Ticket
from app.models.NotificationUsers import NotificationUsers
from app.models.TicketLogs import TicketLogs
from app.models import db
import openpyxl, calendar
from app.mail import mail
import app.config as config
from flask_mail import Message

bp = Blueprint("ticket", __name__)


@bp.route("/addTicket", methods=["POST"])
@use_args(TicketSchema, location="json")
@flask_praetorian.roles_accepted("admin", "user")
@flask_praetorian.auth_required
def add_ticket(args):
    """
    POST API to add a Ticket to database.
    :param: values for a single record to be added
            in tickets table.
    :response:  primary key for the record being added
                with status 200.
    """
    ticket = Ticket(**args)

    date = datetime.now().strftime("F-%y%m%d")
    last_ticket_for_today = (
        db.session.query(Ticket)
        .filter(
            and_(
                extract("month", Ticket.opening_time) == datetime.today().month,
                extract("year", Ticket.opening_time) == datetime.today().year,
                extract("day", Ticket.opening_time) == datetime.today().day,
            )
        )
        .order_by(Ticket.opening_time.desc())
        .first()
    )
    if last_ticket_for_today:
        nmbr = int(last_ticket_for_today.internal_incident_no[-3:]) + 1
        nmbr = str(nmbr).zfill(3)
        ticket.internal_incident_no = date + nmbr
    else:
        ticket.internal_incident_no = date + "001"

    db.session.add(ticket)
    ticket.status_id = 1
    ticket.opening_time = datetime.now()
    ticket.maintanance_agent = flask_praetorian.current_user().username

    ticket_log = TicketLogs(
        internal_incident_no=ticket.internal_incident_no,
        user_id=flask_praetorian.current_user().id,
        maintanance_agent=ticket.maintanance_agent,
        status=ticket.status_id,
        resolution=ticket.resolution_id,
        TDM_no=ticket.TDM_no,
        comments=ticket.comments,
        timestamp=ticket.opening_time,
    )
    db.session.add(ticket_log)

    mail_user_data = (
        db.session.query(NotificationUsers)
        .filter(NotificationUsers.notification_types.contains("Open"))
        .all()
    )
    mail_recepients = [item.email for item in mail_user_data]
    msg = Message()
    msg.subject = f"{ticket.internal_incident_no} Opened"
    msg.sender = config.MAIL_USERNAME
    msg.recipients = mail_recepients
    msg.html = render_template("email_notification.html", ticket=ticket)
    mail.send(msg)

    db.session.commit()

    return {"id": ticket.internal_incident_no, "message": "Ticket Added"}


@bp.route("/updateTicket", methods=["PUT"])
@use_args(EditTicketSchema, location="json")
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted("admin", "user")
def update_ticket(args):
    """
    PUT API to update a Ticket.
    Fetch a record from Tickets table based
    on internal_incident_no, and update the fields
    based on parameters passed to the API.
    """
    id = args.pop("internal_incident_no")
    ticket = db.session.query(Ticket).filter(Ticket.internal_incident_no == id).first()
    if args.get("status_id"):
        ticket.status_id = args.get("status_id")
    if args.get("resolution_id"):
        ticket.resolution_id = args.get("resolution_id")
    if args.get("TDM_no"):
        ticket.TDM_no = args.get("TDM_no")
    if args.get("comments"):
        ticket.comments = args.get("comments")
    if ticket.status_id == 8:
        ticket.closing_time = datetime.now()

    ticket_log = TicketLogs(
        internal_incident_no=ticket.internal_incident_no,
        user_id=flask_praetorian.current_user().id,
        maintanance_agent=flask_praetorian.current_user().username,
        status=ticket.status_id,
        resolution=args.get("resolution_id"),
        TDM_no=args.get("TDM_no"),
        comments=args.get("comments"),
        timestamp=datetime.now(),
    )
    db.session.add(ticket_log)

    if ticket.status_id == 3:
        mail_user_data = (
            db.session.query(NotificationUsers)
            .filter(NotificationUsers.notification_types.contains("Resolved"))
            .all()
        )
        mail_recepients = [item.email for item in mail_user_data]
        msg = Message()
        msg.subject = f"{ticket.internal_incident_no} Resolved"
        msg.sender = config.MAIL_USERNAME
        msg.recipients = mail_recepients
        msg.html = render_template("email_notification.html", ticket=ticket)
        mail.send(msg)

    if ticket.status_id == 8:
        mail_user_data = (
            db.session.query(NotificationUsers)
            .filter(NotificationUsers.notification_types.contains("Closed"))
            .all()
        )
        mail_recepients = [item.email for item in mail_user_data]
        msg = Message()
        msg.subject = f"{ticket.internal_incident_no} Closed"
        msg.sender = config.MAIL_USERNAME
        msg.recipients = mail_recepients
        msg.html = render_template("email_notification.html", ticket=ticket)
        mail.send(msg)

    db.session.commit()
    return {"message": "Ticket Updated"}


@bp.route("/getTickets", methods=["GET"])
# @flask_praetorian.auth_required
# @flask_praetorian.roles_accepted("admin", "user", "client")
@use_args(
    {
        "search": fields.String(required=False, missing=None),
        "date": fields.String(),
        "start_date": fields.String(allow_none=True),
        "end_date": fields.String(allow_none=True),
    },
    location="query",
)
def get_tickets(args):
    """
    Get API to get all Tickets from db with
    SLA information. If search parameter is
    passed will return filtered records based
    on search parameter.
    """
    data = db.session.query(Ticket)
    if args.get("search"):
        data = data.filter(
            or_(
                # func.date(Ticket.opening_time) == (args.get("search")),
                Ticket.internal_incident_no == args.get("search"),
                Ticket.source_incident_no == args.get("search"),
                Ticket.device_type == args.get("search"),
            )
        )
    if args.get("date"):
        if args["date"] == "daily":
            dt = datetime.today()
            start = dt - timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
            end = dt + timedelta(hours=24)

        elif args["date"] == "weekly":
            dt = datetime.today()
            start = dt - timedelta(
                days=dt.weekday(), hours=dt.hour, minutes=dt.minute, seconds=dt.second
            )
            end = start + timedelta(days=6, hours=24)

        elif args["date"] == "monthly":
            dt = datetime.today()
            start = dt - timedelta(
                days=dt.day - 1, hours=dt.hour, minutes=dt.minute, seconds=dt.second
            )
            daysInMonth = calendar.monthrange(dt.year, dt.month)[1]
            end = start + timedelta(days=daysInMonth)

        elif args.get("start_date") and args.get("end_date"):
            start = datetime.strptime(args["start_date"], "%Y-%m-%d")
            end = datetime.strptime(args["end_date"], "%Y-%m-%d") + timedelta(hours=24)

        data = data.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )

    data = data.order_by(Ticket.opening_time.desc()).all()
    schema = GetTicketSchema(many=True)
    # SLA fields are calculated in post_dump of this schema
    result = schema.dump(data)
    return jsonify(result), 200


@bp.route("/ticketStats", methods=["GET"])
# @flask_praetorian.auth_required
# @flask_praetorian.roles_accepted("admin", "user", "client")
@use_args(
    {
        "date": fields.String(),
        "start_date": fields.String(allow_none=True),
        "end_date": fields.String(allow_none=True),
    },
    location="query",
)
def get_status_count(args):
    """
    GET API to fetch different Ticket stats
    """
    open = db.session.query(func.count(Ticket.status_id)).filter(Ticket.status_id == 1)
    in_progress = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 2
    )
    resolved = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 3
    )
    on_hold_stock = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 4
    )
    on_hold_tdm = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 5
    )
    on_hold_poc = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 6
    )
    on_hold_noc = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 7
    )
    closed = db.session.query(func.count(Ticket.status_id)).filter(
        Ticket.status_id == 8
    )
    if args.get("date"):
        if args["date"] == "daily":
            dt = datetime.today()
            start = dt - timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
            end = dt + timedelta(hours=24)

        elif args["date"] == "weekly":
            dt = datetime.today()
            start = dt - timedelta(
                days=dt.weekday(), hours=dt.hour, minutes=dt.minute, seconds=dt.second
            )
            end = start + timedelta(days=6, hours=24)

        elif args["date"] == "monthly":
            dt = datetime.today()
            start = dt - timedelta(
                days=dt.day - 1, hours=dt.hour, minutes=dt.minute, seconds=dt.second
            )
            daysInMonth = calendar.monthrange(dt.year, dt.month)[1]
            end = start + timedelta(days=daysInMonth)

        elif args.get("start_date") and args.get("end_date"):
            start = datetime.strptime(args["start_date"], "%Y-%m-%d")
            end = datetime.strptime(args["end_date"], "%Y-%m-%d") + timedelta(hours=24)
        open = open.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        in_progress = in_progress.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        resolved = resolved.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        on_hold_stock = on_hold_stock.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        on_hold_tdm = on_hold_tdm.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        on_hold_poc = on_hold_poc.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        on_hold_noc = on_hold_noc.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
        closed = closed.filter(
            and_(Ticket.opening_time >= start, Ticket.opening_time < end)
        )
    open = open.first()
    in_progress = in_progress.first()
    resolved = resolved.first()
    on_hold_stock = on_hold_stock.first()
    on_hold_tdm = on_hold_tdm.first()
    on_hold_poc = on_hold_poc.first()
    on_hold_noc = on_hold_noc.first()
    closed = closed.first()

    tickets_created_today = (
        db.session.query(func.count(Ticket.status_id))
        .filter(
            and_(
                extract("month", Ticket.opening_time) == datetime.today().month,
                extract("year", Ticket.opening_time) == datetime.today().year,
                extract("day", Ticket.opening_time) == datetime.today().day,
            )
        )
        .first()
    )
    tickets_closed_today = (
        db.session.query(func.count(Ticket.status_id))
        .filter(
            and_(
                extract("month", Ticket.closing_time) == datetime.today().month,
                extract("year", Ticket.closing_time) == datetime.today().year,
                extract("day", Ticket.closing_time) == datetime.today().day,
            )
        )
        .first()
    )

    ret = {
        "open": open[0],
        "in_progress": in_progress[0],
        "resolved": resolved[0],
        "on_hold_stock": on_hold_stock[0],
        "on_hold_tdm": on_hold_tdm[0],
        "on_hold_poc": on_hold_poc[0],
        "on_hold_noc": on_hold_noc[0],
        "closed": closed[0],
        "tickets_created_today": tickets_created_today[0],
        "tickets_closed_today": tickets_closed_today[0],
    }
    return jsonify(ret), 200


@bp.route("/importTicketsData", methods=["POST"])
@use_args({"file": fields.Field()}, location="files")
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted("admin")
def import_tickets_to_db(args):
    """
    POST API to import data for Tickets to db from csv or excel file
    """
    wb_obj = openpyxl.load_workbook(args["file"])
    sheet_obj = wb_obj.active
    ret = []

    x = 0
    for row in sheet_obj:
        if x > 0:
            data_row = {
                "source_incident_no": row[0].value,
                "reporting_source": row[1].value,
                "internal_incident_no": datetime.now().strftime("F%y%m%d%f")[:-2],
                "status": row[3].value,
                "opening_time": row[4].value,
                "source_time": row[5].value,
                "phase": row[6].value,
                "network_no": row[7].value,
                "site": row[8].value,
                "element_type": row[9].value,
                "element_id": row[10].value,
                "device_type": row[11].value,
                "last_octet": row[12].value,
                "fault_description": row[13].value,
                "resolution": row[14].value,
                "TDM_no": row[15].value,
                "closing_time": row[16].value,
                "maintanance_agent": row[17].value,
                "comments": row[18].value,
            }
            ticket = Ticket(**data_row)
            db.session.add(ticket)
            db.session.commit()
            ret.append(data_row)
        x += 1

    return jsonify(ret), 200


@bp.route("/getTicketLogs", methods=["GET"])
# @flask_praetorian.auth_required
# @flask_praetorian.roles_accepted("admin", "user", "client")
@use_args(
    {
        "internal_incident_no": fields.String(required=True, allow_none=False),
    },
    location="query",
)
def get_ticket_logs(args):
    """
    Get API to get all Tickets logs from db
    """
    data = (
        db.session.query(TicketLogs)
        .filter(TicketLogs.internal_incident_no == args["internal_incident_no"])
        .all()
    )

    schema = TicketLogsSchema(many=True)
    result = schema.dump(data)
    return jsonify(result), 200
