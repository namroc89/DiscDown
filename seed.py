from datetime import datetime
from app import app
from models import db, User, UserRound, GroupRound, Follows

db.drop_all()
db.create_all()

new_user1 = User.signup(username="natwil", first_name="Nate",
                        last_name="Williams", email='nate@mail.com', password='password')
new_user1.id = 100
new_user1.avatar = "https://ctl.s6img.com/society6/img/l_LKu9n8zevppxJpzuAzYozej6Y/w_700/prints/~artwork/s6-original-art-uploads/society6/uploads/misc/3d7d174ae4b7480db348f96793e06293/~~/retro-disc-golf-icon-prints.jpg?wait=0&attempt=0"

new_user2 = User.signup(username="danove", first_name="Dan",
                        last_name="Overholt", email='dan@mail.com', password='password')
new_user2.id = 101
new_user2.avatar = "https://ctl.s6img.com/society6/img/lvNAinVJ8AZZfZR-ecfJMtrScME/w_700/prints/~artwork/s6-original-art-uploads/society6/uploads/misc/e3dac46891c54a0ba36df4a34e44a29c/~~/twilight-disc-golf-prints.jpg"

new_user3 = User.signup(username="micgur", first_name="Michael",
                        last_name="Gurley", email='michael@mail.com', password='password')
new_user3.id = 102
new_user3.avatar = "https://ctl.s6img.com/society6/img/Y1O73EZqZ7Y0ApknUiV_C_U_nNQ/w_700/prints/~artwork/s6-0067/a/27638953_8937019/~~/disc-golf-abstract-basket-6-prints.jpg"

new_user4 = User.signup(username="danher", first_name="Daniel",
                        last_name="Herbert", email='daniel@mail.com', password='password')
new_user4.id = 103
new_user4.avatar = "https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/disc-golf-products-for-men-stupid-tree-frisbee-golf-print-coumoliv.jpg"

new_user5 = User.signup(username="kribro", first_name="Kris",
                        last_name="Broadley", email='kris@mail.com', password='password')
new_user5.id = 104
new_user5.avatar = "https://rlv.zcache.com/colorful_disc_golf_basket_poster-r55d17bd3975e4ff5bf3d9640c8ab7a9a_abw1_8byvr_307.jpg"

new_user6 = User.signup(username="davjoc", first_name="David",
                        last_name="Jochems", email='david@mail.com', password='password')
new_user6.id = 105
new_user6.avatar = "https://cdna.artstation.com/p/assets/images/images/013/067/746/large/john-paul-cavara-hole-1-withbag-edited-1.jpg?1537902719"

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

group_round = GroupRound(id=100, course_id=164, date=datetime(
    2019, 10, 2), course_name="Joralemon")

db.session.add(group_round)
db.session.commit()

new_round1 = UserRound(user_id=100, course_id=6284,
                       date=datetime(2019, 10, 16), score=68, course_name="Stonykill")
new_round2 = UserRound(user_id=100, course_id=164,
                       date=datetime(2019, 11, 16), score=68, course_name="Joralemon")
new_round3 = UserRound(user_id=101, course_id=164,
                       date=datetime(2019, 12, 16), score=68, course_name="Joralemon")
new_round4 = UserRound(user_id=102, course_id=6284,
                       date=datetime(2019, 10, 1), score=68, course_name="Stonykill")
new_round5 = UserRound(user_id=103, course_id=6284,
                       date=datetime(2019, 9, 16), score=68, course_name="Stonykill")
new_round6 = UserRound(user_id=104, course_id=6893,
                       date=datetime(2019, 8, 16), score=68,
                       course_name="Colonial Acres")
new_round7 = UserRound(user_id=105, course_id=6893,
                       date=datetime(2019, 10, 16), score=68,
                       course_name="Colonial Acres")
new_round8 = UserRound(user_id=103, course_id=6284,
                       date=datetime(2019, 7, 16), score=68, course_name="Stonykill")
new_round9 = UserRound(user_id=103, course_id=164,
                       date=datetime(2019, 10, 20), score=68, course_name="Joralemon")
new_round10 = UserRound(user_id=104, course_id=164,
                        date=datetime(2019, 10, 2), score=69, group_rd_id=100, course_name="Joralemon")
new_round11 = UserRound(user_id=105, course_id=164,
                        date=datetime(2019, 10, 2), score=68, group_rd_id=100, course_name="Joralemon")


db.session.add_all([new_round1, new_round2, new_round3, new_round4,
                    new_round5, new_round6, new_round7, new_round8, new_round9, new_round10, new_round11])
db.session.commit()
