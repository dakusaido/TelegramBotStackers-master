from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

from utils.datbase import session
from utils.schemas import User


def register_user(tg_id: int, first_name: str, second_name: str):
    session.connection()
    user = User(
        tg_id=tg_id,
        first_name=first_name,
        second_name=second_name,
        activity=1,
        mark_tests=0,
        max_tests=0,
        result=0
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def deleteUser(tg_id):
    user = session.query(User).filter(User.tg_id == tg_id).one()
    session.delete(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def select_users():
    users = session.query(User).all()
    return users


def add_coin_user(tg_id, count):
    user = session.query(User).filter(
        User.tg_id.like(tg_id)
    ).all()[0]
    if user.activity:
        user.activity += count
    else:
        user.activity = count
    session.add(user)
    session.commit()


def add_test_mark(tg_id, count):
    user = session.query(User).filter(
        User.tg_id.like(tg_id)
    ).all()[0]
    if user.mark_tests:
        user.mark_tests += count
    else:
        user.mark_tests = count
    session.add(user)
    session.commit()


def get_user(tg_id):
    user = session.query(User).filter(
        User.tg_id.like(tg_id)
    ).all()[0]
    return user


def updateUser(tg_iD, second_namE, first_namE, activitY, mark_testS, max_tests, result):
    deleteUser(tg_iD)
    some_user = User(
        tg_id=tg_iD,
        second_name=second_namE,
        first_name=first_namE,
        activity=activitY,
        mark_tests=mark_testS,
        max_tests=max_tests,
        result=result
    )
    session.add(some_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def activityMark(tg_iD):
    user = get_user(tg_iD)

    SN = user.second_name
    FN = user.first_name
    MK = user.mark_tests
    MT = user.mark_tests

    activityP = session.query(User.activity).filter(User.tg_id == tg_iD).all()[0][0]
    activityP += 1

    updateUser(tg_iD, SN, FN, activityP, MK, MT)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def send_result_ques(tg_iD, MarkTest, maxMarkTest):
    user = get_user(tg_iD)

    SN = user.second_name
    FN = user.first_name
    AK = user.activity

    updateUser(tg_iD, SN, FN, AK, MarkTest, maxMarkTest, user.result)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def rank_counter(tg_iD):
    max_activity = session.query(func.max(User.activity)).scalar()
    user = get_user(tg_iD)

    active_k = 1  # коэффициент увеличения активности
    test_k = 1  # коэффициент увеличения тестов

    test_points = user.mark_tests  # балл студента за последний тест
    max_test = user.max_tests
    active_points = user.activity  # сумма баллов за посещение мероприятий. 1 посещение = 10 баллов
    max_active = max_activity  # максимальный балл за активность среди всех студентов

    if (0 <= active_points / max_active < 0.3):
        test_k = 1
    if (0.3 <= active_points / max_active < 0.6):
        test_k = 1.3
    if (0.6 <= active_points / max_active < 0.8):
        test_k = 1.6
    if (0.8 <= active_points / max_active <= 1):
        test_k = 2

    if (0 <= test_points / max_test < 0.3):
        active_k = 1
    if (0.3 <= test_points / max_test < 0.6):
        active_k = 1.5
    if (0.6 <= test_points / max_test < 0.8):
        active_k = 2
    if (0.8 <= test_points / max_test <= 1):
        active_k = 3

    rank_points = test_k * test_points + active_k * active_points / 20
    updateUser(tg_iD, user.second_name, user.first_name, user.activity, user.mark_tests, user.max_tests, rank_points)

    return rank_points


def get_list_student(a_: str = "result"):
    lst = session.query(User).order_by(desc(User.result))
    return lst
