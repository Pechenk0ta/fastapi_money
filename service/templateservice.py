from models.models import money_tx, User_table, trx_type_table, category_table, money_template_table
from sqlalchemy import and_, insert, select


def get_user_id(Authorize, db):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_id = db.execute(select(User_table.c.id)
                         .where(User_table.c.username == current_user)).scalar()
    return user_id

def create_temaplate(db, Authorize, upload):
    user_id = get_user_id(Authorize, db)
    category_id = db.execute(select(category_table.c.id)
                             .where(category_table.c.name == upload.category)).scalar()
    if not category_id:
        category_id = 11
    db.execute(
        insert(money_template_table).values(
            user_id = user_id,
            name = upload.name,
            description = upload.description,
            value = upload.value,
            category = category_id
        )
    )
    db.commit()
    return 'good'



def check_templates(Authorize, db):
    user_id = get_user_id(Authorize, db)
    q = db.execute(
        select(money_template_table.c.name, money_template_table.c.description, money_template_table.c.value, category_table.c.name)\
            .join(category_table, category_table.c.id == money_template_table.c.category)
            .where(and_(money_template_table.c.user_id == user_id))
    ).fetchall()
    print(q)
    res = []
    for i in q:
        res.append(
            {
                'template_name': i[0],
                'template_description': i[1],
                'template_value': i[2],
                'template_category': i[3]
            }
        )
    return res

