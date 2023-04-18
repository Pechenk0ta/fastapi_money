from models.models import money_tx, User_table, trx_type_table
from sqlalchemy import select, insert
from sqlalchemy.sql import functions
import datetime

def create_money(db, upload, Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_id = db.execute(select(User_table.c.id)
                         .where(User_table.c.username == current_user)).scalar()
    if upload.type == 'income':
        type = 1
    else:
        type = 2
    com = insert(money_tx).values(
        type = type,
        value = upload.value,
        description = upload.description,
        person = user_id
    )
    db.execute(com)
    db.commit()
    return "good"


def get_balance(db, Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_id = db.execute(
        select(User_table.c.id)
                         .where(User_table.c.username == current_user)).scalar()
    income_sum = db.execute(
        select(functions.sum(money_tx.c.value))
        .where((money_tx.c.type == 1) & (money_tx.c.person == user_id))
        ).scalar()
    outcome_sum = db.execute(
        select(functions.sum(money_tx.c.value))
        .where((money_tx.c.type == 2) & (money_tx.c.person == user_id))
        ).scalar()
    print(db.execute(
        select(money_tx.c.value, money_tx.c.description).join()
        .where(money_tx.c.person == user_id)
        ).fetchall())

    return {'balance':income_sum-outcome_sum}


def get_balance_by_days(db, Authorize, upload):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_id = db.execute(
        select(User_table.c.id)
        .where(User_table.c.username == current_user)).scalar()
    if (upload.day_start and  upload.day_end):
        date_start = datetime.datetime.strptime(upload.day_start, '%m/%d/%Y').date()
        date_end = datetime.datetime.strptime(upload.day_end, '%m/%d/%Y').date()

        income_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 1) & (money_tx.c.person == user_id) &
                   (date_start < money_tx.c.date) & (date_end > money_tx.c.date))
        ).scalar()
        outcome_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 2) & (money_tx.c.person == user_id) &
                   (date_start < money_tx.c.date) & (date_end > money_tx.c.date))
        ).scalar()
        if not outcome_sum:
            outcome_sum = 0
        if not income_sum:
            income_sum = 0
        return {'balance_changes':income_sum-outcome_sum}
    elif (upload.day_start):
        date_start = datetime.datetime.strptime(upload.day_start, '%m/%d/%Y').date()
        income_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 1) & (money_tx.c.person == user_id) &
                   (date_start < money_tx.c.date))
        ).scalar()

        outcome_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 2) & (money_tx.c.person == user_id) &
                   (date_start < money_tx.c.date))
        ).scalar()
        if not outcome_sum:
            outcome_sum = 0
        if not income_sum:
            income_sum = 0
        return {'balance_changes': income_sum - outcome_sum}

    elif upload.day_end:
        date_end = datetime.datetime.strptime(upload.day_end, '%m/%d/%Y').date()
        income_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 1) & (money_tx.c.person == user_id) &
                   (date_end > money_tx.c.date))
        ).scalar()
        outcome_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 2) & (money_tx.c.person == user_id) &
                   (date_end > money_tx.c.date))
        ).scalar()
        if not outcome_sum:
            outcome_sum = 0
        if not income_sum:
            income_sum = 0
        return {'balance_changes': income_sum - outcome_sum}
    else:
        income_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 1) & (money_tx.c.person == user_id))
        ).scalar()
        outcome_sum = db.execute(
            select(functions.sum(money_tx.c.value))
            .where((money_tx.c.type == 2) & (money_tx.c.person == user_id))
        ).scalar()
        if not outcome_sum:
            outcome_sum = 0
        if not income_sum:
            income_sum = 0
        return {'balance_changes': income_sum - outcome_sum}
