from datetime import datetime
from app import app
from models import db, User, UserRound, GroupRound, Follows

db.drop_all()
db.create_all()

new_user1 = User.signup(username="natwil", first_name="Nate",
                        last_name="Williams", email='nate@mail.com', password='password')
new_user1.id = 100
new_user2 = User.signup(username="danove", first_name="Dan",
                        last_name="Overholt", email='dan@mail.com', password='password')
new_user2.id = 101
new_user3 = User.signup(username="micgur", first_name="Michael",
                        last_name="Gurley", email='michael@mail.com', password='password')
new_user3.id = 102
new_user4 = User.signup(username="danher", first_name="Daniel",
                        last_name="Herbert", email='daniel@mail.com', password='password')
new_user4.id = 103
new_user5 = User.signup(username="kribro", first_name="Kris",
                        last_name="Broadley", email='kris@mail.com', password='password')
new_user5.id = 104
new_user6 = User.signup(username="davjoc", first_name="David",
                        last_name="Jochems", email='david@mail.com', password='password')
new_user6.id = 105

db.session.commit()


new_user1.following.append(new_user2)
new_user1.following.append(new_user3)
new_user1.following.append(new_user4)
new_user1.following.append(new_user5)
new_user1.following.append(new_user6)
new_user2.following.append(new_user1)
new_user2.following.append(new_user3)
new_user2.following.append(new_user4)
new_user3.following.append(new_user2)
new_user4.following.append(new_user3)
new_user4.following.append(new_user5)
new_user4.following.append(new_user6)
new_user5.following.append(new_user1)
new_user6.following.append(new_user3)
new_user6.following.append(new_user5)

db.session.commit()

group_round = GroupRound(id=100, course_id=164, date=datetime(2019, 10, 2))

db.session.add(group_round)
db.session.commit()

new_round1 = UserRound(user_id=100, course_id=6284,
                       date=datetime(2019, 10, 16), score=68)
new_round2 = UserRound(user_id=100, course_id=164,
                       date=datetime(2019, 11, 16), score=68)
new_round3 = UserRound(user_id=101, course_id=164,
                       date=datetime(2019, 12, 16), score=68)
new_round4 = UserRound(user_id=102, course_id=6284,
                       date=datetime(2019, 10, 1), score=68)
new_round5 = UserRound(user_id=103, course_id=6284,
                       date=datetime(2019, 9, 16), score=68)
new_round6 = UserRound(user_id=104, course_id=6893,
                       date=datetime(2019, 8, 16), score=68)
new_round7 = UserRound(user_id=105, course_id=6893,
                       date=datetime(2019, 10, 16), score=68)
new_round8 = UserRound(user_id=103, course_id=6284,
                       date=datetime(2019, 7, 16), score=68)
new_round9 = UserRound(user_id=103, course_id=164,
                       date=datetime(2019, 10, 20), score=68)
new_round10 = UserRound(user_id=104, course_id=164,
                        date=datetime(2019, 10, 2), score=69, group_rd_id=100)
new_round11 = UserRound(user_id=105, course_id=164,
                        date=datetime(2019, 10, 2), score=68, group_rd_id=100)


db.session.add_all([new_round1, new_round2, new_round3, new_round4,
                    new_round5, new_round6, new_round7, new_round8, new_round9, new_round10, new_round11])
db.session.commit()
