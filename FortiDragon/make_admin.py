# from FortiDragon.db import get_db
# from FortiDragon import create_app
# import sys
#
# MAX_ATTEMPTS = 3
#
# app = create_app()
# with app.app_context():
#     db = get_db()
#
#     # Prompt for username
#     # username = input("Enter the username to promote to admin: ").strip()
#
# def promote_user_to_admin(db):
#         attempts = MAX_ATTEMPTS
#     while attempts >0:
#         username = input("Enter the username to promote to admin: ").strip()
#
#         if not username:
#            remaining = MAX_ATTEMPTS - attempts
#            print(" Valid username not provided.")
#            if remaining > 0:
#                print(f" User '{username}' not found. {remaining} attempt(s) remaining.\n")
#            continue
#         else:
#             sys.exit(1)
#
#         user = db.execute("SELECT id, username FROM user WHERE username = ?", (username,)).fetchone()
#
#         if not user:
#             remaining = MAX_ATTEMPTS - attempt
#         if remaining > 0:
#            print(f" User '{username}' not found. {remaining} attempt(s) remaining.\n")
#            continue
#            # print(f" User '{username}' not found in database.")
#            # sys.exit()
#         else:
#            print(f" User '{username}' not found. No attempts remaining. Nice try, Hackerman.")
#            sys.exit(1)
#
#         # Success path
#     db.execute("UPDATE user SET role='admin' WHERE id=?", (user["id"],))
#     db.commit()
#     print(f" User '{username}' has been updated to admin.")
#     sys.exit(0)
#
#     #     db.execute("UPDATE user SET role='admin' WHERE username=?", (username,))
#     #     db.commit()
#     # print(f" User '{username}' has been updated to admin.")
#
#     # db.execute("UPDATE user SET role='admin' WHERE username=?", ("jamie",))
#     # db.commit()
#     # print("User role updated to admin.")

import sys
from FortiDragon import create_app
from FortiDragon.db import get_db

MAX_ATTEMPTS = 3

def promote_user_to_admin(db):
    attempts = MAX_ATTEMPTS
    while attempts > 0:
        username = input("Enter the username to promote to admin: ").strip()

        if not username:
            attempts -= 1
            print(" Valid username not provided.")
            if attempts > 0:
                print(f"{attempts} attempt(s) remaining.\n")
                continue
            print("No attempts remaining.")
            return 1  # non-zero exit

        # Case-insensitive lookup
        user = db.execute(
            "SELECT id, username FROM user WHERE username = ? COLLATE NOCASE",
            (username,)
        ).fetchone()

        if not user:
            attempts -= 1
            if attempts > 0:
                print(f" User '{username}' not found. {attempts} attempt(s) remaining.\n")
                continue
            print(f" User '{username}' not found. No attempts remaining. Nice try, Hackerman.")
            return 1

        # Success: promote and exit
        db.execute("UPDATE user SET role='admin' WHERE id=?", (user["id"],))
        db.commit()
        print(f" User '{user['username']}' has been updated to admin.")
        return 0

    return 1  # should not reach here

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db = get_db()
        sys.exit(promote_user_to_admin(db))