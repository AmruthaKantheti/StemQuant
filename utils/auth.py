import bcrypt
from utils.db import connect


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


def register_user(
username,
email,
password
):

    conn=connect()
    c=conn.cursor()

    pw=hash_password(password)

    try:
        c.execute(
"""
INSERT INTO users
(username,email,password)
VALUES(?,?,?)
""",
(
username,
email,
pw
)
)
        conn.commit()
        return True

    except:
        return False


def verify_user(
username,
password
):
    conn=connect()
    c=conn.cursor()

    c.execute(
"""
SELECT password
FROM users
WHERE username=?
""",
(username,)
)

    result=c.fetchone()

    if result:

        if bcrypt.checkpw(
        password.encode(),
        result[0]
        ):
            return True

    return False