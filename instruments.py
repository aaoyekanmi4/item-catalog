from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker

from catalog_setup import Category, Base, Item, User

engine = create_engine('sqlite:///musicstore.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#User
User1 = User(name="Don Jones", email="djmusic@udacity.com",
picture='https://pbs.twimg.com/profile_/static/images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()



#contents of each item from amazon.com

#Guitars

category1 = Category(name="Guitars")
category1.items_val = 0
session.add(category1)
session.commit()

guitar1 = Item(name="Rogue RA-090 Dreadnought Acoustic Guitar Natural",
price="$59.99", kind ="acoustic", description="""From Rogue comes this amazing
deal in the RA-90 dreadnought acoustic guitar.
The Rogue guitar is an ideal instrument for the beginner, or young musician.
The body depth and width bring out balanced tone and plenty of projection to
be heard from across the room.This ultra-affordable dreadnought acoustic guitar
features a whitewood body, which brings out lots of mid-range punch. This Rogue
acoustic guitar will certainly get the job done, at a price that anybody can
afford.
""", picture="guitar1.jpg", user_id =1, category = category1)
category1.items_val += 1
session.add(category1)
session.add(guitar1)
session.commit()

guitar2 = Item(
name="Fender Acoustic Guitar CD-60 - Black - Dreadnought",
price="$229.99", kind="acoustic", description="""One of our best-selling
acoustic guitars is now available with the sweet mellow tone of an all-mahogany
body. Recently upgraded features include a new black pickguard, mother-of-pearl
acrylic rosette design, new compensated bridge design, white bridge pins with
black dots and smaller (3mm) dot fingerboard inlays.""",
user_id="1", picture="guitar2.jpg", category =category1)

category1.items_val += 1
session.add(category1)
session.add(guitar2)
session.commit()

guitar3 = Item(name="Yamaha CG122MCH Solid Cedar Top Classical Guitar",
price="$219.99 ", kind="classical",
description="""Drawing upon the vast knowledge and techniques of our master
craftsmen, the CG series nylon string guitars were developed to deliver
top-level sound quality, performance, and playability at a reasonable price.
Many factors of the high-end handcrafted GC series classical guitars have been
implemented to share the improved sound, playability, and cosmetic design.""",
picture = "guitar3.jpg", user_id="1", category =category1)

category1.items_val += 1
session.add(category1)
session.add(guitar3)
session.commit()

guitar4 = Item(name="Student Starter Classical Guitar for Beginner",
price="$59.99 ", kind="classical", description="""
ADM guitars are a prefered choice for music educators and students worldwide.
Sound:With spruce top and laminated basswood back, the guitar produces sound
hat is clear and not distorted.
Playability:Small and light, but produces big, beautiful melodies.
34 inch half size is perfect for kids age 6 to 12.
This classical guitar provides the perfect
combination of style, sound, and savings.
""", picture = "guitar4.jpg", user_id="1", category =category1)

category1.items_val += 1
session.add(category1)
session.add(guitar4)
session.commit()

guitar5 = Item(name="Epiphone Les Paul SPECIAL-II Electric Guitar",
price="$129.00", kind="electric", description="""It gives you all the essential
elements of a Les Paul. Made with a mahogany body, bolt-on mahogany neck,
smooth 22-fret rosewood fingerboard, this baby is every bit as handsome as its
uptown cousins. Features 700T/650R open-coil humbucking pickups that deliver
long, singing sustain and true Les Paul tones. The LockTone Tune-O-Matic bridge
and stopbar tailpiece add more sustain and make string changing easier.
Limited lifetime warranty.""", picture = "guitar5.jpg", user_id="1", category =category1)

category1.items_val += 1
session.add(category1)
session.add(guitar5)
session.commit()

guitar6 = Item(name="Ibanez Artcore AF55 Hollow-Body Electric Guitar",
price="$329.99", kind="electric", description="""The bound, all-maple full
hollowbody provides tight resonance without feedback, perfect for that muted
jazz tone and fully flexible for everything from alt rock to pounding punk.
The mahogany set neck with bound rosewood fretboard is a delight to the digits.
An ACH-ST humbucker at the neck and ACH-ST at the bridge provide a beefy,
quiet signal with pronounced mids.Case sold separately.""",picture = "guitar6.jpg",
 user_id="1", category =category1)

category1.items_val += 1
session.add(category1)
session.add(guitar6)
session.commit()


guitar7 = Item(name="Fender Standard Stratocaster Plus",
price="$599.99", kind="electric", description="""The Standard Stratocaster Plus
Top delivers famous Fender tone and classic style,
with the added elegance of a flame maple top on the alder body.
Other features include three single coil pickups, tinted maple neck with modern
"C"- shaped profile and satin urethane back finish, rosewood or maple
fingerboard with 21 medium jumbo frets and 9.5" radius, three-ply parchment
pick guard and parchment control knobs, vintage-style synchronized tremolo
bridge and '70s-style headstock logo.""", picture = "guitar7.jpg", user_id="1",
category =category1)

category1.items_val += 1
session.add(category1)
session.add(guitar7)
session.commit()

#Basses

category2 = Category(name = "Basses")
category2.items_val = 0

session.add(category2)
session.commit()

bass1 = Item(name="Ibanez GSR200BWNF 4-String Bass Guitar",
price="$199.99", kind="electric", description="""A guitar doesn't have to cost
a bundle to sound good. The GIO series was developed for players who want
Ibanez quality in a more affordable package. Not only do they look and
play better than everything else in their price range, but their rigorous
inspection, set-up and warranty is the same as Ibanez's more expensive models.
""", picture = "bass1.jpg", user_id = 1, category = category2)

category2.items_val += 1
session.add(category2)
session.add(bass1)
session.commit()

bass2 = Item(name="Black Full Size Electric Bass Guitar",
price="$79.95 ", kind="electric",
description="""Davison Guitars is known for providing exceptional value in
quality instruments at affordable prices. This full size bass is the perfect
instrument for anyone looking to add a bass to their collection and its Music
Instructor Approved. Also perfect for any guitar player who has always wanted
 a bass. """, picture = "bass2.jpg",
user_id = 1, category = category2)
category2.items_val += 1
session.add(category2)
session.add(bass2)
session.commit()


bass3 = Item(name="Ibanez PCBE12MHOPN ", price="$249.99 ", kind="acoustic",
description="""With tone, style, playability at an incredible value, Ibanez
acoustic basses are creatively inspiring tools designed to thrive
in wide variety of musical situations.""", picture = "bass3.jpg",
user_id = 1, category = category2)
category2.items_val += 1
session.add(category2)
session.add(bass3)
session.commit()


#Keyboards
category3 = Category(name = "Keyboards")

category3.items_val = 0
session.add(category3)
session.commit()

keyboard1 = Item(name="Williams Legato 88-Key Digital Piano",
price="$199.99 ", description="""Williams Legato is an affordable digital piano
with 88 semi-weighted keys, five great sounds (piano, electric piano, organ,
synth, and bass) and built-in speakers. It also features split/layer function
(to combine sounds) and a built-in metronome. This ultra-portable piano is
perfect for performing and practicing""", picture = "keyboard1.jpg",
user_id = 1, category = category3)

category3.items_val += 1
session.add(category3)
session.add(keyboard1)
session.commit()

keyboard2 = Item(name="RockJam 54-Key Portable Electronic Keyboard",
price="$59.99", description="""The Rock Jam RJ-654 54-Key Digital Piano
Keyboard is perfect for aspiring pianists of all ages.
This compact, portable, and high quality keyboard has built-in stereo speakers
and a large, easy-to-read LCD screen, which serves as a great teaching tool.
""", picture = "keyboard2.jpg", user_id = 1, category = category3)

category3.items_val += 1
session.add(category3)
session.add(keyboard2)
session.commit()

keyboard3 = Item(name="Hamzer 61 Key Electronic Music Electric Keyboard",
price="$79.99", description="""This is a beginner to intermediate level,
multi-function, 61 standard piano-key electronic keyboard. This premium musical
instrument by Hamzer is brand new and includes everything needed to play
right out of the box.""", picture = "keyboard3.jpg", user_id = 1, category = category3)

category3.items_val += 1
session.add(category3)
session.add(keyboard3)
session.commit()

#Drums
category4 = Category(name = "Drumsets")

category4.items_val = 0
session.add(category4)
session.commit()


drum1 = Item(name="Gammon Percussion Full Size Complete Adult 5 Piece Drum Set",
price="$249.95", description="""There are lots of reasons this drum set has been
the BEST SELLER for years! The Gammon Battle Series is the perfect entry level
drum set at the lowest price ever for a complete, adult/full size drum set
complete with all cymbals, stands, hardware, stool heads and sticks! This Brand
New FULL-SIZE Drum Set has everything you need to start playing right away""",
picture = "drum1.jpg", user_id="1", category=category4)
category4.items_val += 1
session.add(category4)
session.add(drum1)
session.commit()

drum2 = Item(name="Mendini by Cecilio 13 Inch 3-Piece Junior Drum Set",
price="$89.99", description="""This is a great drum set for the aspiring
drummer. Smaller sized genuine hard wood shells with triple flanged hoops make
this the perfect first set for the younger player.
It includes everything needed to get off to a great start.
The drums and cymbal are mounted off the bass drum for easy set up
while providing a small foot print, taking up minimal space.""",
picture = "drum2.jpg", user_id="1", category=category4)

category4.items_val += 1
session.add(category4)
session.add(drum2)
session.commit()

drum3 = Item(name="Mendini MJDS-5-BK Complete 16-Inch 5-Piece Junior Drum Set",
price="$156.99", description="""This Mendini by Cecilio 5-Piece Junior Drum Set
with Cymbals is a fully functional drum set designed specifically
for beginner drummers. This set has everything you need to get set up and
playing in no time.  It is a perfect gift for the young drummer who wants the
most realistic experience but may be too small for a full size drum set.""",
picture = "drum3.jpg", user_id="1", category=category4)

category4.items_val += 1
session.add(category4)
session.add(drum3)
session.commit()

#Amps
category5= Category(name = "Amps")

category5.items_val = 0
session.add(category5)
session.commit()

amp1 = Item(name="Fender Frontman 10G Electric Guitar Amplifier",
price="$59.99", description="""Our Frontman amps deliver quality tone at a
great price, with custom-voiced built-in overdrive for great tone and the
unmistakable Fender Blackface look. The 10-watt Frontman 10G features a 6-inch
Special Design speaker and a selectable gain control that can rock guitar tones
from tube-emulated overdrive to full-strength ultra-saturated distortion;
perfect for blues, metal and the famous Fender clean tone.""",
user_id="1", picture = "amp1.jpg", category=category5)

category5.items_val += 1
session.add(category5)
session.add(amp1)
session.commit()

amp2 = Item(name="Marshall Code 25 - 25W 1x10 Digital Combo Amp",
price="$199.99", description="""The Marshall CODE range combines the Marshall
legacy with state of the art technology, culminating in their most versatile and
impressive digital product ever. The range offers a choice of digital amp models,
power amps, cabinet simulations, FX, and more allowing you to dial in every
tonal possibility you need.""", picture = "amp2.jpg", user_id="1", category=category5)
category5.items_val += 1
session.add(category5)
session.add(amp2)
session.commit()

amp3 = Item(name="Fender Champion 20 - 20-Watt Electric Guitar Amplifier",
price="$99.99", description="""Compact, easy to use and versatile enough for any
style of guitar playing, the 20-watt Champion 20 is an ideal choice for your
first practice amp.""", picture = "amp3.jpg", user_id="1", category=category5)
category5.items_val += 1
session.add(category5)
session.add(amp3)
session.commit()




#Accesories
category6 = Category(name = "Accesories")

category6.items_val = 0
session.add(category6)
session.commit()

acc1 = Item(name="KLIQ AirCell Guitar Strap for Bass & Electric Guitar",
price="$34.99", description="""Guitar and bass players familiar with that
end-of-the-gig tight shoulder caused by conventional straps can now find relief
 with the KLIQ AirCell Guitar Strap--the only guitar strap to utilize patented
 air cell core technology for increased comfort and strength. Made from heavy-duty
  reinforced black lycra and neoprene, this strap provides enough elasticity
  needed for relief and shock absorption without being overly stretchy or bouncy
  like most other comfort straps. """,
user_id="1", picture = "acc1.jpg", category=category6)

category6.items_val += 1
session.add(category6)
session.add(acc1)
session.commit()

acc2 = Item(name="String Swing CC01KOAK Hardwood Home & Studio Guitar Hanger",
price="$10.99", description="""The String Swing Guitar Hanger features exclusive
tubing that will not mark the finish on your instrument - Guaranteed!
Its hardwood construction looks fantastic and is built to last. The yoke pivots
to hold any type of headstock and is is adjustable to any width. This hanger
 will display wide or narrow body instruments. """,
 picture = "acc2.jpg", user_id="1", category=category6)

category6.items_val += 1
session.add(category6)
session.add(acc2)
session.commit()







print "added items!"




















































