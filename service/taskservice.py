from models.models import money_tx, User_table, trx_type_table, category_table
from sqlalchemy import select, insert, and_
from sqlalchemy.sql import functions
import datetime

def create_money(db, upload, Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_id = db.execute(select(User_table.c.id)
                         .where(User_table.c.username == current_user)).scalar()
    if upload.type == 'incoming':
        type = 1
    else:
        type = 2
    category_id = db.execute(select(category_table.c.id)
                             .where(category_table.c.name == upload.category)).scalar()
    com = insert(money_tx).values(
        type = type,
        value = upload.value,
        description = upload.description,
        person = user_id,
        category = category_id
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
        select(money_tx.c.value, money_tx.c.description)
        .where(money_tx.c.person == user_id)
        ).fetchall())

    return {'balance':income_sum-outcome_sum}


def get_balance_by_days(db, Authorize, upload):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_id = db.execute(
        select(User_table.c.id)
        .where(User_table.c.username == current_user)).scalar()
    qwe = select(User_table.c.id).where(User_table.c.username == current_user)
    def date_filter():
        if not upload.day_start:
            date_start = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        else:
            date_start = datetime.datetime.strptime(upload.day_start, '%m/%d/%Y').date()
        if not upload.day_end:
            date_end = datetime.datetime.utcnow()
        else:
            date_end = datetime.datetime.strptime(upload.day_end, '%m/%d/%Y').date()
        return and_(date_start < money_tx.c.date , date_end > money_tx.c.date)

    income_sum = db.execute(
        select(functions.sum(money_tx.c.value))
        .where(and_(money_tx.c.type == 1, money_tx.c.person == user_id, date_filter()))
        ).scalar()

    outcome_sum = db.execute(
       select(functions.sum(money_tx.c.value))
      .where( (money_tx.c.type == 2) &  (money_tx.c.person == user_id) &
      (date_filter()))
       ).scalar()
    if not outcome_sum:
        outcome_sum = 0
    if not income_sum:
        income_sum = 0
    return {'balance_changes':income_sum-outcome_sum}



def filter(db, upload, Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    def type_filter(upload):
        if upload.type:
            return trx_type_table.c.type == upload.type
        return True
    def category_filter(upload):
        if upload.category:
            return category_table.c.name == upload.category
        return True
    def value_filter(upload):
        if upload.value:
            return money_tx.c.value == upload.value
        return money_tx.c.value > 0
    def description_filter(upload):
        if upload.description:
            return money_tx.c.description == upload.description
        return True
    def date_filter(upload):
        if not upload.day_start:
            date_start = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        else:
            date_start = datetime.datetime.strptime(upload.day_start, '%m/%d/%Y').date()
        if not upload.day_end:
            date_end = datetime.datetime.utcnow()
        else:
            date_end = datetime.datetime.strptime(upload.day_end, '%m/%d/%Y').date()
        return and_(date_start < money_tx.c.date, date_end > money_tx.c.date)
    def get_user(current_user):
        user_id = db.execute(
            select(User_table.c.id)
            .where(User_table.c.username == current_user)).scalar()
        return money_tx.c.person == user_id
    q = db.execute(
        select(money_tx.c.id, money_tx.c.description, money_tx.c.date).join(trx_type_table,
                                                           money_tx.c.type == trx_type_table.c.id).join(category_table, category_table.c.id == money_tx.c.category)
        .where(and_(type_filter(upload), category_filter(upload), value_filter(upload), description_filter(upload), date_filter(upload), get_user(current_user)))
    ).fetchall()
    res = []
    for i in range(len(q)):
        res.append({
            'task_id':q[i][0],
            'description': q[i][1],
            'date':q[i][2]
        })
    return res

