import os
import bcrypt
from operator import methodcaller
from functools import partial


def basic_authorization(user, password):
    allowed_user_datas = filter(None, os.environ['ALLOWED_USERS'].split(','))

    allowed_users = dict(
        map(
            partial(map, methodcaller('strip')),
            map(
                partial(str.split, sep=':'),
                allowed_user_datas
            )
        )
    )

    return user in allowed_users and bcrypt.checkpw(
        password.encode('utf-8'),
        allowed_users[user].encode('utf-8')
    )
