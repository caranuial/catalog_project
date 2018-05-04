# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User


engine = create_engine('sqlite:///mycatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# add a default user
user1 = User(name="default", email="default@user.here")
session.add(user1)
session.commit()

# add new categories
cat1 = Category(name="Skis", id=1)
session.add(cat1)
session.commit()

cat2 = Category(name="Snowboards", id=2)
session.add(cat2)
session.commit()

cat3 = Category(name="Gloves", id=3)
session.add(cat3)
session.commit()

cat4 = Category(name="Goggles", id=4)
session.add(cat4)
session.commit()

cat5 = Category(name="Helmets", id=5)
session.add(cat5)
session.commit()

cat6 = Category(name="Poles", id=6)
session.add(cat6)
session.commit()

cat7 = Category(name="Ski Boots", id=7)
session.add(cat7)
session.commit()

cat8 = Category(name="Snowboard Boots", id=8)
session.add(cat8)
session.commit()


# add new items in each category
item = Item(user_id=1, category_id=1, title="Elan Amphobio 16 Ti2 Fusion",
             description="Please fasten your seatbelt because the Amphibio 16 Ti2 is about to take you on the ride of your life. The ultimate ski for groomed snow, this ski is more powerful than a twin turbo and rips long arcs at speed, yet it is nimble enough for tight tracks")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=1, title="Elan Amphobio 14 TI Fusion",
             description=" agility is what you desire and laying down effortless quick and nimble arcs gets your blood pumping, then prepare for the ultimate ride with the Amphibio 14 Ti. Built for quickness, designed to shatter heart monitors.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=1, title="Elan Amphobio 14 TI Power Shift",
             description="Finding one ski that does everything on groomed runs just got easier with the Amphibio 12 Ti. High speed long turns - check. Short turns on steep terrain - check. Cruisng at moderate speeds - Check. No need to keep looking at the menu - take the check")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=1, title="Elan Amphobio 84 Xti Fusion",
             description="They say that 40 is the new 30, but don't believe it. 40 is still 40. BUT, the 84mm is the new 78mm! Versatile, quick, powerful and full of energy - don't let the waist width fool you. It will make you feel like you're 30 again, which is the new 20")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=1, title="Elan Amphobio 84 Ti Fusion",
             description="Groomers, crud, powder and hard pack - pick your poison, because the Amphibio 84 Ti is the elixir. High performance enough for hard charging yet built to be forgiving and easy for those cruising runs at the end of the day. ")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=2, title="Men's Burton Flight Attendant Snowboard", 
			 description=" Balanced Freeride Geometry is the secret with setback camber and sidecut that are centered on your stance to create a twin freestyle feel when riding flat base.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=2, title="Men's Burton Name Dropper LTD Snowboard", 
			 description="Designed to be a terrain-slaying alternative to more traditional twin shapes, the Burton Flight Attendant is a free spirit that dissects both pow and hard-pack with equal precision. ")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=3, title="Women's Burton Glove + Gore warm technology",
             description="Burton Glove + Gore warm technology. DRYRIDE 2L fabric, and a GUARANTEED TO KEEP YOU DRY GORE-TEX membrane protect this Thermacore insulated glove")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=6, title="Leki VENOM SL",
             description="The Venom SL has already won everything in the World Cup circuit. Now it's your turn. The high-strength aluminium upper segment and the strengthened-carbon lower one makes your racing experience an exciting challenge. Trigger S grips are a safe and sporty option while away.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=3, title="Leki WORLDCUP RACE TI S SPEED SYSTEM",
             description="True Race Glove, used by the competitive racer. Pre-curved fingers and digital palm and finger tips allow for enhanced pole grip. Ceramic 3-D finger covers and long padded gauntlet protect in the gates. Heavy duty wristlet provides a good tight fit.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=7, title="Atomic Redster",
             description="It has a 92mm narrow last for a super anatomical fit, Progressive Race Shell and World Cup Liner, our weapon of choice.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=7, title="Technica Firebird",
             description="A proven performer, has podiumed in both speed and tech events, proving itself to be one of the most versatile boots on the World Cup circuit. The R9.3 has exceptional touch on the snow and a smooth progressive flex pattern.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=4, title="SPLASHTACULAR",
             description="Everything is just a little extra with our goggles, and we wouldnt have it any other way")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=4, title="Atomic REVENT L FDL HD OTG",
             description="It is no fun skiing when you are guessing where the bumps are. So we have gone to town on the lenses in our Atomic Revent all-mountain range. In this top model we have added Fusion Double Lens (FDL), a revolutionary double lens with both lenses laminated together.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=8, title="Burton Rampant",
             description="Soft yet supportive with a flex similar to the Concord Speed Zone boot, the Rampant keeps you comfortably connected without sacrificing the support, strength, or cushioning your all-out riding requires.")
session.add(item)
session.commit()

item = Item(user_id=1, category_id=8, title="Burton Concord",
             description="The Burton Concord boot defies convention by combining versatile mid-range response and full-featured tech in a boot thats lighter and lasts longer than the competition.")
session.add(item)
session.commit()

