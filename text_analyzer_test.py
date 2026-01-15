import tempfile
import json
import os
from graph import Graph, Node
from preprocessed_handler import PreProcessedHandler
from tasks_runner import TaskRunner
from main import valid_task_1_arguments, valid_task_2_arguments, valid_task_3_arguments, valid_task_4_arguments, valid_task_5_arguments, valid_task_6_arguments, valid_task_7_arguments, valid_task_8_arguments, valid_task_9_arguments

SENTENCES_TEMPFILE_NAME = 'sentences_tempfile.csv'
NAMES_TEMPFILE_NAME = 'names_tempfile.csv'
REMOVE_WORDS_TEMPFILE_NAME = 'remove_words_tempfile.csv'

JSON_INDENT = 4




WORDS_TO_REMOVE_RAW_DATA = """words
a
about
above
actual
after
again
against
all
alreadi
also
alway
am
amp
an
and
ani
anoth
any
anyth
are
around
as
at
aww
babi
back
be
becaus
because
bed
been
befor
before
being
below
between
birthday
bit
book
both
boy
but
by
call
can
cannot
cant
car
check
com
come
could
day
did
didn
dinner
do
doe
does
doesn
doing
don
done
dont
down
during
each
eat
end
even
ever
everyon
exam
famili
feel
few
final
find
first
follow
for
found
friday
from
further
game
get
girl
give
gone
gonna
got
gotta
guess
guy
had
hair
happen
has
have
haven
having
he
head
hear
her
here
hers
herself
hey
him
himself
his
home
hour
hous
how
http
i
if
im
in
into
is
isn
it
its
itself
job
just
keep
know
last
later
least
leav
let
life
listen
littl
live
look
lot
lunch
made
make
man
mani
may
mayb
me
mean
meet
might
mom
monday
month
more
morn
most
move
movi
much
must
my
myself
need
never
new
night
no
nor
not
noth
now
of
off
on
once
one
onli
only
or
other
ought
our
ours
ourselves
out
over
own
peopl
phone
pic
pictur
play
post
put
quot
rain
read
readi
realli
run
said
same
saw
say
school
see
seem
she
shop
should
show
sinc
sleep
so
some
someon
someth
song
soon
sound
start
stay
still
studi
stuff
such
summer
sunday
sure
take
talk
tell
than
thank
that
the
their
theirs
them
themselves
then
there
these
they
thing
think
this
those
though
thought
through
time
to
today
tomorrow
tonight
too
total
tri
tweet
twitpic
twitter
two
u
under
until
up
updat
use
veri
very
video
wait
wanna
want
was
watch
way
we
weather
week
weekend
went
were
what
when
where
whi
which
while
who
whom
why
will
with
woke
won
work
world
would
www
yay
yeah
year
yes
yesterday
yet
you
your
yours
yourself
yourselves
a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
k
r
s
t
u
v
w
x
u
z
mr
miss
mrs
ms"""

# CONSTANTS FOR CHECKING TASK 1 OUTPUT FLOW

TASK_1_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
    "Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
    ` Is that where-?` whispered Professor  McGonagall.
    "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
    Scars can come in handy.
    I have one myself above my left knee that is a perfect map of the London Underground.
    "Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
    "` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
    "Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
    "Then, suddenly,  Hagrid let out a howl like a wounded dog."
    "` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
    "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
    "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
    "` Well,` said  Dumbledore finally,` that's that."
    We've no business staying here.
    "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
    "` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
    Professor  McGonagall blew  McGonagall nose in reply.
    Dumbledore turned and walked back down the street.
    On the corner  Dumbledore stopped and took out the silver Put- Outer.
    "Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
    Dumbledore could just see the bundle of blankets on the step of number four.
    "` Good luck,  Harry,`  Dumbledore murmured."
    "Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
    "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
    Harry  Potter rolled over inside  Dumbledore blankets without waking up.
    "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
    "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
    "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
    Only the photographs on the mantelpiece really showed how much time had passed.
    "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
    "The room held no sign at all that another boy lived in the house, too."
    """
TASK_1_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
    "Karkaroff looked extremely worried, and  Snape looked angry."
    Karkaroff hovered behind  Snape's desk for the rest of the double period.
    Karkaroff seemed intent on preventing  Snape from slipping away at the end of class.
    "Keen to hear what Karkaroff wanted to say,  Harry deliberately knocked over  Harry bottle of armadillo bile with two minutes to go to the bell, which gave  Harry an excuse to duck down behind  Harry cauldron and mop up while the rest of the class moved noisily toward the door."
    ` What's so urgent?`  Harry heard  Snape hiss at Karkaroff.
    "` This,` said Karkaroff, and  Harry, peering around the edge of  Harry cauldron, saw Karkaroff  pull up the left- hand sleeve of  Harry robe and show  Snape something on  Harry inner forearm."
    "` Well?` said Karkaroff, still making every effort not to move  Harry lips.` Do you see?"
    the boy
    """
TASK_1_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
    "This is urgent,' said  Harry curtly.   '"
    "Ooooh, urgent, is This?'"
    said the other gargoyle in a high- pitched voice.'
    "Well, that's put us in our place, hasn't that?'"
    Harry knocked.
    "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
    You haven't been given another detention!'
    "McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
    """

TASK_1_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
    Over-Attentive Wizard,
    Bertram Aubrey,
    Audrey Weasley,
    "Augusta ""Gran"" Longbottom",
    Augustus Pye,
    Augustus Rookwood,
    Augustus Worme,
    Auntie Muriel,
    Aunt Marge Dursley,
    Aurelius Dumbledore,
    Aurora Sinistra,
    Avery,
    Babajide Akingbade,
    Babayaga,
    Babbitty Rabbitty,
    Bagman Sr.,
    Ludo Bagman,
    Otto Bagman,
    Millicent Bagnold,
    Bathilda Bagshot,batty
    Kquewanda Bailey,
    Ballyfumble Stranger,"quin, quivering quintus, quintusofthesillyname"
    """
TASK_1_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
    Ignatia Wildsmith,
    Ignatius Prewett,
    Ignatius Tuft,
    Ignotus Peverell,
    Igor Karkaroff,
    Illyius,
    Ingolfr the Iambic,
    """
TASK_1_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
    "Magnus ""Dent Head"" Macdonald",
    Magorian,
    Maisie Cattermole,
    Malcolm,
    Malcolm Baddock,
    Malcolm McGonagall,
    Harold Skively,
    Harper,
    Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
    Harvey Ridgebit,
    Hassan Mostafa,
    """

TASK_1_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 1": {
        "Processed Sentences": [
            [
                "tuft",
                "jet",
                "black",
                "forehead",
                "dumbledore",
                "mcgonagall",
                "curiously",
                "shaped",
                "cut",
                "like",
                "bolt",
                "lightning"
            ],
            [
                "whispered",
                "professor",
                "mcgonagall"
            ],
            [
                "dumbledore",
                "dumbledore",
                "ll",
                "scar",
                "forever",
                "couldn",
                "something",
                "scar",
                "dumbledore",
                "wouldn"
            ],
            [
                "scars",
                "handy"
            ],
            [
                "left",
                "knee",
                "perfect",
                "map",
                "london",
                "underground"
            ],
            [
                "well",
                "dumbledore",
                "hagrid",
                "better",
                "dumbledore",
                "took",
                "harry",
                "harry",
                "arms",
                "turned",
                "toward",
                "dursley",
                "dursley",
                "dudley",
                "dursley",
                "house"
            ],
            [
                "good",
                "bye",
                "harry",
                "sir",
                "asked",
                "hagrid"
            ],
            [
                "harry",
                "bent",
                "harry",
                "great",
                "shaggy",
                "harry",
                "gave",
                "scratchy",
                "whiskery",
                "kiss"
            ],
            [
                "suddenly",
                "hagrid",
                "howl",
                "like",
                "wounded",
                "dog"
            ],
            [
                "shhh",
                "hissed",
                "professor",
                "mcgonagall",
                "ll",
                "wake",
                "muggles",
                "sorry",
                "sobbed",
                "hagrid",
                "taking",
                "large",
                "spotted",
                "handkerchief",
                "burying",
                "hagrid",
                "face",
                "handkerchief",
                "stand",
                "handkerchief",
                "lily",
                "james",
                "dead",
                "poor",
                "little",
                "harry",
                "ter",
                "muggles",
                "handkerchief",
                "sad",
                "grip",
                "hagrid",
                "ll",
                "professor",
                "mcgonagall",
                "whispered",
                "patting",
                "hagrid",
                "gingerly",
                "arm",
                "dumbledore",
                "stepped",
                "low",
                "garden",
                "wall",
                "walked",
                "front",
                "door"
            ],
            [
                "dumbledore",
                "laid",
                "harry",
                "gently",
                "doorstep",
                "took",
                "letter",
                "dumbledore",
                "cloak",
                "tucked",
                "letter",
                "inside",
                "harry",
                "blankets",
                "came"
            ],
            [
                "full",
                "minute",
                "three",
                "stood",
                "looked",
                "little",
                "bundle",
                "hagrid",
                "shoulders",
                "shook",
                "professor",
                "mcgonagall",
                "blinked",
                "furiously",
                "twinkling",
                "light",
                "usually",
                "shone",
                "dumbledore",
                "eyes",
                "seemed"
            ],
            [
                "well",
                "dumbledore",
                "finally"
            ],
            [
                "ve",
                "business",
                "staying"
            ],
            [
                "well",
                "go",
                "join",
                "celebrations",
                "hagrid",
                "muffled",
                "voice",
                "ll",
                "takin",
                "sirius",
                "sirius",
                "bike",
                "professor",
                "mcgonagall",
                "professor",
                "dumbledore",
                "sir",
                "wiping",
                "sirius",
                "streaming",
                "eyes",
                "sirius",
                "jacket",
                "sleeve",
                "hagrid",
                "swung",
                "hagrid",
                "onto",
                "motorcycle",
                "kicked",
                "engine",
                "roar",
                "engine",
                "rose",
                "air"
            ],
            [
                "shall",
                "expect",
                "professor",
                "mcgonagall",
                "dumbledore",
                "nodding",
                "voice"
            ],
            [
                "professor",
                "mcgonagall",
                "blew",
                "mcgonagall",
                "nose",
                "reply"
            ],
            [
                "dumbledore",
                "turned",
                "walked",
                "street"
            ],
            [
                "corner",
                "dumbledore",
                "stopped",
                "took",
                "silver",
                "outer"
            ],
            [
                "dumbledore",
                "clicked",
                "outer",
                "twelve",
                "balls",
                "light",
                "sped",
                "balls",
                "street",
                "lamps",
                "privet",
                "drive",
                "glowed",
                "suddenly",
                "orange",
                "dumbledore",
                "tabby",
                "cat",
                "slinking",
                "corner",
                "street"
            ],
            [
                "dumbledore",
                "bundle",
                "blankets",
                "step",
                "number",
                "four"
            ],
            [
                "good",
                "luck",
                "harry",
                "dumbledore",
                "murmured"
            ],
            [
                "dumbledore",
                "turned",
                "dumbledore",
                "heel",
                "swish",
                "dumbledore",
                "cloak",
                "dumbledore"
            ],
            [
                "breeze",
                "ruffled",
                "neat",
                "hedges",
                "privet",
                "drive",
                "lay",
                "silent",
                "tidy",
                "inky",
                "sky",
                "place",
                "expect",
                "astonishing",
                "things"
            ],
            [
                "harry",
                "potter",
                "rolled",
                "inside",
                "dumbledore",
                "blankets",
                "without",
                "waking"
            ],
            [
                "small",
                "hand",
                "closed",
                "letter",
                "beside",
                "dumbledore",
                "dumbledore",
                "slept",
                "knowing",
                "dumbledore",
                "special",
                "knowing",
                "dumbledore",
                "famous",
                "knowing",
                "dumbledore",
                "woken",
                "hours",
                "dursley",
                "scream",
                "dursley",
                "opened",
                "front",
                "door",
                "milk",
                "bottles",
                "dumbledore",
                "spend",
                "next",
                "weeks",
                "prodded",
                "pinched",
                "dumbledore",
                "cousin",
                "dudley",
                "dumbledore",
                "couldn",
                "moment",
                "people",
                "meeting",
                "secret",
                "country",
                "holding",
                "people",
                "glasses",
                "saying",
                "hushed",
                "voices",
                "harry",
                "potter",
                "lived"
            ],
            [
                "vanishing",
                "glass",
                "nearly",
                "ten",
                "years",
                "passed",
                "since",
                "dursley",
                "dursley",
                "dudley",
                "dursley",
                "woken",
                "dursley",
                "dursley",
                "dudley",
                "dursley",
                "nephew",
                "front",
                "step",
                "privet",
                "drive",
                "hardly",
                "changed"
            ],
            [
                "sun",
                "rose",
                "tidy",
                "front",
                "gardens",
                "lit",
                "brass",
                "number",
                "four",
                "dursley",
                "dursley",
                "dudley",
                "dursley",
                "front",
                "door",
                "number",
                "crept",
                "dursley",
                "dursley",
                "dudley",
                "dursley",
                "living",
                "room",
                "almost",
                "exactly",
                "dursley",
                "seen",
                "fateful",
                "news",
                "report",
                "owls"
            ],
            [
                "photographs",
                "mantelpiece",
                "really",
                "showed",
                "passed"
            ],
            [
                "ten",
                "years",
                "ago",
                "lots",
                "pictures",
                "looked",
                "like",
                "large",
                "pink",
                "beach",
                "ball",
                "wearing",
                "different",
                "colored",
                "bonnets",
                "dudley",
                "dursley",
                "longer",
                "baby",
                "photographs",
                "showed",
                "large",
                "blond",
                "riding",
                "bicycle",
                "carousel",
                "fair",
                "playing",
                "computer",
                "father",
                "hugged",
                "kissed",
                "mother"
            ],
            [
                "room",
                "held",
                "sign",
                "another",
                "lived",
                "house"
            ]
        ],
        "Processed Names": [
            [
                [
                    "attentive",
                    "wizard"
                ],
                []
            ],
            [
                [
                    "bertram",
                    "aubrey"
                ],
                []
            ],
            [
                [
                    "audrey",
                    "weasley"
                ],
                []
            ],
            [
                [
                    "augusta",
                    "gran",
                    "longbottom"
                ],
                []
            ],
            [
                [
                    "augustus",
                    "pye"
                ],
                []
            ],
            [
                [
                    "augustus",
                    "rookwood"
                ],
                []
            ],
            [
                [
                    "augustus",
                    "worme"
                ],
                []
            ],
            [
                [
                    "auntie",
                    "muriel"
                ],
                []
            ],
            [
                [
                    "aunt",
                    "marge",
                    "dursley"
                ],
                []
            ],
            [
                [
                    "aurelius",
                    "dumbledore"
                ],
                []
            ],
            [
                [
                    "aurora",
                    "sinistra"
                ],
                []
            ],
            [
                [
                    "avery"
                ],
                []
            ],
            [
                [
                    "babajide",
                    "akingbade"
                ],
                []
            ],
            [
                [
                    "babayaga"
                ],
                []
            ],
            [
                [
                    "babbitty",
                    "rabbitty"
                ],
                []
            ],
            [
                [
                    "bagman",
                    "sr"
                ],
                []
            ],
            [
                [
                    "ludo",
                    "bagman"
                ],
                []
            ],
            [
                [
                    "otto",
                    "bagman"
                ],
                []
            ],
            [
                [
                    "millicent",
                    "bagnold"
                ],
                []
            ],
            [
                [
                    "bathilda",
                    "bagshot"
                ],
                [
                    [
                        "batty"
                    ]
                ]
            ],
            [
                [
                    "kquewanda",
                    "bailey"
                ],
                []
            ],
            [
                [
                    "ballyfumble",
                    "stranger"
                ],
                [
                    [
                        "quin"
                    ],
                    [
                        "quivering",
                        "quintus"
                    ],
                    [
                        "quintusofthesillyname"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_1_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 1": {
        "Processed Sentences": [
            [
                "karkaroff",
                "looked",
                "extremely",
                "worried",
                "snape",
                "looked",
                "angry"
            ],
            [
                "karkaroff",
                "hovered",
                "behind",
                "snape",
                "desk",
                "rest",
                "double",
                "period"
            ],
            [
                "karkaroff",
                "seemed",
                "intent",
                "preventing",
                "snape",
                "slipping",
                "away",
                "class"
            ],
            [
                "keen",
                "karkaroff",
                "wanted",
                "harry",
                "deliberately",
                "knocked",
                "harry",
                "bottle",
                "armadillo",
                "bile",
                "minutes",
                "go",
                "bell",
                "gave",
                "harry",
                "excuse",
                "duck",
                "behind",
                "harry",
                "cauldron",
                "mop",
                "rest",
                "class",
                "moved",
                "noisily",
                "toward",
                "door"
            ],
            [
                "urgent",
                "harry",
                "heard",
                "snape",
                "hiss",
                "karkaroff"
            ],
            [
                "karkaroff",
                "harry",
                "peering",
                "edge",
                "harry",
                "cauldron",
                "karkaroff",
                "pull",
                "left",
                "hand",
                "sleeve",
                "harry",
                "robe",
                "snape",
                "something",
                "harry",
                "inner",
                "forearm"
            ],
            [
                "well",
                "karkaroff",
                "making",
                "every",
                "effort",
                "harry",
                "lips"
            ]
        ],
        "Processed Names": [
            [
                [
                    "ignatia",
                    "wildsmith"
                ],
                []
            ],
            [
                [
                    "ignatius",
                    "prewett"
                ],
                []
            ],
            [
                [
                    "ignatius",
                    "tuft"
                ],
                []
            ],
            [
                [
                    "ignotus",
                    "peverell"
                ],
                []
            ],
            [
                [
                    "igor",
                    "karkaroff"
                ],
                []
            ],
            [
                [
                    "illyius"
                ],
                []
            ],
            [
                [
                    "ingolfr",
                    "iambic"
                ],
                []
            ]
        ]
    }
}'''
TASK_1_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 1": {
        "Processed Sentences": [
            [
                "urgent",
                "harry",
                "curtly"
            ],
            [
                "ooooh",
                "urgent"
            ],
            [
                "gargoyle",
                "high",
                "pitched",
                "voice"
            ],
            [
                "well",
                "us",
                "place",
                "hasn"
            ],
            [
                "harry",
                "knocked"
            ],
            [
                "harry",
                "heard",
                "footsteps",
                "door",
                "opened",
                "harry",
                "harry",
                "face",
                "face",
                "professor",
                "mcgonagall"
            ],
            [
                "given",
                "another",
                "detention"
            ],
            [
                "mcgonagall",
                "mcgonagall",
                "square",
                "spectacles",
                "flashing",
                "alarmingly"
            ]
        ],
        "Processed Names": [
            [
                [
                    "magnus",
                    "dent",
                    "macdonald"
                ],
                []
            ],
            [
                [
                    "magorian"
                ],
                []
            ],
            [
                [
                    "maisie",
                    "cattermole"
                ],
                []
            ],
            [
                [
                    "malcolm"
                ],
                []
            ],
            [
                [
                    "malcolm",
                    "baddock"
                ],
                []
            ],
            [
                [
                    "malcolm",
                    "mcgonagall"
                ],
                []
            ],
            [
                [
                    "harold",
                    "skively"
                ],
                []
            ],
            [
                [
                    "harper"
                ],
                []
            ],
            [
                [
                    "harry",
                    "potter"
                ],
                [
                    [
                        "lived"
                    ],
                    [
                        "undesirable",
                        "number"
                    ],
                    [
                        "chosen"
                    ],
                    [
                        "parry",
                        "otter"
                    ],
                    [
                        "chosen"
                    ],
                    [
                        "mudbloods",
                        "friend"
                    ]
                ]
            ],
            [
                [
                    "harvey",
                    "ridgebit"
                ],
                []
            ],
            [
                [
                    "hassan",
                    "mostafa"
                ],
                []
            ]
        ]
    }
}'''


# CONSTANT FOR TASK 2 UNPROCESSED FLOW TEST

TASK_2_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""
TASK_2_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
    "Karkaroff looked extremely worried, and  Snape looked angry."
    Karkaroff hovered behind  Snape's desk for the rest of the double period.
    Karkaroff seemed intent on preventing  Snape from slipping away at the end of class.
    "Keen to hear what Karkaroff wanted to say,  Harry deliberately knocked over  Harry bottle of armadillo bile with two minutes to go to the bell, which gave  Harry an excuse to duck down behind  Harry cauldron and mop up while the rest of the class moved noisily toward the door."
    ` What's so urgent?`  Harry heard  Snape hiss at Karkaroff.
    "` This,` said Karkaroff, and  Harry, peering around the edge of  Harry cauldron, saw Karkaroff  pull up the left- hand sleeve of  Harry robe and show  Snape something on  Harry inner forearm."
    "` Well?` said Karkaroff, still making every effort not to move  Harry lips.` Do you see?"
    the boy
    """
TASK_2_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
"This is urgent,' said  Harry curtly.   '"
"Ooooh, urgent, is This?'"
said the other gargoyle in a high- pitched voice.'
"Well, that's put us in our place, hasn't that?'"
Harry knocked.
"Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
You haven't been given another detention!'
"McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
"""

TASK_2_EXAMPLE_1_MAXK = 3
TASK_2_EXAMPLE_2_MAXK = 4
TASK_2_EXAMPLE_3_MAXK = 5

TASK_2_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 2": {
        "3-Seq Counts": [
            [
                "1_seq",
                [
                    [
                        "ago",
                        1
                    ],
                    [
                        "air",
                        1
                    ],
                    [
                        "almost",
                        1
                    ],
                    [
                        "another",
                        1
                    ],
                    [
                        "arm",
                        1
                    ],
                    [
                        "arms",
                        1
                    ],
                    [
                        "asked",
                        1
                    ],
                    [
                        "astonishing",
                        1
                    ],
                    [
                        "baby",
                        1
                    ],
                    [
                        "ball",
                        1
                    ],
                    [
                        "balls",
                        2
                    ],
                    [
                        "beach",
                        1
                    ],
                    [
                        "bent",
                        1
                    ],
                    [
                        "beside",
                        1
                    ],
                    [
                        "better",
                        1
                    ],
                    [
                        "bicycle",
                        1
                    ],
                    [
                        "bike",
                        1
                    ],
                    [
                        "black",
                        1
                    ],
                    [
                        "blankets",
                        3
                    ],
                    [
                        "blew",
                        1
                    ],
                    [
                        "blinked",
                        1
                    ],
                    [
                        "blond",
                        1
                    ],
                    [
                        "bolt",
                        1
                    ],
                    [
                        "bonnets",
                        1
                    ],
                    [
                        "bottles",
                        1
                    ],
                    [
                        "brass",
                        1
                    ],
                    [
                        "breeze",
                        1
                    ],
                    [
                        "bundle",
                        2
                    ],
                    [
                        "burying",
                        1
                    ],
                    [
                        "business",
                        1
                    ],
                    [
                        "bye",
                        1
                    ],
                    [
                        "came",
                        1
                    ],
                    [
                        "carousel",
                        1
                    ],
                    [
                        "cat",
                        1
                    ],
                    [
                        "celebrations",
                        1
                    ],
                    [
                        "changed",
                        1
                    ],
                    [
                        "clicked",
                        1
                    ],
                    [
                        "cloak",
                        2
                    ],
                    [
                        "closed",
                        1
                    ],
                    [
                        "colored",
                        1
                    ],
                    [
                        "computer",
                        1
                    ],
                    [
                        "corner",
                        2
                    ],
                    [
                        "couldn",
                        2
                    ],
                    [
                        "country",
                        1
                    ],
                    [
                        "cousin",
                        1
                    ],
                    [
                        "crept",
                        1
                    ],
                    [
                        "curiously",
                        1
                    ],
                    [
                        "cut",
                        1
                    ],
                    [
                        "dead",
                        1
                    ],
                    [
                        "different",
                        1
                    ],
                    [
                        "dog",
                        1
                    ],
                    [
                        "door",
                        3
                    ],
                    [
                        "doorstep",
                        1
                    ],
                    [
                        "drive",
                        3
                    ],
                    [
                        "dudley",
                        7
                    ],
                    [
                        "dumbledore",
                        32
                    ],
                    [
                        "dursley",
                        19
                    ],
                    [
                        "engine",
                        2
                    ],
                    [
                        "exactly",
                        1
                    ],
                    [
                        "expect",
                        2
                    ],
                    [
                        "eyes",
                        2
                    ],
                    [
                        "face",
                        1
                    ],
                    [
                        "fair",
                        1
                    ],
                    [
                        "famous",
                        1
                    ],
                    [
                        "fateful",
                        1
                    ],
                    [
                        "father",
                        1
                    ],
                    [
                        "finally",
                        1
                    ],
                    [
                        "forehead",
                        1
                    ],
                    [
                        "forever",
                        1
                    ],
                    [
                        "four",
                        2
                    ],
                    [
                        "front",
                        5
                    ],
                    [
                        "full",
                        1
                    ],
                    [
                        "furiously",
                        1
                    ],
                    [
                        "garden",
                        1
                    ],
                    [
                        "gardens",
                        1
                    ],
                    [
                        "gave",
                        1
                    ],
                    [
                        "gently",
                        1
                    ],
                    [
                        "gingerly",
                        1
                    ],
                    [
                        "glass",
                        1
                    ],
                    [
                        "glasses",
                        1
                    ],
                    [
                        "glowed",
                        1
                    ],
                    [
                        "go",
                        1
                    ],
                    [
                        "good",
                        2
                    ],
                    [
                        "great",
                        1
                    ],
                    [
                        "grip",
                        1
                    ],
                    [
                        "hagrid",
                        11
                    ],
                    [
                        "hand",
                        1
                    ],
                    [
                        "handkerchief",
                        4
                    ],
                    [
                        "handy",
                        1
                    ],
                    [
                        "hardly",
                        1
                    ],
                    [
                        "harry",
                        12
                    ],
                    [
                        "hedges",
                        1
                    ],
                    [
                        "heel",
                        1
                    ],
                    [
                        "held",
                        1
                    ],
                    [
                        "hissed",
                        1
                    ],
                    [
                        "holding",
                        1
                    ],
                    [
                        "hours",
                        1
                    ],
                    [
                        "house",
                        2
                    ],
                    [
                        "howl",
                        1
                    ],
                    [
                        "hugged",
                        1
                    ],
                    [
                        "hushed",
                        1
                    ],
                    [
                        "inky",
                        1
                    ],
                    [
                        "inside",
                        2
                    ],
                    [
                        "jacket",
                        1
                    ],
                    [
                        "james",
                        1
                    ],
                    [
                        "jet",
                        1
                    ],
                    [
                        "join",
                        1
                    ],
                    [
                        "kicked",
                        1
                    ],
                    [
                        "kiss",
                        1
                    ],
                    [
                        "kissed",
                        1
                    ],
                    [
                        "knee",
                        1
                    ],
                    [
                        "knowing",
                        3
                    ],
                    [
                        "laid",
                        1
                    ],
                    [
                        "lamps",
                        1
                    ],
                    [
                        "large",
                        3
                    ],
                    [
                        "lay",
                        1
                    ],
                    [
                        "left",
                        1
                    ],
                    [
                        "letter",
                        3
                    ],
                    [
                        "light",
                        2
                    ],
                    [
                        "lightning",
                        1
                    ],
                    [
                        "like",
                        3
                    ],
                    [
                        "lily",
                        1
                    ],
                    [
                        "lit",
                        1
                    ],
                    [
                        "little",
                        2
                    ],
                    [
                        "lived",
                        2
                    ],
                    [
                        "living",
                        1
                    ],
                    [
                        "ll",
                        4
                    ],
                    [
                        "london",
                        1
                    ],
                    [
                        "longer",
                        1
                    ],
                    [
                        "looked",
                        2
                    ],
                    [
                        "lots",
                        1
                    ],
                    [
                        "low",
                        1
                    ],
                    [
                        "luck",
                        1
                    ],
                    [
                        "mantelpiece",
                        1
                    ],
                    [
                        "map",
                        1
                    ],
                    [
                        "mcgonagall",
                        9
                    ],
                    [
                        "meeting",
                        1
                    ],
                    [
                        "milk",
                        1
                    ],
                    [
                        "minute",
                        1
                    ],
                    [
                        "moment",
                        1
                    ],
                    [
                        "mother",
                        1
                    ],
                    [
                        "motorcycle",
                        1
                    ],
                    [
                        "muffled",
                        1
                    ],
                    [
                        "muggles",
                        2
                    ],
                    [
                        "murmured",
                        1
                    ],
                    [
                        "nearly",
                        1
                    ],
                    [
                        "neat",
                        1
                    ],
                    [
                        "nephew",
                        1
                    ],
                    [
                        "news",
                        1
                    ],
                    [
                        "next",
                        1
                    ],
                    [
                        "nodding",
                        1
                    ],
                    [
                        "nose",
                        1
                    ],
                    [
                        "number",
                        3
                    ],
                    [
                        "onto",
                        1
                    ],
                    [
                        "opened",
                        1
                    ],
                    [
                        "orange",
                        1
                    ],
                    [
                        "outer",
                        2
                    ],
                    [
                        "owls",
                        1
                    ],
                    [
                        "passed",
                        2
                    ],
                    [
                        "patting",
                        1
                    ],
                    [
                        "people",
                        2
                    ],
                    [
                        "perfect",
                        1
                    ],
                    [
                        "photographs",
                        2
                    ],
                    [
                        "pictures",
                        1
                    ],
                    [
                        "pinched",
                        1
                    ],
                    [
                        "pink",
                        1
                    ],
                    [
                        "place",
                        1
                    ],
                    [
                        "playing",
                        1
                    ],
                    [
                        "poor",
                        1
                    ],
                    [
                        "potter",
                        2
                    ],
                    [
                        "privet",
                        3
                    ],
                    [
                        "prodded",
                        1
                    ],
                    [
                        "professor",
                        8
                    ],
                    [
                        "really",
                        1
                    ],
                    [
                        "reply",
                        1
                    ],
                    [
                        "report",
                        1
                    ],
                    [
                        "riding",
                        1
                    ],
                    [
                        "roar",
                        1
                    ],
                    [
                        "rolled",
                        1
                    ],
                    [
                        "room",
                        2
                    ],
                    [
                        "rose",
                        2
                    ],
                    [
                        "ruffled",
                        1
                    ],
                    [
                        "sad",
                        1
                    ],
                    [
                        "saying",
                        1
                    ],
                    [
                        "scar",
                        2
                    ],
                    [
                        "scars",
                        1
                    ],
                    [
                        "scratchy",
                        1
                    ],
                    [
                        "scream",
                        1
                    ],
                    [
                        "secret",
                        1
                    ],
                    [
                        "seemed",
                        1
                    ],
                    [
                        "seen",
                        1
                    ],
                    [
                        "shaggy",
                        1
                    ],
                    [
                        "shall",
                        1
                    ],
                    [
                        "shaped",
                        1
                    ],
                    [
                        "shhh",
                        1
                    ],
                    [
                        "shone",
                        1
                    ],
                    [
                        "shook",
                        1
                    ],
                    [
                        "shoulders",
                        1
                    ],
                    [
                        "showed",
                        2
                    ],
                    [
                        "sign",
                        1
                    ],
                    [
                        "silent",
                        1
                    ],
                    [
                        "silver",
                        1
                    ],
                    [
                        "since",
                        1
                    ],
                    [
                        "sir",
                        2
                    ],
                    [
                        "sirius",
                        4
                    ],
                    [
                        "sky",
                        1
                    ],
                    [
                        "sleeve",
                        1
                    ],
                    [
                        "slept",
                        1
                    ],
                    [
                        "slinking",
                        1
                    ],
                    [
                        "small",
                        1
                    ],
                    [
                        "sobbed",
                        1
                    ],
                    [
                        "something",
                        1
                    ],
                    [
                        "sorry",
                        1
                    ],
                    [
                        "special",
                        1
                    ],
                    [
                        "sped",
                        1
                    ],
                    [
                        "spend",
                        1
                    ],
                    [
                        "spotted",
                        1
                    ],
                    [
                        "stand",
                        1
                    ],
                    [
                        "staying",
                        1
                    ],
                    [
                        "step",
                        2
                    ],
                    [
                        "stepped",
                        1
                    ],
                    [
                        "stood",
                        1
                    ],
                    [
                        "stopped",
                        1
                    ],
                    [
                        "streaming",
                        1
                    ],
                    [
                        "street",
                        3
                    ],
                    [
                        "suddenly",
                        2
                    ],
                    [
                        "sun",
                        1
                    ],
                    [
                        "swish",
                        1
                    ],
                    [
                        "swung",
                        1
                    ],
                    [
                        "tabby",
                        1
                    ],
                    [
                        "takin",
                        1
                    ],
                    [
                        "taking",
                        1
                    ],
                    [
                        "ten",
                        2
                    ],
                    [
                        "ter",
                        1
                    ],
                    [
                        "things",
                        1
                    ],
                    [
                        "three",
                        1
                    ],
                    [
                        "tidy",
                        2
                    ],
                    [
                        "took",
                        3
                    ],
                    [
                        "toward",
                        1
                    ],
                    [
                        "tucked",
                        1
                    ],
                    [
                        "tuft",
                        1
                    ],
                    [
                        "turned",
                        3
                    ],
                    [
                        "twelve",
                        1
                    ],
                    [
                        "twinkling",
                        1
                    ],
                    [
                        "underground",
                        1
                    ],
                    [
                        "usually",
                        1
                    ],
                    [
                        "vanishing",
                        1
                    ],
                    [
                        "ve",
                        1
                    ],
                    [
                        "voice",
                        2
                    ],
                    [
                        "voices",
                        1
                    ],
                    [
                        "wake",
                        1
                    ],
                    [
                        "waking",
                        1
                    ],
                    [
                        "walked",
                        2
                    ],
                    [
                        "wall",
                        1
                    ],
                    [
                        "wearing",
                        1
                    ],
                    [
                        "weeks",
                        1
                    ],
                    [
                        "well",
                        3
                    ],
                    [
                        "whiskery",
                        1
                    ],
                    [
                        "whispered",
                        2
                    ],
                    [
                        "wiping",
                        1
                    ],
                    [
                        "without",
                        1
                    ],
                    [
                        "woken",
                        2
                    ],
                    [
                        "wouldn",
                        1
                    ],
                    [
                        "wounded",
                        1
                    ],
                    [
                        "years",
                        2
                    ]
                ]
            ],
            [
                "2_seq",
                [
                    [
                        "ago lots",
                        1
                    ],
                    [
                        "almost exactly",
                        1
                    ],
                    [
                        "another lived",
                        1
                    ],
                    [
                        "arm dumbledore",
                        1
                    ],
                    [
                        "arms turned",
                        1
                    ],
                    [
                        "asked hagrid",
                        1
                    ],
                    [
                        "astonishing things",
                        1
                    ],
                    [
                        "baby photographs",
                        1
                    ],
                    [
                        "ball wearing",
                        1
                    ],
                    [
                        "balls light",
                        1
                    ],
                    [
                        "balls street",
                        1
                    ],
                    [
                        "beach ball",
                        1
                    ],
                    [
                        "bent harry",
                        1
                    ],
                    [
                        "beside dumbledore",
                        1
                    ],
                    [
                        "better dumbledore",
                        1
                    ],
                    [
                        "bicycle carousel",
                        1
                    ],
                    [
                        "bike professor",
                        1
                    ],
                    [
                        "black forehead",
                        1
                    ],
                    [
                        "blankets came",
                        1
                    ],
                    [
                        "blankets step",
                        1
                    ],
                    [
                        "blankets without",
                        1
                    ],
                    [
                        "blew mcgonagall",
                        1
                    ],
                    [
                        "blinked furiously",
                        1
                    ],
                    [
                        "blond riding",
                        1
                    ],
                    [
                        "bolt lightning",
                        1
                    ],
                    [
                        "bonnets dudley",
                        1
                    ],
                    [
                        "bottles dumbledore",
                        1
                    ],
                    [
                        "brass number",
                        1
                    ],
                    [
                        "breeze ruffled",
                        1
                    ],
                    [
                        "bundle blankets",
                        1
                    ],
                    [
                        "bundle hagrid",
                        1
                    ],
                    [
                        "burying hagrid",
                        1
                    ],
                    [
                        "business staying",
                        1
                    ],
                    [
                        "bye harry",
                        1
                    ],
                    [
                        "carousel fair",
                        1
                    ],
                    [
                        "cat slinking",
                        1
                    ],
                    [
                        "celebrations hagrid",
                        1
                    ],
                    [
                        "clicked outer",
                        1
                    ],
                    [
                        "cloak dumbledore",
                        1
                    ],
                    [
                        "cloak tucked",
                        1
                    ],
                    [
                        "closed letter",
                        1
                    ],
                    [
                        "colored bonnets",
                        1
                    ],
                    [
                        "computer father",
                        1
                    ],
                    [
                        "corner dumbledore",
                        1
                    ],
                    [
                        "corner street",
                        1
                    ],
                    [
                        "couldn moment",
                        1
                    ],
                    [
                        "couldn something",
                        1
                    ],
                    [
                        "country holding",
                        1
                    ],
                    [
                        "cousin dudley",
                        1
                    ],
                    [
                        "crept dursley",
                        1
                    ],
                    [
                        "curiously shaped",
                        1
                    ],
                    [
                        "cut like",
                        1
                    ],
                    [
                        "dead poor",
                        1
                    ],
                    [
                        "different colored",
                        1
                    ],
                    [
                        "door milk",
                        1
                    ],
                    [
                        "door number",
                        1
                    ],
                    [
                        "doorstep took",
                        1
                    ],
                    [
                        "drive glowed",
                        1
                    ],
                    [
                        "drive hardly",
                        1
                    ],
                    [
                        "drive lay",
                        1
                    ],
                    [
                        "dudley dumbledore",
                        1
                    ],
                    [
                        "dudley dursley",
                        6
                    ],
                    [
                        "dumbledore blankets",
                        1
                    ],
                    [
                        "dumbledore bundle",
                        1
                    ],
                    [
                        "dumbledore clicked",
                        1
                    ],
                    [
                        "dumbledore cloak",
                        2
                    ],
                    [
                        "dumbledore couldn",
                        1
                    ],
                    [
                        "dumbledore cousin",
                        1
                    ],
                    [
                        "dumbledore dumbledore",
                        2
                    ],
                    [
                        "dumbledore eyes",
                        1
                    ],
                    [
                        "dumbledore famous",
                        1
                    ],
                    [
                        "dumbledore finally",
                        1
                    ],
                    [
                        "dumbledore hagrid",
                        1
                    ],
                    [
                        "dumbledore heel",
                        1
                    ],
                    [
                        "dumbledore laid",
                        1
                    ],
                    [
                        "dumbledore ll",
                        1
                    ],
                    [
                        "dumbledore mcgonagall",
                        1
                    ],
                    [
                        "dumbledore murmured",
                        1
                    ],
                    [
                        "dumbledore nodding",
                        1
                    ],
                    [
                        "dumbledore sir",
                        1
                    ],
                    [
                        "dumbledore slept",
                        1
                    ],
                    [
                        "dumbledore special",
                        1
                    ],
                    [
                        "dumbledore spend",
                        1
                    ],
                    [
                        "dumbledore stepped",
                        1
                    ],
                    [
                        "dumbledore stopped",
                        1
                    ],
                    [
                        "dumbledore tabby",
                        1
                    ],
                    [
                        "dumbledore took",
                        1
                    ],
                    [
                        "dumbledore turned",
                        2
                    ],
                    [
                        "dumbledore woken",
                        1
                    ],
                    [
                        "dumbledore wouldn",
                        1
                    ],
                    [
                        "dursley dudley",
                        5
                    ],
                    [
                        "dursley dursley",
                        5
                    ],
                    [
                        "dursley front",
                        1
                    ],
                    [
                        "dursley house",
                        1
                    ],
                    [
                        "dursley living",
                        1
                    ],
                    [
                        "dursley longer",
                        1
                    ],
                    [
                        "dursley nephew",
                        1
                    ],
                    [
                        "dursley opened",
                        1
                    ],
                    [
                        "dursley scream",
                        1
                    ],
                    [
                        "dursley seen",
                        1
                    ],
                    [
                        "dursley woken",
                        1
                    ],
                    [
                        "engine roar",
                        1
                    ],
                    [
                        "engine rose",
                        1
                    ],
                    [
                        "exactly dursley",
                        1
                    ],
                    [
                        "expect astonishing",
                        1
                    ],
                    [
                        "expect professor",
                        1
                    ],
                    [
                        "eyes seemed",
                        1
                    ],
                    [
                        "eyes sirius",
                        1
                    ],
                    [
                        "face handkerchief",
                        1
                    ],
                    [
                        "fair playing",
                        1
                    ],
                    [
                        "famous knowing",
                        1
                    ],
                    [
                        "fateful news",
                        1
                    ],
                    [
                        "father hugged",
                        1
                    ],
                    [
                        "forehead dumbledore",
                        1
                    ],
                    [
                        "forever couldn",
                        1
                    ],
                    [
                        "four dursley",
                        1
                    ],
                    [
                        "front door",
                        3
                    ],
                    [
                        "front gardens",
                        1
                    ],
                    [
                        "front step",
                        1
                    ],
                    [
                        "full minute",
                        1
                    ],
                    [
                        "furiously twinkling",
                        1
                    ],
                    [
                        "garden wall",
                        1
                    ],
                    [
                        "gardens lit",
                        1
                    ],
                    [
                        "gave scratchy",
                        1
                    ],
                    [
                        "gently doorstep",
                        1
                    ],
                    [
                        "gingerly arm",
                        1
                    ],
                    [
                        "glass nearly",
                        1
                    ],
                    [
                        "glasses saying",
                        1
                    ],
                    [
                        "glowed suddenly",
                        1
                    ],
                    [
                        "go join",
                        1
                    ],
                    [
                        "good bye",
                        1
                    ],
                    [
                        "good luck",
                        1
                    ],
                    [
                        "great shaggy",
                        1
                    ],
                    [
                        "grip hagrid",
                        1
                    ],
                    [
                        "hagrid better",
                        1
                    ],
                    [
                        "hagrid face",
                        1
                    ],
                    [
                        "hagrid gingerly",
                        1
                    ],
                    [
                        "hagrid howl",
                        1
                    ],
                    [
                        "hagrid ll",
                        1
                    ],
                    [
                        "hagrid muffled",
                        1
                    ],
                    [
                        "hagrid onto",
                        1
                    ],
                    [
                        "hagrid shoulders",
                        1
                    ],
                    [
                        "hagrid swung",
                        1
                    ],
                    [
                        "hagrid taking",
                        1
                    ],
                    [
                        "hand closed",
                        1
                    ],
                    [
                        "handkerchief burying",
                        1
                    ],
                    [
                        "handkerchief lily",
                        1
                    ],
                    [
                        "handkerchief sad",
                        1
                    ],
                    [
                        "handkerchief stand",
                        1
                    ],
                    [
                        "hardly changed",
                        1
                    ],
                    [
                        "harry arms",
                        1
                    ],
                    [
                        "harry bent",
                        1
                    ],
                    [
                        "harry blankets",
                        1
                    ],
                    [
                        "harry dumbledore",
                        1
                    ],
                    [
                        "harry gave",
                        1
                    ],
                    [
                        "harry gently",
                        1
                    ],
                    [
                        "harry great",
                        1
                    ],
                    [
                        "harry harry",
                        1
                    ],
                    [
                        "harry potter",
                        2
                    ],
                    [
                        "harry sir",
                        1
                    ],
                    [
                        "harry ter",
                        1
                    ],
                    [
                        "hedges privet",
                        1
                    ],
                    [
                        "heel swish",
                        1
                    ],
                    [
                        "held sign",
                        1
                    ],
                    [
                        "hissed professor",
                        1
                    ],
                    [
                        "holding people",
                        1
                    ],
                    [
                        "hours dursley",
                        1
                    ],
                    [
                        "howl like",
                        1
                    ],
                    [
                        "hugged kissed",
                        1
                    ],
                    [
                        "hushed voices",
                        1
                    ],
                    [
                        "inky sky",
                        1
                    ],
                    [
                        "inside dumbledore",
                        1
                    ],
                    [
                        "inside harry",
                        1
                    ],
                    [
                        "jacket sleeve",
                        1
                    ],
                    [
                        "james dead",
                        1
                    ],
                    [
                        "jet black",
                        1
                    ],
                    [
                        "join celebrations",
                        1
                    ],
                    [
                        "kicked engine",
                        1
                    ],
                    [
                        "kissed mother",
                        1
                    ],
                    [
                        "knee perfect",
                        1
                    ],
                    [
                        "knowing dumbledore",
                        3
                    ],
                    [
                        "laid harry",
                        1
                    ],
                    [
                        "lamps privet",
                        1
                    ],
                    [
                        "large blond",
                        1
                    ],
                    [
                        "large pink",
                        1
                    ],
                    [
                        "large spotted",
                        1
                    ],
                    [
                        "lay silent",
                        1
                    ],
                    [
                        "left knee",
                        1
                    ],
                    [
                        "letter beside",
                        1
                    ],
                    [
                        "letter dumbledore",
                        1
                    ],
                    [
                        "letter inside",
                        1
                    ],
                    [
                        "light sped",
                        1
                    ],
                    [
                        "light usually",
                        1
                    ],
                    [
                        "like bolt",
                        1
                    ],
                    [
                        "like large",
                        1
                    ],
                    [
                        "like wounded",
                        1
                    ],
                    [
                        "lily james",
                        1
                    ],
                    [
                        "lit brass",
                        1
                    ],
                    [
                        "little bundle",
                        1
                    ],
                    [
                        "little harry",
                        1
                    ],
                    [
                        "lived house",
                        1
                    ],
                    [
                        "living room",
                        1
                    ],
                    [
                        "ll professor",
                        1
                    ],
                    [
                        "ll scar",
                        1
                    ],
                    [
                        "ll takin",
                        1
                    ],
                    [
                        "ll wake",
                        1
                    ],
                    [
                        "london underground",
                        1
                    ],
                    [
                        "longer baby",
                        1
                    ],
                    [
                        "looked like",
                        1
                    ],
                    [
                        "looked little",
                        1
                    ],
                    [
                        "lots pictures",
                        1
                    ],
                    [
                        "low garden",
                        1
                    ],
                    [
                        "luck harry",
                        1
                    ],
                    [
                        "mantelpiece really",
                        1
                    ],
                    [
                        "map london",
                        1
                    ],
                    [
                        "mcgonagall blew",
                        1
                    ],
                    [
                        "mcgonagall blinked",
                        1
                    ],
                    [
                        "mcgonagall curiously",
                        1
                    ],
                    [
                        "mcgonagall dumbledore",
                        1
                    ],
                    [
                        "mcgonagall ll",
                        1
                    ],
                    [
                        "mcgonagall nose",
                        1
                    ],
                    [
                        "mcgonagall professor",
                        1
                    ],
                    [
                        "mcgonagall whispered",
                        1
                    ],
                    [
                        "meeting secret",
                        1
                    ],
                    [
                        "milk bottles",
                        1
                    ],
                    [
                        "minute three",
                        1
                    ],
                    [
                        "moment people",
                        1
                    ],
                    [
                        "motorcycle kicked",
                        1
                    ],
                    [
                        "muffled voice",
                        1
                    ],
                    [
                        "muggles handkerchief",
                        1
                    ],
                    [
                        "muggles sorry",
                        1
                    ],
                    [
                        "nearly ten",
                        1
                    ],
                    [
                        "neat hedges",
                        1
                    ],
                    [
                        "nephew front",
                        1
                    ],
                    [
                        "news report",
                        1
                    ],
                    [
                        "next weeks",
                        1
                    ],
                    [
                        "nodding voice",
                        1
                    ],
                    [
                        "nose reply",
                        1
                    ],
                    [
                        "number crept",
                        1
                    ],
                    [
                        "number four",
                        2
                    ],
                    [
                        "onto motorcycle",
                        1
                    ],
                    [
                        "opened front",
                        1
                    ],
                    [
                        "orange dumbledore",
                        1
                    ],
                    [
                        "outer twelve",
                        1
                    ],
                    [
                        "passed since",
                        1
                    ],
                    [
                        "patting hagrid",
                        1
                    ],
                    [
                        "people glasses",
                        1
                    ],
                    [
                        "people meeting",
                        1
                    ],
                    [
                        "perfect map",
                        1
                    ],
                    [
                        "photographs mantelpiece",
                        1
                    ],
                    [
                        "photographs showed",
                        1
                    ],
                    [
                        "pictures looked",
                        1
                    ],
                    [
                        "pinched dumbledore",
                        1
                    ],
                    [
                        "pink beach",
                        1
                    ],
                    [
                        "place expect",
                        1
                    ],
                    [
                        "playing computer",
                        1
                    ],
                    [
                        "poor little",
                        1
                    ],
                    [
                        "potter lived",
                        1
                    ],
                    [
                        "potter rolled",
                        1
                    ],
                    [
                        "privet drive",
                        3
                    ],
                    [
                        "prodded pinched",
                        1
                    ],
                    [
                        "professor dumbledore",
                        1
                    ],
                    [
                        "professor mcgonagall",
                        7
                    ],
                    [
                        "really showed",
                        1
                    ],
                    [
                        "report owls",
                        1
                    ],
                    [
                        "riding bicycle",
                        1
                    ],
                    [
                        "roar engine",
                        1
                    ],
                    [
                        "rolled inside",
                        1
                    ],
                    [
                        "room almost",
                        1
                    ],
                    [
                        "room held",
                        1
                    ],
                    [
                        "rose air",
                        1
                    ],
                    [
                        "rose tidy",
                        1
                    ],
                    [
                        "ruffled neat",
                        1
                    ],
                    [
                        "sad grip",
                        1
                    ],
                    [
                        "saying hushed",
                        1
                    ],
                    [
                        "scar dumbledore",
                        1
                    ],
                    [
                        "scar forever",
                        1
                    ],
                    [
                        "scars handy",
                        1
                    ],
                    [
                        "scratchy whiskery",
                        1
                    ],
                    [
                        "scream dursley",
                        1
                    ],
                    [
                        "secret country",
                        1
                    ],
                    [
                        "seen fateful",
                        1
                    ],
                    [
                        "shaggy harry",
                        1
                    ],
                    [
                        "shall expect",
                        1
                    ],
                    [
                        "shaped cut",
                        1
                    ],
                    [
                        "shhh hissed",
                        1
                    ],
                    [
                        "shone dumbledore",
                        1
                    ],
                    [
                        "shook professor",
                        1
                    ],
                    [
                        "shoulders shook",
                        1
                    ],
                    [
                        "showed large",
                        1
                    ],
                    [
                        "showed passed",
                        1
                    ],
                    [
                        "sign another",
                        1
                    ],
                    [
                        "silent tidy",
                        1
                    ],
                    [
                        "silver outer",
                        1
                    ],
                    [
                        "since dursley",
                        1
                    ],
                    [
                        "sir asked",
                        1
                    ],
                    [
                        "sir wiping",
                        1
                    ],
                    [
                        "sirius bike",
                        1
                    ],
                    [
                        "sirius jacket",
                        1
                    ],
                    [
                        "sirius sirius",
                        1
                    ],
                    [
                        "sirius streaming",
                        1
                    ],
                    [
                        "sky place",
                        1
                    ],
                    [
                        "sleeve hagrid",
                        1
                    ],
                    [
                        "slept knowing",
                        1
                    ],
                    [
                        "slinking corner",
                        1
                    ],
                    [
                        "small hand",
                        1
                    ],
                    [
                        "sobbed hagrid",
                        1
                    ],
                    [
                        "something scar",
                        1
                    ],
                    [
                        "sorry sobbed",
                        1
                    ],
                    [
                        "special knowing",
                        1
                    ],
                    [
                        "sped balls",
                        1
                    ],
                    [
                        "spend next",
                        1
                    ],
                    [
                        "spotted handkerchief",
                        1
                    ],
                    [
                        "stand handkerchief",
                        1
                    ],
                    [
                        "step number",
                        1
                    ],
                    [
                        "step privet",
                        1
                    ],
                    [
                        "stepped low",
                        1
                    ],
                    [
                        "stood looked",
                        1
                    ],
                    [
                        "stopped took",
                        1
                    ],
                    [
                        "streaming eyes",
                        1
                    ],
                    [
                        "street lamps",
                        1
                    ],
                    [
                        "suddenly hagrid",
                        1
                    ],
                    [
                        "suddenly orange",
                        1
                    ],
                    [
                        "sun rose",
                        1
                    ],
                    [
                        "swish dumbledore",
                        1
                    ],
                    [
                        "swung hagrid",
                        1
                    ],
                    [
                        "tabby cat",
                        1
                    ],
                    [
                        "takin sirius",
                        1
                    ],
                    [
                        "taking large",
                        1
                    ],
                    [
                        "ten years",
                        2
                    ],
                    [
                        "ter muggles",
                        1
                    ],
                    [
                        "three stood",
                        1
                    ],
                    [
                        "tidy front",
                        1
                    ],
                    [
                        "tidy inky",
                        1
                    ],
                    [
                        "took harry",
                        1
                    ],
                    [
                        "took letter",
                        1
                    ],
                    [
                        "took silver",
                        1
                    ],
                    [
                        "toward dursley",
                        1
                    ],
                    [
                        "tucked letter",
                        1
                    ],
                    [
                        "tuft jet",
                        1
                    ],
                    [
                        "turned dumbledore",
                        1
                    ],
                    [
                        "turned toward",
                        1
                    ],
                    [
                        "turned walked",
                        1
                    ],
                    [
                        "twelve balls",
                        1
                    ],
                    [
                        "twinkling light",
                        1
                    ],
                    [
                        "usually shone",
                        1
                    ],
                    [
                        "vanishing glass",
                        1
                    ],
                    [
                        "ve business",
                        1
                    ],
                    [
                        "voice ll",
                        1
                    ],
                    [
                        "voices harry",
                        1
                    ],
                    [
                        "wake muggles",
                        1
                    ],
                    [
                        "walked front",
                        1
                    ],
                    [
                        "walked street",
                        1
                    ],
                    [
                        "wall walked",
                        1
                    ],
                    [
                        "wearing different",
                        1
                    ],
                    [
                        "weeks prodded",
                        1
                    ],
                    [
                        "well dumbledore",
                        2
                    ],
                    [
                        "well go",
                        1
                    ],
                    [
                        "whiskery kiss",
                        1
                    ],
                    [
                        "whispered patting",
                        1
                    ],
                    [
                        "whispered professor",
                        1
                    ],
                    [
                        "wiping sirius",
                        1
                    ],
                    [
                        "without waking",
                        1
                    ],
                    [
                        "woken dursley",
                        1
                    ],
                    [
                        "woken hours",
                        1
                    ],
                    [
                        "wounded dog",
                        1
                    ],
                    [
                        "years ago",
                        1
                    ],
                    [
                        "years passed",
                        1
                    ]
                ]
            ],
            [
                "3_seq",
                [
                    [
                        "ago lots pictures",
                        1
                    ],
                    [
                        "almost exactly dursley",
                        1
                    ],
                    [
                        "another lived house",
                        1
                    ],
                    [
                        "arm dumbledore stepped",
                        1
                    ],
                    [
                        "arms turned toward",
                        1
                    ],
                    [
                        "baby photographs showed",
                        1
                    ],
                    [
                        "ball wearing different",
                        1
                    ],
                    [
                        "balls light sped",
                        1
                    ],
                    [
                        "balls street lamps",
                        1
                    ],
                    [
                        "beach ball wearing",
                        1
                    ],
                    [
                        "bent harry great",
                        1
                    ],
                    [
                        "beside dumbledore dumbledore",
                        1
                    ],
                    [
                        "better dumbledore took",
                        1
                    ],
                    [
                        "bicycle carousel fair",
                        1
                    ],
                    [
                        "bike professor mcgonagall",
                        1
                    ],
                    [
                        "black forehead dumbledore",
                        1
                    ],
                    [
                        "blankets step number",
                        1
                    ],
                    [
                        "blankets without waking",
                        1
                    ],
                    [
                        "blew mcgonagall nose",
                        1
                    ],
                    [
                        "blinked furiously twinkling",
                        1
                    ],
                    [
                        "blond riding bicycle",
                        1
                    ],
                    [
                        "bonnets dudley dursley",
                        1
                    ],
                    [
                        "bottles dumbledore spend",
                        1
                    ],
                    [
                        "brass number four",
                        1
                    ],
                    [
                        "breeze ruffled neat",
                        1
                    ],
                    [
                        "bundle blankets step",
                        1
                    ],
                    [
                        "bundle hagrid shoulders",
                        1
                    ],
                    [
                        "burying hagrid face",
                        1
                    ],
                    [
                        "bye harry sir",
                        1
                    ],
                    [
                        "carousel fair playing",
                        1
                    ],
                    [
                        "cat slinking corner",
                        1
                    ],
                    [
                        "celebrations hagrid muffled",
                        1
                    ],
                    [
                        "clicked outer twelve",
                        1
                    ],
                    [
                        "cloak tucked letter",
                        1
                    ],
                    [
                        "closed letter beside",
                        1
                    ],
                    [
                        "colored bonnets dudley",
                        1
                    ],
                    [
                        "computer father hugged",
                        1
                    ],
                    [
                        "corner dumbledore stopped",
                        1
                    ],
                    [
                        "couldn moment people",
                        1
                    ],
                    [
                        "couldn something scar",
                        1
                    ],
                    [
                        "country holding people",
                        1
                    ],
                    [
                        "cousin dudley dumbledore",
                        1
                    ],
                    [
                        "crept dursley dursley",
                        1
                    ],
                    [
                        "curiously shaped cut",
                        1
                    ],
                    [
                        "cut like bolt",
                        1
                    ],
                    [
                        "dead poor little",
                        1
                    ],
                    [
                        "different colored bonnets",
                        1
                    ],
                    [
                        "door milk bottles",
                        1
                    ],
                    [
                        "door number crept",
                        1
                    ],
                    [
                        "doorstep took letter",
                        1
                    ],
                    [
                        "drive glowed suddenly",
                        1
                    ],
                    [
                        "drive hardly changed",
                        1
                    ],
                    [
                        "drive lay silent",
                        1
                    ],
                    [
                        "dudley dumbledore couldn",
                        1
                    ],
                    [
                        "dudley dursley front",
                        1
                    ],
                    [
                        "dudley dursley house",
                        1
                    ],
                    [
                        "dudley dursley living",
                        1
                    ],
                    [
                        "dudley dursley longer",
                        1
                    ],
                    [
                        "dudley dursley nephew",
                        1
                    ],
                    [
                        "dudley dursley woken",
                        1
                    ],
                    [
                        "dumbledore blankets without",
                        1
                    ],
                    [
                        "dumbledore bundle blankets",
                        1
                    ],
                    [
                        "dumbledore clicked outer",
                        1
                    ],
                    [
                        "dumbledore cloak dumbledore",
                        1
                    ],
                    [
                        "dumbledore cloak tucked",
                        1
                    ],
                    [
                        "dumbledore couldn moment",
                        1
                    ],
                    [
                        "dumbledore cousin dudley",
                        1
                    ],
                    [
                        "dumbledore dumbledore ll",
                        1
                    ],
                    [
                        "dumbledore dumbledore slept",
                        1
                    ],
                    [
                        "dumbledore eyes seemed",
                        1
                    ],
                    [
                        "dumbledore famous knowing",
                        1
                    ],
                    [
                        "dumbledore hagrid better",
                        1
                    ],
                    [
                        "dumbledore heel swish",
                        1
                    ],
                    [
                        "dumbledore laid harry",
                        1
                    ],
                    [
                        "dumbledore ll scar",
                        1
                    ],
                    [
                        "dumbledore mcgonagall curiously",
                        1
                    ],
                    [
                        "dumbledore nodding voice",
                        1
                    ],
                    [
                        "dumbledore sir wiping",
                        1
                    ],
                    [
                        "dumbledore slept knowing",
                        1
                    ],
                    [
                        "dumbledore special knowing",
                        1
                    ],
                    [
                        "dumbledore spend next",
                        1
                    ],
                    [
                        "dumbledore stepped low",
                        1
                    ],
                    [
                        "dumbledore stopped took",
                        1
                    ],
                    [
                        "dumbledore tabby cat",
                        1
                    ],
                    [
                        "dumbledore took harry",
                        1
                    ],
                    [
                        "dumbledore turned dumbledore",
                        1
                    ],
                    [
                        "dumbledore turned walked",
                        1
                    ],
                    [
                        "dumbledore woken hours",
                        1
                    ],
                    [
                        "dursley dudley dursley",
                        5
                    ],
                    [
                        "dursley dursley dudley",
                        5
                    ],
                    [
                        "dursley front door",
                        1
                    ],
                    [
                        "dursley living room",
                        1
                    ],
                    [
                        "dursley longer baby",
                        1
                    ],
                    [
                        "dursley nephew front",
                        1
                    ],
                    [
                        "dursley opened front",
                        1
                    ],
                    [
                        "dursley scream dursley",
                        1
                    ],
                    [
                        "dursley seen fateful",
                        1
                    ],
                    [
                        "dursley woken dursley",
                        1
                    ],
                    [
                        "engine roar engine",
                        1
                    ],
                    [
                        "engine rose air",
                        1
                    ],
                    [
                        "exactly dursley seen",
                        1
                    ],
                    [
                        "expect astonishing things",
                        1
                    ],
                    [
                        "expect professor mcgonagall",
                        1
                    ],
                    [
                        "eyes sirius jacket",
                        1
                    ],
                    [
                        "face handkerchief stand",
                        1
                    ],
                    [
                        "fair playing computer",
                        1
                    ],
                    [
                        "famous knowing dumbledore",
                        1
                    ],
                    [
                        "fateful news report",
                        1
                    ],
                    [
                        "father hugged kissed",
                        1
                    ],
                    [
                        "forehead dumbledore mcgonagall",
                        1
                    ],
                    [
                        "forever couldn something",
                        1
                    ],
                    [
                        "four dursley dursley",
                        1
                    ],
                    [
                        "front door milk",
                        1
                    ],
                    [
                        "front door number",
                        1
                    ],
                    [
                        "front gardens lit",
                        1
                    ],
                    [
                        "front step privet",
                        1
                    ],
                    [
                        "full minute three",
                        1
                    ],
                    [
                        "furiously twinkling light",
                        1
                    ],
                    [
                        "garden wall walked",
                        1
                    ],
                    [
                        "gardens lit brass",
                        1
                    ],
                    [
                        "gave scratchy whiskery",
                        1
                    ],
                    [
                        "gently doorstep took",
                        1
                    ],
                    [
                        "gingerly arm dumbledore",
                        1
                    ],
                    [
                        "glass nearly ten",
                        1
                    ],
                    [
                        "glasses saying hushed",
                        1
                    ],
                    [
                        "glowed suddenly orange",
                        1
                    ],
                    [
                        "go join celebrations",
                        1
                    ],
                    [
                        "good bye harry",
                        1
                    ],
                    [
                        "good luck harry",
                        1
                    ],
                    [
                        "great shaggy harry",
                        1
                    ],
                    [
                        "grip hagrid ll",
                        1
                    ],
                    [
                        "hagrid better dumbledore",
                        1
                    ],
                    [
                        "hagrid face handkerchief",
                        1
                    ],
                    [
                        "hagrid gingerly arm",
                        1
                    ],
                    [
                        "hagrid howl like",
                        1
                    ],
                    [
                        "hagrid ll professor",
                        1
                    ],
                    [
                        "hagrid muffled voice",
                        1
                    ],
                    [
                        "hagrid onto motorcycle",
                        1
                    ],
                    [
                        "hagrid shoulders shook",
                        1
                    ],
                    [
                        "hagrid swung hagrid",
                        1
                    ],
                    [
                        "hagrid taking large",
                        1
                    ],
                    [
                        "hand closed letter",
                        1
                    ],
                    [
                        "handkerchief burying hagrid",
                        1
                    ],
                    [
                        "handkerchief lily james",
                        1
                    ],
                    [
                        "handkerchief sad grip",
                        1
                    ],
                    [
                        "handkerchief stand handkerchief",
                        1
                    ],
                    [
                        "harry arms turned",
                        1
                    ],
                    [
                        "harry bent harry",
                        1
                    ],
                    [
                        "harry blankets came",
                        1
                    ],
                    [
                        "harry dumbledore murmured",
                        1
                    ],
                    [
                        "harry gave scratchy",
                        1
                    ],
                    [
                        "harry gently doorstep",
                        1
                    ],
                    [
                        "harry great shaggy",
                        1
                    ],
                    [
                        "harry harry arms",
                        1
                    ],
                    [
                        "harry potter lived",
                        1
                    ],
                    [
                        "harry potter rolled",
                        1
                    ],
                    [
                        "harry sir asked",
                        1
                    ],
                    [
                        "harry ter muggles",
                        1
                    ],
                    [
                        "hedges privet drive",
                        1
                    ],
                    [
                        "heel swish dumbledore",
                        1
                    ],
                    [
                        "held sign another",
                        1
                    ],
                    [
                        "hissed professor mcgonagall",
                        1
                    ],
                    [
                        "holding people glasses",
                        1
                    ],
                    [
                        "hours dursley scream",
                        1
                    ],
                    [
                        "howl like wounded",
                        1
                    ],
                    [
                        "hugged kissed mother",
                        1
                    ],
                    [
                        "hushed voices harry",
                        1
                    ],
                    [
                        "inky sky place",
                        1
                    ],
                    [
                        "inside dumbledore blankets",
                        1
                    ],
                    [
                        "inside harry blankets",
                        1
                    ],
                    [
                        "jacket sleeve hagrid",
                        1
                    ],
                    [
                        "james dead poor",
                        1
                    ],
                    [
                        "jet black forehead",
                        1
                    ],
                    [
                        "join celebrations hagrid",
                        1
                    ],
                    [
                        "kicked engine roar",
                        1
                    ],
                    [
                        "knee perfect map",
                        1
                    ],
                    [
                        "knowing dumbledore famous",
                        1
                    ],
                    [
                        "knowing dumbledore special",
                        1
                    ],
                    [
                        "knowing dumbledore woken",
                        1
                    ],
                    [
                        "laid harry gently",
                        1
                    ],
                    [
                        "lamps privet drive",
                        1
                    ],
                    [
                        "large blond riding",
                        1
                    ],
                    [
                        "large pink beach",
                        1
                    ],
                    [
                        "large spotted handkerchief",
                        1
                    ],
                    [
                        "lay silent tidy",
                        1
                    ],
                    [
                        "left knee perfect",
                        1
                    ],
                    [
                        "letter beside dumbledore",
                        1
                    ],
                    [
                        "letter dumbledore cloak",
                        1
                    ],
                    [
                        "letter inside harry",
                        1
                    ],
                    [
                        "light sped balls",
                        1
                    ],
                    [
                        "light usually shone",
                        1
                    ],
                    [
                        "like bolt lightning",
                        1
                    ],
                    [
                        "like large pink",
                        1
                    ],
                    [
                        "like wounded dog",
                        1
                    ],
                    [
                        "lily james dead",
                        1
                    ],
                    [
                        "lit brass number",
                        1
                    ],
                    [
                        "little bundle hagrid",
                        1
                    ],
                    [
                        "little harry ter",
                        1
                    ],
                    [
                        "living room almost",
                        1
                    ],
                    [
                        "ll professor mcgonagall",
                        1
                    ],
                    [
                        "ll scar forever",
                        1
                    ],
                    [
                        "ll takin sirius",
                        1
                    ],
                    [
                        "ll wake muggles",
                        1
                    ],
                    [
                        "longer baby photographs",
                        1
                    ],
                    [
                        "looked like large",
                        1
                    ],
                    [
                        "looked little bundle",
                        1
                    ],
                    [
                        "lots pictures looked",
                        1
                    ],
                    [
                        "low garden wall",
                        1
                    ],
                    [
                        "luck harry dumbledore",
                        1
                    ],
                    [
                        "mantelpiece really showed",
                        1
                    ],
                    [
                        "map london underground",
                        1
                    ],
                    [
                        "mcgonagall blew mcgonagall",
                        1
                    ],
                    [
                        "mcgonagall blinked furiously",
                        1
                    ],
                    [
                        "mcgonagall curiously shaped",
                        1
                    ],
                    [
                        "mcgonagall dumbledore nodding",
                        1
                    ],
                    [
                        "mcgonagall ll wake",
                        1
                    ],
                    [
                        "mcgonagall nose reply",
                        1
                    ],
                    [
                        "mcgonagall professor dumbledore",
                        1
                    ],
                    [
                        "mcgonagall whispered patting",
                        1
                    ],
                    [
                        "meeting secret country",
                        1
                    ],
                    [
                        "milk bottles dumbledore",
                        1
                    ],
                    [
                        "minute three stood",
                        1
                    ],
                    [
                        "moment people meeting",
                        1
                    ],
                    [
                        "motorcycle kicked engine",
                        1
                    ],
                    [
                        "muffled voice ll",
                        1
                    ],
                    [
                        "muggles handkerchief sad",
                        1
                    ],
                    [
                        "muggles sorry sobbed",
                        1
                    ],
                    [
                        "nearly ten years",
                        1
                    ],
                    [
                        "neat hedges privet",
                        1
                    ],
                    [
                        "nephew front step",
                        1
                    ],
                    [
                        "news report owls",
                        1
                    ],
                    [
                        "next weeks prodded",
                        1
                    ],
                    [
                        "number crept dursley",
                        1
                    ],
                    [
                        "number four dursley",
                        1
                    ],
                    [
                        "onto motorcycle kicked",
                        1
                    ],
                    [
                        "opened front door",
                        1
                    ],
                    [
                        "orange dumbledore tabby",
                        1
                    ],
                    [
                        "outer twelve balls",
                        1
                    ],
                    [
                        "passed since dursley",
                        1
                    ],
                    [
                        "patting hagrid gingerly",
                        1
                    ],
                    [
                        "people glasses saying",
                        1
                    ],
                    [
                        "people meeting secret",
                        1
                    ],
                    [
                        "perfect map london",
                        1
                    ],
                    [
                        "photographs mantelpiece really",
                        1
                    ],
                    [
                        "photographs showed large",
                        1
                    ],
                    [
                        "pictures looked like",
                        1
                    ],
                    [
                        "pinched dumbledore cousin",
                        1
                    ],
                    [
                        "pink beach ball",
                        1
                    ],
                    [
                        "place expect astonishing",
                        1
                    ],
                    [
                        "playing computer father",
                        1
                    ],
                    [
                        "poor little harry",
                        1
                    ],
                    [
                        "potter rolled inside",
                        1
                    ],
                    [
                        "privet drive glowed",
                        1
                    ],
                    [
                        "privet drive hardly",
                        1
                    ],
                    [
                        "privet drive lay",
                        1
                    ],
                    [
                        "prodded pinched dumbledore",
                        1
                    ],
                    [
                        "professor dumbledore sir",
                        1
                    ],
                    [
                        "professor mcgonagall blew",
                        1
                    ],
                    [
                        "professor mcgonagall blinked",
                        1
                    ],
                    [
                        "professor mcgonagall dumbledore",
                        1
                    ],
                    [
                        "professor mcgonagall ll",
                        1
                    ],
                    [
                        "professor mcgonagall professor",
                        1
                    ],
                    [
                        "professor mcgonagall whispered",
                        1
                    ],
                    [
                        "really showed passed",
                        1
                    ],
                    [
                        "riding bicycle carousel",
                        1
                    ],
                    [
                        "roar engine rose",
                        1
                    ],
                    [
                        "rolled inside dumbledore",
                        1
                    ],
                    [
                        "room almost exactly",
                        1
                    ],
                    [
                        "room held sign",
                        1
                    ],
                    [
                        "rose tidy front",
                        1
                    ],
                    [
                        "ruffled neat hedges",
                        1
                    ],
                    [
                        "sad grip hagrid",
                        1
                    ],
                    [
                        "saying hushed voices",
                        1
                    ],
                    [
                        "scar dumbledore wouldn",
                        1
                    ],
                    [
                        "scar forever couldn",
                        1
                    ],
                    [
                        "scratchy whiskery kiss",
                        1
                    ],
                    [
                        "scream dursley opened",
                        1
                    ],
                    [
                        "secret country holding",
                        1
                    ],
                    [
                        "seen fateful news",
                        1
                    ],
                    [
                        "shaggy harry gave",
                        1
                    ],
                    [
                        "shall expect professor",
                        1
                    ],
                    [
                        "shaped cut like",
                        1
                    ],
                    [
                        "shhh hissed professor",
                        1
                    ],
                    [
                        "shone dumbledore eyes",
                        1
                    ],
                    [
                        "shook professor mcgonagall",
                        1
                    ],
                    [
                        "shoulders shook professor",
                        1
                    ],
                    [
                        "showed large blond",
                        1
                    ],
                    [
                        "sign another lived",
                        1
                    ],
                    [
                        "silent tidy inky",
                        1
                    ],
                    [
                        "since dursley dursley",
                        1
                    ],
                    [
                        "sir asked hagrid",
                        1
                    ],
                    [
                        "sir wiping sirius",
                        1
                    ],
                    [
                        "sirius bike professor",
                        1
                    ],
                    [
                        "sirius jacket sleeve",
                        1
                    ],
                    [
                        "sirius sirius bike",
                        1
                    ],
                    [
                        "sirius streaming eyes",
                        1
                    ],
                    [
                        "sky place expect",
                        1
                    ],
                    [
                        "sleeve hagrid swung",
                        1
                    ],
                    [
                        "slept knowing dumbledore",
                        1
                    ],
                    [
                        "slinking corner street",
                        1
                    ],
                    [
                        "small hand closed",
                        1
                    ],
                    [
                        "sobbed hagrid taking",
                        1
                    ],
                    [
                        "something scar dumbledore",
                        1
                    ],
                    [
                        "sorry sobbed hagrid",
                        1
                    ],
                    [
                        "special knowing dumbledore",
                        1
                    ],
                    [
                        "sped balls street",
                        1
                    ],
                    [
                        "spend next weeks",
                        1
                    ],
                    [
                        "spotted handkerchief burying",
                        1
                    ],
                    [
                        "stand handkerchief lily",
                        1
                    ],
                    [
                        "step number four",
                        1
                    ],
                    [
                        "step privet drive",
                        1
                    ],
                    [
                        "stepped low garden",
                        1
                    ],
                    [
                        "stood looked little",
                        1
                    ],
                    [
                        "stopped took silver",
                        1
                    ],
                    [
                        "streaming eyes sirius",
                        1
                    ],
                    [
                        "street lamps privet",
                        1
                    ],
                    [
                        "suddenly hagrid howl",
                        1
                    ],
                    [
                        "suddenly orange dumbledore",
                        1
                    ],
                    [
                        "sun rose tidy",
                        1
                    ],
                    [
                        "swish dumbledore cloak",
                        1
                    ],
                    [
                        "swung hagrid onto",
                        1
                    ],
                    [
                        "tabby cat slinking",
                        1
                    ],
                    [
                        "takin sirius sirius",
                        1
                    ],
                    [
                        "taking large spotted",
                        1
                    ],
                    [
                        "ten years ago",
                        1
                    ],
                    [
                        "ten years passed",
                        1
                    ],
                    [
                        "ter muggles handkerchief",
                        1
                    ],
                    [
                        "three stood looked",
                        1
                    ],
                    [
                        "tidy front gardens",
                        1
                    ],
                    [
                        "tidy inky sky",
                        1
                    ],
                    [
                        "took harry harry",
                        1
                    ],
                    [
                        "took letter dumbledore",
                        1
                    ],
                    [
                        "took silver outer",
                        1
                    ],
                    [
                        "toward dursley dursley",
                        1
                    ],
                    [
                        "tucked letter inside",
                        1
                    ],
                    [
                        "tuft jet black",
                        1
                    ],
                    [
                        "turned dumbledore heel",
                        1
                    ],
                    [
                        "turned toward dursley",
                        1
                    ],
                    [
                        "turned walked street",
                        1
                    ],
                    [
                        "twelve balls light",
                        1
                    ],
                    [
                        "twinkling light usually",
                        1
                    ],
                    [
                        "usually shone dumbledore",
                        1
                    ],
                    [
                        "vanishing glass nearly",
                        1
                    ],
                    [
                        "ve business staying",
                        1
                    ],
                    [
                        "voice ll takin",
                        1
                    ],
                    [
                        "voices harry potter",
                        1
                    ],
                    [
                        "wake muggles sorry",
                        1
                    ],
                    [
                        "walked front door",
                        1
                    ],
                    [
                        "wall walked front",
                        1
                    ],
                    [
                        "wearing different colored",
                        1
                    ],
                    [
                        "weeks prodded pinched",
                        1
                    ],
                    [
                        "well dumbledore finally",
                        1
                    ],
                    [
                        "well dumbledore hagrid",
                        1
                    ],
                    [
                        "well go join",
                        1
                    ],
                    [
                        "whispered patting hagrid",
                        1
                    ],
                    [
                        "whispered professor mcgonagall",
                        1
                    ],
                    [
                        "wiping sirius streaming",
                        1
                    ],
                    [
                        "woken dursley dursley",
                        1
                    ],
                    [
                        "woken hours dursley",
                        1
                    ],
                    [
                        "years ago lots",
                        1
                    ],
                    [
                        "years passed since",
                        1
                    ]
                ]
            ]
        ]
    }
}'''
TASK_2_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 2": {
        "4-Seq Counts": [
            [
                "1_seq",
                [
                    [
                        "angry",
                        1
                    ],
                    [
                        "armadillo",
                        1
                    ],
                    [
                        "away",
                        1
                    ],
                    [
                        "behind",
                        2
                    ],
                    [
                        "bell",
                        1
                    ],
                    [
                        "bile",
                        1
                    ],
                    [
                        "bottle",
                        1
                    ],
                    [
                        "cauldron",
                        2
                    ],
                    [
                        "class",
                        2
                    ],
                    [
                        "deliberately",
                        1
                    ],
                    [
                        "desk",
                        1
                    ],
                    [
                        "door",
                        1
                    ],
                    [
                        "double",
                        1
                    ],
                    [
                        "duck",
                        1
                    ],
                    [
                        "edge",
                        1
                    ],
                    [
                        "effort",
                        1
                    ],
                    [
                        "every",
                        1
                    ],
                    [
                        "excuse",
                        1
                    ],
                    [
                        "extremely",
                        1
                    ],
                    [
                        "forearm",
                        1
                    ],
                    [
                        "gave",
                        1
                    ],
                    [
                        "go",
                        1
                    ],
                    [
                        "hand",
                        1
                    ],
                    [
                        "harry",
                        10
                    ],
                    [
                        "heard",
                        1
                    ],
                    [
                        "hiss",
                        1
                    ],
                    [
                        "hovered",
                        1
                    ],
                    [
                        "inner",
                        1
                    ],
                    [
                        "intent",
                        1
                    ],
                    [
                        "karkaroff",
                        8
                    ],
                    [
                        "keen",
                        1
                    ],
                    [
                        "knocked",
                        1
                    ],
                    [
                        "left",
                        1
                    ],
                    [
                        "lips",
                        1
                    ],
                    [
                        "looked",
                        2
                    ],
                    [
                        "making",
                        1
                    ],
                    [
                        "minutes",
                        1
                    ],
                    [
                        "mop",
                        1
                    ],
                    [
                        "moved",
                        1
                    ],
                    [
                        "noisily",
                        1
                    ],
                    [
                        "peering",
                        1
                    ],
                    [
                        "period",
                        1
                    ],
                    [
                        "preventing",
                        1
                    ],
                    [
                        "pull",
                        1
                    ],
                    [
                        "rest",
                        2
                    ],
                    [
                        "robe",
                        1
                    ],
                    [
                        "seemed",
                        1
                    ],
                    [
                        "sleeve",
                        1
                    ],
                    [
                        "slipping",
                        1
                    ],
                    [
                        "snape",
                        5
                    ],
                    [
                        "something",
                        1
                    ],
                    [
                        "toward",
                        1
                    ],
                    [
                        "urgent",
                        1
                    ],
                    [
                        "wanted",
                        1
                    ],
                    [
                        "well",
                        1
                    ],
                    [
                        "worried",
                        1
                    ]
                ]
            ],
            [
                "2_seq",
                [
                    [
                        "armadillo bile",
                        1
                    ],
                    [
                        "away class",
                        1
                    ],
                    [
                        "behind harry",
                        1
                    ],
                    [
                        "behind snape",
                        1
                    ],
                    [
                        "bell gave",
                        1
                    ],
                    [
                        "bile minutes",
                        1
                    ],
                    [
                        "bottle armadillo",
                        1
                    ],
                    [
                        "cauldron karkaroff",
                        1
                    ],
                    [
                        "cauldron mop",
                        1
                    ],
                    [
                        "class moved",
                        1
                    ],
                    [
                        "deliberately knocked",
                        1
                    ],
                    [
                        "desk rest",
                        1
                    ],
                    [
                        "double period",
                        1
                    ],
                    [
                        "duck behind",
                        1
                    ],
                    [
                        "edge harry",
                        1
                    ],
                    [
                        "effort harry",
                        1
                    ],
                    [
                        "every effort",
                        1
                    ],
                    [
                        "excuse duck",
                        1
                    ],
                    [
                        "extremely worried",
                        1
                    ],
                    [
                        "gave harry",
                        1
                    ],
                    [
                        "go bell",
                        1
                    ],
                    [
                        "hand sleeve",
                        1
                    ],
                    [
                        "harry bottle",
                        1
                    ],
                    [
                        "harry cauldron",
                        2
                    ],
                    [
                        "harry deliberately",
                        1
                    ],
                    [
                        "harry excuse",
                        1
                    ],
                    [
                        "harry heard",
                        1
                    ],
                    [
                        "harry inner",
                        1
                    ],
                    [
                        "harry lips",
                        1
                    ],
                    [
                        "harry peering",
                        1
                    ],
                    [
                        "harry robe",
                        1
                    ],
                    [
                        "heard snape",
                        1
                    ],
                    [
                        "hiss karkaroff",
                        1
                    ],
                    [
                        "hovered behind",
                        1
                    ],
                    [
                        "inner forearm",
                        1
                    ],
                    [
                        "intent preventing",
                        1
                    ],
                    [
                        "karkaroff harry",
                        1
                    ],
                    [
                        "karkaroff hovered",
                        1
                    ],
                    [
                        "karkaroff looked",
                        1
                    ],
                    [
                        "karkaroff making",
                        1
                    ],
                    [
                        "karkaroff pull",
                        1
                    ],
                    [
                        "karkaroff seemed",
                        1
                    ],
                    [
                        "karkaroff wanted",
                        1
                    ],
                    [
                        "keen karkaroff",
                        1
                    ],
                    [
                        "knocked harry",
                        1
                    ],
                    [
                        "left hand",
                        1
                    ],
                    [
                        "looked angry",
                        1
                    ],
                    [
                        "looked extremely",
                        1
                    ],
                    [
                        "making every",
                        1
                    ],
                    [
                        "minutes go",
                        1
                    ],
                    [
                        "mop rest",
                        1
                    ],
                    [
                        "moved noisily",
                        1
                    ],
                    [
                        "noisily toward",
                        1
                    ],
                    [
                        "peering edge",
                        1
                    ],
                    [
                        "preventing snape",
                        1
                    ],
                    [
                        "pull left",
                        1
                    ],
                    [
                        "rest class",
                        1
                    ],
                    [
                        "rest double",
                        1
                    ],
                    [
                        "robe snape",
                        1
                    ],
                    [
                        "seemed intent",
                        1
                    ],
                    [
                        "sleeve harry",
                        1
                    ],
                    [
                        "slipping away",
                        1
                    ],
                    [
                        "snape desk",
                        1
                    ],
                    [
                        "snape hiss",
                        1
                    ],
                    [
                        "snape looked",
                        1
                    ],
                    [
                        "snape slipping",
                        1
                    ],
                    [
                        "snape something",
                        1
                    ],
                    [
                        "something harry",
                        1
                    ],
                    [
                        "toward door",
                        1
                    ],
                    [
                        "urgent harry",
                        1
                    ],
                    [
                        "wanted harry",
                        1
                    ],
                    [
                        "well karkaroff",
                        1
                    ],
                    [
                        "worried snape",
                        1
                    ]
                ]
            ],
            [
                "3_seq",
                [
                    [
                        "armadillo bile minutes",
                        1
                    ],
                    [
                        "behind harry cauldron",
                        1
                    ],
                    [
                        "behind snape desk",
                        1
                    ],
                    [
                        "bell gave harry",
                        1
                    ],
                    [
                        "bile minutes go",
                        1
                    ],
                    [
                        "bottle armadillo bile",
                        1
                    ],
                    [
                        "cauldron karkaroff pull",
                        1
                    ],
                    [
                        "cauldron mop rest",
                        1
                    ],
                    [
                        "class moved noisily",
                        1
                    ],
                    [
                        "deliberately knocked harry",
                        1
                    ],
                    [
                        "desk rest double",
                        1
                    ],
                    [
                        "duck behind harry",
                        1
                    ],
                    [
                        "edge harry cauldron",
                        1
                    ],
                    [
                        "effort harry lips",
                        1
                    ],
                    [
                        "every effort harry",
                        1
                    ],
                    [
                        "excuse duck behind",
                        1
                    ],
                    [
                        "extremely worried snape",
                        1
                    ],
                    [
                        "gave harry excuse",
                        1
                    ],
                    [
                        "go bell gave",
                        1
                    ],
                    [
                        "hand sleeve harry",
                        1
                    ],
                    [
                        "harry bottle armadillo",
                        1
                    ],
                    [
                        "harry cauldron karkaroff",
                        1
                    ],
                    [
                        "harry cauldron mop",
                        1
                    ],
                    [
                        "harry deliberately knocked",
                        1
                    ],
                    [
                        "harry excuse duck",
                        1
                    ],
                    [
                        "harry heard snape",
                        1
                    ],
                    [
                        "harry inner forearm",
                        1
                    ],
                    [
                        "harry peering edge",
                        1
                    ],
                    [
                        "harry robe snape",
                        1
                    ],
                    [
                        "heard snape hiss",
                        1
                    ],
                    [
                        "hovered behind snape",
                        1
                    ],
                    [
                        "intent preventing snape",
                        1
                    ],
                    [
                        "karkaroff harry peering",
                        1
                    ],
                    [
                        "karkaroff hovered behind",
                        1
                    ],
                    [
                        "karkaroff looked extremely",
                        1
                    ],
                    [
                        "karkaroff making every",
                        1
                    ],
                    [
                        "karkaroff pull left",
                        1
                    ],
                    [
                        "karkaroff seemed intent",
                        1
                    ],
                    [
                        "karkaroff wanted harry",
                        1
                    ],
                    [
                        "keen karkaroff wanted",
                        1
                    ],
                    [
                        "knocked harry bottle",
                        1
                    ],
                    [
                        "left hand sleeve",
                        1
                    ],
                    [
                        "looked extremely worried",
                        1
                    ],
                    [
                        "making every effort",
                        1
                    ],
                    [
                        "minutes go bell",
                        1
                    ],
                    [
                        "mop rest class",
                        1
                    ],
                    [
                        "moved noisily toward",
                        1
                    ],
                    [
                        "noisily toward door",
                        1
                    ],
                    [
                        "peering edge harry",
                        1
                    ],
                    [
                        "preventing snape slipping",
                        1
                    ],
                    [
                        "pull left hand",
                        1
                    ],
                    [
                        "rest class moved",
                        1
                    ],
                    [
                        "rest double period",
                        1
                    ],
                    [
                        "robe snape something",
                        1
                    ],
                    [
                        "seemed intent preventing",
                        1
                    ],
                    [
                        "sleeve harry robe",
                        1
                    ],
                    [
                        "slipping away class",
                        1
                    ],
                    [
                        "snape desk rest",
                        1
                    ],
                    [
                        "snape hiss karkaroff",
                        1
                    ],
                    [
                        "snape looked angry",
                        1
                    ],
                    [
                        "snape slipping away",
                        1
                    ],
                    [
                        "snape something harry",
                        1
                    ],
                    [
                        "something harry inner",
                        1
                    ],
                    [
                        "urgent harry heard",
                        1
                    ],
                    [
                        "wanted harry deliberately",
                        1
                    ],
                    [
                        "well karkaroff making",
                        1
                    ],
                    [
                        "worried snape looked",
                        1
                    ]
                ]
            ],
            [
                "4_seq",
                [
                    [
                        "armadillo bile minutes go",
                        1
                    ],
                    [
                        "behind harry cauldron mop",
                        1
                    ],
                    [
                        "behind snape desk rest",
                        1
                    ],
                    [
                        "bell gave harry excuse",
                        1
                    ],
                    [
                        "bile minutes go bell",
                        1
                    ],
                    [
                        "bottle armadillo bile minutes",
                        1
                    ],
                    [
                        "cauldron karkaroff pull left",
                        1
                    ],
                    [
                        "cauldron mop rest class",
                        1
                    ],
                    [
                        "class moved noisily toward",
                        1
                    ],
                    [
                        "deliberately knocked harry bottle",
                        1
                    ],
                    [
                        "desk rest double period",
                        1
                    ],
                    [
                        "duck behind harry cauldron",
                        1
                    ],
                    [
                        "edge harry cauldron karkaroff",
                        1
                    ],
                    [
                        "every effort harry lips",
                        1
                    ],
                    [
                        "excuse duck behind harry",
                        1
                    ],
                    [
                        "extremely worried snape looked",
                        1
                    ],
                    [
                        "gave harry excuse duck",
                        1
                    ],
                    [
                        "go bell gave harry",
                        1
                    ],
                    [
                        "hand sleeve harry robe",
                        1
                    ],
                    [
                        "harry bottle armadillo bile",
                        1
                    ],
                    [
                        "harry cauldron karkaroff pull",
                        1
                    ],
                    [
                        "harry cauldron mop rest",
                        1
                    ],
                    [
                        "harry deliberately knocked harry",
                        1
                    ],
                    [
                        "harry excuse duck behind",
                        1
                    ],
                    [
                        "harry heard snape hiss",
                        1
                    ],
                    [
                        "harry peering edge harry",
                        1
                    ],
                    [
                        "harry robe snape something",
                        1
                    ],
                    [
                        "heard snape hiss karkaroff",
                        1
                    ],
                    [
                        "hovered behind snape desk",
                        1
                    ],
                    [
                        "intent preventing snape slipping",
                        1
                    ],
                    [
                        "karkaroff harry peering edge",
                        1
                    ],
                    [
                        "karkaroff hovered behind snape",
                        1
                    ],
                    [
                        "karkaroff looked extremely worried",
                        1
                    ],
                    [
                        "karkaroff making every effort",
                        1
                    ],
                    [
                        "karkaroff pull left hand",
                        1
                    ],
                    [
                        "karkaroff seemed intent preventing",
                        1
                    ],
                    [
                        "karkaroff wanted harry deliberately",
                        1
                    ],
                    [
                        "keen karkaroff wanted harry",
                        1
                    ],
                    [
                        "knocked harry bottle armadillo",
                        1
                    ],
                    [
                        "left hand sleeve harry",
                        1
                    ],
                    [
                        "looked extremely worried snape",
                        1
                    ],
                    [
                        "making every effort harry",
                        1
                    ],
                    [
                        "minutes go bell gave",
                        1
                    ],
                    [
                        "mop rest class moved",
                        1
                    ],
                    [
                        "moved noisily toward door",
                        1
                    ],
                    [
                        "peering edge harry cauldron",
                        1
                    ],
                    [
                        "preventing snape slipping away",
                        1
                    ],
                    [
                        "pull left hand sleeve",
                        1
                    ],
                    [
                        "rest class moved noisily",
                        1
                    ],
                    [
                        "robe snape something harry",
                        1
                    ],
                    [
                        "seemed intent preventing snape",
                        1
                    ],
                    [
                        "sleeve harry robe snape",
                        1
                    ],
                    [
                        "snape desk rest double",
                        1
                    ],
                    [
                        "snape slipping away class",
                        1
                    ],
                    [
                        "snape something harry inner",
                        1
                    ],
                    [
                        "something harry inner forearm",
                        1
                    ],
                    [
                        "urgent harry heard snape",
                        1
                    ],
                    [
                        "wanted harry deliberately knocked",
                        1
                    ],
                    [
                        "well karkaroff making every",
                        1
                    ],
                    [
                        "worried snape looked angry",
                        1
                    ]
                ]
            ]
        ]
    }
}'''
TASK_2_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 2": {
        "5-Seq Counts": [
            [
                "1_seq",
                [
                    [
                        "alarmingly",
                        1
                    ],
                    [
                        "another",
                        1
                    ],
                    [
                        "curtly",
                        1
                    ],
                    [
                        "detention",
                        1
                    ],
                    [
                        "door",
                        1
                    ],
                    [
                        "face",
                        2
                    ],
                    [
                        "flashing",
                        1
                    ],
                    [
                        "footsteps",
                        1
                    ],
                    [
                        "gargoyle",
                        1
                    ],
                    [
                        "given",
                        1
                    ],
                    [
                        "harry",
                        5
                    ],
                    [
                        "hasn",
                        1
                    ],
                    [
                        "heard",
                        1
                    ],
                    [
                        "high",
                        1
                    ],
                    [
                        "knocked",
                        1
                    ],
                    [
                        "mcgonagall",
                        3
                    ],
                    [
                        "ooooh",
                        1
                    ],
                    [
                        "opened",
                        1
                    ],
                    [
                        "pitched",
                        1
                    ],
                    [
                        "place",
                        1
                    ],
                    [
                        "professor",
                        1
                    ],
                    [
                        "spectacles",
                        1
                    ],
                    [
                        "square",
                        1
                    ],
                    [
                        "urgent",
                        2
                    ],
                    [
                        "us",
                        1
                    ],
                    [
                        "voice",
                        1
                    ],
                    [
                        "well",
                        1
                    ]
                ]
            ],
            [
                "2_seq",
                [
                    [
                        "another detention",
                        1
                    ],
                    [
                        "door opened",
                        1
                    ],
                    [
                        "face face",
                        1
                    ],
                    [
                        "face professor",
                        1
                    ],
                    [
                        "flashing alarmingly",
                        1
                    ],
                    [
                        "footsteps door",
                        1
                    ],
                    [
                        "gargoyle high",
                        1
                    ],
                    [
                        "given another",
                        1
                    ],
                    [
                        "harry curtly",
                        1
                    ],
                    [
                        "harry face",
                        1
                    ],
                    [
                        "harry harry",
                        1
                    ],
                    [
                        "harry heard",
                        1
                    ],
                    [
                        "harry knocked",
                        1
                    ],
                    [
                        "heard footsteps",
                        1
                    ],
                    [
                        "high pitched",
                        1
                    ],
                    [
                        "mcgonagall mcgonagall",
                        1
                    ],
                    [
                        "mcgonagall square",
                        1
                    ],
                    [
                        "ooooh urgent",
                        1
                    ],
                    [
                        "opened harry",
                        1
                    ],
                    [
                        "pitched voice",
                        1
                    ],
                    [
                        "place hasn",
                        1
                    ],
                    [
                        "professor mcgonagall",
                        1
                    ],
                    [
                        "spectacles flashing",
                        1
                    ],
                    [
                        "square spectacles",
                        1
                    ],
                    [
                        "urgent harry",
                        1
                    ],
                    [
                        "us place",
                        1
                    ],
                    [
                        "well us",
                        1
                    ]
                ]
            ],
            [
                "3_seq",
                [
                    [
                        "door opened harry",
                        1
                    ],
                    [
                        "face face professor",
                        1
                    ],
                    [
                        "face professor mcgonagall",
                        1
                    ],
                    [
                        "footsteps door opened",
                        1
                    ],
                    [
                        "gargoyle high pitched",
                        1
                    ],
                    [
                        "given another detention",
                        1
                    ],
                    [
                        "harry face face",
                        1
                    ],
                    [
                        "harry harry face",
                        1
                    ],
                    [
                        "harry heard footsteps",
                        1
                    ],
                    [
                        "heard footsteps door",
                        1
                    ],
                    [
                        "high pitched voice",
                        1
                    ],
                    [
                        "mcgonagall mcgonagall square",
                        1
                    ],
                    [
                        "mcgonagall square spectacles",
                        1
                    ],
                    [
                        "opened harry harry",
                        1
                    ],
                    [
                        "spectacles flashing alarmingly",
                        1
                    ],
                    [
                        "square spectacles flashing",
                        1
                    ],
                    [
                        "urgent harry curtly",
                        1
                    ],
                    [
                        "us place hasn",
                        1
                    ],
                    [
                        "well us place",
                        1
                    ]
                ]
            ],
            [
                "4_seq",
                [
                    [
                        "door opened harry harry",
                        1
                    ],
                    [
                        "face face professor mcgonagall",
                        1
                    ],
                    [
                        "footsteps door opened harry",
                        1
                    ],
                    [
                        "gargoyle high pitched voice",
                        1
                    ],
                    [
                        "harry face face professor",
                        1
                    ],
                    [
                        "harry harry face face",
                        1
                    ],
                    [
                        "harry heard footsteps door",
                        1
                    ],
                    [
                        "heard footsteps door opened",
                        1
                    ],
                    [
                        "mcgonagall mcgonagall square spectacles",
                        1
                    ],
                    [
                        "mcgonagall square spectacles flashing",
                        1
                    ],
                    [
                        "opened harry harry face",
                        1
                    ],
                    [
                        "square spectacles flashing alarmingly",
                        1
                    ],
                    [
                        "well us place hasn",
                        1
                    ]
                ]
            ],
            [
                "5_seq",
                [
                    [
                        "door opened harry harry face",
                        1
                    ],
                    [
                        "footsteps door opened harry harry",
                        1
                    ],
                    [
                        "harry face face professor mcgonagall",
                        1
                    ],
                    [
                        "harry harry face face professor",
                        1
                    ],
                    [
                        "harry heard footsteps door opened",
                        1
                    ],
                    [
                        "heard footsteps door opened harry",
                        1
                    ],
                    [
                        "mcgonagall mcgonagall square spectacles flashing",
                        1
                    ],
                    [
                        "mcgonagall square spectacles flashing alarmingly",
                        1
                    ],
                    [
                        "opened harry harry face face",
                        1
                    ]
                ]
            ]
        ]
    }
}'''


# CONSTANT FOR TASK 3 UNPROCESSED FLOW TEST

TASK_3_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""
TASK_3_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
    "Karkaroff looked extremely worried, and  Snape looked angry."
    Karkaroff hovered behind  Snape's desk for the rest of the double period.
    Karkaroff seemed intent on preventing  Snape from slipping away at the end of class.
    "Keen to hear what Karkaroff wanted to say,  Harry deliberately knocked over  Harry bottle of armadillo bile with two minutes to go to the bell, which gave  Harry an excuse to duck down behind  Harry cauldron and mop up while the rest of the class moved noisily toward the door."
    ` What's so urgent?`  Harry heard  Snape hiss at Karkaroff.
    "` This,` said Karkaroff, and  Harry, peering around the edge of  Harry cauldron, saw Karkaroff  pull up the left- hand sleeve of  Harry robe and show  Snape something on  Harry inner forearm."
    "` Well?` said Karkaroff, still making every effort not to move  Harry lips.` Do you see?"
    the boy
    """
TASK_3_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
    "This is urgent,' said  Harry curtly.   '"
    "Ooooh, urgent, is This?'"
    said the other gargoyle in a high- pitched voice.'
    "Well, that's put us in our place, hasn't that?'"
    Harry knocked.
    "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
    You haven't been given another detention!'
    "McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
    """
TASK_3_EXAMPLE_4_SENTENCES_CSV_RAW = """sentence
    "This is urgent,' said  Harry curtly.   '"
    "Ooooh, urgent, is This?'"
    said the other gargoyle in a high- pitched voice.'
    "Well, that's put us in our place, hasn't that?'"
    Harry knocked.
    "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
    You haven't been given another detention!'
    "McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
    """

TASK_3_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,batty
Kquewanda Bailey,
Ballyfumble Stranger,"quin, quivering quintus, quintusofthesillyname"
"""
TASK_3_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
    Ignatia Wildsmith,
    Ignatius Prewett,
    Ignatius Tuft,
    Ignotus Peverell,
    Igor Karkaroff,
    Illyius,
    Ingolfr the Iambic,
    """
TASK_3_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
    "Magnus ""Dent Head"" Macdonald",
    Magorian,
    Maisie Cattermole,
    Malcolm,
    Malcolm Baddock,
    Malcolm McGonagall,
    Harold Skively,
    Harper,
    Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
    Harvey Ridgebit,
    Hassan Mostafa,
    """
TASK_3_EXAMPLE_4_NAMES_CSV_RAW = """Name,Other Names
    Abernathy,
    Abraham Peasegood,
    Abraham Potter,
    Abraxas Malfoy,
    Achilles Tolliver,
    Stewart Ackerley,
    Mrs. Granger,
    Hermione Granger,
    Hugo Granger-Weasley,
    Rose Granger-Weasley,
    Granville Jorkins,
    """

TASK_3_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 3": {
            "Name Mentions": [
                [
                    "aunt marge dursley",
                    19
                ],
                [
                    "aurelius dumbledore",
                    32
                ]
            ]
        }
    }'''
TASK_3_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 3": {
            "Name Mentions": [
                [
                    "igor karkaroff",
                    8
                ]
            ]
        }
    }'''
TASK_3_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 3": {
            "Name Mentions": [
                [
                    "harry potter",
                    5
                ],
                [
                    "malcolm mcgonagall",
                    3
                ]
            ]
        }
    }'''
TASK_3_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 3": {
            "Name Mentions": []
        }
    }'''


# CONSTANT FOR TASK 4 UNPROCESSED FLOW TEST

TASK_4_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
    "Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
    ` Is that where-?` whispered Professor  McGonagall.
    "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
    Scars can come in handy.
    I have one myself above my left knee that is a perfect map of the London Underground.
    "Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
    "` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
    "Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
    "Then, suddenly,  Hagrid let out a howl like a wounded dog."
    "` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
    "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
    "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
    "` Well,` said  Dumbledore finally,` that's that."
    We've no business staying here.
    "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
    "` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
    Professor  McGonagall blew  McGonagall nose in reply.
    Dumbledore turned and walked back down the street.
    On the corner  Dumbledore stopped and took out the silver Put- Outer.
    "Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
    Dumbledore could just see the bundle of blankets on the step of number four.
    "` Good luck,  Harry,`  Dumbledore murmured."
    "Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
    "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
    Harry  Potter rolled over inside  Dumbledore blankets without waking up.
    "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
    "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
    "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
    Only the photographs on the mantelpiece really showed how much time had passed.
    "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
    "The room held no sign at all that another boy lived in the house, too."
    """
TASK_4_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
    "Karkaroff looked extremely worried, and  Snape looked angry."
    Karkaroff hovered behind  Snape's desk for the rest of the double period.
    Karkaroff seemed intent on preventing  Snape from slipping away at the end of class.
    "Keen to hear what Karkaroff wanted to say,  Harry deliberately knocked over  Harry bottle of armadillo bile with two minutes to go to the bell, which gave  Harry an excuse to duck down behind  Harry cauldron and mop up while the rest of the class moved noisily toward the door."
    ` What's so urgent?`  Harry heard  Snape hiss at Karkaroff.
    "` This,` said Karkaroff, and  Harry, peering around the edge of  Harry cauldron, saw Karkaroff  pull up the left- hand sleeve of  Harry robe and show  Snape something on  Harry inner forearm."
    "` Well?` said Karkaroff, still making every effort not to move  Harry lips.` Do you see?"
    the boy
    """
TASK_4_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
    "This is urgent,' said  Harry curtly.   '"
    "Ooooh, urgent, is This?'"
    said the other gargoyle in a high- pitched voice.'
    "Well, that's put us in our place, hasn't that?'"
    Harry knocked.
    "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
    You haven't been given another detention!'
    "McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
    """
TASK_4_EXAMPLE_4_SENTENCES_CSV_RAW = """sentence
    "Fine, let's swap,' said  Hermione, seizing  Ron's raven and replacing raven with  Hermione own fat bullfrog.'"
    Silencio!'
    "The raven continued to open and close raven sharp beak, but no sound came out.   '"
    "Very good, Miss   Granger!'"
    "said Professor Flitwick's squeaky little voice, making  Harry,  Ron and  Hermione all jump.'"
    "Now, let me see you try,  Mr  Weasley'   'Wha-?"
    "Oh- oh, right,' said  Ron, very flustered.'"
    Er- silencio!'
    Hermione jabbed at the bullfrog so hard  Hermione poked bullfrog in the eye: the frog gave a deafening croak and leapt off the desk.
    croak came as no surprise to any of frog that  Harry and  Ron were given additional practice of the Silencing Charm for homework.
    frog were allowed to remain inside over break due to the downpour outside.
    "frog found seats in a noisy and overcrowded classroom on the first floor in which  Peeves was floating dreamily up near the chandelier, occasionally blowing an ink pellet at the top of somebody's head."
    somebody had barely sat down when  Angelina came struggling towards somebody through the groups of gossiping students.   '
    I've got permission!'
    Angelina said.
    To re- form the Quidditch team!'
    ' Excellent!'
    said  Ron and  Harry together.   '
    "Yeah,' said  Angelina, beaming.'"
    I went to  McGonagall and I think  McGonagall might have appealed to  Dumbledore.
    "Anyway,  Umbridge had to give in."
    Ha!
    "So I want you down at the pitch at seveno'clock tonight, all right, because we've got to make up time."
    You realise we're only three weeks away from our first match?'
    "McGonagall squeezed away from match, narrowly dodged an ink pellet from  Peeves, which hit a nearby first- year instead, and vanished from sight."
    "Ron's smile slipped slightly as  Ron looked out of the window, which was now opaque with hammering rain.   '"
    """

TASK_4_EXAMPLE_1_KSEQ_JSON_RAW = """{
    "keys":[
		["breeze", "ruffled"],
        ["small", "hand", "closed"],
        ["dumbledore", "finally"],
        ["dumbledore"],
        ["well", "go", "join", "celebrations"],
        ["hagrid", "muffled", "voice"]
    ]
}"""
TASK_4_EXAMPLE_2_KSEQ_JSON_RAW = """{
        "keys":[
            ["snape", "looked"],
            ["harry", "heard"],
            ["karkaroff"],
            ["well", "go", "join", "celebrations"],
            ["lips"]
        ]
    }"""
TASK_4_EXAMPLE_3_KSEQ_JSON_RAW = """{
    "keys":[
		["another"],
		["harry", "heard"],
		["another"],
		["well", "go", "join", "celebrations"],
		["knocked"]
    ]
}"""
TASK_4_EXAMPLE_4_KSEQ_JSON_RAW = """{
        "keys":[
            ["another"],
            ["harry", "heard"],
            ["break"],
            ["together"],
            ["three", "weeks"]
        ]
    }"""

TASK_4_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 4": {
            "K-Seq Matches": [
                [
                    "breeze ruffled",
                    [
                        [
                            "breeze",
                            "ruffled",
                            "neat",
                            "hedges",
                            "privet",
                            "drive",
                            "lay",
                            "silent",
                            "tidy",
                            "inky",
                            "sky",
                            "place",
                            "expect",
                            "astonishing",
                            "things"
                        ]
                    ]
                ],
                [
                    "dumbledore",
                    [
                        [
                            "corner",
                            "dumbledore",
                            "stopped",
                            "took",
                            "silver",
                            "outer"
                        ],
                        [
                            "dumbledore",
                            "bundle",
                            "blankets",
                            "step",
                            "number",
                            "four"
                        ],
                        [
                            "dumbledore",
                            "clicked",
                            "outer",
                            "twelve",
                            "balls",
                            "light",
                            "sped",
                            "balls",
                            "street",
                            "lamps",
                            "privet",
                            "drive",
                            "glowed",
                            "suddenly",
                            "orange",
                            "dumbledore",
                            "tabby",
                            "cat",
                            "slinking",
                            "corner",
                            "street"
                        ],
                        [
                            "dumbledore",
                            "dumbledore",
                            "ll",
                            "scar",
                            "forever",
                            "couldn",
                            "something",
                            "scar",
                            "dumbledore",
                            "wouldn"
                        ],
                        [
                            "dumbledore",
                            "laid",
                            "harry",
                            "gently",
                            "doorstep",
                            "took",
                            "letter",
                            "dumbledore",
                            "cloak",
                            "tucked",
                            "letter",
                            "inside",
                            "harry",
                            "blankets",
                            "came"
                        ],
                        [
                            "dumbledore",
                            "turned",
                            "dumbledore",
                            "heel",
                            "swish",
                            "dumbledore",
                            "cloak",
                            "dumbledore"
                        ],
                        [
                            "dumbledore",
                            "turned",
                            "walked",
                            "street"
                        ],
                        [
                            "full",
                            "minute",
                            "three",
                            "stood",
                            "looked",
                            "little",
                            "bundle",
                            "hagrid",
                            "shoulders",
                            "shook",
                            "professor",
                            "mcgonagall",
                            "blinked",
                            "furiously",
                            "twinkling",
                            "light",
                            "usually",
                            "shone",
                            "dumbledore",
                            "eyes",
                            "seemed"
                        ],
                        [
                            "good",
                            "luck",
                            "harry",
                            "dumbledore",
                            "murmured"
                        ],
                        [
                            "harry",
                            "potter",
                            "rolled",
                            "inside",
                            "dumbledore",
                            "blankets",
                            "without",
                            "waking"
                        ],
                        [
                            "shall",
                            "expect",
                            "professor",
                            "mcgonagall",
                            "dumbledore",
                            "nodding",
                            "voice"
                        ],
                        [
                            "shhh",
                            "hissed",
                            "professor",
                            "mcgonagall",
                            "ll",
                            "wake",
                            "muggles",
                            "sorry",
                            "sobbed",
                            "hagrid",
                            "taking",
                            "large",
                            "spotted",
                            "handkerchief",
                            "burying",
                            "hagrid",
                            "face",
                            "handkerchief",
                            "stand",
                            "handkerchief",
                            "lily",
                            "james",
                            "dead",
                            "poor",
                            "little",
                            "harry",
                            "ter",
                            "muggles",
                            "handkerchief",
                            "sad",
                            "grip",
                            "hagrid",
                            "ll",
                            "professor",
                            "mcgonagall",
                            "whispered",
                            "patting",
                            "hagrid",
                            "gingerly",
                            "arm",
                            "dumbledore",
                            "stepped",
                            "low",
                            "garden",
                            "wall",
                            "walked",
                            "front",
                            "door"
                        ],
                        [
                            "small",
                            "hand",
                            "closed",
                            "letter",
                            "beside",
                            "dumbledore",
                            "dumbledore",
                            "slept",
                            "knowing",
                            "dumbledore",
                            "special",
                            "knowing",
                            "dumbledore",
                            "famous",
                            "knowing",
                            "dumbledore",
                            "woken",
                            "hours",
                            "dursley",
                            "scream",
                            "dursley",
                            "opened",
                            "front",
                            "door",
                            "milk",
                            "bottles",
                            "dumbledore",
                            "spend",
                            "next",
                            "weeks",
                            "prodded",
                            "pinched",
                            "dumbledore",
                            "cousin",
                            "dudley",
                            "dumbledore",
                            "couldn",
                            "moment",
                            "people",
                            "meeting",
                            "secret",
                            "country",
                            "holding",
                            "people",
                            "glasses",
                            "saying",
                            "hushed",
                            "voices",
                            "harry",
                            "potter",
                            "lived"
                        ],
                        [
                            "tuft",
                            "jet",
                            "black",
                            "forehead",
                            "dumbledore",
                            "mcgonagall",
                            "curiously",
                            "shaped",
                            "cut",
                            "like",
                            "bolt",
                            "lightning"
                        ],
                        [
                            "well",
                            "dumbledore",
                            "finally"
                        ],
                        [
                            "well",
                            "dumbledore",
                            "hagrid",
                            "better",
                            "dumbledore",
                            "took",
                            "harry",
                            "harry",
                            "arms",
                            "turned",
                            "toward",
                            "dursley",
                            "dursley",
                            "dudley",
                            "dursley",
                            "house"
                        ],
                        [
                            "well",
                            "go",
                            "join",
                            "celebrations",
                            "hagrid",
                            "muffled",
                            "voice",
                            "ll",
                            "takin",
                            "sirius",
                            "sirius",
                            "bike",
                            "professor",
                            "mcgonagall",
                            "professor",
                            "dumbledore",
                            "sir",
                            "wiping",
                            "sirius",
                            "streaming",
                            "eyes",
                            "sirius",
                            "jacket",
                            "sleeve",
                            "hagrid",
                            "swung",
                            "hagrid",
                            "onto",
                            "motorcycle",
                            "kicked",
                            "engine",
                            "roar",
                            "engine",
                            "rose",
                            "air"
                        ]
                    ]
                ],
                [
                    "dumbledore finally",
                    [
                        [
                            "well",
                            "dumbledore",
                            "finally"
                        ]
                    ]
                ],
                [
                    "hagrid muffled voice",
                    [
                        [
                            "well",
                            "go",
                            "join",
                            "celebrations",
                            "hagrid",
                            "muffled",
                            "voice",
                            "ll",
                            "takin",
                            "sirius",
                            "sirius",
                            "bike",
                            "professor",
                            "mcgonagall",
                            "professor",
                            "dumbledore",
                            "sir",
                            "wiping",
                            "sirius",
                            "streaming",
                            "eyes",
                            "sirius",
                            "jacket",
                            "sleeve",
                            "hagrid",
                            "swung",
                            "hagrid",
                            "onto",
                            "motorcycle",
                            "kicked",
                            "engine",
                            "roar",
                            "engine",
                            "rose",
                            "air"
                        ]
                    ]
                ],
                [
                    "small hand closed",
                    [
                        [
                            "small",
                            "hand",
                            "closed",
                            "letter",
                            "beside",
                            "dumbledore",
                            "dumbledore",
                            "slept",
                            "knowing",
                            "dumbledore",
                            "special",
                            "knowing",
                            "dumbledore",
                            "famous",
                            "knowing",
                            "dumbledore",
                            "woken",
                            "hours",
                            "dursley",
                            "scream",
                            "dursley",
                            "opened",
                            "front",
                            "door",
                            "milk",
                            "bottles",
                            "dumbledore",
                            "spend",
                            "next",
                            "weeks",
                            "prodded",
                            "pinched",
                            "dumbledore",
                            "cousin",
                            "dudley",
                            "dumbledore",
                            "couldn",
                            "moment",
                            "people",
                            "meeting",
                            "secret",
                            "country",
                            "holding",
                            "people",
                            "glasses",
                            "saying",
                            "hushed",
                            "voices",
                            "harry",
                            "potter",
                            "lived"
                        ]
                    ]
                ],
                [
                    "well go join celebrations",
                    [
                        [
                            "well",
                            "go",
                            "join",
                            "celebrations",
                            "hagrid",
                            "muffled",
                            "voice",
                            "ll",
                            "takin",
                            "sirius",
                            "sirius",
                            "bike",
                            "professor",
                            "mcgonagall",
                            "professor",
                            "dumbledore",
                            "sir",
                            "wiping",
                            "sirius",
                            "streaming",
                            "eyes",
                            "sirius",
                            "jacket",
                            "sleeve",
                            "hagrid",
                            "swung",
                            "hagrid",
                            "onto",
                            "motorcycle",
                            "kicked",
                            "engine",
                            "roar",
                            "engine",
                            "rose",
                            "air"
                        ]
                    ]
                ]
            ]
        }
    }'''
TASK_4_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 4": {
            "K-Seq Matches": [
                [
                    "harry heard",
                    [
                        [
                            "urgent",
                            "harry",
                            "heard",
                            "snape",
                            "hiss",
                            "karkaroff"
                        ]
                    ]
                ],
                [
                    "karkaroff",
                    [
                        [
                            "karkaroff",
                            "harry",
                            "peering",
                            "edge",
                            "harry",
                            "cauldron",
                            "karkaroff",
                            "pull",
                            "left",
                            "hand",
                            "sleeve",
                            "harry",
                            "robe",
                            "snape",
                            "something",
                            "harry",
                            "inner",
                            "forearm"
                        ],
                        [
                            "karkaroff",
                            "hovered",
                            "behind",
                            "snape",
                            "desk",
                            "rest",
                            "double",
                            "period"
                        ],
                        [
                            "karkaroff",
                            "looked",
                            "extremely",
                            "worried",
                            "snape",
                            "looked",
                            "angry"
                        ],
                        [
                            "karkaroff",
                            "seemed",
                            "intent",
                            "preventing",
                            "snape",
                            "slipping",
                            "away",
                            "class"
                        ],
                        [
                            "keen",
                            "karkaroff",
                            "wanted",
                            "harry",
                            "deliberately",
                            "knocked",
                            "harry",
                            "bottle",
                            "armadillo",
                            "bile",
                            "minutes",
                            "go",
                            "bell",
                            "gave",
                            "harry",
                            "excuse",
                            "duck",
                            "behind",
                            "harry",
                            "cauldron",
                            "mop",
                            "rest",
                            "class",
                            "moved",
                            "noisily",
                            "toward",
                            "door"
                        ],
                        [
                            "urgent",
                            "harry",
                            "heard",
                            "snape",
                            "hiss",
                            "karkaroff"
                        ],
                        [
                            "well",
                            "karkaroff",
                            "making",
                            "every",
                            "effort",
                            "harry",
                            "lips"
                        ]
                    ]
                ],
                [
                    "lips",
                    [
                        [
                            "well",
                            "karkaroff",
                            "making",
                            "every",
                            "effort",
                            "harry",
                            "lips"
                        ]
                    ]
                ],
                [
                    "snape looked",
                    [
                        [
                            "karkaroff",
                            "looked",
                            "extremely",
                            "worried",
                            "snape",
                            "looked",
                            "angry"
                        ]
                    ]
                ]
            ]
        }
    }'''
TASK_4_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 4": {
        "K-Seq Matches": [
            [
                "another",
                [
                    [
                        "given",
                        "another",
                        "detention"
                    ]
                ]
            ],
            [
                "harry heard",
                [
                    [
                        "harry",
                        "heard",
                        "footsteps",
                        "door",
                        "opened",
                        "harry",
                        "harry",
                        "face",
                        "face",
                        "professor",
                        "mcgonagall"
                    ]
                ]
            ],
            [
                "knocked",
                [
                    [
                        "harry",
                        "knocked"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_4_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW = '''{
        "Question 4": {
            "K-Seq Matches": [
                [
                    "break",
                    [
                        [
                            "frog",
                            "allowed",
                            "remain",
                            "inside",
                            "break",
                            "due",
                            "downpour",
                            "outside"
                        ]
                    ]
                ],
                [
                    "three weeks",
                    [
                        [
                            "realise",
                            "re",
                            "three",
                            "weeks",
                            "away",
                            "match"
                        ]
                    ]
                ],
                [
                    "together",
                    [
                        [
                            "ron",
                            "harry",
                            "together"
                        ]
                    ]
                ]
            ]
        }
    }'''


# CONSTANT FOR TASK 5 UNPROCESSED FLOW TEST

TASK_5_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
    "Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
    ` Is that where-?` whispered Professor  McGonagall.
    "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
    Scars can come in handy.
    I have one myself above my left knee that is a perfect map of the London Underground.
    "Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
    "` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
    "Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
    "Then, suddenly,  Hagrid let out a howl like a wounded dog."
    "` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
    "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
    "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
    "` Well,` said  Dumbledore finally,` that's that."
    We've no business staying here.
    "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
    "` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
    Professor  McGonagall blew  McGonagall nose in reply.
    Dumbledore turned and walked back down the street.
    On the corner  Dumbledore stopped and took out the silver Put- Outer.
    "Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
    Dumbledore could just see the bundle of blankets on the step of number four.
    "` Good luck,  Harry,`  Dumbledore murmured."
    "Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
    "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
    Harry  Potter rolled over inside  Dumbledore blankets without waking up.
    "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
    "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
    "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
    Only the photographs on the mantelpiece really showed how much time had passed.
    "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
    "The room held no sign at all that another boy lived in the house, too."
    """
TASK_5_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
"Karkaroff looked extremely worried, and  Snape looked angry."
Karkaroff hovered behind  Snape's desk for the rest of the double period.
Karkaroff seemed intent on preventing  Snape from slipping away at the end of class.
"Keen to hear what Karkaroff wanted to say,  Harry deliberately knocked over  Harry bottle of armadillo bile with two minutes to go to the bell, which gave  Harry an excuse to duck down behind  Harry cauldron and mop up while the rest of the class moved noisily toward the door."
` What's so urgent?`  Harry heard  Snape hiss at Karkaroff.
"` This,` said Karkaroff, and  Harry, peering around the edge of  Harry cauldron, saw Karkaroff  pull up the left- hand sleeve of  Harry robe and show  Snape something on  Harry inner forearm."
"` Well?` said Karkaroff, still making every effort not to move  Harry lips.` Do you see?"
the boy
"""
TASK_5_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
"This is urgent,' said  Harry curtly.   '"
"Ooooh, urgent, is This?'"
said the other gargoyle in a high- pitched voice.'
"Well, that's put us in our place, hasn't that?'"
Harry knocked.
"Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
You haven't been given another detention!'
"McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
"""
TASK_5_EXAMPLE_4_SENTENCES_CSV_RAW = """sentence
"This is urgent,' said  Harry curtly.   '"
"Ooooh, urgent, is This?'"
said the other gargoyle in a high- pitched voice.'
"Well, that's put us in our place, hasn't that?'"
Harry knocked.
"Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
You haven't been given another detention!'
"McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
"""

TASK_5_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
    Over-Attentive Wizard,
    Bertram Aubrey,
    Audrey Weasley,
    "Augusta ""Gran"" Longbottom",Gran
    Augustus Pye,
    Augustus Rookwood,
    Augustus Worme,
    Auntie Muriel,
    Aunt Marge Dursley,
    Aurelius Dumbledore,
    Aurora Sinistra,
    Avery,
    Babajide Akingbade,
    Babayaga,
    Babbitty Rabbitty,
    Bagman Sr.,
    Ludo Bagman,
    Otto Bagman,
    Millicent Bagnold,
    Bathilda Bagshot,Batty
    Kquewanda Bailey,
    Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
    Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
    Albus Dumbledore,
    """
TASK_5_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
Ignatia Wildsmith,
Ignatius Prewett,
Ignatius Tuft,
Ignotus Peverell,
Igor Karkaroff,
Illyius,
Ingolfr the Iambic,
"""
TASK_5_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
"Magnus ""Dent Head"" Macdonald",
Magorian,
Maisie Cattermole,
Malcolm,
Malcolm Baddock,
Malcolm McGonagall,
Harold Skively,
Harper,
Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
Harvey Ridgebit,
Hassan Mostafa,
"""
TASK_5_EXAMPLE_4_NAMES_CSV_RAW = """Name,Other Names
Abernathy,
Abraham Peasegood,
Abraham Potter,
Abraxas Malfoy,
Achilles Tolliver,
Stewart Ackerley,
"""

TASK_5_EXAMPLE_1_MAXK = 3
TASK_5_EXAMPLE_2_MAXK = 4
TASK_5_EXAMPLE_3_MAXK = 5
TASK_5_EXAMPLE_4_MAXK = 6

TASK_5_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 5": {
        "Person Contexts and K-Seqs": [
            [
                "albus dumbledore",
                [
                    [
                        "air"
                    ],
                    [
                        "arm"
                    ],
                    [
                        "arm",
                        "dumbledore"
                    ],
                    [
                        "arm",
                        "dumbledore",
                        "stepped"
                    ],
                    [
                        "arms"
                    ],
                    [
                        "arms",
                        "turned"
                    ],
                    [
                        "arms",
                        "turned",
                        "toward"
                    ],
                    [
                        "balls"
                    ],
                    [
                        "balls",
                        "light"
                    ],
                    [
                        "balls",
                        "light",
                        "sped"
                    ],
                    [
                        "balls",
                        "street"
                    ],
                    [
                        "balls",
                        "street",
                        "lamps"
                    ],
                    [
                        "beside"
                    ],
                    [
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "beside",
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "better"
                    ],
                    [
                        "better",
                        "dumbledore"
                    ],
                    [
                        "better",
                        "dumbledore",
                        "took"
                    ],
                    [
                        "bike"
                    ],
                    [
                        "bike",
                        "professor"
                    ],
                    [
                        "bike",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "black"
                    ],
                    [
                        "black",
                        "forehead"
                    ],
                    [
                        "black",
                        "forehead",
                        "dumbledore"
                    ],
                    [
                        "blankets"
                    ],
                    [
                        "blankets",
                        "came"
                    ],
                    [
                        "blankets",
                        "step"
                    ],
                    [
                        "blankets",
                        "step",
                        "number"
                    ],
                    [
                        "blankets",
                        "without"
                    ],
                    [
                        "blankets",
                        "without",
                        "waking"
                    ],
                    [
                        "blinked"
                    ],
                    [
                        "blinked",
                        "furiously"
                    ],
                    [
                        "blinked",
                        "furiously",
                        "twinkling"
                    ],
                    [
                        "bolt"
                    ],
                    [
                        "bolt",
                        "lightning"
                    ],
                    [
                        "bottles"
                    ],
                    [
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "bottles",
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "bundle"
                    ],
                    [
                        "bundle",
                        "blankets"
                    ],
                    [
                        "bundle",
                        "blankets",
                        "step"
                    ],
                    [
                        "bundle",
                        "hagrid"
                    ],
                    [
                        "bundle",
                        "hagrid",
                        "shoulders"
                    ],
                    [
                        "burying"
                    ],
                    [
                        "burying",
                        "hagrid"
                    ],
                    [
                        "burying",
                        "hagrid",
                        "face"
                    ],
                    [
                        "came"
                    ],
                    [
                        "cat"
                    ],
                    [
                        "cat",
                        "slinking"
                    ],
                    [
                        "cat",
                        "slinking",
                        "corner"
                    ],
                    [
                        "celebrations"
                    ],
                    [
                        "celebrations",
                        "hagrid"
                    ],
                    [
                        "celebrations",
                        "hagrid",
                        "muffled"
                    ],
                    [
                        "clicked"
                    ],
                    [
                        "clicked",
                        "outer"
                    ],
                    [
                        "clicked",
                        "outer",
                        "twelve"
                    ],
                    [
                        "cloak"
                    ],
                    [
                        "cloak",
                        "dumbledore"
                    ],
                    [
                        "cloak",
                        "tucked"
                    ],
                    [
                        "cloak",
                        "tucked",
                        "letter"
                    ],
                    [
                        "closed"
                    ],
                    [
                        "closed",
                        "letter"
                    ],
                    [
                        "closed",
                        "letter",
                        "beside"
                    ],
                    [
                        "corner"
                    ],
                    [
                        "corner",
                        "dumbledore"
                    ],
                    [
                        "corner",
                        "dumbledore",
                        "stopped"
                    ],
                    [
                        "corner",
                        "street"
                    ],
                    [
                        "couldn"
                    ],
                    [
                        "couldn",
                        "moment"
                    ],
                    [
                        "couldn",
                        "moment",
                        "people"
                    ],
                    [
                        "couldn",
                        "something"
                    ],
                    [
                        "couldn",
                        "something",
                        "scar"
                    ],
                    [
                        "country"
                    ],
                    [
                        "country",
                        "holding"
                    ],
                    [
                        "country",
                        "holding",
                        "people"
                    ],
                    [
                        "cousin"
                    ],
                    [
                        "cousin",
                        "dudley"
                    ],
                    [
                        "cousin",
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "curiously"
                    ],
                    [
                        "curiously",
                        "shaped"
                    ],
                    [
                        "curiously",
                        "shaped",
                        "cut"
                    ],
                    [
                        "cut"
                    ],
                    [
                        "cut",
                        "like"
                    ],
                    [
                        "cut",
                        "like",
                        "bolt"
                    ],
                    [
                        "dead"
                    ],
                    [
                        "dead",
                        "poor"
                    ],
                    [
                        "dead",
                        "poor",
                        "little"
                    ],
                    [
                        "door"
                    ],
                    [
                        "door",
                        "milk"
                    ],
                    [
                        "door",
                        "milk",
                        "bottles"
                    ],
                    [
                        "doorstep"
                    ],
                    [
                        "doorstep",
                        "took"
                    ],
                    [
                        "doorstep",
                        "took",
                        "letter"
                    ],
                    [
                        "drive"
                    ],
                    [
                        "drive",
                        "glowed"
                    ],
                    [
                        "drive",
                        "glowed",
                        "suddenly"
                    ],
                    [
                        "dudley"
                    ],
                    [
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "dudley",
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "house"
                    ],
                    [
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "blankets"
                    ],
                    [
                        "dumbledore",
                        "blankets",
                        "without"
                    ],
                    [
                        "dumbledore",
                        "bundle"
                    ],
                    [
                        "dumbledore",
                        "bundle",
                        "blankets"
                    ],
                    [
                        "dumbledore",
                        "clicked"
                    ],
                    [
                        "dumbledore",
                        "clicked",
                        "outer"
                    ],
                    [
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "dumbledore",
                        "cloak",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "cloak",
                        "tucked"
                    ],
                    [
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dumbledore",
                        "couldn",
                        "moment"
                    ],
                    [
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "dumbledore",
                        "cousin",
                        "dudley"
                    ],
                    [
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "ll"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "eyes"
                    ],
                    [
                        "dumbledore",
                        "eyes",
                        "seemed"
                    ],
                    [
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "dumbledore",
                        "famous",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "finally"
                    ],
                    [
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "dumbledore",
                        "hagrid",
                        "better"
                    ],
                    [
                        "dumbledore",
                        "heel"
                    ],
                    [
                        "dumbledore",
                        "heel",
                        "swish"
                    ],
                    [
                        "dumbledore",
                        "laid"
                    ],
                    [
                        "dumbledore",
                        "laid",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "ll"
                    ],
                    [
                        "dumbledore",
                        "ll",
                        "scar"
                    ],
                    [
                        "dumbledore",
                        "mcgonagall"
                    ],
                    [
                        "dumbledore",
                        "mcgonagall",
                        "curiously"
                    ],
                    [
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "dumbledore",
                        "nodding"
                    ],
                    [
                        "dumbledore",
                        "nodding",
                        "voice"
                    ],
                    [
                        "dumbledore",
                        "sir"
                    ],
                    [
                        "dumbledore",
                        "sir",
                        "wiping"
                    ],
                    [
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "slept",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "special"
                    ],
                    [
                        "dumbledore",
                        "special",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "dumbledore",
                        "spend",
                        "next"
                    ],
                    [
                        "dumbledore",
                        "stepped"
                    ],
                    [
                        "dumbledore",
                        "stepped",
                        "low"
                    ],
                    [
                        "dumbledore",
                        "stopped"
                    ],
                    [
                        "dumbledore",
                        "stopped",
                        "took"
                    ],
                    [
                        "dumbledore",
                        "tabby"
                    ],
                    [
                        "dumbledore",
                        "tabby",
                        "cat"
                    ],
                    [
                        "dumbledore",
                        "took"
                    ],
                    [
                        "dumbledore",
                        "took",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "turned"
                    ],
                    [
                        "dumbledore",
                        "turned",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "turned",
                        "walked"
                    ],
                    [
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "dumbledore",
                        "woken",
                        "hours"
                    ],
                    [
                        "dumbledore",
                        "wouldn"
                    ],
                    [
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "house"
                    ],
                    [
                        "dursley",
                        "opened"
                    ],
                    [
                        "dursley",
                        "opened",
                        "front"
                    ],
                    [
                        "dursley",
                        "scream"
                    ],
                    [
                        "dursley",
                        "scream",
                        "dursley"
                    ],
                    [
                        "engine"
                    ],
                    [
                        "engine",
                        "roar"
                    ],
                    [
                        "engine",
                        "roar",
                        "engine"
                    ],
                    [
                        "engine",
                        "rose"
                    ],
                    [
                        "engine",
                        "rose",
                        "air"
                    ],
                    [
                        "expect"
                    ],
                    [
                        "expect",
                        "professor"
                    ],
                    [
                        "expect",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "eyes"
                    ],
                    [
                        "eyes",
                        "seemed"
                    ],
                    [
                        "eyes",
                        "sirius"
                    ],
                    [
                        "eyes",
                        "sirius",
                        "jacket"
                    ],
                    [
                        "face"
                    ],
                    [
                        "face",
                        "handkerchief"
                    ],
                    [
                        "face",
                        "handkerchief",
                        "stand"
                    ],
                    [
                        "famous"
                    ],
                    [
                        "famous",
                        "knowing"
                    ],
                    [
                        "famous",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "finally"
                    ],
                    [
                        "forehead"
                    ],
                    [
                        "forehead",
                        "dumbledore"
                    ],
                    [
                        "forehead",
                        "dumbledore",
                        "mcgonagall"
                    ],
                    [
                        "forever"
                    ],
                    [
                        "forever",
                        "couldn"
                    ],
                    [
                        "forever",
                        "couldn",
                        "something"
                    ],
                    [
                        "four"
                    ],
                    [
                        "front"
                    ],
                    [
                        "front",
                        "door"
                    ],
                    [
                        "front",
                        "door",
                        "milk"
                    ],
                    [
                        "full"
                    ],
                    [
                        "full",
                        "minute"
                    ],
                    [
                        "full",
                        "minute",
                        "three"
                    ],
                    [
                        "furiously"
                    ],
                    [
                        "furiously",
                        "twinkling"
                    ],
                    [
                        "furiously",
                        "twinkling",
                        "light"
                    ],
                    [
                        "garden"
                    ],
                    [
                        "garden",
                        "wall"
                    ],
                    [
                        "garden",
                        "wall",
                        "walked"
                    ],
                    [
                        "gently"
                    ],
                    [
                        "gently",
                        "doorstep"
                    ],
                    [
                        "gently",
                        "doorstep",
                        "took"
                    ],
                    [
                        "gingerly"
                    ],
                    [
                        "gingerly",
                        "arm"
                    ],
                    [
                        "gingerly",
                        "arm",
                        "dumbledore"
                    ],
                    [
                        "glasses"
                    ],
                    [
                        "glasses",
                        "saying"
                    ],
                    [
                        "glasses",
                        "saying",
                        "hushed"
                    ],
                    [
                        "glowed"
                    ],
                    [
                        "glowed",
                        "suddenly"
                    ],
                    [
                        "glowed",
                        "suddenly",
                        "orange"
                    ],
                    [
                        "go"
                    ],
                    [
                        "go",
                        "join"
                    ],
                    [
                        "go",
                        "join",
                        "celebrations"
                    ],
                    [
                        "good"
                    ],
                    [
                        "good",
                        "luck"
                    ],
                    [
                        "good",
                        "luck",
                        "harry"
                    ],
                    [
                        "grip"
                    ],
                    [
                        "grip",
                        "hagrid"
                    ],
                    [
                        "grip",
                        "hagrid",
                        "ll"
                    ],
                    [
                        "hagrid"
                    ],
                    [
                        "hagrid",
                        "better"
                    ],
                    [
                        "hagrid",
                        "better",
                        "dumbledore"
                    ],
                    [
                        "hagrid",
                        "face"
                    ],
                    [
                        "hagrid",
                        "face",
                        "handkerchief"
                    ],
                    [
                        "hagrid",
                        "gingerly"
                    ],
                    [
                        "hagrid",
                        "gingerly",
                        "arm"
                    ],
                    [
                        "hagrid",
                        "ll"
                    ],
                    [
                        "hagrid",
                        "ll",
                        "professor"
                    ],
                    [
                        "hagrid",
                        "muffled"
                    ],
                    [
                        "hagrid",
                        "muffled",
                        "voice"
                    ],
                    [
                        "hagrid",
                        "onto"
                    ],
                    [
                        "hagrid",
                        "onto",
                        "motorcycle"
                    ],
                    [
                        "hagrid",
                        "shoulders"
                    ],
                    [
                        "hagrid",
                        "shoulders",
                        "shook"
                    ],
                    [
                        "hagrid",
                        "swung"
                    ],
                    [
                        "hagrid",
                        "swung",
                        "hagrid"
                    ],
                    [
                        "hagrid",
                        "taking"
                    ],
                    [
                        "hagrid",
                        "taking",
                        "large"
                    ],
                    [
                        "hand"
                    ],
                    [
                        "hand",
                        "closed"
                    ],
                    [
                        "hand",
                        "closed",
                        "letter"
                    ],
                    [
                        "handkerchief"
                    ],
                    [
                        "handkerchief",
                        "burying"
                    ],
                    [
                        "handkerchief",
                        "burying",
                        "hagrid"
                    ],
                    [
                        "handkerchief",
                        "lily"
                    ],
                    [
                        "handkerchief",
                        "lily",
                        "james"
                    ],
                    [
                        "handkerchief",
                        "sad"
                    ],
                    [
                        "handkerchief",
                        "sad",
                        "grip"
                    ],
                    [
                        "handkerchief",
                        "stand"
                    ],
                    [
                        "handkerchief",
                        "stand",
                        "handkerchief"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "arms",
                        "turned"
                    ],
                    [
                        "harry",
                        "blankets"
                    ],
                    [
                        "harry",
                        "blankets",
                        "came"
                    ],
                    [
                        "harry",
                        "dumbledore"
                    ],
                    [
                        "harry",
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "harry",
                        "gently"
                    ],
                    [
                        "harry",
                        "gently",
                        "doorstep"
                    ],
                    [
                        "harry",
                        "harry"
                    ],
                    [
                        "harry",
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "harry",
                        "potter",
                        "lived"
                    ],
                    [
                        "harry",
                        "potter",
                        "rolled"
                    ],
                    [
                        "harry",
                        "ter"
                    ],
                    [
                        "harry",
                        "ter",
                        "muggles"
                    ],
                    [
                        "heel"
                    ],
                    [
                        "heel",
                        "swish"
                    ],
                    [
                        "heel",
                        "swish",
                        "dumbledore"
                    ],
                    [
                        "hissed"
                    ],
                    [
                        "hissed",
                        "professor"
                    ],
                    [
                        "hissed",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "holding"
                    ],
                    [
                        "holding",
                        "people"
                    ],
                    [
                        "holding",
                        "people",
                        "glasses"
                    ],
                    [
                        "hours"
                    ],
                    [
                        "hours",
                        "dursley"
                    ],
                    [
                        "hours",
                        "dursley",
                        "scream"
                    ],
                    [
                        "house"
                    ],
                    [
                        "hushed"
                    ],
                    [
                        "hushed",
                        "voices"
                    ],
                    [
                        "hushed",
                        "voices",
                        "harry"
                    ],
                    [
                        "inside"
                    ],
                    [
                        "inside",
                        "dumbledore"
                    ],
                    [
                        "inside",
                        "dumbledore",
                        "blankets"
                    ],
                    [
                        "inside",
                        "harry"
                    ],
                    [
                        "inside",
                        "harry",
                        "blankets"
                    ],
                    [
                        "jacket"
                    ],
                    [
                        "jacket",
                        "sleeve"
                    ],
                    [
                        "jacket",
                        "sleeve",
                        "hagrid"
                    ],
                    [
                        "james"
                    ],
                    [
                        "james",
                        "dead"
                    ],
                    [
                        "james",
                        "dead",
                        "poor"
                    ],
                    [
                        "jet"
                    ],
                    [
                        "jet",
                        "black"
                    ],
                    [
                        "jet",
                        "black",
                        "forehead"
                    ],
                    [
                        "join"
                    ],
                    [
                        "join",
                        "celebrations"
                    ],
                    [
                        "join",
                        "celebrations",
                        "hagrid"
                    ],
                    [
                        "kicked"
                    ],
                    [
                        "kicked",
                        "engine"
                    ],
                    [
                        "kicked",
                        "engine",
                        "roar"
                    ],
                    [
                        "knowing"
                    ],
                    [
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "special"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "laid"
                    ],
                    [
                        "laid",
                        "harry"
                    ],
                    [
                        "laid",
                        "harry",
                        "gently"
                    ],
                    [
                        "lamps"
                    ],
                    [
                        "lamps",
                        "privet"
                    ],
                    [
                        "lamps",
                        "privet",
                        "drive"
                    ],
                    [
                        "large"
                    ],
                    [
                        "large",
                        "spotted"
                    ],
                    [
                        "large",
                        "spotted",
                        "handkerchief"
                    ],
                    [
                        "letter"
                    ],
                    [
                        "letter",
                        "beside"
                    ],
                    [
                        "letter",
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "letter",
                        "dumbledore"
                    ],
                    [
                        "letter",
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "letter",
                        "inside"
                    ],
                    [
                        "letter",
                        "inside",
                        "harry"
                    ],
                    [
                        "light"
                    ],
                    [
                        "light",
                        "sped"
                    ],
                    [
                        "light",
                        "sped",
                        "balls"
                    ],
                    [
                        "light",
                        "usually"
                    ],
                    [
                        "light",
                        "usually",
                        "shone"
                    ],
                    [
                        "lightning"
                    ],
                    [
                        "like"
                    ],
                    [
                        "like",
                        "bolt"
                    ],
                    [
                        "like",
                        "bolt",
                        "lightning"
                    ],
                    [
                        "lily"
                    ],
                    [
                        "lily",
                        "james"
                    ],
                    [
                        "lily",
                        "james",
                        "dead"
                    ],
                    [
                        "little"
                    ],
                    [
                        "little",
                        "bundle"
                    ],
                    [
                        "little",
                        "bundle",
                        "hagrid"
                    ],
                    [
                        "little",
                        "harry"
                    ],
                    [
                        "little",
                        "harry",
                        "ter"
                    ],
                    [
                        "lived"
                    ],
                    [
                        "ll"
                    ],
                    [
                        "ll",
                        "professor"
                    ],
                    [
                        "ll",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "ll",
                        "scar"
                    ],
                    [
                        "ll",
                        "scar",
                        "forever"
                    ],
                    [
                        "ll",
                        "takin"
                    ],
                    [
                        "ll",
                        "takin",
                        "sirius"
                    ],
                    [
                        "ll",
                        "wake"
                    ],
                    [
                        "ll",
                        "wake",
                        "muggles"
                    ],
                    [
                        "looked"
                    ],
                    [
                        "looked",
                        "little"
                    ],
                    [
                        "looked",
                        "little",
                        "bundle"
                    ],
                    [
                        "low"
                    ],
                    [
                        "low",
                        "garden"
                    ],
                    [
                        "low",
                        "garden",
                        "wall"
                    ],
                    [
                        "luck"
                    ],
                    [
                        "luck",
                        "harry"
                    ],
                    [
                        "luck",
                        "harry",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall"
                    ],
                    [
                        "mcgonagall",
                        "blinked"
                    ],
                    [
                        "mcgonagall",
                        "blinked",
                        "furiously"
                    ],
                    [
                        "mcgonagall",
                        "curiously"
                    ],
                    [
                        "mcgonagall",
                        "curiously",
                        "shaped"
                    ],
                    [
                        "mcgonagall",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall",
                        "dumbledore",
                        "nodding"
                    ],
                    [
                        "mcgonagall",
                        "ll"
                    ],
                    [
                        "mcgonagall",
                        "ll",
                        "wake"
                    ],
                    [
                        "mcgonagall",
                        "professor"
                    ],
                    [
                        "mcgonagall",
                        "professor",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall",
                        "whispered"
                    ],
                    [
                        "mcgonagall",
                        "whispered",
                        "patting"
                    ],
                    [
                        "meeting"
                    ],
                    [
                        "meeting",
                        "secret"
                    ],
                    [
                        "meeting",
                        "secret",
                        "country"
                    ],
                    [
                        "milk"
                    ],
                    [
                        "milk",
                        "bottles"
                    ],
                    [
                        "milk",
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "minute"
                    ],
                    [
                        "minute",
                        "three"
                    ],
                    [
                        "minute",
                        "three",
                        "stood"
                    ],
                    [
                        "moment"
                    ],
                    [
                        "moment",
                        "people"
                    ],
                    [
                        "moment",
                        "people",
                        "meeting"
                    ],
                    [
                        "motorcycle"
                    ],
                    [
                        "motorcycle",
                        "kicked"
                    ],
                    [
                        "motorcycle",
                        "kicked",
                        "engine"
                    ],
                    [
                        "muffled"
                    ],
                    [
                        "muffled",
                        "voice"
                    ],
                    [
                        "muffled",
                        "voice",
                        "ll"
                    ],
                    [
                        "muggles"
                    ],
                    [
                        "muggles",
                        "handkerchief"
                    ],
                    [
                        "muggles",
                        "handkerchief",
                        "sad"
                    ],
                    [
                        "muggles",
                        "sorry"
                    ],
                    [
                        "muggles",
                        "sorry",
                        "sobbed"
                    ],
                    [
                        "murmured"
                    ],
                    [
                        "next"
                    ],
                    [
                        "next",
                        "weeks"
                    ],
                    [
                        "next",
                        "weeks",
                        "prodded"
                    ],
                    [
                        "nodding"
                    ],
                    [
                        "nodding",
                        "voice"
                    ],
                    [
                        "number"
                    ],
                    [
                        "number",
                        "four"
                    ],
                    [
                        "onto"
                    ],
                    [
                        "onto",
                        "motorcycle"
                    ],
                    [
                        "onto",
                        "motorcycle",
                        "kicked"
                    ],
                    [
                        "opened"
                    ],
                    [
                        "opened",
                        "front"
                    ],
                    [
                        "opened",
                        "front",
                        "door"
                    ],
                    [
                        "orange"
                    ],
                    [
                        "orange",
                        "dumbledore"
                    ],
                    [
                        "orange",
                        "dumbledore",
                        "tabby"
                    ],
                    [
                        "outer"
                    ],
                    [
                        "outer",
                        "twelve"
                    ],
                    [
                        "outer",
                        "twelve",
                        "balls"
                    ],
                    [
                        "patting"
                    ],
                    [
                        "patting",
                        "hagrid"
                    ],
                    [
                        "patting",
                        "hagrid",
                        "gingerly"
                    ],
                    [
                        "people"
                    ],
                    [
                        "people",
                        "glasses"
                    ],
                    [
                        "people",
                        "glasses",
                        "saying"
                    ],
                    [
                        "people",
                        "meeting"
                    ],
                    [
                        "people",
                        "meeting",
                        "secret"
                    ],
                    [
                        "pinched"
                    ],
                    [
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "pinched",
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "poor"
                    ],
                    [
                        "poor",
                        "little"
                    ],
                    [
                        "poor",
                        "little",
                        "harry"
                    ],
                    [
                        "potter"
                    ],
                    [
                        "potter",
                        "lived"
                    ],
                    [
                        "potter",
                        "rolled"
                    ],
                    [
                        "potter",
                        "rolled",
                        "inside"
                    ],
                    [
                        "privet"
                    ],
                    [
                        "privet",
                        "drive"
                    ],
                    [
                        "privet",
                        "drive",
                        "glowed"
                    ],
                    [
                        "prodded"
                    ],
                    [
                        "prodded",
                        "pinched"
                    ],
                    [
                        "prodded",
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "professor"
                    ],
                    [
                        "professor",
                        "dumbledore"
                    ],
                    [
                        "professor",
                        "dumbledore",
                        "sir"
                    ],
                    [
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "blinked"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "dumbledore"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "ll"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "professor"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "whispered"
                    ],
                    [
                        "roar"
                    ],
                    [
                        "roar",
                        "engine"
                    ],
                    [
                        "roar",
                        "engine",
                        "rose"
                    ],
                    [
                        "rolled"
                    ],
                    [
                        "rolled",
                        "inside"
                    ],
                    [
                        "rolled",
                        "inside",
                        "dumbledore"
                    ],
                    [
                        "rose"
                    ],
                    [
                        "rose",
                        "air"
                    ],
                    [
                        "sad"
                    ],
                    [
                        "sad",
                        "grip"
                    ],
                    [
                        "sad",
                        "grip",
                        "hagrid"
                    ],
                    [
                        "saying"
                    ],
                    [
                        "saying",
                        "hushed"
                    ],
                    [
                        "saying",
                        "hushed",
                        "voices"
                    ],
                    [
                        "scar"
                    ],
                    [
                        "scar",
                        "dumbledore"
                    ],
                    [
                        "scar",
                        "dumbledore",
                        "wouldn"
                    ],
                    [
                        "scar",
                        "forever"
                    ],
                    [
                        "scar",
                        "forever",
                        "couldn"
                    ],
                    [
                        "scream"
                    ],
                    [
                        "scream",
                        "dursley"
                    ],
                    [
                        "scream",
                        "dursley",
                        "opened"
                    ],
                    [
                        "secret"
                    ],
                    [
                        "secret",
                        "country"
                    ],
                    [
                        "secret",
                        "country",
                        "holding"
                    ],
                    [
                        "seemed"
                    ],
                    [
                        "shall"
                    ],
                    [
                        "shall",
                        "expect"
                    ],
                    [
                        "shall",
                        "expect",
                        "professor"
                    ],
                    [
                        "shaped"
                    ],
                    [
                        "shaped",
                        "cut"
                    ],
                    [
                        "shaped",
                        "cut",
                        "like"
                    ],
                    [
                        "shhh"
                    ],
                    [
                        "shhh",
                        "hissed"
                    ],
                    [
                        "shhh",
                        "hissed",
                        "professor"
                    ],
                    [
                        "shone"
                    ],
                    [
                        "shone",
                        "dumbledore"
                    ],
                    [
                        "shone",
                        "dumbledore",
                        "eyes"
                    ],
                    [
                        "shook"
                    ],
                    [
                        "shook",
                        "professor"
                    ],
                    [
                        "shook",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "shoulders"
                    ],
                    [
                        "shoulders",
                        "shook"
                    ],
                    [
                        "shoulders",
                        "shook",
                        "professor"
                    ],
                    [
                        "silver"
                    ],
                    [
                        "silver",
                        "outer"
                    ],
                    [
                        "sir"
                    ],
                    [
                        "sir",
                        "wiping"
                    ],
                    [
                        "sir",
                        "wiping",
                        "sirius"
                    ],
                    [
                        "sirius"
                    ],
                    [
                        "sirius",
                        "bike"
                    ],
                    [
                        "sirius",
                        "bike",
                        "professor"
                    ],
                    [
                        "sirius",
                        "jacket"
                    ],
                    [
                        "sirius",
                        "jacket",
                        "sleeve"
                    ],
                    [
                        "sirius",
                        "sirius"
                    ],
                    [
                        "sirius",
                        "sirius",
                        "bike"
                    ],
                    [
                        "sirius",
                        "streaming"
                    ],
                    [
                        "sirius",
                        "streaming",
                        "eyes"
                    ],
                    [
                        "sleeve"
                    ],
                    [
                        "sleeve",
                        "hagrid"
                    ],
                    [
                        "sleeve",
                        "hagrid",
                        "swung"
                    ],
                    [
                        "slept"
                    ],
                    [
                        "slept",
                        "knowing"
                    ],
                    [
                        "slept",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "slinking"
                    ],
                    [
                        "slinking",
                        "corner"
                    ],
                    [
                        "slinking",
                        "corner",
                        "street"
                    ],
                    [
                        "small"
                    ],
                    [
                        "small",
                        "hand"
                    ],
                    [
                        "small",
                        "hand",
                        "closed"
                    ],
                    [
                        "sobbed"
                    ],
                    [
                        "sobbed",
                        "hagrid"
                    ],
                    [
                        "sobbed",
                        "hagrid",
                        "taking"
                    ],
                    [
                        "something"
                    ],
                    [
                        "something",
                        "scar"
                    ],
                    [
                        "something",
                        "scar",
                        "dumbledore"
                    ],
                    [
                        "sorry"
                    ],
                    [
                        "sorry",
                        "sobbed"
                    ],
                    [
                        "sorry",
                        "sobbed",
                        "hagrid"
                    ],
                    [
                        "special"
                    ],
                    [
                        "special",
                        "knowing"
                    ],
                    [
                        "special",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "sped"
                    ],
                    [
                        "sped",
                        "balls"
                    ],
                    [
                        "sped",
                        "balls",
                        "street"
                    ],
                    [
                        "spend"
                    ],
                    [
                        "spend",
                        "next"
                    ],
                    [
                        "spend",
                        "next",
                        "weeks"
                    ],
                    [
                        "spotted"
                    ],
                    [
                        "spotted",
                        "handkerchief"
                    ],
                    [
                        "spotted",
                        "handkerchief",
                        "burying"
                    ],
                    [
                        "stand"
                    ],
                    [
                        "stand",
                        "handkerchief"
                    ],
                    [
                        "stand",
                        "handkerchief",
                        "lily"
                    ],
                    [
                        "step"
                    ],
                    [
                        "step",
                        "number"
                    ],
                    [
                        "step",
                        "number",
                        "four"
                    ],
                    [
                        "stepped"
                    ],
                    [
                        "stepped",
                        "low"
                    ],
                    [
                        "stepped",
                        "low",
                        "garden"
                    ],
                    [
                        "stood"
                    ],
                    [
                        "stood",
                        "looked"
                    ],
                    [
                        "stood",
                        "looked",
                        "little"
                    ],
                    [
                        "stopped"
                    ],
                    [
                        "stopped",
                        "took"
                    ],
                    [
                        "stopped",
                        "took",
                        "silver"
                    ],
                    [
                        "streaming"
                    ],
                    [
                        "streaming",
                        "eyes"
                    ],
                    [
                        "streaming",
                        "eyes",
                        "sirius"
                    ],
                    [
                        "street"
                    ],
                    [
                        "street",
                        "lamps"
                    ],
                    [
                        "street",
                        "lamps",
                        "privet"
                    ],
                    [
                        "suddenly"
                    ],
                    [
                        "suddenly",
                        "orange"
                    ],
                    [
                        "suddenly",
                        "orange",
                        "dumbledore"
                    ],
                    [
                        "swish"
                    ],
                    [
                        "swish",
                        "dumbledore"
                    ],
                    [
                        "swish",
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "swung"
                    ],
                    [
                        "swung",
                        "hagrid"
                    ],
                    [
                        "swung",
                        "hagrid",
                        "onto"
                    ],
                    [
                        "tabby"
                    ],
                    [
                        "tabby",
                        "cat"
                    ],
                    [
                        "tabby",
                        "cat",
                        "slinking"
                    ],
                    [
                        "takin"
                    ],
                    [
                        "takin",
                        "sirius"
                    ],
                    [
                        "takin",
                        "sirius",
                        "sirius"
                    ],
                    [
                        "taking"
                    ],
                    [
                        "taking",
                        "large"
                    ],
                    [
                        "taking",
                        "large",
                        "spotted"
                    ],
                    [
                        "ter"
                    ],
                    [
                        "ter",
                        "muggles"
                    ],
                    [
                        "ter",
                        "muggles",
                        "handkerchief"
                    ],
                    [
                        "three"
                    ],
                    [
                        "three",
                        "stood"
                    ],
                    [
                        "three",
                        "stood",
                        "looked"
                    ],
                    [
                        "took"
                    ],
                    [
                        "took",
                        "harry"
                    ],
                    [
                        "took",
                        "harry",
                        "harry"
                    ],
                    [
                        "took",
                        "letter"
                    ],
                    [
                        "took",
                        "letter",
                        "dumbledore"
                    ],
                    [
                        "took",
                        "silver"
                    ],
                    [
                        "took",
                        "silver",
                        "outer"
                    ],
                    [
                        "toward"
                    ],
                    [
                        "toward",
                        "dursley"
                    ],
                    [
                        "toward",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "tucked"
                    ],
                    [
                        "tucked",
                        "letter"
                    ],
                    [
                        "tucked",
                        "letter",
                        "inside"
                    ],
                    [
                        "tuft"
                    ],
                    [
                        "tuft",
                        "jet"
                    ],
                    [
                        "tuft",
                        "jet",
                        "black"
                    ],
                    [
                        "turned"
                    ],
                    [
                        "turned",
                        "dumbledore"
                    ],
                    [
                        "turned",
                        "dumbledore",
                        "heel"
                    ],
                    [
                        "turned",
                        "toward"
                    ],
                    [
                        "turned",
                        "toward",
                        "dursley"
                    ],
                    [
                        "turned",
                        "walked"
                    ],
                    [
                        "turned",
                        "walked",
                        "street"
                    ],
                    [
                        "twelve"
                    ],
                    [
                        "twelve",
                        "balls"
                    ],
                    [
                        "twelve",
                        "balls",
                        "light"
                    ],
                    [
                        "twinkling"
                    ],
                    [
                        "twinkling",
                        "light"
                    ],
                    [
                        "twinkling",
                        "light",
                        "usually"
                    ],
                    [
                        "usually"
                    ],
                    [
                        "usually",
                        "shone"
                    ],
                    [
                        "usually",
                        "shone",
                        "dumbledore"
                    ],
                    [
                        "voice"
                    ],
                    [
                        "voice",
                        "ll"
                    ],
                    [
                        "voice",
                        "ll",
                        "takin"
                    ],
                    [
                        "voices"
                    ],
                    [
                        "voices",
                        "harry"
                    ],
                    [
                        "voices",
                        "harry",
                        "potter"
                    ],
                    [
                        "wake"
                    ],
                    [
                        "wake",
                        "muggles"
                    ],
                    [
                        "wake",
                        "muggles",
                        "sorry"
                    ],
                    [
                        "waking"
                    ],
                    [
                        "walked"
                    ],
                    [
                        "walked",
                        "front"
                    ],
                    [
                        "walked",
                        "front",
                        "door"
                    ],
                    [
                        "walked",
                        "street"
                    ],
                    [
                        "wall"
                    ],
                    [
                        "wall",
                        "walked"
                    ],
                    [
                        "wall",
                        "walked",
                        "front"
                    ],
                    [
                        "weeks"
                    ],
                    [
                        "weeks",
                        "prodded"
                    ],
                    [
                        "weeks",
                        "prodded",
                        "pinched"
                    ],
                    [
                        "well"
                    ],
                    [
                        "well",
                        "dumbledore"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "finally"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "well",
                        "go"
                    ],
                    [
                        "well",
                        "go",
                        "join"
                    ],
                    [
                        "whispered"
                    ],
                    [
                        "whispered",
                        "patting"
                    ],
                    [
                        "whispered",
                        "patting",
                        "hagrid"
                    ],
                    [
                        "wiping"
                    ],
                    [
                        "wiping",
                        "sirius"
                    ],
                    [
                        "wiping",
                        "sirius",
                        "streaming"
                    ],
                    [
                        "without"
                    ],
                    [
                        "without",
                        "waking"
                    ],
                    [
                        "woken"
                    ],
                    [
                        "woken",
                        "hours"
                    ],
                    [
                        "woken",
                        "hours",
                        "dursley"
                    ],
                    [
                        "wouldn"
                    ]
                ]
            ],
            [
                "aunt marge dursley",
                [
                    [
                        "ago"
                    ],
                    [
                        "ago",
                        "lots"
                    ],
                    [
                        "ago",
                        "lots",
                        "pictures"
                    ],
                    [
                        "almost"
                    ],
                    [
                        "almost",
                        "exactly"
                    ],
                    [
                        "almost",
                        "exactly",
                        "dursley"
                    ],
                    [
                        "arms"
                    ],
                    [
                        "arms",
                        "turned"
                    ],
                    [
                        "arms",
                        "turned",
                        "toward"
                    ],
                    [
                        "baby"
                    ],
                    [
                        "baby",
                        "photographs"
                    ],
                    [
                        "baby",
                        "photographs",
                        "showed"
                    ],
                    [
                        "ball"
                    ],
                    [
                        "ball",
                        "wearing"
                    ],
                    [
                        "ball",
                        "wearing",
                        "different"
                    ],
                    [
                        "beach"
                    ],
                    [
                        "beach",
                        "ball"
                    ],
                    [
                        "beach",
                        "ball",
                        "wearing"
                    ],
                    [
                        "beside"
                    ],
                    [
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "beside",
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "better"
                    ],
                    [
                        "better",
                        "dumbledore"
                    ],
                    [
                        "better",
                        "dumbledore",
                        "took"
                    ],
                    [
                        "bicycle"
                    ],
                    [
                        "bicycle",
                        "carousel"
                    ],
                    [
                        "bicycle",
                        "carousel",
                        "fair"
                    ],
                    [
                        "blond"
                    ],
                    [
                        "blond",
                        "riding"
                    ],
                    [
                        "blond",
                        "riding",
                        "bicycle"
                    ],
                    [
                        "bonnets"
                    ],
                    [
                        "bonnets",
                        "dudley"
                    ],
                    [
                        "bonnets",
                        "dudley",
                        "dursley"
                    ],
                    [
                        "bottles"
                    ],
                    [
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "bottles",
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "brass"
                    ],
                    [
                        "brass",
                        "number"
                    ],
                    [
                        "brass",
                        "number",
                        "four"
                    ],
                    [
                        "carousel"
                    ],
                    [
                        "carousel",
                        "fair"
                    ],
                    [
                        "carousel",
                        "fair",
                        "playing"
                    ],
                    [
                        "changed"
                    ],
                    [
                        "closed"
                    ],
                    [
                        "closed",
                        "letter"
                    ],
                    [
                        "closed",
                        "letter",
                        "beside"
                    ],
                    [
                        "colored"
                    ],
                    [
                        "colored",
                        "bonnets"
                    ],
                    [
                        "colored",
                        "bonnets",
                        "dudley"
                    ],
                    [
                        "computer"
                    ],
                    [
                        "computer",
                        "father"
                    ],
                    [
                        "computer",
                        "father",
                        "hugged"
                    ],
                    [
                        "couldn"
                    ],
                    [
                        "couldn",
                        "moment"
                    ],
                    [
                        "couldn",
                        "moment",
                        "people"
                    ],
                    [
                        "country"
                    ],
                    [
                        "country",
                        "holding"
                    ],
                    [
                        "country",
                        "holding",
                        "people"
                    ],
                    [
                        "cousin"
                    ],
                    [
                        "cousin",
                        "dudley"
                    ],
                    [
                        "cousin",
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "crept"
                    ],
                    [
                        "crept",
                        "dursley"
                    ],
                    [
                        "crept",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "different"
                    ],
                    [
                        "different",
                        "colored"
                    ],
                    [
                        "different",
                        "colored",
                        "bonnets"
                    ],
                    [
                        "door"
                    ],
                    [
                        "door",
                        "milk"
                    ],
                    [
                        "door",
                        "milk",
                        "bottles"
                    ],
                    [
                        "door",
                        "number"
                    ],
                    [
                        "door",
                        "number",
                        "crept"
                    ],
                    [
                        "drive"
                    ],
                    [
                        "drive",
                        "hardly"
                    ],
                    [
                        "drive",
                        "hardly",
                        "changed"
                    ],
                    [
                        "dudley"
                    ],
                    [
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "dudley",
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "front"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "house"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "living"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "longer"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "nephew"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "woken"
                    ],
                    [
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dumbledore",
                        "couldn",
                        "moment"
                    ],
                    [
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "dumbledore",
                        "cousin",
                        "dudley"
                    ],
                    [
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "dumbledore",
                        "famous",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "dumbledore",
                        "hagrid",
                        "better"
                    ],
                    [
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "slept",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "special"
                    ],
                    [
                        "dumbledore",
                        "special",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "dumbledore",
                        "spend",
                        "next"
                    ],
                    [
                        "dumbledore",
                        "took"
                    ],
                    [
                        "dumbledore",
                        "took",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "dumbledore",
                        "woken",
                        "hours"
                    ],
                    [
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "front"
                    ],
                    [
                        "dursley",
                        "front",
                        "door"
                    ],
                    [
                        "dursley",
                        "house"
                    ],
                    [
                        "dursley",
                        "living"
                    ],
                    [
                        "dursley",
                        "living",
                        "room"
                    ],
                    [
                        "dursley",
                        "longer"
                    ],
                    [
                        "dursley",
                        "longer",
                        "baby"
                    ],
                    [
                        "dursley",
                        "nephew"
                    ],
                    [
                        "dursley",
                        "nephew",
                        "front"
                    ],
                    [
                        "dursley",
                        "opened"
                    ],
                    [
                        "dursley",
                        "opened",
                        "front"
                    ],
                    [
                        "dursley",
                        "scream"
                    ],
                    [
                        "dursley",
                        "scream",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "seen"
                    ],
                    [
                        "dursley",
                        "seen",
                        "fateful"
                    ],
                    [
                        "dursley",
                        "woken"
                    ],
                    [
                        "dursley",
                        "woken",
                        "dursley"
                    ],
                    [
                        "exactly"
                    ],
                    [
                        "exactly",
                        "dursley"
                    ],
                    [
                        "exactly",
                        "dursley",
                        "seen"
                    ],
                    [
                        "fair"
                    ],
                    [
                        "fair",
                        "playing"
                    ],
                    [
                        "fair",
                        "playing",
                        "computer"
                    ],
                    [
                        "famous"
                    ],
                    [
                        "famous",
                        "knowing"
                    ],
                    [
                        "famous",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "fateful"
                    ],
                    [
                        "fateful",
                        "news"
                    ],
                    [
                        "fateful",
                        "news",
                        "report"
                    ],
                    [
                        "father"
                    ],
                    [
                        "father",
                        "hugged"
                    ],
                    [
                        "father",
                        "hugged",
                        "kissed"
                    ],
                    [
                        "four"
                    ],
                    [
                        "four",
                        "dursley"
                    ],
                    [
                        "four",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "front"
                    ],
                    [
                        "front",
                        "door"
                    ],
                    [
                        "front",
                        "door",
                        "milk"
                    ],
                    [
                        "front",
                        "door",
                        "number"
                    ],
                    [
                        "front",
                        "gardens"
                    ],
                    [
                        "front",
                        "gardens",
                        "lit"
                    ],
                    [
                        "front",
                        "step"
                    ],
                    [
                        "front",
                        "step",
                        "privet"
                    ],
                    [
                        "gardens"
                    ],
                    [
                        "gardens",
                        "lit"
                    ],
                    [
                        "gardens",
                        "lit",
                        "brass"
                    ],
                    [
                        "glass"
                    ],
                    [
                        "glass",
                        "nearly"
                    ],
                    [
                        "glass",
                        "nearly",
                        "ten"
                    ],
                    [
                        "glasses"
                    ],
                    [
                        "glasses",
                        "saying"
                    ],
                    [
                        "glasses",
                        "saying",
                        "hushed"
                    ],
                    [
                        "hagrid"
                    ],
                    [
                        "hagrid",
                        "better"
                    ],
                    [
                        "hagrid",
                        "better",
                        "dumbledore"
                    ],
                    [
                        "hand"
                    ],
                    [
                        "hand",
                        "closed"
                    ],
                    [
                        "hand",
                        "closed",
                        "letter"
                    ],
                    [
                        "hardly"
                    ],
                    [
                        "hardly",
                        "changed"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "arms",
                        "turned"
                    ],
                    [
                        "harry",
                        "harry"
                    ],
                    [
                        "harry",
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "harry",
                        "potter",
                        "lived"
                    ],
                    [
                        "holding"
                    ],
                    [
                        "holding",
                        "people"
                    ],
                    [
                        "holding",
                        "people",
                        "glasses"
                    ],
                    [
                        "hours"
                    ],
                    [
                        "hours",
                        "dursley"
                    ],
                    [
                        "hours",
                        "dursley",
                        "scream"
                    ],
                    [
                        "house"
                    ],
                    [
                        "hugged"
                    ],
                    [
                        "hugged",
                        "kissed"
                    ],
                    [
                        "hugged",
                        "kissed",
                        "mother"
                    ],
                    [
                        "hushed"
                    ],
                    [
                        "hushed",
                        "voices"
                    ],
                    [
                        "hushed",
                        "voices",
                        "harry"
                    ],
                    [
                        "kissed"
                    ],
                    [
                        "kissed",
                        "mother"
                    ],
                    [
                        "knowing"
                    ],
                    [
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "special"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "large"
                    ],
                    [
                        "large",
                        "blond"
                    ],
                    [
                        "large",
                        "blond",
                        "riding"
                    ],
                    [
                        "large",
                        "pink"
                    ],
                    [
                        "large",
                        "pink",
                        "beach"
                    ],
                    [
                        "letter"
                    ],
                    [
                        "letter",
                        "beside"
                    ],
                    [
                        "letter",
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "like"
                    ],
                    [
                        "like",
                        "large"
                    ],
                    [
                        "like",
                        "large",
                        "pink"
                    ],
                    [
                        "lit"
                    ],
                    [
                        "lit",
                        "brass"
                    ],
                    [
                        "lit",
                        "brass",
                        "number"
                    ],
                    [
                        "lived"
                    ],
                    [
                        "living"
                    ],
                    [
                        "living",
                        "room"
                    ],
                    [
                        "living",
                        "room",
                        "almost"
                    ],
                    [
                        "longer"
                    ],
                    [
                        "longer",
                        "baby"
                    ],
                    [
                        "longer",
                        "baby",
                        "photographs"
                    ],
                    [
                        "looked"
                    ],
                    [
                        "looked",
                        "like"
                    ],
                    [
                        "looked",
                        "like",
                        "large"
                    ],
                    [
                        "lots"
                    ],
                    [
                        "lots",
                        "pictures"
                    ],
                    [
                        "lots",
                        "pictures",
                        "looked"
                    ],
                    [
                        "meeting"
                    ],
                    [
                        "meeting",
                        "secret"
                    ],
                    [
                        "meeting",
                        "secret",
                        "country"
                    ],
                    [
                        "milk"
                    ],
                    [
                        "milk",
                        "bottles"
                    ],
                    [
                        "milk",
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "moment"
                    ],
                    [
                        "moment",
                        "people"
                    ],
                    [
                        "moment",
                        "people",
                        "meeting"
                    ],
                    [
                        "mother"
                    ],
                    [
                        "nearly"
                    ],
                    [
                        "nearly",
                        "ten"
                    ],
                    [
                        "nearly",
                        "ten",
                        "years"
                    ],
                    [
                        "nephew"
                    ],
                    [
                        "nephew",
                        "front"
                    ],
                    [
                        "nephew",
                        "front",
                        "step"
                    ],
                    [
                        "news"
                    ],
                    [
                        "news",
                        "report"
                    ],
                    [
                        "news",
                        "report",
                        "owls"
                    ],
                    [
                        "next"
                    ],
                    [
                        "next",
                        "weeks"
                    ],
                    [
                        "next",
                        "weeks",
                        "prodded"
                    ],
                    [
                        "number"
                    ],
                    [
                        "number",
                        "crept"
                    ],
                    [
                        "number",
                        "crept",
                        "dursley"
                    ],
                    [
                        "number",
                        "four"
                    ],
                    [
                        "number",
                        "four",
                        "dursley"
                    ],
                    [
                        "opened"
                    ],
                    [
                        "opened",
                        "front"
                    ],
                    [
                        "opened",
                        "front",
                        "door"
                    ],
                    [
                        "owls"
                    ],
                    [
                        "passed"
                    ],
                    [
                        "passed",
                        "since"
                    ],
                    [
                        "passed",
                        "since",
                        "dursley"
                    ],
                    [
                        "people"
                    ],
                    [
                        "people",
                        "glasses"
                    ],
                    [
                        "people",
                        "glasses",
                        "saying"
                    ],
                    [
                        "people",
                        "meeting"
                    ],
                    [
                        "people",
                        "meeting",
                        "secret"
                    ],
                    [
                        "photographs"
                    ],
                    [
                        "photographs",
                        "showed"
                    ],
                    [
                        "photographs",
                        "showed",
                        "large"
                    ],
                    [
                        "pictures"
                    ],
                    [
                        "pictures",
                        "looked"
                    ],
                    [
                        "pictures",
                        "looked",
                        "like"
                    ],
                    [
                        "pinched"
                    ],
                    [
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "pinched",
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "pink"
                    ],
                    [
                        "pink",
                        "beach"
                    ],
                    [
                        "pink",
                        "beach",
                        "ball"
                    ],
                    [
                        "playing"
                    ],
                    [
                        "playing",
                        "computer"
                    ],
                    [
                        "playing",
                        "computer",
                        "father"
                    ],
                    [
                        "potter"
                    ],
                    [
                        "potter",
                        "lived"
                    ],
                    [
                        "privet"
                    ],
                    [
                        "privet",
                        "drive"
                    ],
                    [
                        "privet",
                        "drive",
                        "hardly"
                    ],
                    [
                        "prodded"
                    ],
                    [
                        "prodded",
                        "pinched"
                    ],
                    [
                        "prodded",
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "report"
                    ],
                    [
                        "report",
                        "owls"
                    ],
                    [
                        "riding"
                    ],
                    [
                        "riding",
                        "bicycle"
                    ],
                    [
                        "riding",
                        "bicycle",
                        "carousel"
                    ],
                    [
                        "room"
                    ],
                    [
                        "room",
                        "almost"
                    ],
                    [
                        "room",
                        "almost",
                        "exactly"
                    ],
                    [
                        "rose"
                    ],
                    [
                        "rose",
                        "tidy"
                    ],
                    [
                        "rose",
                        "tidy",
                        "front"
                    ],
                    [
                        "saying"
                    ],
                    [
                        "saying",
                        "hushed"
                    ],
                    [
                        "saying",
                        "hushed",
                        "voices"
                    ],
                    [
                        "scream"
                    ],
                    [
                        "scream",
                        "dursley"
                    ],
                    [
                        "scream",
                        "dursley",
                        "opened"
                    ],
                    [
                        "secret"
                    ],
                    [
                        "secret",
                        "country"
                    ],
                    [
                        "secret",
                        "country",
                        "holding"
                    ],
                    [
                        "seen"
                    ],
                    [
                        "seen",
                        "fateful"
                    ],
                    [
                        "seen",
                        "fateful",
                        "news"
                    ],
                    [
                        "showed"
                    ],
                    [
                        "showed",
                        "large"
                    ],
                    [
                        "showed",
                        "large",
                        "blond"
                    ],
                    [
                        "since"
                    ],
                    [
                        "since",
                        "dursley"
                    ],
                    [
                        "since",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "slept"
                    ],
                    [
                        "slept",
                        "knowing"
                    ],
                    [
                        "slept",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "small"
                    ],
                    [
                        "small",
                        "hand"
                    ],
                    [
                        "small",
                        "hand",
                        "closed"
                    ],
                    [
                        "special"
                    ],
                    [
                        "special",
                        "knowing"
                    ],
                    [
                        "special",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "spend"
                    ],
                    [
                        "spend",
                        "next"
                    ],
                    [
                        "spend",
                        "next",
                        "weeks"
                    ],
                    [
                        "step"
                    ],
                    [
                        "step",
                        "privet"
                    ],
                    [
                        "step",
                        "privet",
                        "drive"
                    ],
                    [
                        "sun"
                    ],
                    [
                        "sun",
                        "rose"
                    ],
                    [
                        "sun",
                        "rose",
                        "tidy"
                    ],
                    [
                        "ten"
                    ],
                    [
                        "ten",
                        "years"
                    ],
                    [
                        "ten",
                        "years",
                        "ago"
                    ],
                    [
                        "ten",
                        "years",
                        "passed"
                    ],
                    [
                        "tidy"
                    ],
                    [
                        "tidy",
                        "front"
                    ],
                    [
                        "tidy",
                        "front",
                        "gardens"
                    ],
                    [
                        "took"
                    ],
                    [
                        "took",
                        "harry"
                    ],
                    [
                        "took",
                        "harry",
                        "harry"
                    ],
                    [
                        "toward"
                    ],
                    [
                        "toward",
                        "dursley"
                    ],
                    [
                        "toward",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "turned"
                    ],
                    [
                        "turned",
                        "toward"
                    ],
                    [
                        "turned",
                        "toward",
                        "dursley"
                    ],
                    [
                        "vanishing"
                    ],
                    [
                        "vanishing",
                        "glass"
                    ],
                    [
                        "vanishing",
                        "glass",
                        "nearly"
                    ],
                    [
                        "voices"
                    ],
                    [
                        "voices",
                        "harry"
                    ],
                    [
                        "voices",
                        "harry",
                        "potter"
                    ],
                    [
                        "wearing"
                    ],
                    [
                        "wearing",
                        "different"
                    ],
                    [
                        "wearing",
                        "different",
                        "colored"
                    ],
                    [
                        "weeks"
                    ],
                    [
                        "weeks",
                        "prodded"
                    ],
                    [
                        "weeks",
                        "prodded",
                        "pinched"
                    ],
                    [
                        "well"
                    ],
                    [
                        "well",
                        "dumbledore"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "woken"
                    ],
                    [
                        "woken",
                        "dursley"
                    ],
                    [
                        "woken",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "woken",
                        "hours"
                    ],
                    [
                        "woken",
                        "hours",
                        "dursley"
                    ],
                    [
                        "years"
                    ],
                    [
                        "years",
                        "ago"
                    ],
                    [
                        "years",
                        "ago",
                        "lots"
                    ],
                    [
                        "years",
                        "passed"
                    ],
                    [
                        "years",
                        "passed",
                        "since"
                    ]
                ]
            ],
            [
                "aurelius dumbledore",
                [
                    [
                        "air"
                    ],
                    [
                        "arm"
                    ],
                    [
                        "arm",
                        "dumbledore"
                    ],
                    [
                        "arm",
                        "dumbledore",
                        "stepped"
                    ],
                    [
                        "arms"
                    ],
                    [
                        "arms",
                        "turned"
                    ],
                    [
                        "arms",
                        "turned",
                        "toward"
                    ],
                    [
                        "balls"
                    ],
                    [
                        "balls",
                        "light"
                    ],
                    [
                        "balls",
                        "light",
                        "sped"
                    ],
                    [
                        "balls",
                        "street"
                    ],
                    [
                        "balls",
                        "street",
                        "lamps"
                    ],
                    [
                        "beside"
                    ],
                    [
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "beside",
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "better"
                    ],
                    [
                        "better",
                        "dumbledore"
                    ],
                    [
                        "better",
                        "dumbledore",
                        "took"
                    ],
                    [
                        "bike"
                    ],
                    [
                        "bike",
                        "professor"
                    ],
                    [
                        "bike",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "black"
                    ],
                    [
                        "black",
                        "forehead"
                    ],
                    [
                        "black",
                        "forehead",
                        "dumbledore"
                    ],
                    [
                        "blankets"
                    ],
                    [
                        "blankets",
                        "came"
                    ],
                    [
                        "blankets",
                        "step"
                    ],
                    [
                        "blankets",
                        "step",
                        "number"
                    ],
                    [
                        "blankets",
                        "without"
                    ],
                    [
                        "blankets",
                        "without",
                        "waking"
                    ],
                    [
                        "blinked"
                    ],
                    [
                        "blinked",
                        "furiously"
                    ],
                    [
                        "blinked",
                        "furiously",
                        "twinkling"
                    ],
                    [
                        "bolt"
                    ],
                    [
                        "bolt",
                        "lightning"
                    ],
                    [
                        "bottles"
                    ],
                    [
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "bottles",
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "bundle"
                    ],
                    [
                        "bundle",
                        "blankets"
                    ],
                    [
                        "bundle",
                        "blankets",
                        "step"
                    ],
                    [
                        "bundle",
                        "hagrid"
                    ],
                    [
                        "bundle",
                        "hagrid",
                        "shoulders"
                    ],
                    [
                        "burying"
                    ],
                    [
                        "burying",
                        "hagrid"
                    ],
                    [
                        "burying",
                        "hagrid",
                        "face"
                    ],
                    [
                        "came"
                    ],
                    [
                        "cat"
                    ],
                    [
                        "cat",
                        "slinking"
                    ],
                    [
                        "cat",
                        "slinking",
                        "corner"
                    ],
                    [
                        "celebrations"
                    ],
                    [
                        "celebrations",
                        "hagrid"
                    ],
                    [
                        "celebrations",
                        "hagrid",
                        "muffled"
                    ],
                    [
                        "clicked"
                    ],
                    [
                        "clicked",
                        "outer"
                    ],
                    [
                        "clicked",
                        "outer",
                        "twelve"
                    ],
                    [
                        "cloak"
                    ],
                    [
                        "cloak",
                        "dumbledore"
                    ],
                    [
                        "cloak",
                        "tucked"
                    ],
                    [
                        "cloak",
                        "tucked",
                        "letter"
                    ],
                    [
                        "closed"
                    ],
                    [
                        "closed",
                        "letter"
                    ],
                    [
                        "closed",
                        "letter",
                        "beside"
                    ],
                    [
                        "corner"
                    ],
                    [
                        "corner",
                        "dumbledore"
                    ],
                    [
                        "corner",
                        "dumbledore",
                        "stopped"
                    ],
                    [
                        "corner",
                        "street"
                    ],
                    [
                        "couldn"
                    ],
                    [
                        "couldn",
                        "moment"
                    ],
                    [
                        "couldn",
                        "moment",
                        "people"
                    ],
                    [
                        "couldn",
                        "something"
                    ],
                    [
                        "couldn",
                        "something",
                        "scar"
                    ],
                    [
                        "country"
                    ],
                    [
                        "country",
                        "holding"
                    ],
                    [
                        "country",
                        "holding",
                        "people"
                    ],
                    [
                        "cousin"
                    ],
                    [
                        "cousin",
                        "dudley"
                    ],
                    [
                        "cousin",
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "curiously"
                    ],
                    [
                        "curiously",
                        "shaped"
                    ],
                    [
                        "curiously",
                        "shaped",
                        "cut"
                    ],
                    [
                        "cut"
                    ],
                    [
                        "cut",
                        "like"
                    ],
                    [
                        "cut",
                        "like",
                        "bolt"
                    ],
                    [
                        "dead"
                    ],
                    [
                        "dead",
                        "poor"
                    ],
                    [
                        "dead",
                        "poor",
                        "little"
                    ],
                    [
                        "door"
                    ],
                    [
                        "door",
                        "milk"
                    ],
                    [
                        "door",
                        "milk",
                        "bottles"
                    ],
                    [
                        "doorstep"
                    ],
                    [
                        "doorstep",
                        "took"
                    ],
                    [
                        "doorstep",
                        "took",
                        "letter"
                    ],
                    [
                        "drive"
                    ],
                    [
                        "drive",
                        "glowed"
                    ],
                    [
                        "drive",
                        "glowed",
                        "suddenly"
                    ],
                    [
                        "dudley"
                    ],
                    [
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "dudley",
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "house"
                    ],
                    [
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "blankets"
                    ],
                    [
                        "dumbledore",
                        "blankets",
                        "without"
                    ],
                    [
                        "dumbledore",
                        "bundle"
                    ],
                    [
                        "dumbledore",
                        "bundle",
                        "blankets"
                    ],
                    [
                        "dumbledore",
                        "clicked"
                    ],
                    [
                        "dumbledore",
                        "clicked",
                        "outer"
                    ],
                    [
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "dumbledore",
                        "cloak",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "cloak",
                        "tucked"
                    ],
                    [
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dumbledore",
                        "couldn",
                        "moment"
                    ],
                    [
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "dumbledore",
                        "cousin",
                        "dudley"
                    ],
                    [
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "ll"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "eyes"
                    ],
                    [
                        "dumbledore",
                        "eyes",
                        "seemed"
                    ],
                    [
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "dumbledore",
                        "famous",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "finally"
                    ],
                    [
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "dumbledore",
                        "hagrid",
                        "better"
                    ],
                    [
                        "dumbledore",
                        "heel"
                    ],
                    [
                        "dumbledore",
                        "heel",
                        "swish"
                    ],
                    [
                        "dumbledore",
                        "laid"
                    ],
                    [
                        "dumbledore",
                        "laid",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "ll"
                    ],
                    [
                        "dumbledore",
                        "ll",
                        "scar"
                    ],
                    [
                        "dumbledore",
                        "mcgonagall"
                    ],
                    [
                        "dumbledore",
                        "mcgonagall",
                        "curiously"
                    ],
                    [
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "dumbledore",
                        "nodding"
                    ],
                    [
                        "dumbledore",
                        "nodding",
                        "voice"
                    ],
                    [
                        "dumbledore",
                        "sir"
                    ],
                    [
                        "dumbledore",
                        "sir",
                        "wiping"
                    ],
                    [
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "slept",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "special"
                    ],
                    [
                        "dumbledore",
                        "special",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "dumbledore",
                        "spend",
                        "next"
                    ],
                    [
                        "dumbledore",
                        "stepped"
                    ],
                    [
                        "dumbledore",
                        "stepped",
                        "low"
                    ],
                    [
                        "dumbledore",
                        "stopped"
                    ],
                    [
                        "dumbledore",
                        "stopped",
                        "took"
                    ],
                    [
                        "dumbledore",
                        "tabby"
                    ],
                    [
                        "dumbledore",
                        "tabby",
                        "cat"
                    ],
                    [
                        "dumbledore",
                        "took"
                    ],
                    [
                        "dumbledore",
                        "took",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "turned"
                    ],
                    [
                        "dumbledore",
                        "turned",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "turned",
                        "walked"
                    ],
                    [
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "dumbledore",
                        "woken",
                        "hours"
                    ],
                    [
                        "dumbledore",
                        "wouldn"
                    ],
                    [
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "house"
                    ],
                    [
                        "dursley",
                        "opened"
                    ],
                    [
                        "dursley",
                        "opened",
                        "front"
                    ],
                    [
                        "dursley",
                        "scream"
                    ],
                    [
                        "dursley",
                        "scream",
                        "dursley"
                    ],
                    [
                        "engine"
                    ],
                    [
                        "engine",
                        "roar"
                    ],
                    [
                        "engine",
                        "roar",
                        "engine"
                    ],
                    [
                        "engine",
                        "rose"
                    ],
                    [
                        "engine",
                        "rose",
                        "air"
                    ],
                    [
                        "expect"
                    ],
                    [
                        "expect",
                        "professor"
                    ],
                    [
                        "expect",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "eyes"
                    ],
                    [
                        "eyes",
                        "seemed"
                    ],
                    [
                        "eyes",
                        "sirius"
                    ],
                    [
                        "eyes",
                        "sirius",
                        "jacket"
                    ],
                    [
                        "face"
                    ],
                    [
                        "face",
                        "handkerchief"
                    ],
                    [
                        "face",
                        "handkerchief",
                        "stand"
                    ],
                    [
                        "famous"
                    ],
                    [
                        "famous",
                        "knowing"
                    ],
                    [
                        "famous",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "finally"
                    ],
                    [
                        "forehead"
                    ],
                    [
                        "forehead",
                        "dumbledore"
                    ],
                    [
                        "forehead",
                        "dumbledore",
                        "mcgonagall"
                    ],
                    [
                        "forever"
                    ],
                    [
                        "forever",
                        "couldn"
                    ],
                    [
                        "forever",
                        "couldn",
                        "something"
                    ],
                    [
                        "four"
                    ],
                    [
                        "front"
                    ],
                    [
                        "front",
                        "door"
                    ],
                    [
                        "front",
                        "door",
                        "milk"
                    ],
                    [
                        "full"
                    ],
                    [
                        "full",
                        "minute"
                    ],
                    [
                        "full",
                        "minute",
                        "three"
                    ],
                    [
                        "furiously"
                    ],
                    [
                        "furiously",
                        "twinkling"
                    ],
                    [
                        "furiously",
                        "twinkling",
                        "light"
                    ],
                    [
                        "garden"
                    ],
                    [
                        "garden",
                        "wall"
                    ],
                    [
                        "garden",
                        "wall",
                        "walked"
                    ],
                    [
                        "gently"
                    ],
                    [
                        "gently",
                        "doorstep"
                    ],
                    [
                        "gently",
                        "doorstep",
                        "took"
                    ],
                    [
                        "gingerly"
                    ],
                    [
                        "gingerly",
                        "arm"
                    ],
                    [
                        "gingerly",
                        "arm",
                        "dumbledore"
                    ],
                    [
                        "glasses"
                    ],
                    [
                        "glasses",
                        "saying"
                    ],
                    [
                        "glasses",
                        "saying",
                        "hushed"
                    ],
                    [
                        "glowed"
                    ],
                    [
                        "glowed",
                        "suddenly"
                    ],
                    [
                        "glowed",
                        "suddenly",
                        "orange"
                    ],
                    [
                        "go"
                    ],
                    [
                        "go",
                        "join"
                    ],
                    [
                        "go",
                        "join",
                        "celebrations"
                    ],
                    [
                        "good"
                    ],
                    [
                        "good",
                        "luck"
                    ],
                    [
                        "good",
                        "luck",
                        "harry"
                    ],
                    [
                        "grip"
                    ],
                    [
                        "grip",
                        "hagrid"
                    ],
                    [
                        "grip",
                        "hagrid",
                        "ll"
                    ],
                    [
                        "hagrid"
                    ],
                    [
                        "hagrid",
                        "better"
                    ],
                    [
                        "hagrid",
                        "better",
                        "dumbledore"
                    ],
                    [
                        "hagrid",
                        "face"
                    ],
                    [
                        "hagrid",
                        "face",
                        "handkerchief"
                    ],
                    [
                        "hagrid",
                        "gingerly"
                    ],
                    [
                        "hagrid",
                        "gingerly",
                        "arm"
                    ],
                    [
                        "hagrid",
                        "ll"
                    ],
                    [
                        "hagrid",
                        "ll",
                        "professor"
                    ],
                    [
                        "hagrid",
                        "muffled"
                    ],
                    [
                        "hagrid",
                        "muffled",
                        "voice"
                    ],
                    [
                        "hagrid",
                        "onto"
                    ],
                    [
                        "hagrid",
                        "onto",
                        "motorcycle"
                    ],
                    [
                        "hagrid",
                        "shoulders"
                    ],
                    [
                        "hagrid",
                        "shoulders",
                        "shook"
                    ],
                    [
                        "hagrid",
                        "swung"
                    ],
                    [
                        "hagrid",
                        "swung",
                        "hagrid"
                    ],
                    [
                        "hagrid",
                        "taking"
                    ],
                    [
                        "hagrid",
                        "taking",
                        "large"
                    ],
                    [
                        "hand"
                    ],
                    [
                        "hand",
                        "closed"
                    ],
                    [
                        "hand",
                        "closed",
                        "letter"
                    ],
                    [
                        "handkerchief"
                    ],
                    [
                        "handkerchief",
                        "burying"
                    ],
                    [
                        "handkerchief",
                        "burying",
                        "hagrid"
                    ],
                    [
                        "handkerchief",
                        "lily"
                    ],
                    [
                        "handkerchief",
                        "lily",
                        "james"
                    ],
                    [
                        "handkerchief",
                        "sad"
                    ],
                    [
                        "handkerchief",
                        "sad",
                        "grip"
                    ],
                    [
                        "handkerchief",
                        "stand"
                    ],
                    [
                        "handkerchief",
                        "stand",
                        "handkerchief"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "arms",
                        "turned"
                    ],
                    [
                        "harry",
                        "blankets"
                    ],
                    [
                        "harry",
                        "blankets",
                        "came"
                    ],
                    [
                        "harry",
                        "dumbledore"
                    ],
                    [
                        "harry",
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "harry",
                        "gently"
                    ],
                    [
                        "harry",
                        "gently",
                        "doorstep"
                    ],
                    [
                        "harry",
                        "harry"
                    ],
                    [
                        "harry",
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "harry",
                        "potter",
                        "lived"
                    ],
                    [
                        "harry",
                        "potter",
                        "rolled"
                    ],
                    [
                        "harry",
                        "ter"
                    ],
                    [
                        "harry",
                        "ter",
                        "muggles"
                    ],
                    [
                        "heel"
                    ],
                    [
                        "heel",
                        "swish"
                    ],
                    [
                        "heel",
                        "swish",
                        "dumbledore"
                    ],
                    [
                        "hissed"
                    ],
                    [
                        "hissed",
                        "professor"
                    ],
                    [
                        "hissed",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "holding"
                    ],
                    [
                        "holding",
                        "people"
                    ],
                    [
                        "holding",
                        "people",
                        "glasses"
                    ],
                    [
                        "hours"
                    ],
                    [
                        "hours",
                        "dursley"
                    ],
                    [
                        "hours",
                        "dursley",
                        "scream"
                    ],
                    [
                        "house"
                    ],
                    [
                        "hushed"
                    ],
                    [
                        "hushed",
                        "voices"
                    ],
                    [
                        "hushed",
                        "voices",
                        "harry"
                    ],
                    [
                        "inside"
                    ],
                    [
                        "inside",
                        "dumbledore"
                    ],
                    [
                        "inside",
                        "dumbledore",
                        "blankets"
                    ],
                    [
                        "inside",
                        "harry"
                    ],
                    [
                        "inside",
                        "harry",
                        "blankets"
                    ],
                    [
                        "jacket"
                    ],
                    [
                        "jacket",
                        "sleeve"
                    ],
                    [
                        "jacket",
                        "sleeve",
                        "hagrid"
                    ],
                    [
                        "james"
                    ],
                    [
                        "james",
                        "dead"
                    ],
                    [
                        "james",
                        "dead",
                        "poor"
                    ],
                    [
                        "jet"
                    ],
                    [
                        "jet",
                        "black"
                    ],
                    [
                        "jet",
                        "black",
                        "forehead"
                    ],
                    [
                        "join"
                    ],
                    [
                        "join",
                        "celebrations"
                    ],
                    [
                        "join",
                        "celebrations",
                        "hagrid"
                    ],
                    [
                        "kicked"
                    ],
                    [
                        "kicked",
                        "engine"
                    ],
                    [
                        "kicked",
                        "engine",
                        "roar"
                    ],
                    [
                        "knowing"
                    ],
                    [
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "special"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "laid"
                    ],
                    [
                        "laid",
                        "harry"
                    ],
                    [
                        "laid",
                        "harry",
                        "gently"
                    ],
                    [
                        "lamps"
                    ],
                    [
                        "lamps",
                        "privet"
                    ],
                    [
                        "lamps",
                        "privet",
                        "drive"
                    ],
                    [
                        "large"
                    ],
                    [
                        "large",
                        "spotted"
                    ],
                    [
                        "large",
                        "spotted",
                        "handkerchief"
                    ],
                    [
                        "letter"
                    ],
                    [
                        "letter",
                        "beside"
                    ],
                    [
                        "letter",
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "letter",
                        "dumbledore"
                    ],
                    [
                        "letter",
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "letter",
                        "inside"
                    ],
                    [
                        "letter",
                        "inside",
                        "harry"
                    ],
                    [
                        "light"
                    ],
                    [
                        "light",
                        "sped"
                    ],
                    [
                        "light",
                        "sped",
                        "balls"
                    ],
                    [
                        "light",
                        "usually"
                    ],
                    [
                        "light",
                        "usually",
                        "shone"
                    ],
                    [
                        "lightning"
                    ],
                    [
                        "like"
                    ],
                    [
                        "like",
                        "bolt"
                    ],
                    [
                        "like",
                        "bolt",
                        "lightning"
                    ],
                    [
                        "lily"
                    ],
                    [
                        "lily",
                        "james"
                    ],
                    [
                        "lily",
                        "james",
                        "dead"
                    ],
                    [
                        "little"
                    ],
                    [
                        "little",
                        "bundle"
                    ],
                    [
                        "little",
                        "bundle",
                        "hagrid"
                    ],
                    [
                        "little",
                        "harry"
                    ],
                    [
                        "little",
                        "harry",
                        "ter"
                    ],
                    [
                        "lived"
                    ],
                    [
                        "ll"
                    ],
                    [
                        "ll",
                        "professor"
                    ],
                    [
                        "ll",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "ll",
                        "scar"
                    ],
                    [
                        "ll",
                        "scar",
                        "forever"
                    ],
                    [
                        "ll",
                        "takin"
                    ],
                    [
                        "ll",
                        "takin",
                        "sirius"
                    ],
                    [
                        "ll",
                        "wake"
                    ],
                    [
                        "ll",
                        "wake",
                        "muggles"
                    ],
                    [
                        "looked"
                    ],
                    [
                        "looked",
                        "little"
                    ],
                    [
                        "looked",
                        "little",
                        "bundle"
                    ],
                    [
                        "low"
                    ],
                    [
                        "low",
                        "garden"
                    ],
                    [
                        "low",
                        "garden",
                        "wall"
                    ],
                    [
                        "luck"
                    ],
                    [
                        "luck",
                        "harry"
                    ],
                    [
                        "luck",
                        "harry",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall"
                    ],
                    [
                        "mcgonagall",
                        "blinked"
                    ],
                    [
                        "mcgonagall",
                        "blinked",
                        "furiously"
                    ],
                    [
                        "mcgonagall",
                        "curiously"
                    ],
                    [
                        "mcgonagall",
                        "curiously",
                        "shaped"
                    ],
                    [
                        "mcgonagall",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall",
                        "dumbledore",
                        "nodding"
                    ],
                    [
                        "mcgonagall",
                        "ll"
                    ],
                    [
                        "mcgonagall",
                        "ll",
                        "wake"
                    ],
                    [
                        "mcgonagall",
                        "professor"
                    ],
                    [
                        "mcgonagall",
                        "professor",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall",
                        "whispered"
                    ],
                    [
                        "mcgonagall",
                        "whispered",
                        "patting"
                    ],
                    [
                        "meeting"
                    ],
                    [
                        "meeting",
                        "secret"
                    ],
                    [
                        "meeting",
                        "secret",
                        "country"
                    ],
                    [
                        "milk"
                    ],
                    [
                        "milk",
                        "bottles"
                    ],
                    [
                        "milk",
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "minute"
                    ],
                    [
                        "minute",
                        "three"
                    ],
                    [
                        "minute",
                        "three",
                        "stood"
                    ],
                    [
                        "moment"
                    ],
                    [
                        "moment",
                        "people"
                    ],
                    [
                        "moment",
                        "people",
                        "meeting"
                    ],
                    [
                        "motorcycle"
                    ],
                    [
                        "motorcycle",
                        "kicked"
                    ],
                    [
                        "motorcycle",
                        "kicked",
                        "engine"
                    ],
                    [
                        "muffled"
                    ],
                    [
                        "muffled",
                        "voice"
                    ],
                    [
                        "muffled",
                        "voice",
                        "ll"
                    ],
                    [
                        "muggles"
                    ],
                    [
                        "muggles",
                        "handkerchief"
                    ],
                    [
                        "muggles",
                        "handkerchief",
                        "sad"
                    ],
                    [
                        "muggles",
                        "sorry"
                    ],
                    [
                        "muggles",
                        "sorry",
                        "sobbed"
                    ],
                    [
                        "murmured"
                    ],
                    [
                        "next"
                    ],
                    [
                        "next",
                        "weeks"
                    ],
                    [
                        "next",
                        "weeks",
                        "prodded"
                    ],
                    [
                        "nodding"
                    ],
                    [
                        "nodding",
                        "voice"
                    ],
                    [
                        "number"
                    ],
                    [
                        "number",
                        "four"
                    ],
                    [
                        "onto"
                    ],
                    [
                        "onto",
                        "motorcycle"
                    ],
                    [
                        "onto",
                        "motorcycle",
                        "kicked"
                    ],
                    [
                        "opened"
                    ],
                    [
                        "opened",
                        "front"
                    ],
                    [
                        "opened",
                        "front",
                        "door"
                    ],
                    [
                        "orange"
                    ],
                    [
                        "orange",
                        "dumbledore"
                    ],
                    [
                        "orange",
                        "dumbledore",
                        "tabby"
                    ],
                    [
                        "outer"
                    ],
                    [
                        "outer",
                        "twelve"
                    ],
                    [
                        "outer",
                        "twelve",
                        "balls"
                    ],
                    [
                        "patting"
                    ],
                    [
                        "patting",
                        "hagrid"
                    ],
                    [
                        "patting",
                        "hagrid",
                        "gingerly"
                    ],
                    [
                        "people"
                    ],
                    [
                        "people",
                        "glasses"
                    ],
                    [
                        "people",
                        "glasses",
                        "saying"
                    ],
                    [
                        "people",
                        "meeting"
                    ],
                    [
                        "people",
                        "meeting",
                        "secret"
                    ],
                    [
                        "pinched"
                    ],
                    [
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "pinched",
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "poor"
                    ],
                    [
                        "poor",
                        "little"
                    ],
                    [
                        "poor",
                        "little",
                        "harry"
                    ],
                    [
                        "potter"
                    ],
                    [
                        "potter",
                        "lived"
                    ],
                    [
                        "potter",
                        "rolled"
                    ],
                    [
                        "potter",
                        "rolled",
                        "inside"
                    ],
                    [
                        "privet"
                    ],
                    [
                        "privet",
                        "drive"
                    ],
                    [
                        "privet",
                        "drive",
                        "glowed"
                    ],
                    [
                        "prodded"
                    ],
                    [
                        "prodded",
                        "pinched"
                    ],
                    [
                        "prodded",
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "professor"
                    ],
                    [
                        "professor",
                        "dumbledore"
                    ],
                    [
                        "professor",
                        "dumbledore",
                        "sir"
                    ],
                    [
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "blinked"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "dumbledore"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "ll"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "professor"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "whispered"
                    ],
                    [
                        "roar"
                    ],
                    [
                        "roar",
                        "engine"
                    ],
                    [
                        "roar",
                        "engine",
                        "rose"
                    ],
                    [
                        "rolled"
                    ],
                    [
                        "rolled",
                        "inside"
                    ],
                    [
                        "rolled",
                        "inside",
                        "dumbledore"
                    ],
                    [
                        "rose"
                    ],
                    [
                        "rose",
                        "air"
                    ],
                    [
                        "sad"
                    ],
                    [
                        "sad",
                        "grip"
                    ],
                    [
                        "sad",
                        "grip",
                        "hagrid"
                    ],
                    [
                        "saying"
                    ],
                    [
                        "saying",
                        "hushed"
                    ],
                    [
                        "saying",
                        "hushed",
                        "voices"
                    ],
                    [
                        "scar"
                    ],
                    [
                        "scar",
                        "dumbledore"
                    ],
                    [
                        "scar",
                        "dumbledore",
                        "wouldn"
                    ],
                    [
                        "scar",
                        "forever"
                    ],
                    [
                        "scar",
                        "forever",
                        "couldn"
                    ],
                    [
                        "scream"
                    ],
                    [
                        "scream",
                        "dursley"
                    ],
                    [
                        "scream",
                        "dursley",
                        "opened"
                    ],
                    [
                        "secret"
                    ],
                    [
                        "secret",
                        "country"
                    ],
                    [
                        "secret",
                        "country",
                        "holding"
                    ],
                    [
                        "seemed"
                    ],
                    [
                        "shall"
                    ],
                    [
                        "shall",
                        "expect"
                    ],
                    [
                        "shall",
                        "expect",
                        "professor"
                    ],
                    [
                        "shaped"
                    ],
                    [
                        "shaped",
                        "cut"
                    ],
                    [
                        "shaped",
                        "cut",
                        "like"
                    ],
                    [
                        "shhh"
                    ],
                    [
                        "shhh",
                        "hissed"
                    ],
                    [
                        "shhh",
                        "hissed",
                        "professor"
                    ],
                    [
                        "shone"
                    ],
                    [
                        "shone",
                        "dumbledore"
                    ],
                    [
                        "shone",
                        "dumbledore",
                        "eyes"
                    ],
                    [
                        "shook"
                    ],
                    [
                        "shook",
                        "professor"
                    ],
                    [
                        "shook",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "shoulders"
                    ],
                    [
                        "shoulders",
                        "shook"
                    ],
                    [
                        "shoulders",
                        "shook",
                        "professor"
                    ],
                    [
                        "silver"
                    ],
                    [
                        "silver",
                        "outer"
                    ],
                    [
                        "sir"
                    ],
                    [
                        "sir",
                        "wiping"
                    ],
                    [
                        "sir",
                        "wiping",
                        "sirius"
                    ],
                    [
                        "sirius"
                    ],
                    [
                        "sirius",
                        "bike"
                    ],
                    [
                        "sirius",
                        "bike",
                        "professor"
                    ],
                    [
                        "sirius",
                        "jacket"
                    ],
                    [
                        "sirius",
                        "jacket",
                        "sleeve"
                    ],
                    [
                        "sirius",
                        "sirius"
                    ],
                    [
                        "sirius",
                        "sirius",
                        "bike"
                    ],
                    [
                        "sirius",
                        "streaming"
                    ],
                    [
                        "sirius",
                        "streaming",
                        "eyes"
                    ],
                    [
                        "sleeve"
                    ],
                    [
                        "sleeve",
                        "hagrid"
                    ],
                    [
                        "sleeve",
                        "hagrid",
                        "swung"
                    ],
                    [
                        "slept"
                    ],
                    [
                        "slept",
                        "knowing"
                    ],
                    [
                        "slept",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "slinking"
                    ],
                    [
                        "slinking",
                        "corner"
                    ],
                    [
                        "slinking",
                        "corner",
                        "street"
                    ],
                    [
                        "small"
                    ],
                    [
                        "small",
                        "hand"
                    ],
                    [
                        "small",
                        "hand",
                        "closed"
                    ],
                    [
                        "sobbed"
                    ],
                    [
                        "sobbed",
                        "hagrid"
                    ],
                    [
                        "sobbed",
                        "hagrid",
                        "taking"
                    ],
                    [
                        "something"
                    ],
                    [
                        "something",
                        "scar"
                    ],
                    [
                        "something",
                        "scar",
                        "dumbledore"
                    ],
                    [
                        "sorry"
                    ],
                    [
                        "sorry",
                        "sobbed"
                    ],
                    [
                        "sorry",
                        "sobbed",
                        "hagrid"
                    ],
                    [
                        "special"
                    ],
                    [
                        "special",
                        "knowing"
                    ],
                    [
                        "special",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "sped"
                    ],
                    [
                        "sped",
                        "balls"
                    ],
                    [
                        "sped",
                        "balls",
                        "street"
                    ],
                    [
                        "spend"
                    ],
                    [
                        "spend",
                        "next"
                    ],
                    [
                        "spend",
                        "next",
                        "weeks"
                    ],
                    [
                        "spotted"
                    ],
                    [
                        "spotted",
                        "handkerchief"
                    ],
                    [
                        "spotted",
                        "handkerchief",
                        "burying"
                    ],
                    [
                        "stand"
                    ],
                    [
                        "stand",
                        "handkerchief"
                    ],
                    [
                        "stand",
                        "handkerchief",
                        "lily"
                    ],
                    [
                        "step"
                    ],
                    [
                        "step",
                        "number"
                    ],
                    [
                        "step",
                        "number",
                        "four"
                    ],
                    [
                        "stepped"
                    ],
                    [
                        "stepped",
                        "low"
                    ],
                    [
                        "stepped",
                        "low",
                        "garden"
                    ],
                    [
                        "stood"
                    ],
                    [
                        "stood",
                        "looked"
                    ],
                    [
                        "stood",
                        "looked",
                        "little"
                    ],
                    [
                        "stopped"
                    ],
                    [
                        "stopped",
                        "took"
                    ],
                    [
                        "stopped",
                        "took",
                        "silver"
                    ],
                    [
                        "streaming"
                    ],
                    [
                        "streaming",
                        "eyes"
                    ],
                    [
                        "streaming",
                        "eyes",
                        "sirius"
                    ],
                    [
                        "street"
                    ],
                    [
                        "street",
                        "lamps"
                    ],
                    [
                        "street",
                        "lamps",
                        "privet"
                    ],
                    [
                        "suddenly"
                    ],
                    [
                        "suddenly",
                        "orange"
                    ],
                    [
                        "suddenly",
                        "orange",
                        "dumbledore"
                    ],
                    [
                        "swish"
                    ],
                    [
                        "swish",
                        "dumbledore"
                    ],
                    [
                        "swish",
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "swung"
                    ],
                    [
                        "swung",
                        "hagrid"
                    ],
                    [
                        "swung",
                        "hagrid",
                        "onto"
                    ],
                    [
                        "tabby"
                    ],
                    [
                        "tabby",
                        "cat"
                    ],
                    [
                        "tabby",
                        "cat",
                        "slinking"
                    ],
                    [
                        "takin"
                    ],
                    [
                        "takin",
                        "sirius"
                    ],
                    [
                        "takin",
                        "sirius",
                        "sirius"
                    ],
                    [
                        "taking"
                    ],
                    [
                        "taking",
                        "large"
                    ],
                    [
                        "taking",
                        "large",
                        "spotted"
                    ],
                    [
                        "ter"
                    ],
                    [
                        "ter",
                        "muggles"
                    ],
                    [
                        "ter",
                        "muggles",
                        "handkerchief"
                    ],
                    [
                        "three"
                    ],
                    [
                        "three",
                        "stood"
                    ],
                    [
                        "three",
                        "stood",
                        "looked"
                    ],
                    [
                        "took"
                    ],
                    [
                        "took",
                        "harry"
                    ],
                    [
                        "took",
                        "harry",
                        "harry"
                    ],
                    [
                        "took",
                        "letter"
                    ],
                    [
                        "took",
                        "letter",
                        "dumbledore"
                    ],
                    [
                        "took",
                        "silver"
                    ],
                    [
                        "took",
                        "silver",
                        "outer"
                    ],
                    [
                        "toward"
                    ],
                    [
                        "toward",
                        "dursley"
                    ],
                    [
                        "toward",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "tucked"
                    ],
                    [
                        "tucked",
                        "letter"
                    ],
                    [
                        "tucked",
                        "letter",
                        "inside"
                    ],
                    [
                        "tuft"
                    ],
                    [
                        "tuft",
                        "jet"
                    ],
                    [
                        "tuft",
                        "jet",
                        "black"
                    ],
                    [
                        "turned"
                    ],
                    [
                        "turned",
                        "dumbledore"
                    ],
                    [
                        "turned",
                        "dumbledore",
                        "heel"
                    ],
                    [
                        "turned",
                        "toward"
                    ],
                    [
                        "turned",
                        "toward",
                        "dursley"
                    ],
                    [
                        "turned",
                        "walked"
                    ],
                    [
                        "turned",
                        "walked",
                        "street"
                    ],
                    [
                        "twelve"
                    ],
                    [
                        "twelve",
                        "balls"
                    ],
                    [
                        "twelve",
                        "balls",
                        "light"
                    ],
                    [
                        "twinkling"
                    ],
                    [
                        "twinkling",
                        "light"
                    ],
                    [
                        "twinkling",
                        "light",
                        "usually"
                    ],
                    [
                        "usually"
                    ],
                    [
                        "usually",
                        "shone"
                    ],
                    [
                        "usually",
                        "shone",
                        "dumbledore"
                    ],
                    [
                        "voice"
                    ],
                    [
                        "voice",
                        "ll"
                    ],
                    [
                        "voice",
                        "ll",
                        "takin"
                    ],
                    [
                        "voices"
                    ],
                    [
                        "voices",
                        "harry"
                    ],
                    [
                        "voices",
                        "harry",
                        "potter"
                    ],
                    [
                        "wake"
                    ],
                    [
                        "wake",
                        "muggles"
                    ],
                    [
                        "wake",
                        "muggles",
                        "sorry"
                    ],
                    [
                        "waking"
                    ],
                    [
                        "walked"
                    ],
                    [
                        "walked",
                        "front"
                    ],
                    [
                        "walked",
                        "front",
                        "door"
                    ],
                    [
                        "walked",
                        "street"
                    ],
                    [
                        "wall"
                    ],
                    [
                        "wall",
                        "walked"
                    ],
                    [
                        "wall",
                        "walked",
                        "front"
                    ],
                    [
                        "weeks"
                    ],
                    [
                        "weeks",
                        "prodded"
                    ],
                    [
                        "weeks",
                        "prodded",
                        "pinched"
                    ],
                    [
                        "well"
                    ],
                    [
                        "well",
                        "dumbledore"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "finally"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "well",
                        "go"
                    ],
                    [
                        "well",
                        "go",
                        "join"
                    ],
                    [
                        "whispered"
                    ],
                    [
                        "whispered",
                        "patting"
                    ],
                    [
                        "whispered",
                        "patting",
                        "hagrid"
                    ],
                    [
                        "wiping"
                    ],
                    [
                        "wiping",
                        "sirius"
                    ],
                    [
                        "wiping",
                        "sirius",
                        "streaming"
                    ],
                    [
                        "without"
                    ],
                    [
                        "without",
                        "waking"
                    ],
                    [
                        "woken"
                    ],
                    [
                        "woken",
                        "hours"
                    ],
                    [
                        "woken",
                        "hours",
                        "dursley"
                    ],
                    [
                        "wouldn"
                    ]
                ]
            ],
            [
                "harry potter",
                [
                    [
                        "another"
                    ],
                    [
                        "another",
                        "lived"
                    ],
                    [
                        "another",
                        "lived",
                        "house"
                    ],
                    [
                        "arm"
                    ],
                    [
                        "arm",
                        "dumbledore"
                    ],
                    [
                        "arm",
                        "dumbledore",
                        "stepped"
                    ],
                    [
                        "arms"
                    ],
                    [
                        "arms",
                        "turned"
                    ],
                    [
                        "arms",
                        "turned",
                        "toward"
                    ],
                    [
                        "asked"
                    ],
                    [
                        "asked",
                        "hagrid"
                    ],
                    [
                        "bent"
                    ],
                    [
                        "bent",
                        "harry"
                    ],
                    [
                        "bent",
                        "harry",
                        "great"
                    ],
                    [
                        "beside"
                    ],
                    [
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "beside",
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "better"
                    ],
                    [
                        "better",
                        "dumbledore"
                    ],
                    [
                        "better",
                        "dumbledore",
                        "took"
                    ],
                    [
                        "blankets"
                    ],
                    [
                        "blankets",
                        "came"
                    ],
                    [
                        "blankets",
                        "without"
                    ],
                    [
                        "blankets",
                        "without",
                        "waking"
                    ],
                    [
                        "bottles"
                    ],
                    [
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "bottles",
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "burying"
                    ],
                    [
                        "burying",
                        "hagrid"
                    ],
                    [
                        "burying",
                        "hagrid",
                        "face"
                    ],
                    [
                        "bye"
                    ],
                    [
                        "bye",
                        "harry"
                    ],
                    [
                        "bye",
                        "harry",
                        "sir"
                    ],
                    [
                        "came"
                    ],
                    [
                        "cloak"
                    ],
                    [
                        "cloak",
                        "tucked"
                    ],
                    [
                        "cloak",
                        "tucked",
                        "letter"
                    ],
                    [
                        "closed"
                    ],
                    [
                        "closed",
                        "letter"
                    ],
                    [
                        "closed",
                        "letter",
                        "beside"
                    ],
                    [
                        "couldn"
                    ],
                    [
                        "couldn",
                        "moment"
                    ],
                    [
                        "couldn",
                        "moment",
                        "people"
                    ],
                    [
                        "country"
                    ],
                    [
                        "country",
                        "holding"
                    ],
                    [
                        "country",
                        "holding",
                        "people"
                    ],
                    [
                        "cousin"
                    ],
                    [
                        "cousin",
                        "dudley"
                    ],
                    [
                        "cousin",
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "dead"
                    ],
                    [
                        "dead",
                        "poor"
                    ],
                    [
                        "dead",
                        "poor",
                        "little"
                    ],
                    [
                        "door"
                    ],
                    [
                        "door",
                        "milk"
                    ],
                    [
                        "door",
                        "milk",
                        "bottles"
                    ],
                    [
                        "doorstep"
                    ],
                    [
                        "doorstep",
                        "took"
                    ],
                    [
                        "doorstep",
                        "took",
                        "letter"
                    ],
                    [
                        "dudley"
                    ],
                    [
                        "dudley",
                        "dumbledore"
                    ],
                    [
                        "dudley",
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dudley",
                        "dursley",
                        "house"
                    ],
                    [
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "blankets"
                    ],
                    [
                        "dumbledore",
                        "blankets",
                        "without"
                    ],
                    [
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "dumbledore",
                        "cloak",
                        "tucked"
                    ],
                    [
                        "dumbledore",
                        "couldn"
                    ],
                    [
                        "dumbledore",
                        "couldn",
                        "moment"
                    ],
                    [
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "dumbledore",
                        "cousin",
                        "dudley"
                    ],
                    [
                        "dumbledore",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "dumbledore",
                        "famous",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "dumbledore",
                        "hagrid",
                        "better"
                    ],
                    [
                        "dumbledore",
                        "laid"
                    ],
                    [
                        "dumbledore",
                        "laid",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "dumbledore",
                        "slept"
                    ],
                    [
                        "dumbledore",
                        "slept",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "special"
                    ],
                    [
                        "dumbledore",
                        "special",
                        "knowing"
                    ],
                    [
                        "dumbledore",
                        "spend"
                    ],
                    [
                        "dumbledore",
                        "spend",
                        "next"
                    ],
                    [
                        "dumbledore",
                        "stepped"
                    ],
                    [
                        "dumbledore",
                        "stepped",
                        "low"
                    ],
                    [
                        "dumbledore",
                        "took"
                    ],
                    [
                        "dumbledore",
                        "took",
                        "harry"
                    ],
                    [
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "dumbledore",
                        "woken",
                        "hours"
                    ],
                    [
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "dudley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley"
                    ],
                    [
                        "dursley",
                        "dursley",
                        "dudley"
                    ],
                    [
                        "dursley",
                        "house"
                    ],
                    [
                        "dursley",
                        "opened"
                    ],
                    [
                        "dursley",
                        "opened",
                        "front"
                    ],
                    [
                        "dursley",
                        "scream"
                    ],
                    [
                        "dursley",
                        "scream",
                        "dursley"
                    ],
                    [
                        "face"
                    ],
                    [
                        "face",
                        "handkerchief"
                    ],
                    [
                        "face",
                        "handkerchief",
                        "stand"
                    ],
                    [
                        "famous"
                    ],
                    [
                        "famous",
                        "knowing"
                    ],
                    [
                        "famous",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "front"
                    ],
                    [
                        "front",
                        "door"
                    ],
                    [
                        "front",
                        "door",
                        "milk"
                    ],
                    [
                        "garden"
                    ],
                    [
                        "garden",
                        "wall"
                    ],
                    [
                        "garden",
                        "wall",
                        "walked"
                    ],
                    [
                        "gave"
                    ],
                    [
                        "gave",
                        "scratchy"
                    ],
                    [
                        "gave",
                        "scratchy",
                        "whiskery"
                    ],
                    [
                        "gently"
                    ],
                    [
                        "gently",
                        "doorstep"
                    ],
                    [
                        "gently",
                        "doorstep",
                        "took"
                    ],
                    [
                        "gingerly"
                    ],
                    [
                        "gingerly",
                        "arm"
                    ],
                    [
                        "gingerly",
                        "arm",
                        "dumbledore"
                    ],
                    [
                        "glasses"
                    ],
                    [
                        "glasses",
                        "saying"
                    ],
                    [
                        "glasses",
                        "saying",
                        "hushed"
                    ],
                    [
                        "good"
                    ],
                    [
                        "good",
                        "bye"
                    ],
                    [
                        "good",
                        "bye",
                        "harry"
                    ],
                    [
                        "good",
                        "luck"
                    ],
                    [
                        "good",
                        "luck",
                        "harry"
                    ],
                    [
                        "great"
                    ],
                    [
                        "great",
                        "shaggy"
                    ],
                    [
                        "great",
                        "shaggy",
                        "harry"
                    ],
                    [
                        "grip"
                    ],
                    [
                        "grip",
                        "hagrid"
                    ],
                    [
                        "grip",
                        "hagrid",
                        "ll"
                    ],
                    [
                        "hagrid"
                    ],
                    [
                        "hagrid",
                        "better"
                    ],
                    [
                        "hagrid",
                        "better",
                        "dumbledore"
                    ],
                    [
                        "hagrid",
                        "face"
                    ],
                    [
                        "hagrid",
                        "face",
                        "handkerchief"
                    ],
                    [
                        "hagrid",
                        "gingerly"
                    ],
                    [
                        "hagrid",
                        "gingerly",
                        "arm"
                    ],
                    [
                        "hagrid",
                        "ll"
                    ],
                    [
                        "hagrid",
                        "ll",
                        "professor"
                    ],
                    [
                        "hagrid",
                        "taking"
                    ],
                    [
                        "hagrid",
                        "taking",
                        "large"
                    ],
                    [
                        "hand"
                    ],
                    [
                        "hand",
                        "closed"
                    ],
                    [
                        "hand",
                        "closed",
                        "letter"
                    ],
                    [
                        "handkerchief"
                    ],
                    [
                        "handkerchief",
                        "burying"
                    ],
                    [
                        "handkerchief",
                        "burying",
                        "hagrid"
                    ],
                    [
                        "handkerchief",
                        "lily"
                    ],
                    [
                        "handkerchief",
                        "lily",
                        "james"
                    ],
                    [
                        "handkerchief",
                        "sad"
                    ],
                    [
                        "handkerchief",
                        "sad",
                        "grip"
                    ],
                    [
                        "handkerchief",
                        "stand"
                    ],
                    [
                        "handkerchief",
                        "stand",
                        "handkerchief"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "arms",
                        "turned"
                    ],
                    [
                        "harry",
                        "bent"
                    ],
                    [
                        "harry",
                        "bent",
                        "harry"
                    ],
                    [
                        "harry",
                        "blankets"
                    ],
                    [
                        "harry",
                        "blankets",
                        "came"
                    ],
                    [
                        "harry",
                        "dumbledore"
                    ],
                    [
                        "harry",
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "harry",
                        "gave"
                    ],
                    [
                        "harry",
                        "gave",
                        "scratchy"
                    ],
                    [
                        "harry",
                        "gently"
                    ],
                    [
                        "harry",
                        "gently",
                        "doorstep"
                    ],
                    [
                        "harry",
                        "great"
                    ],
                    [
                        "harry",
                        "great",
                        "shaggy"
                    ],
                    [
                        "harry",
                        "harry"
                    ],
                    [
                        "harry",
                        "harry",
                        "arms"
                    ],
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "harry",
                        "potter",
                        "lived"
                    ],
                    [
                        "harry",
                        "potter",
                        "rolled"
                    ],
                    [
                        "harry",
                        "sir"
                    ],
                    [
                        "harry",
                        "sir",
                        "asked"
                    ],
                    [
                        "harry",
                        "ter"
                    ],
                    [
                        "harry",
                        "ter",
                        "muggles"
                    ],
                    [
                        "held"
                    ],
                    [
                        "held",
                        "sign"
                    ],
                    [
                        "held",
                        "sign",
                        "another"
                    ],
                    [
                        "hissed"
                    ],
                    [
                        "hissed",
                        "professor"
                    ],
                    [
                        "hissed",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "holding"
                    ],
                    [
                        "holding",
                        "people"
                    ],
                    [
                        "holding",
                        "people",
                        "glasses"
                    ],
                    [
                        "hours"
                    ],
                    [
                        "hours",
                        "dursley"
                    ],
                    [
                        "hours",
                        "dursley",
                        "scream"
                    ],
                    [
                        "house"
                    ],
                    [
                        "hushed"
                    ],
                    [
                        "hushed",
                        "voices"
                    ],
                    [
                        "hushed",
                        "voices",
                        "harry"
                    ],
                    [
                        "inside"
                    ],
                    [
                        "inside",
                        "dumbledore"
                    ],
                    [
                        "inside",
                        "dumbledore",
                        "blankets"
                    ],
                    [
                        "inside",
                        "harry"
                    ],
                    [
                        "inside",
                        "harry",
                        "blankets"
                    ],
                    [
                        "james"
                    ],
                    [
                        "james",
                        "dead"
                    ],
                    [
                        "james",
                        "dead",
                        "poor"
                    ],
                    [
                        "kiss"
                    ],
                    [
                        "knowing"
                    ],
                    [
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "famous"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "special"
                    ],
                    [
                        "knowing",
                        "dumbledore",
                        "woken"
                    ],
                    [
                        "laid"
                    ],
                    [
                        "laid",
                        "harry"
                    ],
                    [
                        "laid",
                        "harry",
                        "gently"
                    ],
                    [
                        "large"
                    ],
                    [
                        "large",
                        "spotted"
                    ],
                    [
                        "large",
                        "spotted",
                        "handkerchief"
                    ],
                    [
                        "letter"
                    ],
                    [
                        "letter",
                        "beside"
                    ],
                    [
                        "letter",
                        "beside",
                        "dumbledore"
                    ],
                    [
                        "letter",
                        "dumbledore"
                    ],
                    [
                        "letter",
                        "dumbledore",
                        "cloak"
                    ],
                    [
                        "letter",
                        "inside"
                    ],
                    [
                        "letter",
                        "inside",
                        "harry"
                    ],
                    [
                        "lily"
                    ],
                    [
                        "lily",
                        "james"
                    ],
                    [
                        "lily",
                        "james",
                        "dead"
                    ],
                    [
                        "little"
                    ],
                    [
                        "little",
                        "harry"
                    ],
                    [
                        "little",
                        "harry",
                        "ter"
                    ],
                    [
                        "lived"
                    ],
                    [
                        "lived",
                        "house"
                    ],
                    [
                        "ll"
                    ],
                    [
                        "ll",
                        "professor"
                    ],
                    [
                        "ll",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "ll",
                        "wake"
                    ],
                    [
                        "ll",
                        "wake",
                        "muggles"
                    ],
                    [
                        "low"
                    ],
                    [
                        "low",
                        "garden"
                    ],
                    [
                        "low",
                        "garden",
                        "wall"
                    ],
                    [
                        "luck"
                    ],
                    [
                        "luck",
                        "harry"
                    ],
                    [
                        "luck",
                        "harry",
                        "dumbledore"
                    ],
                    [
                        "mcgonagall"
                    ],
                    [
                        "mcgonagall",
                        "ll"
                    ],
                    [
                        "mcgonagall",
                        "ll",
                        "wake"
                    ],
                    [
                        "mcgonagall",
                        "whispered"
                    ],
                    [
                        "mcgonagall",
                        "whispered",
                        "patting"
                    ],
                    [
                        "meeting"
                    ],
                    [
                        "meeting",
                        "secret"
                    ],
                    [
                        "meeting",
                        "secret",
                        "country"
                    ],
                    [
                        "milk"
                    ],
                    [
                        "milk",
                        "bottles"
                    ],
                    [
                        "milk",
                        "bottles",
                        "dumbledore"
                    ],
                    [
                        "moment"
                    ],
                    [
                        "moment",
                        "people"
                    ],
                    [
                        "moment",
                        "people",
                        "meeting"
                    ],
                    [
                        "muggles"
                    ],
                    [
                        "muggles",
                        "handkerchief"
                    ],
                    [
                        "muggles",
                        "handkerchief",
                        "sad"
                    ],
                    [
                        "muggles",
                        "sorry"
                    ],
                    [
                        "muggles",
                        "sorry",
                        "sobbed"
                    ],
                    [
                        "murmured"
                    ],
                    [
                        "next"
                    ],
                    [
                        "next",
                        "weeks"
                    ],
                    [
                        "next",
                        "weeks",
                        "prodded"
                    ],
                    [
                        "opened"
                    ],
                    [
                        "opened",
                        "front"
                    ],
                    [
                        "opened",
                        "front",
                        "door"
                    ],
                    [
                        "patting"
                    ],
                    [
                        "patting",
                        "hagrid"
                    ],
                    [
                        "patting",
                        "hagrid",
                        "gingerly"
                    ],
                    [
                        "people"
                    ],
                    [
                        "people",
                        "glasses"
                    ],
                    [
                        "people",
                        "glasses",
                        "saying"
                    ],
                    [
                        "people",
                        "meeting"
                    ],
                    [
                        "people",
                        "meeting",
                        "secret"
                    ],
                    [
                        "pinched"
                    ],
                    [
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "pinched",
                        "dumbledore",
                        "cousin"
                    ],
                    [
                        "poor"
                    ],
                    [
                        "poor",
                        "little"
                    ],
                    [
                        "poor",
                        "little",
                        "harry"
                    ],
                    [
                        "potter"
                    ],
                    [
                        "potter",
                        "lived"
                    ],
                    [
                        "potter",
                        "rolled"
                    ],
                    [
                        "potter",
                        "rolled",
                        "inside"
                    ],
                    [
                        "prodded"
                    ],
                    [
                        "prodded",
                        "pinched"
                    ],
                    [
                        "prodded",
                        "pinched",
                        "dumbledore"
                    ],
                    [
                        "professor"
                    ],
                    [
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "ll"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "whispered"
                    ],
                    [
                        "rolled"
                    ],
                    [
                        "rolled",
                        "inside"
                    ],
                    [
                        "rolled",
                        "inside",
                        "dumbledore"
                    ],
                    [
                        "room"
                    ],
                    [
                        "room",
                        "held"
                    ],
                    [
                        "room",
                        "held",
                        "sign"
                    ],
                    [
                        "sad"
                    ],
                    [
                        "sad",
                        "grip"
                    ],
                    [
                        "sad",
                        "grip",
                        "hagrid"
                    ],
                    [
                        "saying"
                    ],
                    [
                        "saying",
                        "hushed"
                    ],
                    [
                        "saying",
                        "hushed",
                        "voices"
                    ],
                    [
                        "scratchy"
                    ],
                    [
                        "scratchy",
                        "whiskery"
                    ],
                    [
                        "scratchy",
                        "whiskery",
                        "kiss"
                    ],
                    [
                        "scream"
                    ],
                    [
                        "scream",
                        "dursley"
                    ],
                    [
                        "scream",
                        "dursley",
                        "opened"
                    ],
                    [
                        "secret"
                    ],
                    [
                        "secret",
                        "country"
                    ],
                    [
                        "secret",
                        "country",
                        "holding"
                    ],
                    [
                        "shaggy"
                    ],
                    [
                        "shaggy",
                        "harry"
                    ],
                    [
                        "shaggy",
                        "harry",
                        "gave"
                    ],
                    [
                        "shhh"
                    ],
                    [
                        "shhh",
                        "hissed"
                    ],
                    [
                        "shhh",
                        "hissed",
                        "professor"
                    ],
                    [
                        "sign"
                    ],
                    [
                        "sign",
                        "another"
                    ],
                    [
                        "sign",
                        "another",
                        "lived"
                    ],
                    [
                        "sir"
                    ],
                    [
                        "sir",
                        "asked"
                    ],
                    [
                        "sir",
                        "asked",
                        "hagrid"
                    ],
                    [
                        "slept"
                    ],
                    [
                        "slept",
                        "knowing"
                    ],
                    [
                        "slept",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "small"
                    ],
                    [
                        "small",
                        "hand"
                    ],
                    [
                        "small",
                        "hand",
                        "closed"
                    ],
                    [
                        "sobbed"
                    ],
                    [
                        "sobbed",
                        "hagrid"
                    ],
                    [
                        "sobbed",
                        "hagrid",
                        "taking"
                    ],
                    [
                        "sorry"
                    ],
                    [
                        "sorry",
                        "sobbed"
                    ],
                    [
                        "sorry",
                        "sobbed",
                        "hagrid"
                    ],
                    [
                        "special"
                    ],
                    [
                        "special",
                        "knowing"
                    ],
                    [
                        "special",
                        "knowing",
                        "dumbledore"
                    ],
                    [
                        "spend"
                    ],
                    [
                        "spend",
                        "next"
                    ],
                    [
                        "spend",
                        "next",
                        "weeks"
                    ],
                    [
                        "spotted"
                    ],
                    [
                        "spotted",
                        "handkerchief"
                    ],
                    [
                        "spotted",
                        "handkerchief",
                        "burying"
                    ],
                    [
                        "stand"
                    ],
                    [
                        "stand",
                        "handkerchief"
                    ],
                    [
                        "stand",
                        "handkerchief",
                        "lily"
                    ],
                    [
                        "stepped"
                    ],
                    [
                        "stepped",
                        "low"
                    ],
                    [
                        "stepped",
                        "low",
                        "garden"
                    ],
                    [
                        "taking"
                    ],
                    [
                        "taking",
                        "large"
                    ],
                    [
                        "taking",
                        "large",
                        "spotted"
                    ],
                    [
                        "ter"
                    ],
                    [
                        "ter",
                        "muggles"
                    ],
                    [
                        "ter",
                        "muggles",
                        "handkerchief"
                    ],
                    [
                        "took"
                    ],
                    [
                        "took",
                        "harry"
                    ],
                    [
                        "took",
                        "harry",
                        "harry"
                    ],
                    [
                        "took",
                        "letter"
                    ],
                    [
                        "took",
                        "letter",
                        "dumbledore"
                    ],
                    [
                        "toward"
                    ],
                    [
                        "toward",
                        "dursley"
                    ],
                    [
                        "toward",
                        "dursley",
                        "dursley"
                    ],
                    [
                        "tucked"
                    ],
                    [
                        "tucked",
                        "letter"
                    ],
                    [
                        "tucked",
                        "letter",
                        "inside"
                    ],
                    [
                        "turned"
                    ],
                    [
                        "turned",
                        "toward"
                    ],
                    [
                        "turned",
                        "toward",
                        "dursley"
                    ],
                    [
                        "voices"
                    ],
                    [
                        "voices",
                        "harry"
                    ],
                    [
                        "voices",
                        "harry",
                        "potter"
                    ],
                    [
                        "wake"
                    ],
                    [
                        "wake",
                        "muggles"
                    ],
                    [
                        "wake",
                        "muggles",
                        "sorry"
                    ],
                    [
                        "waking"
                    ],
                    [
                        "walked"
                    ],
                    [
                        "walked",
                        "front"
                    ],
                    [
                        "walked",
                        "front",
                        "door"
                    ],
                    [
                        "wall"
                    ],
                    [
                        "wall",
                        "walked"
                    ],
                    [
                        "wall",
                        "walked",
                        "front"
                    ],
                    [
                        "weeks"
                    ],
                    [
                        "weeks",
                        "prodded"
                    ],
                    [
                        "weeks",
                        "prodded",
                        "pinched"
                    ],
                    [
                        "well"
                    ],
                    [
                        "well",
                        "dumbledore"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "hagrid"
                    ],
                    [
                        "whiskery"
                    ],
                    [
                        "whiskery",
                        "kiss"
                    ],
                    [
                        "whispered"
                    ],
                    [
                        "whispered",
                        "patting"
                    ],
                    [
                        "whispered",
                        "patting",
                        "hagrid"
                    ],
                    [
                        "without"
                    ],
                    [
                        "without",
                        "waking"
                    ],
                    [
                        "woken"
                    ],
                    [
                        "woken",
                        "hours"
                    ],
                    [
                        "woken",
                        "hours",
                        "dursley"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_5_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 5": {
        "Person Contexts and K-Seqs": [
            [
                "igor karkaroff",
                [
                    [
                        "angry"
                    ],
                    [
                        "armadillo"
                    ],
                    [
                        "armadillo",
                        "bile"
                    ],
                    [
                        "armadillo",
                        "bile",
                        "minutes"
                    ],
                    [
                        "armadillo",
                        "bile",
                        "minutes",
                        "go"
                    ],
                    [
                        "away"
                    ],
                    [
                        "away",
                        "class"
                    ],
                    [
                        "behind"
                    ],
                    [
                        "behind",
                        "harry"
                    ],
                    [
                        "behind",
                        "harry",
                        "cauldron"
                    ],
                    [
                        "behind",
                        "harry",
                        "cauldron",
                        "mop"
                    ],
                    [
                        "behind",
                        "snape"
                    ],
                    [
                        "behind",
                        "snape",
                        "desk"
                    ],
                    [
                        "behind",
                        "snape",
                        "desk",
                        "rest"
                    ],
                    [
                        "bell"
                    ],
                    [
                        "bell",
                        "gave"
                    ],
                    [
                        "bell",
                        "gave",
                        "harry"
                    ],
                    [
                        "bell",
                        "gave",
                        "harry",
                        "excuse"
                    ],
                    [
                        "bile"
                    ],
                    [
                        "bile",
                        "minutes"
                    ],
                    [
                        "bile",
                        "minutes",
                        "go"
                    ],
                    [
                        "bile",
                        "minutes",
                        "go",
                        "bell"
                    ],
                    [
                        "bottle"
                    ],
                    [
                        "bottle",
                        "armadillo"
                    ],
                    [
                        "bottle",
                        "armadillo",
                        "bile"
                    ],
                    [
                        "bottle",
                        "armadillo",
                        "bile",
                        "minutes"
                    ],
                    [
                        "cauldron"
                    ],
                    [
                        "cauldron",
                        "karkaroff"
                    ],
                    [
                        "cauldron",
                        "karkaroff",
                        "pull"
                    ],
                    [
                        "cauldron",
                        "karkaroff",
                        "pull",
                        "left"
                    ],
                    [
                        "cauldron",
                        "mop"
                    ],
                    [
                        "cauldron",
                        "mop",
                        "rest"
                    ],
                    [
                        "cauldron",
                        "mop",
                        "rest",
                        "class"
                    ],
                    [
                        "class"
                    ],
                    [
                        "class",
                        "moved"
                    ],
                    [
                        "class",
                        "moved",
                        "noisily"
                    ],
                    [
                        "class",
                        "moved",
                        "noisily",
                        "toward"
                    ],
                    [
                        "deliberately"
                    ],
                    [
                        "deliberately",
                        "knocked"
                    ],
                    [
                        "deliberately",
                        "knocked",
                        "harry"
                    ],
                    [
                        "deliberately",
                        "knocked",
                        "harry",
                        "bottle"
                    ],
                    [
                        "desk"
                    ],
                    [
                        "desk",
                        "rest"
                    ],
                    [
                        "desk",
                        "rest",
                        "double"
                    ],
                    [
                        "desk",
                        "rest",
                        "double",
                        "period"
                    ],
                    [
                        "door"
                    ],
                    [
                        "double"
                    ],
                    [
                        "double",
                        "period"
                    ],
                    [
                        "duck"
                    ],
                    [
                        "duck",
                        "behind"
                    ],
                    [
                        "duck",
                        "behind",
                        "harry"
                    ],
                    [
                        "duck",
                        "behind",
                        "harry",
                        "cauldron"
                    ],
                    [
                        "edge"
                    ],
                    [
                        "edge",
                        "harry"
                    ],
                    [
                        "edge",
                        "harry",
                        "cauldron"
                    ],
                    [
                        "edge",
                        "harry",
                        "cauldron",
                        "karkaroff"
                    ],
                    [
                        "effort"
                    ],
                    [
                        "effort",
                        "harry"
                    ],
                    [
                        "effort",
                        "harry",
                        "lips"
                    ],
                    [
                        "every"
                    ],
                    [
                        "every",
                        "effort"
                    ],
                    [
                        "every",
                        "effort",
                        "harry"
                    ],
                    [
                        "every",
                        "effort",
                        "harry",
                        "lips"
                    ],
                    [
                        "excuse"
                    ],
                    [
                        "excuse",
                        "duck"
                    ],
                    [
                        "excuse",
                        "duck",
                        "behind"
                    ],
                    [
                        "excuse",
                        "duck",
                        "behind",
                        "harry"
                    ],
                    [
                        "extremely"
                    ],
                    [
                        "extremely",
                        "worried"
                    ],
                    [
                        "extremely",
                        "worried",
                        "snape"
                    ],
                    [
                        "extremely",
                        "worried",
                        "snape",
                        "looked"
                    ],
                    [
                        "forearm"
                    ],
                    [
                        "gave"
                    ],
                    [
                        "gave",
                        "harry"
                    ],
                    [
                        "gave",
                        "harry",
                        "excuse"
                    ],
                    [
                        "gave",
                        "harry",
                        "excuse",
                        "duck"
                    ],
                    [
                        "go"
                    ],
                    [
                        "go",
                        "bell"
                    ],
                    [
                        "go",
                        "bell",
                        "gave"
                    ],
                    [
                        "go",
                        "bell",
                        "gave",
                        "harry"
                    ],
                    [
                        "hand"
                    ],
                    [
                        "hand",
                        "sleeve"
                    ],
                    [
                        "hand",
                        "sleeve",
                        "harry"
                    ],
                    [
                        "hand",
                        "sleeve",
                        "harry",
                        "robe"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "bottle"
                    ],
                    [
                        "harry",
                        "bottle",
                        "armadillo"
                    ],
                    [
                        "harry",
                        "bottle",
                        "armadillo",
                        "bile"
                    ],
                    [
                        "harry",
                        "cauldron"
                    ],
                    [
                        "harry",
                        "cauldron",
                        "karkaroff"
                    ],
                    [
                        "harry",
                        "cauldron",
                        "karkaroff",
                        "pull"
                    ],
                    [
                        "harry",
                        "cauldron",
                        "mop"
                    ],
                    [
                        "harry",
                        "cauldron",
                        "mop",
                        "rest"
                    ],
                    [
                        "harry",
                        "deliberately"
                    ],
                    [
                        "harry",
                        "deliberately",
                        "knocked"
                    ],
                    [
                        "harry",
                        "deliberately",
                        "knocked",
                        "harry"
                    ],
                    [
                        "harry",
                        "excuse"
                    ],
                    [
                        "harry",
                        "excuse",
                        "duck"
                    ],
                    [
                        "harry",
                        "excuse",
                        "duck",
                        "behind"
                    ],
                    [
                        "harry",
                        "heard"
                    ],
                    [
                        "harry",
                        "heard",
                        "snape"
                    ],
                    [
                        "harry",
                        "heard",
                        "snape",
                        "hiss"
                    ],
                    [
                        "harry",
                        "inner"
                    ],
                    [
                        "harry",
                        "inner",
                        "forearm"
                    ],
                    [
                        "harry",
                        "lips"
                    ],
                    [
                        "harry",
                        "peering"
                    ],
                    [
                        "harry",
                        "peering",
                        "edge"
                    ],
                    [
                        "harry",
                        "peering",
                        "edge",
                        "harry"
                    ],
                    [
                        "harry",
                        "robe"
                    ],
                    [
                        "harry",
                        "robe",
                        "snape"
                    ],
                    [
                        "harry",
                        "robe",
                        "snape",
                        "something"
                    ],
                    [
                        "heard"
                    ],
                    [
                        "heard",
                        "snape"
                    ],
                    [
                        "heard",
                        "snape",
                        "hiss"
                    ],
                    [
                        "heard",
                        "snape",
                        "hiss",
                        "karkaroff"
                    ],
                    [
                        "hiss"
                    ],
                    [
                        "hiss",
                        "karkaroff"
                    ],
                    [
                        "hovered"
                    ],
                    [
                        "hovered",
                        "behind"
                    ],
                    [
                        "hovered",
                        "behind",
                        "snape"
                    ],
                    [
                        "hovered",
                        "behind",
                        "snape",
                        "desk"
                    ],
                    [
                        "inner"
                    ],
                    [
                        "inner",
                        "forearm"
                    ],
                    [
                        "intent"
                    ],
                    [
                        "intent",
                        "preventing"
                    ],
                    [
                        "intent",
                        "preventing",
                        "snape"
                    ],
                    [
                        "intent",
                        "preventing",
                        "snape",
                        "slipping"
                    ],
                    [
                        "karkaroff"
                    ],
                    [
                        "karkaroff",
                        "harry"
                    ],
                    [
                        "karkaroff",
                        "harry",
                        "peering"
                    ],
                    [
                        "karkaroff",
                        "harry",
                        "peering",
                        "edge"
                    ],
                    [
                        "karkaroff",
                        "hovered"
                    ],
                    [
                        "karkaroff",
                        "hovered",
                        "behind"
                    ],
                    [
                        "karkaroff",
                        "hovered",
                        "behind",
                        "snape"
                    ],
                    [
                        "karkaroff",
                        "looked"
                    ],
                    [
                        "karkaroff",
                        "looked",
                        "extremely"
                    ],
                    [
                        "karkaroff",
                        "looked",
                        "extremely",
                        "worried"
                    ],
                    [
                        "karkaroff",
                        "making"
                    ],
                    [
                        "karkaroff",
                        "making",
                        "every"
                    ],
                    [
                        "karkaroff",
                        "making",
                        "every",
                        "effort"
                    ],
                    [
                        "karkaroff",
                        "pull"
                    ],
                    [
                        "karkaroff",
                        "pull",
                        "left"
                    ],
                    [
                        "karkaroff",
                        "pull",
                        "left",
                        "hand"
                    ],
                    [
                        "karkaroff",
                        "seemed"
                    ],
                    [
                        "karkaroff",
                        "seemed",
                        "intent"
                    ],
                    [
                        "karkaroff",
                        "seemed",
                        "intent",
                        "preventing"
                    ],
                    [
                        "karkaroff",
                        "wanted"
                    ],
                    [
                        "karkaroff",
                        "wanted",
                        "harry"
                    ],
                    [
                        "karkaroff",
                        "wanted",
                        "harry",
                        "deliberately"
                    ],
                    [
                        "keen"
                    ],
                    [
                        "keen",
                        "karkaroff"
                    ],
                    [
                        "keen",
                        "karkaroff",
                        "wanted"
                    ],
                    [
                        "keen",
                        "karkaroff",
                        "wanted",
                        "harry"
                    ],
                    [
                        "knocked"
                    ],
                    [
                        "knocked",
                        "harry"
                    ],
                    [
                        "knocked",
                        "harry",
                        "bottle"
                    ],
                    [
                        "knocked",
                        "harry",
                        "bottle",
                        "armadillo"
                    ],
                    [
                        "left"
                    ],
                    [
                        "left",
                        "hand"
                    ],
                    [
                        "left",
                        "hand",
                        "sleeve"
                    ],
                    [
                        "left",
                        "hand",
                        "sleeve",
                        "harry"
                    ],
                    [
                        "lips"
                    ],
                    [
                        "looked"
                    ],
                    [
                        "looked",
                        "angry"
                    ],
                    [
                        "looked",
                        "extremely"
                    ],
                    [
                        "looked",
                        "extremely",
                        "worried"
                    ],
                    [
                        "looked",
                        "extremely",
                        "worried",
                        "snape"
                    ],
                    [
                        "making"
                    ],
                    [
                        "making",
                        "every"
                    ],
                    [
                        "making",
                        "every",
                        "effort"
                    ],
                    [
                        "making",
                        "every",
                        "effort",
                        "harry"
                    ],
                    [
                        "minutes"
                    ],
                    [
                        "minutes",
                        "go"
                    ],
                    [
                        "minutes",
                        "go",
                        "bell"
                    ],
                    [
                        "minutes",
                        "go",
                        "bell",
                        "gave"
                    ],
                    [
                        "mop"
                    ],
                    [
                        "mop",
                        "rest"
                    ],
                    [
                        "mop",
                        "rest",
                        "class"
                    ],
                    [
                        "mop",
                        "rest",
                        "class",
                        "moved"
                    ],
                    [
                        "moved"
                    ],
                    [
                        "moved",
                        "noisily"
                    ],
                    [
                        "moved",
                        "noisily",
                        "toward"
                    ],
                    [
                        "moved",
                        "noisily",
                        "toward",
                        "door"
                    ],
                    [
                        "noisily"
                    ],
                    [
                        "noisily",
                        "toward"
                    ],
                    [
                        "noisily",
                        "toward",
                        "door"
                    ],
                    [
                        "peering"
                    ],
                    [
                        "peering",
                        "edge"
                    ],
                    [
                        "peering",
                        "edge",
                        "harry"
                    ],
                    [
                        "peering",
                        "edge",
                        "harry",
                        "cauldron"
                    ],
                    [
                        "period"
                    ],
                    [
                        "preventing"
                    ],
                    [
                        "preventing",
                        "snape"
                    ],
                    [
                        "preventing",
                        "snape",
                        "slipping"
                    ],
                    [
                        "preventing",
                        "snape",
                        "slipping",
                        "away"
                    ],
                    [
                        "pull"
                    ],
                    [
                        "pull",
                        "left"
                    ],
                    [
                        "pull",
                        "left",
                        "hand"
                    ],
                    [
                        "pull",
                        "left",
                        "hand",
                        "sleeve"
                    ],
                    [
                        "rest"
                    ],
                    [
                        "rest",
                        "class"
                    ],
                    [
                        "rest",
                        "class",
                        "moved"
                    ],
                    [
                        "rest",
                        "class",
                        "moved",
                        "noisily"
                    ],
                    [
                        "rest",
                        "double"
                    ],
                    [
                        "rest",
                        "double",
                        "period"
                    ],
                    [
                        "robe"
                    ],
                    [
                        "robe",
                        "snape"
                    ],
                    [
                        "robe",
                        "snape",
                        "something"
                    ],
                    [
                        "robe",
                        "snape",
                        "something",
                        "harry"
                    ],
                    [
                        "seemed"
                    ],
                    [
                        "seemed",
                        "intent"
                    ],
                    [
                        "seemed",
                        "intent",
                        "preventing"
                    ],
                    [
                        "seemed",
                        "intent",
                        "preventing",
                        "snape"
                    ],
                    [
                        "sleeve"
                    ],
                    [
                        "sleeve",
                        "harry"
                    ],
                    [
                        "sleeve",
                        "harry",
                        "robe"
                    ],
                    [
                        "sleeve",
                        "harry",
                        "robe",
                        "snape"
                    ],
                    [
                        "slipping"
                    ],
                    [
                        "slipping",
                        "away"
                    ],
                    [
                        "slipping",
                        "away",
                        "class"
                    ],
                    [
                        "snape"
                    ],
                    [
                        "snape",
                        "desk"
                    ],
                    [
                        "snape",
                        "desk",
                        "rest"
                    ],
                    [
                        "snape",
                        "desk",
                        "rest",
                        "double"
                    ],
                    [
                        "snape",
                        "hiss"
                    ],
                    [
                        "snape",
                        "hiss",
                        "karkaroff"
                    ],
                    [
                        "snape",
                        "looked"
                    ],
                    [
                        "snape",
                        "looked",
                        "angry"
                    ],
                    [
                        "snape",
                        "slipping"
                    ],
                    [
                        "snape",
                        "slipping",
                        "away"
                    ],
                    [
                        "snape",
                        "slipping",
                        "away",
                        "class"
                    ],
                    [
                        "snape",
                        "something"
                    ],
                    [
                        "snape",
                        "something",
                        "harry"
                    ],
                    [
                        "snape",
                        "something",
                        "harry",
                        "inner"
                    ],
                    [
                        "something"
                    ],
                    [
                        "something",
                        "harry"
                    ],
                    [
                        "something",
                        "harry",
                        "inner"
                    ],
                    [
                        "something",
                        "harry",
                        "inner",
                        "forearm"
                    ],
                    [
                        "toward"
                    ],
                    [
                        "toward",
                        "door"
                    ],
                    [
                        "urgent"
                    ],
                    [
                        "urgent",
                        "harry"
                    ],
                    [
                        "urgent",
                        "harry",
                        "heard"
                    ],
                    [
                        "urgent",
                        "harry",
                        "heard",
                        "snape"
                    ],
                    [
                        "wanted"
                    ],
                    [
                        "wanted",
                        "harry"
                    ],
                    [
                        "wanted",
                        "harry",
                        "deliberately"
                    ],
                    [
                        "wanted",
                        "harry",
                        "deliberately",
                        "knocked"
                    ],
                    [
                        "well"
                    ],
                    [
                        "well",
                        "karkaroff"
                    ],
                    [
                        "well",
                        "karkaroff",
                        "making"
                    ],
                    [
                        "well",
                        "karkaroff",
                        "making",
                        "every"
                    ],
                    [
                        "worried"
                    ],
                    [
                        "worried",
                        "snape"
                    ],
                    [
                        "worried",
                        "snape",
                        "looked"
                    ],
                    [
                        "worried",
                        "snape",
                        "looked",
                        "angry"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_5_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 5": {
        "Person Contexts and K-Seqs": [
            [
                "harry potter",
                [
                    [
                        "curtly"
                    ],
                    [
                        "door"
                    ],
                    [
                        "door",
                        "opened"
                    ],
                    [
                        "door",
                        "opened",
                        "harry"
                    ],
                    [
                        "door",
                        "opened",
                        "harry",
                        "harry"
                    ],
                    [
                        "door",
                        "opened",
                        "harry",
                        "harry",
                        "face"
                    ],
                    [
                        "face"
                    ],
                    [
                        "face",
                        "face"
                    ],
                    [
                        "face",
                        "face",
                        "professor"
                    ],
                    [
                        "face",
                        "face",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "face",
                        "professor"
                    ],
                    [
                        "face",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "footsteps"
                    ],
                    [
                        "footsteps",
                        "door"
                    ],
                    [
                        "footsteps",
                        "door",
                        "opened"
                    ],
                    [
                        "footsteps",
                        "door",
                        "opened",
                        "harry"
                    ],
                    [
                        "footsteps",
                        "door",
                        "opened",
                        "harry",
                        "harry"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "curtly"
                    ],
                    [
                        "harry",
                        "face"
                    ],
                    [
                        "harry",
                        "face",
                        "face"
                    ],
                    [
                        "harry",
                        "face",
                        "face",
                        "professor"
                    ],
                    [
                        "harry",
                        "face",
                        "face",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "harry",
                        "harry"
                    ],
                    [
                        "harry",
                        "harry",
                        "face"
                    ],
                    [
                        "harry",
                        "harry",
                        "face",
                        "face"
                    ],
                    [
                        "harry",
                        "harry",
                        "face",
                        "face",
                        "professor"
                    ],
                    [
                        "harry",
                        "heard"
                    ],
                    [
                        "harry",
                        "heard",
                        "footsteps"
                    ],
                    [
                        "harry",
                        "heard",
                        "footsteps",
                        "door"
                    ],
                    [
                        "harry",
                        "heard",
                        "footsteps",
                        "door",
                        "opened"
                    ],
                    [
                        "harry",
                        "knocked"
                    ],
                    [
                        "heard"
                    ],
                    [
                        "heard",
                        "footsteps"
                    ],
                    [
                        "heard",
                        "footsteps",
                        "door"
                    ],
                    [
                        "heard",
                        "footsteps",
                        "door",
                        "opened"
                    ],
                    [
                        "heard",
                        "footsteps",
                        "door",
                        "opened",
                        "harry"
                    ],
                    [
                        "knocked"
                    ],
                    [
                        "mcgonagall"
                    ],
                    [
                        "opened"
                    ],
                    [
                        "opened",
                        "harry"
                    ],
                    [
                        "opened",
                        "harry",
                        "harry"
                    ],
                    [
                        "opened",
                        "harry",
                        "harry",
                        "face"
                    ],
                    [
                        "opened",
                        "harry",
                        "harry",
                        "face",
                        "face"
                    ],
                    [
                        "professor"
                    ],
                    [
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "urgent"
                    ],
                    [
                        "urgent",
                        "harry"
                    ],
                    [
                        "urgent",
                        "harry",
                        "curtly"
                    ]
                ]
            ],
            [
                "malcolm mcgonagall",
                [
                    [
                        "alarmingly"
                    ],
                    [
                        "door"
                    ],
                    [
                        "door",
                        "opened"
                    ],
                    [
                        "door",
                        "opened",
                        "harry"
                    ],
                    [
                        "door",
                        "opened",
                        "harry",
                        "harry"
                    ],
                    [
                        "door",
                        "opened",
                        "harry",
                        "harry",
                        "face"
                    ],
                    [
                        "face"
                    ],
                    [
                        "face",
                        "face"
                    ],
                    [
                        "face",
                        "face",
                        "professor"
                    ],
                    [
                        "face",
                        "face",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "face",
                        "professor"
                    ],
                    [
                        "face",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "flashing"
                    ],
                    [
                        "flashing",
                        "alarmingly"
                    ],
                    [
                        "footsteps"
                    ],
                    [
                        "footsteps",
                        "door"
                    ],
                    [
                        "footsteps",
                        "door",
                        "opened"
                    ],
                    [
                        "footsteps",
                        "door",
                        "opened",
                        "harry"
                    ],
                    [
                        "footsteps",
                        "door",
                        "opened",
                        "harry",
                        "harry"
                    ],
                    [
                        "harry"
                    ],
                    [
                        "harry",
                        "face"
                    ],
                    [
                        "harry",
                        "face",
                        "face"
                    ],
                    [
                        "harry",
                        "face",
                        "face",
                        "professor"
                    ],
                    [
                        "harry",
                        "face",
                        "face",
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "harry",
                        "harry"
                    ],
                    [
                        "harry",
                        "harry",
                        "face"
                    ],
                    [
                        "harry",
                        "harry",
                        "face",
                        "face"
                    ],
                    [
                        "harry",
                        "harry",
                        "face",
                        "face",
                        "professor"
                    ],
                    [
                        "harry",
                        "heard"
                    ],
                    [
                        "harry",
                        "heard",
                        "footsteps"
                    ],
                    [
                        "harry",
                        "heard",
                        "footsteps",
                        "door"
                    ],
                    [
                        "harry",
                        "heard",
                        "footsteps",
                        "door",
                        "opened"
                    ],
                    [
                        "heard"
                    ],
                    [
                        "heard",
                        "footsteps"
                    ],
                    [
                        "heard",
                        "footsteps",
                        "door"
                    ],
                    [
                        "heard",
                        "footsteps",
                        "door",
                        "opened"
                    ],
                    [
                        "heard",
                        "footsteps",
                        "door",
                        "opened",
                        "harry"
                    ],
                    [
                        "mcgonagall"
                    ],
                    [
                        "mcgonagall",
                        "mcgonagall"
                    ],
                    [
                        "mcgonagall",
                        "mcgonagall",
                        "square"
                    ],
                    [
                        "mcgonagall",
                        "mcgonagall",
                        "square",
                        "spectacles"
                    ],
                    [
                        "mcgonagall",
                        "mcgonagall",
                        "square",
                        "spectacles",
                        "flashing"
                    ],
                    [
                        "mcgonagall",
                        "square"
                    ],
                    [
                        "mcgonagall",
                        "square",
                        "spectacles"
                    ],
                    [
                        "mcgonagall",
                        "square",
                        "spectacles",
                        "flashing"
                    ],
                    [
                        "mcgonagall",
                        "square",
                        "spectacles",
                        "flashing",
                        "alarmingly"
                    ],
                    [
                        "opened"
                    ],
                    [
                        "opened",
                        "harry"
                    ],
                    [
                        "opened",
                        "harry",
                        "harry"
                    ],
                    [
                        "opened",
                        "harry",
                        "harry",
                        "face"
                    ],
                    [
                        "opened",
                        "harry",
                        "harry",
                        "face",
                        "face"
                    ],
                    [
                        "professor"
                    ],
                    [
                        "professor",
                        "mcgonagall"
                    ],
                    [
                        "spectacles"
                    ],
                    [
                        "spectacles",
                        "flashing"
                    ],
                    [
                        "spectacles",
                        "flashing",
                        "alarmingly"
                    ],
                    [
                        "square"
                    ],
                    [
                        "square",
                        "spectacles"
                    ],
                    [
                        "square",
                        "spectacles",
                        "flashing"
                    ],
                    [
                        "square",
                        "spectacles",
                        "flashing",
                        "alarmingly"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_5_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 5": {
        "Person Contexts and K-Seqs": []
    }
}'''


# CONSTANT FOR TASK 6 UNPROCESSED FLOW TEST

TASK_6_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
    "Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
    ` Is that where-?` whispered Professor  McGonagall.
    "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
    Scars can come in handy.
    I have one myself above my left knee that is a perfect map of the London Underground.
    "Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
    "` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
    "Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
    "Then, suddenly,  Hagrid let out a howl like a wounded dog."
    "` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
    "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
    "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
    "` Well,` said  Dumbledore finally,` that's that."
    We've no business staying here.
    "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
    "` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
    Professor  McGonagall blew  McGonagall nose in reply.
    Dumbledore turned and walked back down the street.
    On the corner  Dumbledore stopped and took out the silver Put- Outer.
    "Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
    Dumbledore could just see the bundle of blankets on the step of number four.
    "` Good luck,  Harry,`  Dumbledore murmured."
    "Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
    "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
    Harry  Potter rolled over inside  Dumbledore blankets without waking up.
    "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
    "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
    "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
    Only the photographs on the mantelpiece really showed how much time had passed.
    "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
    "The room held no sign at all that another boy lived in the house, too."
    """
TASK_6_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
    "Karkaroff looked extremely worried, and  Snape looked angry."
    Karkaroff hovered behind  Snape's desk for the rest of the double period.
    Karkaroff seemed intent on preventing  Snape from slipping away at the end of class.
    "Keen to hear what Karkaroff wanted to say,  Harry deliberately knocked over  Harry bottle of armadillo bile with two minutes to go to the bell, which gave  Harry an excuse to duck down behind  Harry cauldron and mop up while the rest of the class moved noisily toward the door."
    ` What's so urgent?`  Harry heard  Snape hiss at Karkaroff.
    "` This,` said Karkaroff, and  Harry, peering around the edge of  Harry cauldron, saw Karkaroff  pull up the left- hand sleeve of  Harry robe and show  Snape something on  Harry inner forearm."
    "` Well?` said Karkaroff, still making every effort not to move  Harry lips.` Do you see?"
    the boy
    """
TASK_6_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
    "This is urgent,' said  Harry curtly.   '"
    "Ooooh, urgent, is This?'"
    said the other gargoyle in a high- pitched voice.'
    "Well, that's put us in our place, hasn't that?'"
    Harry knocked.
    "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
    You haven't been given another detention!'
    "McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
    "Aaaaaand- Lynch!`   Seven green blurs swept onto the field;  Harry spun a small dial on the side of  Harry Omnioculars and slowed the players down enough to read the word` Firebolt` on each of players brooms and see players names, embroidered in silver, upon players backs."
    "` And here, all the way from Egypt, our referee, acclaimed Chairwizard of the International Association of Quidditch,   Hassan Mostafa!`  A small and skinny wizard, completely bald but with a mustache to rival Uncle  Vernon's, wearing robes of pure gold to match the stadium, strode out onto the field."
    "A silver whistle was protruding from under the mustache, and  Vernon was carrying a large wooden crate under one arm,  Vernon broomstick under the other."
    "Harry spun the speed dial on  Vernon Omnioculars back to normal, watching closely as   Hassan Mostafa mounted  Vernon broomstick and kicked the crate open- four balls burst into the air: the scarlet Quaffle, the two black Bludgers, and(  Harry saw Quaffle for the briefest moment, before Quaffle sped out of sight) the minuscule, winged Golden Snitch."
    "With a sharp blast on  Vernon whistle,   Hassan Mostafa shot into the air after the balls."
    `Theeeeeeeey're OFF!` screamed  Bagman.` And air's  Mullet!
    "Stewart Ackerley took off the hat and hurried into a seat at the Ravenclaw table, where everyone was applauding boy."
    "Harry caught a glimpse of  Cho, the Ravenclaw Seeker, cheering   Stewart Ackerley as boy sat down."
    "For a fleeting second,  Harry had a strange desire to join the Ravenclaw table too."
    "` Baddock,  Malcolm!` ` SLYTHERIN!`  The table on the other side of the hall erupted with cheers;  Harry could see  Malfoy clapping as Baddock joined the Slytherins."
    Harry wondered whether Baddock knew that Slytherin House had turned out more Dark witches and wizards than any other.
    Fred and  George hissed   Malcolm Baddock as  Fred sat down.
    "`  Branstone,  Eleanor!` ` HUFFLEPUFF!` ` Cauldwell,  Owen!` ` HUFFLEPUFF!` ` Creevey, Dennis!`  Tiny  Dennis Creevey staggered forward, tripping over   Hagrid's moleskin, just as  Hagrid  Hagrid sidled into the Hall through a door behind the teachers' table."
    "About twice as tall as a normal man, and at least three times as broad,  Hagrid, with  Hagrid long, wild, tangled black hair and beard, looked slightly alarming- a misleading impression, for  Harry,  Ron, and  Hermione knew  Hagrid to possess a very kind nature."
    Hagrid winked at Harry and  Ron and  Hermione as  Hagrid sat down at the end of the staff table and watched  Dennis Creevey putting on the   Sorting Hat.
    The rip at the brim openedwide---` GRYFFINDOR!` the hat shouted.
    "Hagrid clapped along with the Gryffindors as  Dennis Creevey, beaming widely, took off the hat, placed hat back on the stool, and hurried over to join  Dennis Creevey brother."
    "`  Colin, I fell in!`  Dennis Creevey said shrilly, throwing  Dennis Creevey into an empty seat.` seat was brilliant!"
    "And something in the water grabbed me and pushed me back in the boat!` ` Cool!` said  Colin, just as excitedly.` seat was probably the giant squid, Dennis!` ` Wow!` said Dennis, as though nobody in nobody wildest dreams could hope for more than being thrown into a storm- tossed, fathoms- deep lake, and pushed out of lake again by a giant sea monster."
    ` Dennis!
    Dennis!
    See that boy down there?
    The one with the black hair and glasses?
    See boy?
    """
TASK_6_EXAMPLE_4_SENTENCES_CSV_RAW = """sentence
    "This is urgent,' said  Harry curtly.   '"
    "Ooooh, urgent, is This?'"
    said the other gargoyle in a high- pitched voice.'
    "Well, that's put us in our place, hasn't that?'"
    Harry knocked.
    "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
    You haven't been given another detention!'
    "McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
    No... not exactly...` said  Hermione slowly.'
    More... wondering...
    I suppose we're doing the right thing...
    I think... aren't     Harry and  Ron looked at each other.   '
    "Well, that clears that up,' said  Ron.'"
    It would've been really annoying if you hadn't explained yourself properly.'
    Hermione looked at  Ron as though  Hermione had only just realised  Ron was there.   '
    "I was just wondering,'  Hermione said,  Hermione voice stronger now,' whether we're doing the right thing, starting this Defence Against the Dark Arts group.'"
    ' What?'
    said  Harry and  Ron together.   '
    "Hermione, group was your idea in the first place!'"
    said  Ron indignantly.   '
    "I know,' said  Hermione, twisting  Hermione fingers together.'"
    "But after talking to  Snuffles...'   ' But  Snuffles's all for group,' said  Harry.   '"
    "Yes,' said  Hermione, staring at the window again.'"
    "Yes, that's what made me think maybe that wasn't a good idea after all...'     Peeves floated over fingers on  Peeves stomach, peashooter at the ready; automatically all three of fingers lifted fingers bags to cover fingers heads until  Peeves had passed.   '"
    "Let's get this straight,' said  Harry angrily, as fingers put fingers bags back on the floor,'  Sirius agrees with us, so you don't think we should do floor any more?'"
    Hermione looked tense and rather miserable.
    "Now staring at  Hermione own hands,  Hermione said,' Do you honestly trust  Sirius judgement?'"
    "' Yes, I do!'"
    said  Harry at once.'
    Sirius's always given us great advice!'
    "An ink pellet whizzed past hands, striking   Katie Bell squarely in the ear."
    Hermione watched  Katie leap to  Katie feet and start throwing things at  Peeves; it was a few moments before  Hermione spoke again and pellet sounded as though  Hermione was choosing  Hermione words very carefully.   '
    You don't think  Peeves has become... sort of... reckless... since  Peeves's been cooped up in Grimmauld Place?
    You don't think  Peeves's... kind of... living through us?'
    "' Whatd'you mean,` living through us`?'"
    Harry retorted.   '
    "I mean... well, I think  Harry'd love to be forming secret Defence societies right under the nose of someone from the Ministry..."
    I think  Harry's really frustrated at how little  Harry can do where  Harry is... so I think  Harry's keen to kind of... egg us on.'
    Ron looked utterly perplexed.   '
    "Sirius is right,'  Harry said,' you do sound just like my mother.'"
    Hermione bit  Hermione lip and did not answer.
    The bell rang just as  Peeves swooped down on  Katie and emptied an entire ink bottle over  Hermione head.
    "*The weather did not improve as the day wore on, so that at seveno'clock that evening, when  Harry and  Ron went down to the Quidditch pitch for practice, Harry and  Ron were soaked through within minutes, Harry and  Ron feet slipping and sliding on the sodden grass."
    "The sky was a deep, thundery grey and it was a relief to gain the warmth and light of the changing rooms, even if relief knew the respite was only temporary."
    I'll get yer an owl.
    "All the kids want owls, kids're dead useful, carry yer mail an' everythin'.`  Twenty minutes later, kids left Eeylops Owl Emporium, which had been dark and full of rustling and flickering, jewel- bright eyes."
    "Harry now carried a large cage that held a beautiful snowy owl, fast asleep with owl head under owl wing."
    "Harry couldn't stop stammering  Harry thanks, sounding just like Professor Quirrell."
    "` Don' mention cage,` said  Hagrid gruffly.` Don' expect you've had a lotta presents from a   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley."
    "Just Ollivanders left now- only place fer wands, Ollivanders, and yeh got ta have the best wand.`  A magic wand... this was what  Harry had been really looking forward to."
    The last shop was narrow and shabby.
    Peeling gold letters over the door read Ollivanders: Makers of Fine Wands since 382 B.C.
    A single wand lay on a faded purple cushion in the dusty window.
    A tinkling bell rang somewhere in the depths of the shop as depths stepped inside.
    "bell was a tiny place, empty except for a single, spindly chair that  Hagrid sat on to wait."
    Harry felt strangely as though  Harry had entered a very strict library;  Harry swallowed a lot of new questions that had just occurred to  Harry and looked instead at the thousands of narrow boxes piled neatly right up to the ceiling.
    "For some reason, the back of  Harry neck prickled."
    The very dust and silence in here seemed to tingle with some secret magic.
    "` Good afternoon,` said a soft voice."
    "All right, we'll take you to King's Cross."
    "We're going up to London tomorrow anyway, or I wouldn't bother.` ` Why are you going to London?`  Harry asked, trying to keep things friendly."
    "` Taking   Dudley to the hospital,` growled Uncle  Vernon.` Got to have that ruddy tail removed before  Vernon goes to Smeltings.`   Harry woke at fiveo'clock the next morning and was too excited and nervous to go back to sleep."
    Vernon got up and pulled on  Vernon jeans because  Vernon didn't want to walk into the station in  Vernon wizard's robes--  Vernon'd change on the train.
    "Vernon checked  Vernon Hogwarts list yet again to make sure  Vernon had everything  Vernon needed, saw that  Hedwig was shut safely in  Hedwig cage, and then paced the room, waiting for the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley to get up."
    "Two hours later,  Harry's huge, heavy trunk had been loaded into the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' car,  Aunt  Petunia had talked   Dudley into sitting next to  Harry, and   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had set off."
    Mr. Dursley and   Mrs. Dursley and    Dudley Dursley reached King's Cross at half past ten.
    Uncle  Vernon dumped  Harry's trunk onto a cart and wheeled trunk into the station for  Harry.
    "Harry thought this was strangely kind until Uncle  Vernon stopped dead, facing the  platforms with a nasty grin on  Harry face."
    """

TASK_6_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
    Over-Attentive Wizard,
    Bertram Aubrey,
    Audrey Weasley,
    "Augusta ""Gran"" Longbottom",
    Augustus Pye,
    Augustus Rookwood,
    Augustus Worme,
    Auntie Muriel,
    Aunt Marge Dursley,
    Aurelius Dumbledore,
    Aurora Sinistra,
    Avery,
    Babajide Akingbade,
    Babayaga,
    Babbitty Rabbitty,
    Bagman Sr.,
    Ludo Bagman,
    Otto Bagman,
    Millicent Bagnold,
    Bathilda Bagshot,Batty
    Kquewanda Bailey,
    Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
    Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
    Aberforth Dumbledore,
    """
TASK_6_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
    Ignatia Wildsmith,
    Ignatius Prewett,
    Ignatius Tuft,
    Ignotus Peverell,
    Igor Karkaroff,
    Illyius,
    Ingolfr the Iambic,
    """
TASK_6_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
    "Magnus ""Dent Head"" Macdonald",
    Magorian,
    Maisie Cattermole,
    Malcolm,
    Malcolm Baddock,
    Malcolm McGonagall,
    Harold Skively,
    Harper,
    Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
    Harvey Ridgebit,
    Hassan Mostafa,
    Gwenog,
    Gwenog Jones,
    Hagrid's father,
    Hambledon Quince,
    Hamish MacFarlan,
    Hankerton Humble,
    """
TASK_6_EXAMPLE_4_NAMES_CSV_RAW = """Name,Other Names
    Abernathy,
    Abraham Peasegood,
    Abraham Potter,
    Abraxas Malfoy,
    Achilles Tolliver,
    Stewart Ackerley,
    Mrs. Granger,
    Hermione Granger,
    Hugo Granger-Weasley,
    Rose Granger-Weasley,
    Granville Jorkins,
    Gondulphus Graves,
    Merton Graves,
    Percival Graves,
    Grawp,
    Irma Pince,
    Irving Warble,
    Isadora Rose,
    Isobel McGonagall,
    Isobel Ross,
    Isolt Sayre,"morrigan, elias story"
    Ivanova,
    Ivan Popa,
    Harold Minchum,
    Harold Skively,
    Harper,
    Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
    Harvey Ridgebit,
    Hassan Mostafa,
    Havelock Sweeting,
    Hector Lamont,
    Hedwig,
    Helena Ravenclaw,
    Verity,
    Vernon Dudley,
    Veronica Smethley,
    """


TASK_6_EXAMPLE_1_WINDOW_SIZE = 4
TASK_6_EXAMPLE_2_WINDOW_SIZE = 3
TASK_6_EXAMPLE_3_WINDOW_SIZE = 5
TASK_6_EXAMPLE_4_WINDOW_SIZE = 5

TASK_6_EXAMPLE_1_TRESHOLD = 4
TASK_6_EXAMPLE_2_TRESHOLD = 2
TASK_6_EXAMPLE_3_TRESHOLD = 2
TASK_6_EXAMPLE_4_TRESHOLD = 1

TASK_6_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = """{
        "Question 6": {
            "Pair Matches": [
                [
                    [
                        "aberforth",
                        "dumbledore"
                    ],
                    [
                        "aunt",
                        "marge",
                        "dursley"
                    ]
                ],
                [
                    [
                        "aberforth",
                        "dumbledore"
                    ],
                    [
                        "aurelius",
                        "dumbledore"
                    ]
                ],
                [
                    [
                        "aberforth",
                        "dumbledore"
                    ],
                    [
                        "harry",
                        "potter"
                    ]
                ],
                [
                    [
                        "aunt",
                        "marge",
                        "dursley"
                    ],
                    [
                        "aurelius",
                        "dumbledore"
                    ]
                ],
                [
                    [
                        "aunt",
                        "marge",
                        "dursley"
                    ],
                    [
                        "harry",
                        "potter"
                    ]
                ],
                [
                    [
                        "aurelius",
                        "dumbledore"
                    ],
                    [
                        "harry",
                        "potter"
                    ]
                ]
            ]
        }
    }"""
TASK_6_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = """{
        "Question 6": {
            "Pair Matches": []
        }
    }"""
TASK_6_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = """{
        "Question 6": {
            "Pair Matches": [
                [
                    [
                        "hagrid",
                        "father"
                    ],
                    [
                        "harry",
                        "potter"
                    ]
                ],
                [
                    [
                        "hagrid",
                        "father"
                    ],
                    [
                        "malcolm"
                    ]
                ],
                [
                    [
                        "hagrid",
                        "father"
                    ],
                    [
                        "malcolm",
                        "baddock"
                    ]
                ],
                [
                    [
                        "hagrid",
                        "father"
                    ],
                    [
                        "malcolm",
                        "mcgonagall"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "hassan",
                        "mostafa"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "malcolm"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "malcolm",
                        "baddock"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "malcolm",
                        "mcgonagall"
                    ]
                ],
                [
                    [
                        "hassan",
                        "mostafa"
                    ],
                    [
                        "malcolm",
                        "mcgonagall"
                    ]
                ],
                [
                    [
                        "malcolm"
                    ],
                    [
                        "malcolm",
                        "baddock"
                    ]
                ],
                [
                    [
                        "malcolm"
                    ],
                    [
                        "malcolm",
                        "mcgonagall"
                    ]
                ],
                [
                    [
                        "malcolm",
                        "baddock"
                    ],
                    [
                        "malcolm",
                        "mcgonagall"
                    ]
                ]
            ]
        }
    }
    """
TASK_6_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW = """{
        "Question 6": {
            "Pair Matches": [
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "hedwig"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "hermione",
                        "granger"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "isobel",
                        "mcgonagall"
                    ]
                ],
                [
                    [
                        "harry",
                        "potter"
                    ],
                    [
                        "vernon",
                        "dudley"
                    ]
                ],
                [
                    [
                        "hedwig"
                    ],
                    [
                        "vernon",
                        "dudley"
                    ]
                ],
                [
                    [
                        "hermione",
                        "granger"
                    ],
                    [
                        "isobel",
                        "mcgonagall"
                    ]
                ]
            ]
        }
    }
    """


# CONSTANT FOR TASK 7 UNPROCESSED FLOW TEST

TASK_7_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
    "Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
    ` Is that where-?` whispered Professor  McGonagall.
    "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
    Scars can come in handy.
    I have one myself above my left knee that is a perfect map of the London Underground.
    "Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
    "` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
    "Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
    "Then, suddenly,  Hagrid let out a howl like a wounded dog."
    "` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
    "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
    "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
    "` Well,` said  Dumbledore finally,` that's that."
    We've no business staying here.
    "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
    "` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
    Professor  McGonagall blew  McGonagall nose in reply.
    Dumbledore turned and walked back down the street.
    On the corner  Dumbledore stopped and took out the silver Put- Outer.
    "Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
    Dumbledore could just see the bundle of blankets on the step of number four.
    "` Good luck,  Harry,`  Dumbledore murmured."
    "Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
    "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
    Harry  Potter rolled over inside  Dumbledore blankets without waking up.
    "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
    "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
    "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
    Only the photographs on the mantelpiece really showed how much time had passed.
    "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
    "The room held no sign at all that another boy lived in the house, too."
    """
TASK_7_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
    "Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
    ` Is that where-?` whispered Professor  McGonagall.
    "` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
    Scars can come in handy.
    I have one myself above my left knee that is a perfect map of the London Underground.
    "Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
    "` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
    "Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
    "Then, suddenly,  Hagrid let out a howl like a wounded dog."
    "` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
    "Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
    "For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
    "` Well,` said  Dumbledore finally,` that's that."
    We've no business staying here.
    "We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
    "` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
    Professor  McGonagall blew  McGonagall nose in reply.
    Dumbledore turned and walked back down the street.
    On the corner  Dumbledore stopped and took out the silver Put- Outer.
    "Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
    Dumbledore could just see the bundle of blankets on the step of number four.
    "` Good luck,  Harry,`  Dumbledore murmured."
    "Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
    "A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
    Harry  Potter rolled over inside  Dumbledore blankets without waking up.
    "One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
    "THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
    "The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
    Only the photographs on the mantelpiece really showed how much time had passed.
    "Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
    asdf asdf asdf asdf filler sentence asdf ddfdf dfdfdf asdfasdf dkdkdkdk
    asdf Otto asdf asdf filler sentence asdf ddfdf dfdfdf asdfasdf dkdkdkdk
    asdf asdf harry asdf filler sentence asdf ddfdf dfdfdf asdfasdf dkdkdkdk
    asdf asdf asdf asdf filler sentence asdf ddfdf dfdfdf asdfasdf dkdkdkdk
    """
TASK_7_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
"This is urgent,' said  Harry curtly.   '"
"Ooooh, urgent, is This?'"
said the other gargoyle in a high- pitched voice.'
"Well, that's put us in our place, hasn't that?'"
Harry knocked.
"Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
You haven't been given another detention!'
"McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
"Aaaaaand- Lynch!`   Seven green blurs swept onto the field;  Harry spun a small dial on the side of  Harry Omnioculars and slowed the players down enough to read the word` Firebolt` on each of players brooms and see players names, embroidered in silver, upon players backs."
"` And here, all the way from Egypt, our referee, acclaimed Chairwizard of the International Association of Quidditch,   Hassan Mostafa!`  A small and skinny wizard, completely bald but with a mustache to rival Uncle  Vernon's, wearing robes of pure gold to match the stadium, strode out onto the field."
"A silver whistle was protruding from under the mustache, and  Vernon was carrying a large wooden crate under one arm,  Vernon broomstick under the other."
"Harry spun the speed dial on  Vernon Omnioculars back to normal, watching closely as   Hassan Mostafa mounted  Vernon broomstick and kicked the crate open- four balls burst into the air: the scarlet Quaffle, the two black Bludgers, and(  Harry saw Quaffle for the briefest moment, before Quaffle sped out of sight) the minuscule, winged Golden Snitch."
"With a sharp blast on  Vernon whistle,   Hassan Mostafa shot into the air after the balls."
`Theeeeeeeey're OFF!` screamed  Bagman.` And air's  Mullet!
"Stewart Ackerley took off the hat and hurried into a seat at the Ravenclaw table, where everyone was applauding boy."
"Harry caught a glimpse of  Cho, the Ravenclaw Seeker, cheering   Stewart Ackerley as boy sat down."
"For a fleeting second,  Harry had a strange desire to join the Ravenclaw table too."
"` Baddock,  Malcolm!` ` SLYTHERIN!`  The table on the other side of the hall erupted with cheers;  Harry could see  Malfoy clapping as Baddock joined the Slytherins."
Harry wondered whether Baddock knew that Slytherin House had turned out more Dark witches and wizards than any other.
Fred and  George hissed   Malcolm Baddock as  Fred sat down.
"`  Branstone,  Eleanor!` ` HUFFLEPUFF!` ` Cauldwell,  Owen!` ` HUFFLEPUFF!` ` Creevey, Dennis!`  Tiny  Dennis Creevey staggered forward, tripping over   Hagrid's moleskin, just as  Hagrid  Hagrid sidled into the Hall through a door behind the teachers' table."
"About twice as tall as a normal man, and at least three times as broad,  Hagrid, with  Hagrid long, wild, tangled black hair and beard, looked slightly alarming- a misleading impression, for  Harry,  Ron, and  Hermione knew  Hagrid to possess a very kind nature."
Hagrid winked at Harry and  Ron and  Hermione as  Hagrid sat down at the end of the staff table and watched  Dennis Creevey putting on the   Sorting Hat.
The rip at the brim openedwide---` GRYFFINDOR!` the hat shouted.
"Hagrid clapped along with the Gryffindors as  Dennis Creevey, beaming widely, took off the hat, placed hat back on the stool, and hurried over to join  Dennis Creevey brother."
"`  Colin, I fell in!`  Dennis Creevey said shrilly, throwing  Dennis Creevey into an empty seat.` seat was brilliant!"
"And something in the water grabbed me and pushed me back in the boat!` ` Cool!` said  Colin, just as excitedly.` seat was probably the giant squid, Dennis!` ` Wow!` said Dennis, as though nobody in nobody wildest dreams could hope for more than being thrown into a storm- tossed, fathoms- deep lake, and pushed out of lake again by a giant sea monster."
` Dennis!
Dennis!
See that boy down there?
The one with the black hair and glasses?
See boy?
"""
TASK_7_EXAMPLE_4_SENTENCES_CSV_RAW = """sentence
"This is urgent,' said  Harry curtly.   '"
"Ooooh, urgent, is This?'"
said the other gargoyle in a high- pitched voice.'
"Well, that's put us in our place, hasn't that?'"
Harry knocked.
"Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '"
You haven't been given another detention!'
"McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '"
No... not exactly...` said  Hermione slowly.'
More... wondering...
I suppose we're doing the right thing...
I think... aren't     Harry and  Ron looked at each other.   '
"Well, that clears that up,' said  Ron.'"
It would've been really annoying if you hadn't explained yourself properly.'
Hermione looked at  Ron as though  Hermione had only just realised  Ron was there.   '
"I was just wondering,'  Hermione said,  Hermione voice stronger now,' whether we're doing the right thing, starting this Defence Against the Dark Arts group.'"
' What?'
said  Harry and  Ron together.   '
"Hermione, group was your idea in the first place!'"
said  Ron indignantly.   '
"I know,' said  Hermione, twisting  Hermione fingers together.'"
"But after talking to  Snuffles...'   ' But  Snuffles's all for group,' said  Harry.   '"
"Yes,' said  Hermione, staring at the window again.'"
"Yes, that's what made me think maybe that wasn't a good idea after all...'     Peeves floated over fingers on  Peeves stomach, peashooter at the ready; automatically all three of fingers lifted fingers bags to cover fingers heads until  Peeves had passed.   '"
"Let's get this straight,' said  Harry angrily, as fingers put fingers bags back on the floor,'  Sirius agrees with us, so you don't think we should do floor any more?'"
Hermione looked tense and rather miserable.
"Now staring at  Hermione own hands,  Hermione said,' Do you honestly trust  Sirius judgement?'"
"' Yes, I do!'"
said  Harry at once.'
Sirius's always given us great advice!'
"An ink pellet whizzed past hands, striking   Katie Bell squarely in the ear."
Hermione watched  Katie leap to  Katie feet and start throwing things at  Peeves; it was a few moments before  Hermione spoke again and pellet sounded as though  Hermione was choosing  Hermione words very carefully.   '
You don't think  Peeves has become... sort of... reckless... since  Peeves's been cooped up in Grimmauld Place?
You don't think  Peeves's... kind of... living through us?'
"' Whatd'you mean,` living through us`?'"
Harry retorted.   '
"I mean... well, I think  Harry'd love to be forming secret Defence societies right under the nose of someone from the Ministry..."
I think  Harry's really frustrated at how little  Harry can do where  Harry is... so I think  Harry's keen to kind of... egg us on.'
Ron looked utterly perplexed.   '
"Sirius is right,'  Harry said,' you do sound just like my mother.'"
Hermione bit  Hermione lip and did not answer.
The bell rang just as  Peeves swooped down on  Katie and emptied an entire ink bottle over  Hermione head.
"*The weather did not improve as the day wore on, so that at seveno'clock that evening, when  Harry and  Ron went down to the Quidditch pitch for practice, Harry and  Ron were soaked through within minutes, Harry and  Ron feet slipping and sliding on the sodden grass."
"The sky was a deep, thundery grey and it was a relief to gain the warmth and light of the changing rooms, even if relief knew the respite was only temporary."
I'll get yer an owl.
"All the kids want owls, kids're dead useful, carry yer mail an' everythin'.`  Twenty minutes later, kids left Eeylops Owl Emporium, which had been dark and full of rustling and flickering, jewel- bright eyes."
"Harry now carried a large cage that held a beautiful snowy owl, fast asleep with owl head under owl wing."
"Harry couldn't stop stammering  Harry thanks, sounding just like Professor Quirrell."
"` Don' mention cage,` said  Hagrid gruffly.` Don' expect you've had a lotta presents from a   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley."
"Just Ollivanders left now- only place fer wands, Ollivanders, and yeh got ta have the best wand.`  A magic wand... this was what  Harry had been really looking forward to."
The last shop was narrow and shabby.
Peeling gold letters over the door read Ollivanders: Makers of Fine Wands since 382 B.C.
A single wand lay on a faded purple cushion in the dusty window.
A tinkling bell rang somewhere in the depths of the shop as depths stepped inside.
"bell was a tiny place, empty except for a single, spindly chair that  Hagrid sat on to wait."
Harry felt strangely as though  Harry had entered a very strict library;  Harry swallowed a lot of new questions that had just occurred to  Harry and looked instead at the thousands of narrow boxes piled neatly right up to the ceiling.
"For some reason, the back of  Harry neck prickled."
The very dust and silence in here seemed to tingle with some secret magic.
"` Good afternoon,` said a soft voice."
"All right, we'll take you to King's Cross."
"We're going up to London tomorrow anyway, or I wouldn't bother.` ` Why are you going to London?`  Harry asked, trying to keep things friendly."
"` Taking   Dudley to the hospital,` growled Uncle  Vernon.` Got to have that ruddy tail removed before  Vernon goes to Smeltings.`   Harry woke at fiveo'clock the next morning and was too excited and nervous to go back to sleep."
Vernon got up and pulled on  Vernon jeans because  Vernon didn't want to walk into the station in  Vernon wizard's robes--  Vernon'd change on the train.
"Vernon checked  Vernon Hogwarts list yet again to make sure  Vernon had everything  Vernon needed, saw that  Hedwig was shut safely in  Hedwig cage, and then paced the room, waiting for the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley to get up."
"Two hours later,  Harry's huge, heavy trunk had been loaded into the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' car,  Aunt  Petunia had talked   Dudley into sitting next to  Harry, and   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had set off."
Mr. Dursley and   Mrs. Dursley and    Dudley Dursley reached King's Cross at half past ten.
Uncle  Vernon dumped  Harry's trunk onto a cart and wheeled trunk into the station for  Harry.
"Harry thought this was strangely kind until Uncle  Vernon stopped dead, facing the  platforms with a nasty grin on  Harry face."
"""

TASK_7_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
    Over-Attentive Wizard,
    Bertram Aubrey,
    Audrey Weasley,
    "Augusta ""Gran"" Longbottom",
    Augustus Pye,
    Augustus Rookwood,
    Augustus Worme,
    Auntie Muriel,
    Aunt Marge Dursley,
    Aurelius Dumbledore,
    Aurora Sinistra,
    Avery,
    Babajide Akingbade,
    Babayaga,
    Babbitty Rabbitty,
    Bagman Sr.,
    Ludo Bagman,
    Otto Bagman,
    Millicent Bagnold,
    Bathilda Bagshot,Batty
    Kquewanda Bailey,
    Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
    Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
    Aberforth Dumbledore,
    Hermione Granger,
    Draco Malfoy,
    """
TASK_7_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,Batty
Kquewanda Bailey,
Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
Aberforth Dumbledore,
Hermione Granger,
Draco Malfoy,
"""
TASK_7_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
"Magnus ""Dent Head"" Macdonald",
Magorian,
Maisie Cattermole,
Malcolm,
Malcolm Baddock,
Malcolm McGonagall,
Harold Skively,
Harper,
Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
Harvey Ridgebit,
Hassan Mostafa,
Gwenog,
Gwenog Jones,
Hagrid's father,
Hambledon Quince,
Hamish MacFarlan,
Hankerton Humble,
Hermione Granger,
Draco Malfoy,
Aurelius Dumbledore,
"""
TASK_7_EXAMPLE_4_NAMES_CSV_RAW = """Name,Other Names
Abernathy,
Abraham Peasegood,
Abraham Potter,
Abraxas Malfoy,
Achilles Tolliver,
Stewart Ackerley,
Mrs. Granger,
Hermione Granger,
Hugo Granger-Weasley,
Rose Granger-Weasley,
Granville Jorkins,
Gondulphus Graves,
Merton Graves,
Percival Graves,
Grawp,
Irma Pince,
Irving Warble,
Isadora Rose,
Isobel McGonagall,
Isobel Ross,
Isolt Sayre,"morrigan, elias story"
Ivanova,
Ivan Popa,
Harold Minchum,
Harold Skively,
Harper,
Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
Harvey Ridgebit,
Hassan Mostafa,
Havelock Sweeting,
Hector Lamont,
Hedwig,
Helena Ravenclaw,
Verity,
Vernon Dudley,
Veronica Smethley,
Aurelius Dumbledore,
Draco Malfoy,
Gwenog Jones,
Malcolm Baddock,
"""

TASK_7_EXAMPLE_1_WINDOW_SIZE = 5
TASK_7_EXAMPLE_2_WINDOW_SIZE = 3
TASK_7_EXAMPLE_3_WINDOW_SIZE = 5
TASK_7_EXAMPLE_4_WINDOW_SIZE = 5

TASK_7_EXAMPLE_1_TRESHOLD = 2
TASK_7_EXAMPLE_2_TRESHOLD = 2
TASK_7_EXAMPLE_3_TRESHOLD = 2
TASK_7_EXAMPLE_4_TRESHOLD = 2

TASK_7_EXAMPLE_1_CONNECTIONS_JSON_RAW = """{
        "keys": [
            ["harry potter", "aurelius dumbledore"],
            ["hermione granger", "draco malfoy"],
            ["hermione granger", "harry potter"]

        ]
    }
    """
TASK_7_EXAMPLE_2_CONNECTIONS_JSON_RAW = """{
    "keys": [
        ["otto bagman", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"]

    ]
}
"""
TASK_7_EXAMPLE_3_CONNECTIONS_JSON_RAW = """{
    "keys": [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"],
        ["harold skively", "gwenog jones"],
        ["hassan mostafa", "malcolm baddock"]


    ]
}
"""
TASK_7_EXAMPLE_4_CONNECTIONS_JSON_RAW = """{
    "keys": [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"],
        ["harold skively", "gwenog jones"],
        ["hassan mostafa", "malcolm baddock"],
        ["isobel mcgonagall", "hermione granger"],
        ["isobel mcgonagall", "vernon dudley"],
        ["hedwig", "vernon dudley"]
    ]
}
"""

TASK_7_EXAMPLE_1_MAX_DISTANCE = 1000
TASK_7_EXAMPLE_2_MAX_DISTANCE = 1000
TASK_7_EXAMPLE_3_MAX_DISTANCE = 1000
TASK_7_EXAMPLE_4_MAX_DISTANCE = 1000

TASK_7_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 7": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "harry potter",
                true
            ],
            [
                "draco malfoy",
                "hermione granger",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                false
            ]
        ]
    }
}'''
TASK_7_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 7": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "otto bagman",
                true
            ],
            [
                "draco malfoy",
                "hermione granger",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                false
            ]
        ]
    }
}'''
TASK_7_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 7": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "harry potter",
                false
            ],
            [
                "draco malfoy",
                "hermione granger",
                true
            ],
            [
                "gwenog jones",
                "harold skively",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                true
            ],
            [
                "hassan mostafa",
                "malcolm baddock",
                true
            ]
        ]
    }
}'''
TASK_7_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 7": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "harry potter",
                false
            ],
            [
                "draco malfoy",
                "hermione granger",
                false
            ],
            [
                "gwenog jones",
                "harold skively",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                true
            ],
            [
                "hassan mostafa",
                "malcolm baddock",
                false
            ],
            [
                "hedwig",
                "vernon dudley",
                true
            ],
            [
                "hermione granger",
                "isobel mcgonagall",
                true
            ],
            [
                "isobel mcgonagall",
                "vernon dudley",
                true
            ]
        ]
    }
}'''


# CONSTANT FOR TASK 8 UNPROCESSED FLOW TEST

TASK_8_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""
TASK_8_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""
TASK_8_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""

TASK_8_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",Gran
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,Batty
Kquewanda Bailey,
Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
Aberforth Dumbledore,
Hermione Granger,
Draco Malfoy,
"""
TASK_8_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",Gran
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,Batty
Kquewanda Bailey,
Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
Aberforth Dumbledore,
Hermione Granger,
Draco Malfoy,
"""
TASK_8_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",Gran
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,Batty
Kquewanda Bailey,
Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
Aberforth Dumbledore,
Hermione Granger,
Draco Malfoy,
"""

TASK_8_EXAMPLE_1_WINDOW_SIZE = 3
TASK_8_EXAMPLE_2_WINDOW_SIZE = 3
TASK_8_EXAMPLE_3_WINDOW_SIZE = 3

TASK_8_EXAMPLE_1_TRESHOLD = 2
TASK_8_EXAMPLE_2_TRESHOLD = 2
TASK_8_EXAMPLE_3_TRESHOLD = 2

TASK_8_EXAMPLE_1_CONNECTIONS_JSON_RAW = """{
    "keys": [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"]

    ]
}
"""
TASK_8_EXAMPLE_2_CONNECTIONS_JSON_RAW = """{
    "keys": [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"]

    ]
}
"""
TASK_8_EXAMPLE_3_CONNECTIONS_JSON_RAW = """{
    "keys": [
        ["harry potter", "aurelius dumbledore"],
        ["hermione granger", "draco malfoy"],
        ["hermione granger", "harry potter"]

    ]
}
"""

TASK_8_EXAMPLE_1_EXC_DISTANCE = 2
TASK_8_EXAMPLE_2_EXC_DISTANCE = 3
TASK_8_EXAMPLE_3_EXC_DISTANCE = 8

TASK_8_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 8": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "harry potter",
                true
            ],
            [
                "draco malfoy",
                "hermione granger",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                false
            ]
        ]
    }
}'''
TASK_8_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 8": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "harry potter",
                true
            ],
            [
                "draco malfoy",
                "hermione granger",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                false
            ]
        ]
    }
}'''
TASK_8_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 8": {
        "Pair Matches": [
            [
                "aurelius dumbledore",
                "harry potter",
                false
            ],
            [
                "draco malfoy",
                "hermione granger",
                false
            ],
            [
                "harry potter",
                "hermione granger",
                false
            ]
        ]
    }
}'''


# CONSTANT FOR TASK 9 UNPROCESSED FLOW TEST

TASK_9_EXAMPLE_1_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""
TASK_9_EXAMPLE_2_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""
TASK_9_EXAMPLE_3_SENTENCES_CSV_RAW = """sentence
"Under a tuft of jet- black hair over boy forehead Dumbledore and  McGonagall could see a curiously shaped cut, like a bolt of lightning."
` Is that where-?` whispered Professor  McGonagall.
"` Yes,` said  Dumbledore.`  Dumbledore'll have that scar forever.` ` Couldn't you do something about scar,  Dumbledore?` ` Even if I could, I wouldn't."
Scars can come in handy.
I have one myself above my left knee that is a perfect map of the London Underground.
"Well-- give  Dumbledore here,  Hagrid-- we'd better get this over with.`   Dumbledore took  Harry in  Harry arms and turned toward the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' house."
"` Could I-- could I say good- bye to  Harry, sir?` asked  Hagrid."
"Harry bent  Harry great, shaggy head over  Harry and gave head what must have been a very scratchy, whiskery kiss."
"Then, suddenly,  Hagrid let out a howl like a wounded dog."
"` Shhh!` hissed Professor  McGonagall,` you'll wake the  Muggles!` ` S- s- sorry,` sobbed  Hagrid, taking out a large, spotted handkerchief and burying  Hagrid face in handkerchief.` But I c- c-can't stand handkerchief--  Lily an'  James dead-- an' poor little  Harry off ter live with  Muggles-` ` Yes, yes, handkerchief's all very sad, but get a grip on yourself,  Hagrid, or we'll be found,` Professor  McGonagall whispered, patting  Hagrid gingerly on the arm as  Dumbledore stepped over the low garden wall and walked to the front door."
"Dumbledore laid  Harry gently on the doorstep, took a letter out of  Dumbledore cloak, tucked letter inside  Harry's blankets, and then came back to the other two."
"For a full minute the three of two stood and looked at the little bundle;   Hagrid's shoulders shook, Professor  McGonagall blinked furiously, and the twinkling light that usually shone from  Dumbledore's eyes seemed to have gone out."
"` Well,` said  Dumbledore finally,` that's that."
We've no business staying here.
"We may as well go and join the celebrations.` ` Yeah,` said  Hagrid in a very muffled voice,` I'll be takin'  Sirius  Sirius bike back.G'night, Professor  McGonagall-- Professor  Dumbledore, sir.`  Wiping  Sirius streaming eyes on  Sirius jacket sleeve,  Hagrid swung  Hagrid onto the motorcycle and kicked the engine into life; with a roar engine rose into the air and off into the night."
"` I shall see you soon, I expect, Professor  McGonagall,` said  Dumbledore, nodding to voice."
Professor  McGonagall blew  McGonagall nose in reply.
Dumbledore turned and walked back down the street.
On the corner  Dumbledore stopped and took out the silver Put- Outer.
"Dumbledore clicked Outer once, and twelve balls of light sped back to balls street lamps so that Privet Drive glowed suddenly orange and  Dumbledore could make out a tabby cat slinking around the corner at the other end of the street."
Dumbledore could just see the bundle of blankets on the step of number four.
"` Good luck,  Harry,`  Dumbledore murmured."
"Dumbledore turned on  Dumbledore heel and with a swish of  Dumbledore cloak,  Dumbledore was gone."
"A breeze ruffled the neat hedges of Privet Drive, which lay silent and tidy under the inky sky, the very last place you would expect astonishing things to happen."
Harry  Potter rolled over inside  Dumbledore blankets without waking up.
"One small hand closed on the letter beside  Dumbledore and  Dumbledore slept on, not knowing  Dumbledore was special, not knowing  Dumbledore was famous, not knowing  Dumbledore would be woken in a few hours' time by   Mrs. Dursley's scream as   Mrs. Dursley opened the front door to put out the milk bottles, nor that  Dumbledore would spend the next few weeks being prodded and pinched by  Dumbledore cousin   Dudley...  Dumbledore couldn't know that at this very moment, people meeting in secret all over the country were holding up people glasses and saying in hushed voices:` To   Harry  Potter-- the boy who lived!"
"THE VANISHING GLASS  Nearly ten years had passed since the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley had woken up to find   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley nephew on the front step, but Privet Drive had hardly changed at all."
"The sun rose on the same tidy front gardens and lit up the brass number four on the   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley' front door; number crept into   Mr. Dursley and   Mrs. Dursley and    Dudley Dursley living room, which was almost exactly the same as it had been on the night when   Mr. Dursley had seen that fateful news report about the owls."
Only the photographs on the mantelpiece really showed how much time had passed.
"Ten years ago, there had been lots of pictures of what looked like a large pink beach ball wearing different- colored bonnets-- but    Dudley Dursley was no longer a baby, and now the photographs showed a large blond boy riding boy first bicycle, on a carousel at the fair, playing a computer game with boy father, being hugged and kissed by boy mother."
"The room held no sign at all that another boy lived in the house, too."
"""

TASK_9_EXAMPLE_1_TRESHOLD = 1
TASK_9_EXAMPLE_2_TRESHOLD = 3
TASK_9_EXAMPLE_3_TRESHOLD = 6

TASK_9_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 9": {
        "group Matches": [
            [
                "Group 1",
                [
                    [
                        "left",
                        "knee",
                        "perfect",
                        "map",
                        "london",
                        "underground"
                    ]
                ]
            ],
            [
                "Group 2",
                [
                    [
                        "scars",
                        "handy"
                    ]
                ]
            ],
            [
                "Group 3",
                [
                    [
                        "ve",
                        "business",
                        "staying"
                    ]
                ]
            ],
            [
                "Group 4",
                [
                    [
                        "breeze",
                        "ruffled",
                        "neat",
                        "hedges",
                        "privet",
                        "drive",
                        "lay",
                        "silent",
                        "tidy",
                        "inky",
                        "sky",
                        "place",
                        "expect",
                        "astonishing",
                        "things"
                    ],
                    [
                        "corner",
                        "dumbledore",
                        "stopped",
                        "took",
                        "silver",
                        "outer"
                    ],
                    [
                        "dumbledore",
                        "bundle",
                        "blankets",
                        "step",
                        "number",
                        "four"
                    ],
                    [
                        "dumbledore",
                        "clicked",
                        "outer",
                        "twelve",
                        "balls",
                        "light",
                        "sped",
                        "balls",
                        "street",
                        "lamps",
                        "privet",
                        "drive",
                        "glowed",
                        "suddenly",
                        "orange",
                        "dumbledore",
                        "tabby",
                        "cat",
                        "slinking",
                        "corner",
                        "street"
                    ],
                    [
                        "dumbledore",
                        "dumbledore",
                        "ll",
                        "scar",
                        "forever",
                        "couldn",
                        "something",
                        "scar",
                        "dumbledore",
                        "wouldn"
                    ],
                    [
                        "dumbledore",
                        "laid",
                        "harry",
                        "gently",
                        "doorstep",
                        "took",
                        "letter",
                        "dumbledore",
                        "cloak",
                        "tucked",
                        "letter",
                        "inside",
                        "harry",
                        "blankets",
                        "came"
                    ],
                    [
                        "dumbledore",
                        "turned",
                        "dumbledore",
                        "heel",
                        "swish",
                        "dumbledore",
                        "cloak",
                        "dumbledore"
                    ],
                    [
                        "dumbledore",
                        "turned",
                        "walked",
                        "street"
                    ],
                    [
                        "full",
                        "minute",
                        "three",
                        "stood",
                        "looked",
                        "little",
                        "bundle",
                        "hagrid",
                        "shoulders",
                        "shook",
                        "professor",
                        "mcgonagall",
                        "blinked",
                        "furiously",
                        "twinkling",
                        "light",
                        "usually",
                        "shone",
                        "dumbledore",
                        "eyes",
                        "seemed"
                    ],
                    [
                        "good",
                        "bye",
                        "harry",
                        "sir",
                        "asked",
                        "hagrid"
                    ],
                    [
                        "good",
                        "luck",
                        "harry",
                        "dumbledore",
                        "murmured"
                    ],
                    [
                        "harry",
                        "bent",
                        "harry",
                        "great",
                        "shaggy",
                        "harry",
                        "gave",
                        "scratchy",
                        "whiskery",
                        "kiss"
                    ],
                    [
                        "harry",
                        "potter",
                        "rolled",
                        "inside",
                        "dumbledore",
                        "blankets",
                        "without",
                        "waking"
                    ],
                    [
                        "photographs",
                        "mantelpiece",
                        "really",
                        "showed",
                        "passed"
                    ],
                    [
                        "professor",
                        "mcgonagall",
                        "blew",
                        "mcgonagall",
                        "nose",
                        "reply"
                    ],
                    [
                        "room",
                        "held",
                        "sign",
                        "another",
                        "lived",
                        "house"
                    ],
                    [
                        "shall",
                        "expect",
                        "professor",
                        "mcgonagall",
                        "dumbledore",
                        "nodding",
                        "voice"
                    ],
                    [
                        "shhh",
                        "hissed",
                        "professor",
                        "mcgonagall",
                        "ll",
                        "wake",
                        "muggles",
                        "sorry",
                        "sobbed",
                        "hagrid",
                        "taking",
                        "large",
                        "spotted",
                        "handkerchief",
                        "burying",
                        "hagrid",
                        "face",
                        "handkerchief",
                        "stand",
                        "handkerchief",
                        "lily",
                        "james",
                        "dead",
                        "poor",
                        "little",
                        "harry",
                        "ter",
                        "muggles",
                        "handkerchief",
                        "sad",
                        "grip",
                        "hagrid",
                        "ll",
                        "professor",
                        "mcgonagall",
                        "whispered",
                        "patting",
                        "hagrid",
                        "gingerly",
                        "arm",
                        "dumbledore",
                        "stepped",
                        "low",
                        "garden",
                        "wall",
                        "walked",
                        "front",
                        "door"
                    ],
                    [
                        "small",
                        "hand",
                        "closed",
                        "letter",
                        "beside",
                        "dumbledore",
                        "dumbledore",
                        "slept",
                        "knowing",
                        "dumbledore",
                        "special",
                        "knowing",
                        "dumbledore",
                        "famous",
                        "knowing",
                        "dumbledore",
                        "woken",
                        "hours",
                        "dursley",
                        "scream",
                        "dursley",
                        "opened",
                        "front",
                        "door",
                        "milk",
                        "bottles",
                        "dumbledore",
                        "spend",
                        "next",
                        "weeks",
                        "prodded",
                        "pinched",
                        "dumbledore",
                        "cousin",
                        "dudley",
                        "dumbledore",
                        "couldn",
                        "moment",
                        "people",
                        "meeting",
                        "secret",
                        "country",
                        "holding",
                        "people",
                        "glasses",
                        "saying",
                        "hushed",
                        "voices",
                        "harry",
                        "potter",
                        "lived"
                    ],
                    [
                        "suddenly",
                        "hagrid",
                        "howl",
                        "like",
                        "wounded",
                        "dog"
                    ],
                    [
                        "sun",
                        "rose",
                        "tidy",
                        "front",
                        "gardens",
                        "lit",
                        "brass",
                        "number",
                        "four",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "front",
                        "door",
                        "number",
                        "crept",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "living",
                        "room",
                        "almost",
                        "exactly",
                        "dursley",
                        "seen",
                        "fateful",
                        "news",
                        "report",
                        "owls"
                    ],
                    [
                        "ten",
                        "years",
                        "ago",
                        "lots",
                        "pictures",
                        "looked",
                        "like",
                        "large",
                        "pink",
                        "beach",
                        "ball",
                        "wearing",
                        "different",
                        "colored",
                        "bonnets",
                        "dudley",
                        "dursley",
                        "longer",
                        "baby",
                        "photographs",
                        "showed",
                        "large",
                        "blond",
                        "riding",
                        "bicycle",
                        "carousel",
                        "fair",
                        "playing",
                        "computer",
                        "father",
                        "hugged",
                        "kissed",
                        "mother"
                    ],
                    [
                        "tuft",
                        "jet",
                        "black",
                        "forehead",
                        "dumbledore",
                        "mcgonagall",
                        "curiously",
                        "shaped",
                        "cut",
                        "like",
                        "bolt",
                        "lightning"
                    ],
                    [
                        "vanishing",
                        "glass",
                        "nearly",
                        "ten",
                        "years",
                        "passed",
                        "since",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "woken",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "nephew",
                        "front",
                        "step",
                        "privet",
                        "drive",
                        "hardly",
                        "changed"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "finally"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "hagrid",
                        "better",
                        "dumbledore",
                        "took",
                        "harry",
                        "harry",
                        "arms",
                        "turned",
                        "toward",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "house"
                    ],
                    [
                        "well",
                        "go",
                        "join",
                        "celebrations",
                        "hagrid",
                        "muffled",
                        "voice",
                        "ll",
                        "takin",
                        "sirius",
                        "sirius",
                        "bike",
                        "professor",
                        "mcgonagall",
                        "professor",
                        "dumbledore",
                        "sir",
                        "wiping",
                        "sirius",
                        "streaming",
                        "eyes",
                        "sirius",
                        "jacket",
                        "sleeve",
                        "hagrid",
                        "swung",
                        "hagrid",
                        "onto",
                        "motorcycle",
                        "kicked",
                        "engine",
                        "roar",
                        "engine",
                        "rose",
                        "air"
                    ],
                    [
                        "whispered",
                        "professor",
                        "mcgonagall"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_9_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 9": {
        "group Matches": [
            [
                "Group 1",
                [
                    [
                        "breeze",
                        "ruffled",
                        "neat",
                        "hedges",
                        "privet",
                        "drive",
                        "lay",
                        "silent",
                        "tidy",
                        "inky",
                        "sky",
                        "place",
                        "expect",
                        "astonishing",
                        "things"
                    ]
                ]
            ],
            [
                "Group 2",
                [
                    [
                        "dumbledore",
                        "bundle",
                        "blankets",
                        "step",
                        "number",
                        "four"
                    ]
                ]
            ],
            [
                "Group 3",
                [
                    [
                        "dumbledore",
                        "dumbledore",
                        "ll",
                        "scar",
                        "forever",
                        "couldn",
                        "something",
                        "scar",
                        "dumbledore",
                        "wouldn"
                    ]
                ]
            ],
            [
                "Group 4",
                [
                    [
                        "dumbledore",
                        "turned",
                        "dumbledore",
                        "heel",
                        "swish",
                        "dumbledore",
                        "cloak",
                        "dumbledore"
                    ]
                ]
            ],
            [
                "Group 5",
                [
                    [
                        "dumbledore",
                        "turned",
                        "walked",
                        "street"
                    ]
                ]
            ],
            [
                "Group 6",
                [
                    [
                        "good",
                        "bye",
                        "harry",
                        "sir",
                        "asked",
                        "hagrid"
                    ]
                ]
            ],
            [
                "Group 7",
                [
                    [
                        "good",
                        "luck",
                        "harry",
                        "dumbledore",
                        "murmured"
                    ]
                ]
            ],
            [
                "Group 8",
                [
                    [
                        "harry",
                        "bent",
                        "harry",
                        "great",
                        "shaggy",
                        "harry",
                        "gave",
                        "scratchy",
                        "whiskery",
                        "kiss"
                    ]
                ]
            ],
            [
                "Group 9",
                [
                    [
                        "left",
                        "knee",
                        "perfect",
                        "map",
                        "london",
                        "underground"
                    ]
                ]
            ],
            [
                "Group 10",
                [
                    [
                        "photographs",
                        "mantelpiece",
                        "really",
                        "showed",
                        "passed"
                    ]
                ]
            ],
            [
                "Group 11",
                [
                    [
                        "professor",
                        "mcgonagall",
                        "blew",
                        "mcgonagall",
                        "nose",
                        "reply"
                    ]
                ]
            ],
            [
                "Group 12",
                [
                    [
                        "room",
                        "held",
                        "sign",
                        "another",
                        "lived",
                        "house"
                    ]
                ]
            ],
            [
                "Group 13",
                [
                    [
                        "scars",
                        "handy"
                    ]
                ]
            ],
            [
                "Group 14",
                [
                    [
                        "suddenly",
                        "hagrid",
                        "howl",
                        "like",
                        "wounded",
                        "dog"
                    ]
                ]
            ],
            [
                "Group 15",
                [
                    [
                        "tuft",
                        "jet",
                        "black",
                        "forehead",
                        "dumbledore",
                        "mcgonagall",
                        "curiously",
                        "shaped",
                        "cut",
                        "like",
                        "bolt",
                        "lightning"
                    ]
                ]
            ],
            [
                "Group 16",
                [
                    [
                        "ve",
                        "business",
                        "staying"
                    ]
                ]
            ],
            [
                "Group 17",
                [
                    [
                        "well",
                        "dumbledore",
                        "finally"
                    ]
                ]
            ],
            [
                "Group 18",
                [
                    [
                        "corner",
                        "dumbledore",
                        "stopped",
                        "took",
                        "silver",
                        "outer"
                    ],
                    [
                        "dumbledore",
                        "clicked",
                        "outer",
                        "twelve",
                        "balls",
                        "light",
                        "sped",
                        "balls",
                        "street",
                        "lamps",
                        "privet",
                        "drive",
                        "glowed",
                        "suddenly",
                        "orange",
                        "dumbledore",
                        "tabby",
                        "cat",
                        "slinking",
                        "corner",
                        "street"
                    ]
                ]
            ],
            [
                "Group 19",
                [
                    [
                        "dumbledore",
                        "laid",
                        "harry",
                        "gently",
                        "doorstep",
                        "took",
                        "letter",
                        "dumbledore",
                        "cloak",
                        "tucked",
                        "letter",
                        "inside",
                        "harry",
                        "blankets",
                        "came"
                    ],
                    [
                        "full",
                        "minute",
                        "three",
                        "stood",
                        "looked",
                        "little",
                        "bundle",
                        "hagrid",
                        "shoulders",
                        "shook",
                        "professor",
                        "mcgonagall",
                        "blinked",
                        "furiously",
                        "twinkling",
                        "light",
                        "usually",
                        "shone",
                        "dumbledore",
                        "eyes",
                        "seemed"
                    ],
                    [
                        "harry",
                        "potter",
                        "rolled",
                        "inside",
                        "dumbledore",
                        "blankets",
                        "without",
                        "waking"
                    ],
                    [
                        "shall",
                        "expect",
                        "professor",
                        "mcgonagall",
                        "dumbledore",
                        "nodding",
                        "voice"
                    ],
                    [
                        "shhh",
                        "hissed",
                        "professor",
                        "mcgonagall",
                        "ll",
                        "wake",
                        "muggles",
                        "sorry",
                        "sobbed",
                        "hagrid",
                        "taking",
                        "large",
                        "spotted",
                        "handkerchief",
                        "burying",
                        "hagrid",
                        "face",
                        "handkerchief",
                        "stand",
                        "handkerchief",
                        "lily",
                        "james",
                        "dead",
                        "poor",
                        "little",
                        "harry",
                        "ter",
                        "muggles",
                        "handkerchief",
                        "sad",
                        "grip",
                        "hagrid",
                        "ll",
                        "professor",
                        "mcgonagall",
                        "whispered",
                        "patting",
                        "hagrid",
                        "gingerly",
                        "arm",
                        "dumbledore",
                        "stepped",
                        "low",
                        "garden",
                        "wall",
                        "walked",
                        "front",
                        "door"
                    ],
                    [
                        "small",
                        "hand",
                        "closed",
                        "letter",
                        "beside",
                        "dumbledore",
                        "dumbledore",
                        "slept",
                        "knowing",
                        "dumbledore",
                        "special",
                        "knowing",
                        "dumbledore",
                        "famous",
                        "knowing",
                        "dumbledore",
                        "woken",
                        "hours",
                        "dursley",
                        "scream",
                        "dursley",
                        "opened",
                        "front",
                        "door",
                        "milk",
                        "bottles",
                        "dumbledore",
                        "spend",
                        "next",
                        "weeks",
                        "prodded",
                        "pinched",
                        "dumbledore",
                        "cousin",
                        "dudley",
                        "dumbledore",
                        "couldn",
                        "moment",
                        "people",
                        "meeting",
                        "secret",
                        "country",
                        "holding",
                        "people",
                        "glasses",
                        "saying",
                        "hushed",
                        "voices",
                        "harry",
                        "potter",
                        "lived"
                    ],
                    [
                        "sun",
                        "rose",
                        "tidy",
                        "front",
                        "gardens",
                        "lit",
                        "brass",
                        "number",
                        "four",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "front",
                        "door",
                        "number",
                        "crept",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "living",
                        "room",
                        "almost",
                        "exactly",
                        "dursley",
                        "seen",
                        "fateful",
                        "news",
                        "report",
                        "owls"
                    ],
                    [
                        "ten",
                        "years",
                        "ago",
                        "lots",
                        "pictures",
                        "looked",
                        "like",
                        "large",
                        "pink",
                        "beach",
                        "ball",
                        "wearing",
                        "different",
                        "colored",
                        "bonnets",
                        "dudley",
                        "dursley",
                        "longer",
                        "baby",
                        "photographs",
                        "showed",
                        "large",
                        "blond",
                        "riding",
                        "bicycle",
                        "carousel",
                        "fair",
                        "playing",
                        "computer",
                        "father",
                        "hugged",
                        "kissed",
                        "mother"
                    ],
                    [
                        "vanishing",
                        "glass",
                        "nearly",
                        "ten",
                        "years",
                        "passed",
                        "since",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "woken",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "nephew",
                        "front",
                        "step",
                        "privet",
                        "drive",
                        "hardly",
                        "changed"
                    ],
                    [
                        "well",
                        "dumbledore",
                        "hagrid",
                        "better",
                        "dumbledore",
                        "took",
                        "harry",
                        "harry",
                        "arms",
                        "turned",
                        "toward",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "house"
                    ],
                    [
                        "well",
                        "go",
                        "join",
                        "celebrations",
                        "hagrid",
                        "muffled",
                        "voice",
                        "ll",
                        "takin",
                        "sirius",
                        "sirius",
                        "bike",
                        "professor",
                        "mcgonagall",
                        "professor",
                        "dumbledore",
                        "sir",
                        "wiping",
                        "sirius",
                        "streaming",
                        "eyes",
                        "sirius",
                        "jacket",
                        "sleeve",
                        "hagrid",
                        "swung",
                        "hagrid",
                        "onto",
                        "motorcycle",
                        "kicked",
                        "engine",
                        "roar",
                        "engine",
                        "rose",
                        "air"
                    ],
                    [
                        "whispered",
                        "professor",
                        "mcgonagall"
                    ]
                ]
            ]
        ]
    }
}'''
TASK_9_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW = '''{
    "Question 9": {
        "group Matches": [
            [
                "Group 1",
                [
                    [
                        "breeze",
                        "ruffled",
                        "neat",
                        "hedges",
                        "privet",
                        "drive",
                        "lay",
                        "silent",
                        "tidy",
                        "inky",
                        "sky",
                        "place",
                        "expect",
                        "astonishing",
                        "things"
                    ]
                ]
            ],
            [
                "Group 2",
                [
                    [
                        "corner",
                        "dumbledore",
                        "stopped",
                        "took",
                        "silver",
                        "outer"
                    ]
                ]
            ],
            [
                "Group 3",
                [
                    [
                        "dumbledore",
                        "bundle",
                        "blankets",
                        "step",
                        "number",
                        "four"
                    ]
                ]
            ],
            [
                "Group 4",
                [
                    [
                        "dumbledore",
                        "clicked",
                        "outer",
                        "twelve",
                        "balls",
                        "light",
                        "sped",
                        "balls",
                        "street",
                        "lamps",
                        "privet",
                        "drive",
                        "glowed",
                        "suddenly",
                        "orange",
                        "dumbledore",
                        "tabby",
                        "cat",
                        "slinking",
                        "corner",
                        "street"
                    ]
                ]
            ],
            [
                "Group 5",
                [
                    [
                        "dumbledore",
                        "dumbledore",
                        "ll",
                        "scar",
                        "forever",
                        "couldn",
                        "something",
                        "scar",
                        "dumbledore",
                        "wouldn"
                    ]
                ]
            ],
            [
                "Group 6",
                [
                    [
                        "dumbledore",
                        "laid",
                        "harry",
                        "gently",
                        "doorstep",
                        "took",
                        "letter",
                        "dumbledore",
                        "cloak",
                        "tucked",
                        "letter",
                        "inside",
                        "harry",
                        "blankets",
                        "came"
                    ]
                ]
            ],
            [
                "Group 7",
                [
                    [
                        "dumbledore",
                        "turned",
                        "dumbledore",
                        "heel",
                        "swish",
                        "dumbledore",
                        "cloak",
                        "dumbledore"
                    ]
                ]
            ],
            [
                "Group 8",
                [
                    [
                        "dumbledore",
                        "turned",
                        "walked",
                        "street"
                    ]
                ]
            ],
            [
                "Group 9",
                [
                    [
                        "full",
                        "minute",
                        "three",
                        "stood",
                        "looked",
                        "little",
                        "bundle",
                        "hagrid",
                        "shoulders",
                        "shook",
                        "professor",
                        "mcgonagall",
                        "blinked",
                        "furiously",
                        "twinkling",
                        "light",
                        "usually",
                        "shone",
                        "dumbledore",
                        "eyes",
                        "seemed"
                    ]
                ]
            ],
            [
                "Group 10",
                [
                    [
                        "good",
                        "bye",
                        "harry",
                        "sir",
                        "asked",
                        "hagrid"
                    ]
                ]
            ],
            [
                "Group 11",
                [
                    [
                        "good",
                        "luck",
                        "harry",
                        "dumbledore",
                        "murmured"
                    ]
                ]
            ],
            [
                "Group 12",
                [
                    [
                        "harry",
                        "bent",
                        "harry",
                        "great",
                        "shaggy",
                        "harry",
                        "gave",
                        "scratchy",
                        "whiskery",
                        "kiss"
                    ]
                ]
            ],
            [
                "Group 13",
                [
                    [
                        "harry",
                        "potter",
                        "rolled",
                        "inside",
                        "dumbledore",
                        "blankets",
                        "without",
                        "waking"
                    ]
                ]
            ],
            [
                "Group 14",
                [
                    [
                        "left",
                        "knee",
                        "perfect",
                        "map",
                        "london",
                        "underground"
                    ]
                ]
            ],
            [
                "Group 15",
                [
                    [
                        "photographs",
                        "mantelpiece",
                        "really",
                        "showed",
                        "passed"
                    ]
                ]
            ],
            [
                "Group 16",
                [
                    [
                        "professor",
                        "mcgonagall",
                        "blew",
                        "mcgonagall",
                        "nose",
                        "reply"
                    ]
                ]
            ],
            [
                "Group 17",
                [
                    [
                        "room",
                        "held",
                        "sign",
                        "another",
                        "lived",
                        "house"
                    ]
                ]
            ],
            [
                "Group 18",
                [
                    [
                        "scars",
                        "handy"
                    ]
                ]
            ],
            [
                "Group 19",
                [
                    [
                        "shall",
                        "expect",
                        "professor",
                        "mcgonagall",
                        "dumbledore",
                        "nodding",
                        "voice"
                    ]
                ]
            ],
            [
                "Group 20",
                [
                    [
                        "shhh",
                        "hissed",
                        "professor",
                        "mcgonagall",
                        "ll",
                        "wake",
                        "muggles",
                        "sorry",
                        "sobbed",
                        "hagrid",
                        "taking",
                        "large",
                        "spotted",
                        "handkerchief",
                        "burying",
                        "hagrid",
                        "face",
                        "handkerchief",
                        "stand",
                        "handkerchief",
                        "lily",
                        "james",
                        "dead",
                        "poor",
                        "little",
                        "harry",
                        "ter",
                        "muggles",
                        "handkerchief",
                        "sad",
                        "grip",
                        "hagrid",
                        "ll",
                        "professor",
                        "mcgonagall",
                        "whispered",
                        "patting",
                        "hagrid",
                        "gingerly",
                        "arm",
                        "dumbledore",
                        "stepped",
                        "low",
                        "garden",
                        "wall",
                        "walked",
                        "front",
                        "door"
                    ]
                ]
            ],
            [
                "Group 21",
                [
                    [
                        "small",
                        "hand",
                        "closed",
                        "letter",
                        "beside",
                        "dumbledore",
                        "dumbledore",
                        "slept",
                        "knowing",
                        "dumbledore",
                        "special",
                        "knowing",
                        "dumbledore",
                        "famous",
                        "knowing",
                        "dumbledore",
                        "woken",
                        "hours",
                        "dursley",
                        "scream",
                        "dursley",
                        "opened",
                        "front",
                        "door",
                        "milk",
                        "bottles",
                        "dumbledore",
                        "spend",
                        "next",
                        "weeks",
                        "prodded",
                        "pinched",
                        "dumbledore",
                        "cousin",
                        "dudley",
                        "dumbledore",
                        "couldn",
                        "moment",
                        "people",
                        "meeting",
                        "secret",
                        "country",
                        "holding",
                        "people",
                        "glasses",
                        "saying",
                        "hushed",
                        "voices",
                        "harry",
                        "potter",
                        "lived"
                    ]
                ]
            ],
            [
                "Group 22",
                [
                    [
                        "suddenly",
                        "hagrid",
                        "howl",
                        "like",
                        "wounded",
                        "dog"
                    ]
                ]
            ],
            [
                "Group 23",
                [
                    [
                        "sun",
                        "rose",
                        "tidy",
                        "front",
                        "gardens",
                        "lit",
                        "brass",
                        "number",
                        "four",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "front",
                        "door",
                        "number",
                        "crept",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "living",
                        "room",
                        "almost",
                        "exactly",
                        "dursley",
                        "seen",
                        "fateful",
                        "news",
                        "report",
                        "owls"
                    ]
                ]
            ],
            [
                "Group 24",
                [
                    [
                        "ten",
                        "years",
                        "ago",
                        "lots",
                        "pictures",
                        "looked",
                        "like",
                        "large",
                        "pink",
                        "beach",
                        "ball",
                        "wearing",
                        "different",
                        "colored",
                        "bonnets",
                        "dudley",
                        "dursley",
                        "longer",
                        "baby",
                        "photographs",
                        "showed",
                        "large",
                        "blond",
                        "riding",
                        "bicycle",
                        "carousel",
                        "fair",
                        "playing",
                        "computer",
                        "father",
                        "hugged",
                        "kissed",
                        "mother"
                    ]
                ]
            ],
            [
                "Group 25",
                [
                    [
                        "tuft",
                        "jet",
                        "black",
                        "forehead",
                        "dumbledore",
                        "mcgonagall",
                        "curiously",
                        "shaped",
                        "cut",
                        "like",
                        "bolt",
                        "lightning"
                    ]
                ]
            ],
            [
                "Group 26",
                [
                    [
                        "vanishing",
                        "glass",
                        "nearly",
                        "ten",
                        "years",
                        "passed",
                        "since",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "woken",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "nephew",
                        "front",
                        "step",
                        "privet",
                        "drive",
                        "hardly",
                        "changed"
                    ]
                ]
            ],
            [
                "Group 27",
                [
                    [
                        "ve",
                        "business",
                        "staying"
                    ]
                ]
            ],
            [
                "Group 28",
                [
                    [
                        "well",
                        "dumbledore",
                        "finally"
                    ]
                ]
            ],
            [
                "Group 29",
                [
                    [
                        "well",
                        "dumbledore",
                        "hagrid",
                        "better",
                        "dumbledore",
                        "took",
                        "harry",
                        "harry",
                        "arms",
                        "turned",
                        "toward",
                        "dursley",
                        "dursley",
                        "dudley",
                        "dursley",
                        "house"
                    ]
                ]
            ],
            [
                "Group 30",
                [
                    [
                        "well",
                        "go",
                        "join",
                        "celebrations",
                        "hagrid",
                        "muffled",
                        "voice",
                        "ll",
                        "takin",
                        "sirius",
                        "sirius",
                        "bike",
                        "professor",
                        "mcgonagall",
                        "professor",
                        "dumbledore",
                        "sir",
                        "wiping",
                        "sirius",
                        "streaming",
                        "eyes",
                        "sirius",
                        "jacket",
                        "sleeve",
                        "hagrid",
                        "swung",
                        "hagrid",
                        "onto",
                        "motorcycle",
                        "kicked",
                        "engine",
                        "roar",
                        "engine",
                        "rose",
                        "air"
                    ]
                ]
            ],
            [
                "Group 31",
                [
                    [
                        "whispered",
                        "professor",
                        "mcgonagall"
                    ]
                ]
            ]
        ]
    }
}'''


# PREPROCESSED TASK 2

TASK_2_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,batty
Kquewanda Bailey,
Ballyfumble Stranger,"quin, quivering quintus, quintusofthesillyname"
"""
TASK_2_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
Ignatia Wildsmith,
Ignatius Prewett,
Ignatius Tuft,
Ignotus Peverell,
Igor Karkaroff,
Illyius,
Ingolfr the Iambic,
"""
TASK_2_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
"Magnus ""Dent Head"" Macdonald",
Magorian,
Maisie Cattermole,
Malcolm,
Malcolm Baddock,
Malcolm McGonagall,
Harold Skively,
Harper,
Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
Harvey Ridgebit,
Hassan Mostafa,
"""

# PREPROCESSED TASK 4

TASK_4_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
"""
TASK_4_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
"""
TASK_4_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
"""
TASK_4_EXAMPLE_4_NAMES_CSV_RAW = """Name,Other Names
"""

# PREPROCESSED TASK 5

TASK_5_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
Over-Attentive Wizard,
Bertram Aubrey,
Audrey Weasley,
"Augusta ""Gran"" Longbottom",Gran
Augustus Pye,
Augustus Rookwood,
Augustus Worme,
Auntie Muriel,
Aunt Marge Dursley,
Aurelius Dumbledore,
Aurora Sinistra,
Avery,
Babajide Akingbade,
Babayaga,
Babbitty Rabbitty,
Bagman Sr.,
Ludo Bagman,
Otto Bagman,
Millicent Bagnold,
Bathilda Bagshot,Batty
Kquewanda Bailey,
Ballyfumble Stranger,"Quin, Quivering Quintus, Quintus-Of-The-Silly-Name"
Harry Potter,"The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend"
Albus Dumbledore,
"""
TASK_5_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
Ignatia Wildsmith,
Ignatius Prewett,
Ignatius Tuft,
Ignotus Peverell,
Igor Karkaroff,
Illyius,
Ingolfr the Iambic,
"""
TASK_5_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
"Magnus ""Dent Head"" Macdonald",
Magorian,
Maisie Cattermole,
Malcolm,
Malcolm Baddock,
Malcolm McGonagall,
Harold Skively,
Harper,
Harry Potter,"the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend"
Harvey Ridgebit,
Hassan Mostafa,
"""
TASK_5_EXAMPLE_4_NAMES_CSV_RAW = """Name,Other Names
Abernathy,
Abraham Peasegood,
Abraham Potter,
Abraxas Malfoy,
Achilles Tolliver,
Stewart Ackerley,
"""

# PREPROCESSED TASK 9

TASK_9_EXAMPLE_1_NAMES_CSV_RAW = """Name,Other Names
"""
TASK_9_EXAMPLE_2_NAMES_CSV_RAW = """Name,Other Names
"""
TASK_9_EXAMPLE_3_NAMES_CSV_RAW = """Name,Other Names
"""



""" ___________________________TASK 1 TESTS______________________________________"""

def test_first_task_flow():


    # EXAMPLE 1:


    sentences_csv_path_exp_1 = create_temp_csv(TASK_1_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_1_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    expected_raw_json_result_exp_1 = TASK_1_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 2: 


    sentences_csv_path_exp_2 = create_temp_csv(TASK_1_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_1_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    expected_raw_json_result_exp_2 = TASK_1_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 3: 


    sentences_csv_path_exp_3 = create_temp_csv(TASK_1_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_1_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    expected_raw_json_result_exp_3 = TASK_1_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")
        

""" ___________________________TASK 2 TESTS______________________________________"""

def test_second_task_unprocessed_flow():

    # EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_2_EXAMPLE_1_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_2(sentences_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_2_EXAMPLE_1_MAXK)
    expected_raw_json_result_exp_1 = TASK_2_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 2: 


    sentences_csv_path_exp_2 = create_temp_csv(TASK_2_EXAMPLE_2_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_2(sentences_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_2_EXAMPLE_2_MAXK)
    expected_raw_json_result_exp_2 = TASK_2_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 3: 


    sentences_csv_path_exp_3 = create_temp_csv(TASK_2_EXAMPLE_3_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_2(sentences_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_2_EXAMPLE_3_MAXK)
    expected_raw_json_result_exp_3 = TASK_2_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")
        

def test_second_task_processed_flow():

    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_2_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_2_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_1_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    task_2_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_2_runner.run_task_2(None, None, TASK_2_EXAMPLE_1_MAXK)
    expected_raw_json_result_exp_1 = TASK_2_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1



    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_2_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_2_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_1_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    task_2_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_2_runner.run_task_2(None, None, TASK_2_EXAMPLE_2_MAXK)
    expected_raw_json_result_exp_2 = TASK_2_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2



    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_2_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_2_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_1_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    task_2_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_2_runner.run_task_2(None, None, TASK_2_EXAMPLE_3_MAXK)
    expected_raw_json_result_exp_3 = TASK_2_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3


""" ___________________________TASK 3 TESTS______________________________________"""

def test_third_task_unprocessed_flow():


    # EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_3_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_3_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_3(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    expected_raw_json_result_exp_1 = TASK_3_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 2: 


    sentences_csv_path_exp_2 = create_temp_csv(TASK_3_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 = create_temp_csv(TASK_3_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_3(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    expected_raw_json_result_exp_2 = TASK_3_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 3: 


    sentences_csv_path_exp_3 = create_temp_csv(TASK_3_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 = create_temp_csv(TASK_3_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_3(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    expected_raw_json_result_exp_3 = TASK_3_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
    # EXAMPLE 4: 


    sentences_csv_path_exp_4 = create_temp_csv(TASK_3_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 = create_temp_csv(TASK_3_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_4 = task_runner.run_task_3(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4)
    expected_raw_json_result_exp_4 = TASK_3_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")


def test_third_task_processed_flow():

    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_3_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_3_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_1_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    task_3_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_3_runner.run_task_3(None, None, None)
    expected_raw_json_result_exp_1 = TASK_3_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_3_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_3_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_1_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    task_3_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_3_runner.run_task_3(None, None, None)
    expected_raw_json_result_exp_2 = TASK_3_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_3_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_3_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_1_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    task_3_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_3_runner.run_task_3(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    expected_raw_json_result_exp_3 = TASK_3_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
    # PREP THE PREPROCESSED DATA - EXAMPLE 4:

    sentences_csv_path_exp_4 = create_temp_csv(TASK_3_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_3_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_4 = task_1_runner.run_task_1(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4)
    preprocessed_json_path_exp_4 = create_temp_json(preprocessed_json_data_result_exp_4)

    # EXAMPLE 4:

    task_3_runner = TaskRunner(True, preprocessed_json_path_exp_4)

    actual_json_result_exp_4 = task_3_runner.run_task_3(None, None, None)
    expected_raw_json_result_exp_4 = TASK_3_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
        os.remove(preprocessed_json_path_exp_4)
    except:
        print(f"Error: something went wrong.")


""" ___________________________TASK 4 TESTS______________________________________"""

def test_fourth_task_unprocessed_flow():
    
    # EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_4_EXAMPLE_1_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    kseq_keys_json_path_exp_1 =  create_temp_json(TASK_4_EXAMPLE_1_KSEQ_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_4(sentences_csv_path_exp_1, unwanted_words_csv_path_exp_1, kseq_keys_json_path_exp_1)
    expected_raw_json_result_exp_1 = TASK_4_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(kseq_keys_json_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 2: 


    sentences_csv_path_exp_2 = create_temp_csv(TASK_4_EXAMPLE_2_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    kseq_keys_json_path_exp_2 =  create_temp_json(TASK_4_EXAMPLE_2_KSEQ_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_4(sentences_csv_path_exp_2, unwanted_words_csv_path_exp_2, kseq_keys_json_path_exp_2)
    expected_raw_json_result_exp_2 = TASK_4_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(kseq_keys_json_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 3: 


    sentences_csv_path_exp_3 = create_temp_csv(TASK_4_EXAMPLE_3_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    kseq_keys_json_path_exp_3 =  create_temp_json(TASK_4_EXAMPLE_3_KSEQ_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_4(sentences_csv_path_exp_3, unwanted_words_csv_path_exp_3, kseq_keys_json_path_exp_3)
    expected_raw_json_result_exp_3 = TASK_4_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(kseq_keys_json_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 4: 


    sentences_csv_path_exp_4 = create_temp_csv(TASK_4_EXAMPLE_4_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    kseq_keys_json_path_exp_4 =  create_temp_json(TASK_4_EXAMPLE_4_KSEQ_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_4 = task_runner.run_task_4(sentences_csv_path_exp_4, unwanted_words_csv_path_exp_4, kseq_keys_json_path_exp_4)
    expected_raw_json_result_exp_4 = TASK_4_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(kseq_keys_json_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
    except:
        print(f"Error: something went wrong.")


def test_fourth_task_processed_flow():
    
    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_4_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_4_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_1_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    kseq_keys_json_path_exp_1 = create_temp_json(TASK_4_EXAMPLE_1_KSEQ_JSON_RAW)
    task_4_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_4_runner.run_task_4(None, None, kseq_keys_json_path_exp_1)
    expected_raw_json_result_exp_1 = TASK_4_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(kseq_keys_json_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_4_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_4_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_1_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    kseq_keys_json_path_exp_2 = create_temp_json(TASK_4_EXAMPLE_2_KSEQ_JSON_RAW)

    task_4_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_4_runner.run_task_4(None, None, kseq_keys_json_path_exp_2)
    expected_raw_json_result_exp_2 = TASK_4_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
        os.remove(kseq_keys_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_4_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_4_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_1_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:
    kseq_keys_json_path_exp_3 = create_temp_json(TASK_4_EXAMPLE_3_KSEQ_JSON_RAW)

    task_4_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_4_runner.run_task_4(None, None, kseq_keys_json_path_exp_3)
    expected_raw_json_result_exp_3 = TASK_4_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
        os.remove(kseq_keys_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
    # PREP THE PREPROCESSED DATA - EXAMPLE 4:

    sentences_csv_path_exp_4 = create_temp_csv(TASK_4_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_4_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_4 = task_1_runner.run_task_1(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4)
    preprocessed_json_path_exp_4 = create_temp_json(preprocessed_json_data_result_exp_4)

    # EXAMPLE 4:

    kseq_keys_json_path_exp_4 = create_temp_json(TASK_4_EXAMPLE_4_KSEQ_JSON_RAW)

    task_4_runner = TaskRunner(True, preprocessed_json_path_exp_4)

    actual_json_result_exp_4 = task_4_runner.run_task_4(None, None, kseq_keys_json_path_exp_4)
    expected_raw_json_result_exp_4 = TASK_4_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
        os.remove(preprocessed_json_path_exp_4)
        os.remove(kseq_keys_json_path_exp_4)
    except:
        print(f"Error: something went wrong.")


""" ___________________________TASK 5 TESTS______________________________________"""

def test_fifth_task_unprocessed_flow():
    

    # EXAMPLE 1:


    sentences_csv_path_exp_1 = create_temp_csv(TASK_5_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_5_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_5(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_5_EXAMPLE_1_MAXK)
    expected_raw_json_result_exp_1 = TASK_5_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 2:


    sentences_csv_path_exp_2 = create_temp_csv(TASK_5_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_5_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_5(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_5_EXAMPLE_2_MAXK)
    expected_raw_json_result_exp_2 = TASK_5_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 3:


    sentences_csv_path_exp_3 = create_temp_csv(TASK_5_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_5_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_5(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_5_EXAMPLE_3_MAXK)
    expected_raw_json_result_exp_3 = TASK_5_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 4:


    sentences_csv_path_exp_4 = create_temp_csv(TASK_5_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_5_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_4 = task_runner.run_task_5(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4, TASK_5_EXAMPLE_4_MAXK)
    expected_raw_json_result_exp_4 = TASK_5_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
    except:
        print(f"Error: something went wrong.")

def test_fifth_task_processed_flow():
    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_5_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_5_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_1_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    task_5_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_5_runner.run_task_5(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_5_EXAMPLE_1_MAXK)
    expected_raw_json_result_exp_1 = TASK_5_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_5_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_5_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_1_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    task_5_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_5_runner.run_task_5(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_5_EXAMPLE_2_MAXK)
    expected_raw_json_result_exp_2 = TASK_5_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_5_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_5_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_1_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    task_5_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_5_runner.run_task_5(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_5_EXAMPLE_3_MAXK)
    expected_raw_json_result_exp_3 = TASK_5_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
    # PREP THE PREPROCESSED DATA - EXAMPLE 4:

    sentences_csv_path_exp_4 = create_temp_csv(TASK_5_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_5_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_4 = task_1_runner.run_task_1(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4)
    preprocessed_json_path_exp_4 = create_temp_json(preprocessed_json_data_result_exp_4)

    # EXAMPLE 4:

    task_5_runner = TaskRunner(True, preprocessed_json_path_exp_4)

    actual_json_result_exp_4 = task_5_runner.run_task_5(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4, TASK_5_EXAMPLE_4_MAXK)
    expected_raw_json_result_exp_4 = TASK_5_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
        os.remove(preprocessed_json_path_exp_4)
    except:
        print(f"Error: something went wrong.")

""" ___________________________TASK 6 TESTS______________________________________"""

def test_sixth_task_unprocessed_flow():
    

    # EXAMPLE 1:


    sentences_csv_path_exp_1 = create_temp_csv(TASK_6_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_6_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_6(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_6_EXAMPLE_1_WINDOW_SIZE, TASK_6_EXAMPLE_1_TRESHOLD)
    expected_raw_json_result_exp_1 = TASK_6_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 2:


    sentences_csv_path_exp_2 = create_temp_csv(TASK_6_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_6_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_6(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_6_EXAMPLE_2_WINDOW_SIZE, TASK_6_EXAMPLE_2_TRESHOLD)
    expected_raw_json_result_exp_2 = TASK_6_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 3:


    sentences_csv_path_exp_3 = create_temp_csv(TASK_6_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_6_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_6(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_6_EXAMPLE_3_WINDOW_SIZE, TASK_6_EXAMPLE_3_TRESHOLD)
    expected_raw_json_result_exp_3 = TASK_6_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 4:


    sentences_csv_path_exp_4 = create_temp_csv(TASK_6_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_6_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    

    task_runner = TaskRunner()

    actual_json_result_exp_4 = task_runner.run_task_6(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4, TASK_6_EXAMPLE_4_WINDOW_SIZE, TASK_6_EXAMPLE_4_TRESHOLD)
    expected_raw_json_result_exp_4 = TASK_6_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
    except:
        print(f"Error: something went wrong.")

def test_sixth_task_processed_flow():


    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_6_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_6_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_1_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    task_6_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_6_runner.run_task_6(None, None, None, TASK_6_EXAMPLE_1_WINDOW_SIZE, TASK_6_EXAMPLE_1_TRESHOLD)
    expected_raw_json_result_exp_1 = TASK_6_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1


    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_6_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_6_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_1_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    task_6_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_6_runner.run_task_6(None, None, None, TASK_6_EXAMPLE_2_WINDOW_SIZE, TASK_6_EXAMPLE_2_TRESHOLD)
    expected_raw_json_result_exp_2 = TASK_6_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_6_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_6_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_1_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    task_6_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_6_runner.run_task_6(None, None, None, TASK_6_EXAMPLE_3_WINDOW_SIZE, TASK_6_EXAMPLE_3_TRESHOLD)
    expected_raw_json_result_exp_3 = TASK_6_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
    # PREP THE PREPROCESSED DATA - EXAMPLE 4:

    sentences_csv_path_exp_4 = create_temp_csv(TASK_6_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_6_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_4 = task_1_runner.run_task_1(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4)
    preprocessed_json_path_exp_4 = create_temp_json(preprocessed_json_data_result_exp_4)

    # EXAMPLE 4:

    task_6_runner = TaskRunner(True, preprocessed_json_path_exp_4)

    actual_json_result_exp_4 = task_6_runner.run_task_6(None, None, None, TASK_6_EXAMPLE_4_WINDOW_SIZE, TASK_6_EXAMPLE_4_TRESHOLD)
    expected_raw_json_result_exp_4 = TASK_6_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
        os.remove(preprocessed_json_path_exp_4)
    except:
        print(f"Error: something went wrong.")

""" ___________________________TASK 7 TESTS______________________________________"""

def test_seventh_task_unprocessed_flow():
    

    # EXAMPLE 1:


    sentences_csv_path_exp_1 = create_temp_csv(TASK_7_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_7_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_1 = create_temp_json(TASK_7_EXAMPLE_1_CONNECTIONS_JSON_RAW)
    

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_7(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_7_EXAMPLE_1_WINDOW_SIZE, TASK_7_EXAMPLE_1_TRESHOLD, connections_json_path_exp_1, TASK_7_EXAMPLE_1_MAX_DISTANCE)
    expected_raw_json_result_exp_1 = TASK_7_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(connections_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 2:


    sentences_csv_path_exp_2 = create_temp_csv(TASK_7_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_7_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_2 = create_temp_json(TASK_7_EXAMPLE_2_CONNECTIONS_JSON_RAW)
    
    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_7(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_7_EXAMPLE_2_WINDOW_SIZE, TASK_7_EXAMPLE_2_TRESHOLD, connections_json_path_exp_2, TASK_7_EXAMPLE_2_MAX_DISTANCE)
    expected_raw_json_result_exp_2 = TASK_7_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(connections_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 3:


    sentences_csv_path_exp_3 = create_temp_csv(TASK_7_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_7_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_3 = create_temp_json(TASK_7_EXAMPLE_3_CONNECTIONS_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_7(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_7_EXAMPLE_3_WINDOW_SIZE, TASK_7_EXAMPLE_3_TRESHOLD, connections_json_path_exp_3, TASK_7_EXAMPLE_3_MAX_DISTANCE)
    expected_raw_json_result_exp_3 = TASK_7_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(connections_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 4:


    sentences_csv_path_exp_4 = create_temp_csv(TASK_7_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_7_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_4 = create_temp_json(TASK_7_EXAMPLE_4_CONNECTIONS_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_4 = task_runner.run_task_7(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4, TASK_7_EXAMPLE_4_WINDOW_SIZE, TASK_7_EXAMPLE_4_TRESHOLD, connections_json_path_exp_4, TASK_7_EXAMPLE_4_MAX_DISTANCE)
    expected_raw_json_result_exp_4 = TASK_7_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
        os.remove(connections_json_path_exp_4)
    except:
        print(f"Error: something went wrong.")


def test_seventh_task_processed_flow():
    
    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_7_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_7_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_6_runner.run_task_6(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_7_EXAMPLE_1_WINDOW_SIZE, TASK_7_EXAMPLE_1_TRESHOLD)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    connections_json_path_exp_1 = create_temp_json(TASK_7_EXAMPLE_1_CONNECTIONS_JSON_RAW)

    task_7_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_7_runner.run_task_7(None, None, None, TASK_7_EXAMPLE_1_WINDOW_SIZE, TASK_7_EXAMPLE_1_TRESHOLD, connections_json_path_exp_1, TASK_7_EXAMPLE_1_MAX_DISTANCE)
    expected_raw_json_result_exp_1 = TASK_7_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1


    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
        os.remove(connections_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_7_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_7_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_6_runner.run_task_6(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_7_EXAMPLE_2_WINDOW_SIZE, TASK_7_EXAMPLE_2_TRESHOLD)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    connections_json_path_exp_2 = create_temp_json(TASK_7_EXAMPLE_2_CONNECTIONS_JSON_RAW)
    
    task_7_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_7_runner.run_task_7(None, None, None, TASK_7_EXAMPLE_2_WINDOW_SIZE, TASK_7_EXAMPLE_2_TRESHOLD, connections_json_path_exp_2, TASK_7_EXAMPLE_2_MAX_DISTANCE)
    expected_raw_json_result_exp_2 = TASK_7_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_7_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_7_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_6_runner.run_task_6(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_7_EXAMPLE_3_WINDOW_SIZE, TASK_7_EXAMPLE_3_TRESHOLD)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    connections_json_path_exp_3 = create_temp_json(TASK_7_EXAMPLE_3_CONNECTIONS_JSON_RAW)
    
    task_7_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_7_runner.run_task_7(None, None, None, TASK_7_EXAMPLE_3_WINDOW_SIZE, TASK_7_EXAMPLE_3_TRESHOLD, connections_json_path_exp_3, TASK_7_EXAMPLE_3_MAX_DISTANCE)
    expected_raw_json_result_exp_3 = TASK_7_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
        os.remove(connections_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
    # PREP THE PREPROCESSED DATA - EXAMPLE 4:

    sentences_csv_path_exp_4 = create_temp_csv(TASK_7_EXAMPLE_4_SENTENCES_CSV_RAW)
    names_csv_path_exp_4 =  create_temp_csv(TASK_7_EXAMPLE_4_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_4 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_4 = task_6_runner.run_task_6(sentences_csv_path_exp_4, names_csv_path_exp_4, unwanted_words_csv_path_exp_4, TASK_7_EXAMPLE_4_WINDOW_SIZE, TASK_7_EXAMPLE_4_TRESHOLD)
    preprocessed_json_path_exp_4 = create_temp_json(preprocessed_json_data_result_exp_4)

    # EXAMPLE 4:

    connections_json_path_exp_4 = create_temp_json(TASK_7_EXAMPLE_4_CONNECTIONS_JSON_RAW)
    
    task_7_runner = TaskRunner(True, preprocessed_json_path_exp_4)

    actual_json_result_exp_4 = task_7_runner.run_task_7(None, None, None, TASK_7_EXAMPLE_4_WINDOW_SIZE, TASK_7_EXAMPLE_4_TRESHOLD, connections_json_path_exp_4, TASK_7_EXAMPLE_4_MAX_DISTANCE)
    expected_raw_json_result_exp_4 = TASK_7_EXAMPLE_4_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_4 = json.loads(expected_raw_json_result_exp_4)
    expected_json_result_exp_4 = json.dumps(loaded_json_data_exp_4, indent=JSON_INDENT)
    assert actual_json_result_exp_4 == expected_json_result_exp_4

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_4)
        os.remove(names_csv_path_exp_4)
        os.remove(unwanted_words_csv_path_exp_4)
        os.remove(preprocessed_json_path_exp_4)
        os.remove(connections_json_path_exp_4)
    except:
        print(f"Error: something went wrong.")
    

    
""" ___________________________TASK 8 TESTS______________________________________"""

def test_eighth_task_unprocessed_flow():


    # EXAMPLE 1:


    sentences_csv_path_exp_1 = create_temp_csv(TASK_8_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_8_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_1 = create_temp_json(TASK_8_EXAMPLE_1_CONNECTIONS_JSON_RAW)
    

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_8(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_8_EXAMPLE_1_WINDOW_SIZE, TASK_8_EXAMPLE_1_TRESHOLD, connections_json_path_exp_1, TASK_8_EXAMPLE_1_EXC_DISTANCE)
    expected_raw_json_result_exp_1 = TASK_8_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(connections_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 2:


    sentences_csv_path_exp_2 = create_temp_csv(TASK_8_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_8_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_2 = create_temp_json(TASK_8_EXAMPLE_2_CONNECTIONS_JSON_RAW)
    
    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_8(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_8_EXAMPLE_2_WINDOW_SIZE, TASK_8_EXAMPLE_2_TRESHOLD, connections_json_path_exp_2, TASK_8_EXAMPLE_2_EXC_DISTANCE)
    expected_raw_json_result_exp_2 = TASK_8_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(connections_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")
    

    # EXAMPLE 3:


    sentences_csv_path_exp_3 = create_temp_csv(TASK_8_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_8_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    connections_json_path_exp_3 = create_temp_json(TASK_8_EXAMPLE_3_CONNECTIONS_JSON_RAW)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_8(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_8_EXAMPLE_3_WINDOW_SIZE, TASK_8_EXAMPLE_3_TRESHOLD, connections_json_path_exp_3, TASK_8_EXAMPLE_3_EXC_DISTANCE)
    expected_raw_json_result_exp_3 = TASK_8_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(connections_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

def test_eighth_task_processed_flow():
    
    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_8_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_8_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_6_runner.run_task_6(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_8_EXAMPLE_1_WINDOW_SIZE, TASK_8_EXAMPLE_1_TRESHOLD)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    connections_json_path_exp_1 = create_temp_json(TASK_8_EXAMPLE_1_CONNECTIONS_JSON_RAW)

    task_8_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_8_runner.run_task_8(None, None, None, TASK_8_EXAMPLE_1_WINDOW_SIZE, TASK_8_EXAMPLE_1_TRESHOLD, connections_json_path_exp_1, TASK_8_EXAMPLE_1_EXC_DISTANCE)
    expected_raw_json_result_exp_1 = TASK_8_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1


    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
        os.remove(connections_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_8_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_8_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_6_runner.run_task_6(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_8_EXAMPLE_2_WINDOW_SIZE, TASK_8_EXAMPLE_2_TRESHOLD)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    connections_json_path_exp_2 = create_temp_json(TASK_8_EXAMPLE_2_CONNECTIONS_JSON_RAW)
    
    task_8_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_8_runner.run_task_8(None, None, None, TASK_8_EXAMPLE_2_WINDOW_SIZE, TASK_8_EXAMPLE_2_TRESHOLD, connections_json_path_exp_2, TASK_8_EXAMPLE_2_EXC_DISTANCE)
    expected_raw_json_result_exp_2 = TASK_8_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_8_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_8_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_6_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_6_runner.run_task_6(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_8_EXAMPLE_3_WINDOW_SIZE, TASK_8_EXAMPLE_3_TRESHOLD)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    connections_json_path_exp_3 = create_temp_json(TASK_8_EXAMPLE_3_CONNECTIONS_JSON_RAW)
    
    task_8_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_8_runner.run_task_8(None, None, None, TASK_8_EXAMPLE_3_WINDOW_SIZE, TASK_8_EXAMPLE_3_TRESHOLD, connections_json_path_exp_3, TASK_8_EXAMPLE_3_EXC_DISTANCE)
    expected_raw_json_result_exp_3 = TASK_8_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
        os.remove(connections_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")

    
""" ___________________________TASK 9 TESTS______________________________________"""   

def test_nineth_task_unprocessed_flow():
    

    # EXAMPLE 1:


    sentences_csv_path_exp_1 = create_temp_csv(TASK_2_EXAMPLE_1_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_1 = task_runner.run_task_9(sentences_csv_path_exp_1, unwanted_words_csv_path_exp_1, TASK_9_EXAMPLE_1_TRESHOLD)
    expected_raw_json_result_exp_1 = TASK_9_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 2: 


    sentences_csv_path_exp_2 = create_temp_csv(TASK_9_EXAMPLE_2_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_2 = task_runner.run_task_9(sentences_csv_path_exp_2, unwanted_words_csv_path_exp_2, TASK_9_EXAMPLE_2_TRESHOLD)
    expected_raw_json_result_exp_2 = TASK_9_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
    except:
        print(f"Error: something went wrong.")
        

    # EXAMPLE 3: 


    sentences_csv_path_exp_3 = create_temp_csv(TASK_9_EXAMPLE_3_SENTENCES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)

    task_runner = TaskRunner()

    actual_json_result_exp_3 = task_runner.run_task_9(sentences_csv_path_exp_3, unwanted_words_csv_path_exp_3, TASK_9_EXAMPLE_3_TRESHOLD)
    expected_raw_json_result_exp_3 = TASK_9_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
    except:
        print(f"Error: something went wrong.")

def test_nineth_task_processed_flow():
    # PREP THE PREPROCESSED DATA - EXAMPLE 1:

    sentences_csv_path_exp_1 = create_temp_csv(TASK_9_EXAMPLE_1_SENTENCES_CSV_RAW)
    names_csv_path_exp_1 =  create_temp_csv(TASK_9_EXAMPLE_1_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_1 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_1 = task_1_runner.run_task_1(sentences_csv_path_exp_1, names_csv_path_exp_1, unwanted_words_csv_path_exp_1)
    preprocessed_json_path_exp_1 = create_temp_json(preprocessed_json_data_result_exp_1)

    # EXAMPLE 1:

    task_9_runner = TaskRunner(True, preprocessed_json_path_exp_1)

    actual_json_result_exp_1 = task_9_runner.run_task_9(None, None, TASK_9_EXAMPLE_1_TRESHOLD)
    expected_raw_json_result_exp_1 = TASK_9_EXAMPLE_1_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_1 = json.loads(expected_raw_json_result_exp_1)
    expected_json_result_exp_1 = json.dumps(loaded_json_data_exp_1, indent=JSON_INDENT)
    assert actual_json_result_exp_1 == expected_json_result_exp_1

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_1)
        os.remove(names_csv_path_exp_1)
        os.remove(unwanted_words_csv_path_exp_1)
        os.remove(preprocessed_json_path_exp_1)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 2:

    sentences_csv_path_exp_2 = create_temp_csv(TASK_9_EXAMPLE_2_SENTENCES_CSV_RAW)
    names_csv_path_exp_2 =  create_temp_csv(TASK_9_EXAMPLE_2_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_2 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_2 = task_1_runner.run_task_1(sentences_csv_path_exp_2, names_csv_path_exp_2, unwanted_words_csv_path_exp_2)
    preprocessed_json_path_exp_2 = create_temp_json(preprocessed_json_data_result_exp_2)

    # EXAMPLE 2:

    task_9_runner = TaskRunner(True, preprocessed_json_path_exp_2)

    actual_json_result_exp_2 = task_9_runner.run_task_9(None, None, TASK_9_EXAMPLE_2_TRESHOLD)
    expected_raw_json_result_exp_2 = TASK_9_EXAMPLE_2_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_2 = json.loads(expected_raw_json_result_exp_2)
    expected_json_result_exp_2 = json.dumps(loaded_json_data_exp_2, indent=JSON_INDENT)
    assert actual_json_result_exp_2 == expected_json_result_exp_2

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_2)
        os.remove(names_csv_path_exp_2)
        os.remove(unwanted_words_csv_path_exp_2)
        os.remove(preprocessed_json_path_exp_2)
    except:
        print(f"Error: something went wrong.")


    # PREP THE PREPROCESSED DATA - EXAMPLE 3:

    sentences_csv_path_exp_3 = create_temp_csv(TASK_9_EXAMPLE_3_SENTENCES_CSV_RAW)
    names_csv_path_exp_3 =  create_temp_csv(TASK_9_EXAMPLE_3_NAMES_CSV_RAW)
    unwanted_words_csv_path_exp_3 = create_temp_csv(WORDS_TO_REMOVE_RAW_DATA)
    
    task_1_runner = TaskRunner()
    preprocessed_json_data_result_exp_3 = task_1_runner.run_task_1(sentences_csv_path_exp_3, names_csv_path_exp_3, unwanted_words_csv_path_exp_3)
    preprocessed_json_path_exp_3 = create_temp_json(preprocessed_json_data_result_exp_3)

    # EXAMPLE 3:

    task_9_runner = TaskRunner(True, preprocessed_json_path_exp_3)

    actual_json_result_exp_3 = task_9_runner.run_task_9(None, None, TASK_9_EXAMPLE_3_TRESHOLD)
    expected_raw_json_result_exp_3 = TASK_9_EXAMPLE_3_EXPECTED_JSON_RESULT_RAW

    loaded_json_data_exp_3 = json.loads(expected_raw_json_result_exp_3)
    expected_json_result_exp_3 = json.dumps(loaded_json_data_exp_3, indent=JSON_INDENT)
    assert actual_json_result_exp_3 == expected_json_result_exp_3

    # Clean-up:
    try:
        # Try deleting the temporary csv files
        os.remove(sentences_csv_path_exp_3)
        os.remove(names_csv_path_exp_3)
        os.remove(unwanted_words_csv_path_exp_3)
        os.remove(preprocessed_json_path_exp_3)
    except:
        print(f"Error: something went wrong.")


""" ___________________________HELPERS FUNCS______________________________________"""   

def create_temp_csv(csv_raw_data: str):
    # Create a temporary CSV file with a custom name
    with tempfile.NamedTemporaryFile(mode='w', newline='', prefix="custom_csv_", suffix=".csv", delete=False) as temp_file:
        temp_file.write(csv_raw_data)
    
    # Return the name for future uses of the file
    return temp_file.name


def create_temp_json(json_raw_txt_data: str):
    # Create a temporary JSON file with a custom name
    json_data = json.loads(json_raw_txt_data)
    with tempfile.NamedTemporaryFile(mode='w', newline='', prefix="custom_json_", suffix=".json", delete=False) as temp_file:
        json.dump(json_data, temp_file)
    
    # Return the name for future uses of the file
    return temp_file.name
































""" 
__________________ TESTS FOR GRAPH ___________________
"""

# Helper function to create a graph with nodes and edges
def create_test_graph_simple():
    graph = Graph()
    # Add some nodes to the graph
    node_a = Node("A", ["value1"])
    node_b = Node("B", ["value2"])
    node_c = Node("C", ["value3"])
    node_d = Node("D", ["value4"])

    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)

    # Create some edges
    graph.create_edge_between_nodes_by_keys("A", "B")
    graph.create_edge_between_nodes_by_keys("A", "C")
    graph.create_edge_between_nodes_by_keys("B", "C")
    graph.create_edge_between_nodes_by_keys("C", "D")

    return graph

# Helper function to create a graph with nodes and edges
def create_test_graph_hard():
    graph = Graph()
    # Add some nodes to the graph
    node_a = Node("A", ["value1"])
    node_b = Node("B", ["value2"])
    node_c = Node("C", ["value3"])
    node_d = Node("D", ["value4"])
    node_e = Node("E", ["value5"])
    node_f = Node("F", ["value6"])
    
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)
    graph.add_node(node_e)
    graph.add_node(node_f)

    # Create some edges
    graph.create_edge_between_nodes_by_keys("A", "B")
    graph.create_edge_between_nodes_by_keys("A", "C")
    graph.create_edge_between_nodes_by_keys("B", "C")
    graph.create_edge_between_nodes_by_keys("C", "D")
    graph.create_edge_between_nodes_by_keys("A", "E")
    graph.create_edge_between_nodes_by_keys("E", "F")
    graph.create_edge_between_nodes_by_keys("F", "C")

    return graph

# Test adding nodes to the graph
def test_add_node():
    graph = Graph()
    node_a = Node("A", ["value1"])
    assert graph.add_node(node_a) == True  # Node A added
    assert graph.add_node(node_a) == False  # Node A already exists

# Test creating edges between nodes
def test_create_edge_between_nodes():
    graph = create_test_graph_simple()
    
    # Test creating an edge that already exists (the weight should increment)
    assert graph.create_edge_between_nodes_by_keys("A", "B") == True
    edge = graph.get_edge_by_node_keys("A", "B")
    assert edge.weight == 2  # Edge weight should have been incremented
    
    # Test creating an edge between two non-existent nodes
    assert graph.create_edge_between_nodes_by_keys("X", "Y") == False  # Both nodes do not exist

# Test the `get_edge_by_node_keys` method
def test_get_edge_by_node_keys():
    graph = create_test_graph_simple()
    edge = graph.get_edge_by_node_keys("A", "B")
    assert edge != None
    assert edge.weight == 1
    
    # Non-existing edge
    edge = graph.get_edge_by_node_keys("A", "D")
    assert edge == None

# Test connected components
def test_get_connected_components():
    graph = create_test_graph_simple()
    connected_components = graph.get_connected_componnets()
    assert len(connected_components) == 1  # All nodes are in one connected component

# Test `directly_linked` method
def test_directly_linked():
    graph = create_test_graph_simple()
    node_a = graph.nodes["A"]
    node_b = graph.nodes["B"]
    node_c = graph.nodes["C"]
    node_d = graph.nodes["D"]
    
    # Test direct linkage with threshold of 1
    assert graph.directly_linked(node_a, node_b, threshold=1) == True
    assert graph.directly_linked(node_a, node_d, threshold=1) == False
    assert graph.directly_linked(node_a, node_c, threshold=2) == False

# Test `path_exists_up_to_length` method
def test_path_exists_up_to_length():
    graph = create_test_graph_simple()
    assert True == True
    # Path exists between A and D with max 2 edges
    assert graph.path_exists_up_to_length("A", "D", threshold=1, max_length=2) == True
    # Path exists between A and D with max 1 edge
    assert graph.path_exists_up_to_length("A", "D", threshold=1, max_length=1) == False
    # Path doesn't exist between A and D with max 1 edge (wrong threshold)
    assert graph.path_exists_up_to_length("A", "D", threshold=2, max_length=1) == False

# Test `path_exists_exact_length` method
def test_exact_length():
    graph = create_test_graph_hard()
    assert len(graph.nodes) == 6
    res = graph.path_exists_exact_length("A", "D", 1, 2)
    assert res == True
    res = graph.path_exists_exact_length("A", "D", 1, 3)
    assert res == True
    res = graph.path_exists_exact_length("A", "D", 1, 4)
    assert res == True

# Test `link_all_names_in_window` method
def test_link_all_names_in_window():
    graph = Graph()
    node_a = Node("A", ["value1"])
    node_b = Node("B", ["value2"])
    node_c = Node("C", ["value3"])
    
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    
    names_list = ["A", "B", "C"]
    graph.link_all_names_in_window(names_list)

    # Check if all nodes are connected
    edge_ab = graph.get_edge_by_node_keys("A", "B")
    edge_ac = graph.get_edge_by_node_keys("A", "C")
    edge_bc = graph.get_edge_by_node_keys("B", "C")

    assert edge_ab is not None
    assert edge_ac is not None
    assert edge_bc is not None


"""_____TEST EXCTRACTING FUNCS______"""

# Mock data for testing
mock_data_question_1 = {
    "Question 1": {
        "Processed Sentences": [["This", "is", "a", "test"]],
        "Processed Names": [
            [["John", "Doe"], ["Johnny", "JD"]],
            [["Jane", "Smith"], ["Janey"]]
        ],
    },
}

mock_data_query_keys = {
    "keys":
    [
		["first", "key"],
        ["second", "key"]
    ]
}


# Test 1: Test extracting processed sentences
def test_extract_processed_sentences():
    json_file_path = create_temp_json(json.dumps(mock_data_question_1))
    handler = PreProcessedHandler(json_file_path)
    
    processed_sentences = handler.extract_processed_sentences()
    
    assert processed_sentences == [["This", "is", "a", "test"]]
    
    # Clean up the temporary file
    try:
        os.remove(json_file_path)
    except:
        print("Error.")

# Test 2: Test extracting processed names
def test_extract_processed_names():
    json_file_path = create_temp_json(json.dumps(mock_data_question_1))
    handler = PreProcessedHandler(json_file_path)
    
    processed_names = handler.extract_processed_names()
    
    assert processed_names == [
        [["John", "Doe"], ["Johnny", "JD"]],
        [["Jane", "Smith"], ["Janey"]]
    ]
    
    # Clean up the temporary file
    try:
        os.remove(json_file_path)
    except:
        print("Error.")

# Test 3: Test extracting query keys
def test_extract_query_keys():
    json_file_path = create_temp_json(json.dumps(mock_data_query_keys))
    handler = PreProcessedHandler(json_file_path)
    
    query_keys = handler.extract_query_keys()
    
    assert query_keys == [
		["first", "key"],
        ["second", "key"]
    ]
    
    # Clean up the temporary file
    try:
        os.remove(json_file_path)
    except:
        print("Error.")





"""________TESTS FOR VALIDATING FUNCS:______"""

# TASK 1 VALID AGS: 

# Test case 1: One or more paths are missing
def test_missing_sentences_path_task_1_args():
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_1_arguments('', names_csv, remove_words_csv)
    assert result is False  # Invalid case: Missing sentences path

def test_missing_names_path_task_1_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_1_arguments(sentences_csv, '', remove_words_csv)
    assert result is False  # Invalid case: Missing names path

def test_missing_remove_words_path_task_1_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    
    result = valid_task_1_arguments(sentences_csv, names_csv, '')
    assert result is False  # Invalid case: Missing remove words path


# Test case 2: One or more paths are invalid CSVs
def test_invalid_sentences_path_task_1_args():
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    
    result = valid_task_1_arguments('invalidpath.csv', names_csv, remove_words_csv)
    assert result is False  # Invalid case: Invalid sentences path

def test_invalid_names_path_task_1_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_1_arguments(sentences_csv, 'invalidpath.csv', remove_words_csv)
    assert result is False  # Invalid case: Invalid names path

def test_invalid_remove_words_path_task_1_args():
    # Create a temporary invalid file (non-CSV)
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")

    result = valid_task_1_arguments(sentences_csv, names_csv, 'invalidpath.csv')
    assert result is False  # Invalid case: Invalid remove words path

# Test case 3: All paths are valid CSVs
def test_valid_paths_task_1_args():
    # Create valid temporary CSV files for each path
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_1_arguments(sentences_csv, names_csv, remove_words_csv)
    assert result is True  # Valid case: All paths are correct

# TASK 2 VALID AGS: 

# Test case 1: Valid preprocessed_path and maximal_kseq
def test_valid_preprocessed_path_and_maximal_kseq_task_2_args():
    # Create a valid JSON file for preprocessed_path
    preprocessed_json = create_temp_json('{"key": "value"}')
    result = valid_task_2_arguments(preprocessed_json, None, None, 10)
    assert result is True  # Valid case: Preprocessed path and maximal_kseq are valid


# Test case 2: Invalid preprocessed_path or invalid maximal_kseq
def test_invalid_preprocessed_path_task_2_args():
    result = valid_task_2_arguments('invalid_path.txt', None, None, 10)
    assert result is False  # Invalid case: Invalid preprocessed_path (not a JSON)

def test_invalid_maximal_kseq_valid_preprocessed_task_2_args():
    # Create a valid JSON file for preprocessed_path
    preprocessed_json = create_temp_json('{"key": "value"}')
    result = valid_task_2_arguments(preprocessed_json, None, None, -5)  # Invalid kseq
    assert result is False  # Invalid case: maximal_kseq is not valid


# Test case 3: Valid CSV paths and valid maximal_kseq when preprocessed_path is not provided
def test_valid_csv_paths_and_maximal_kseq_task_2_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    result = valid_task_2_arguments(None, sentences_csv, remove_words_csv, 10)
    assert result is True  # Valid case: All paths are valid CSVs and maximal_kseq is valid


# Test case 4: Invalid CSV paths or invalid maximal_kseq when preprocessed_path is not provided
def test_invalid_sentences_path_task_2_args():
    invalid_file = tempfile.NamedTemporaryFile(mode='w', newline='', prefix="invalid_", suffix=".txt", delete=False)
    invalid_file.close()  # Close the file after creation
    result = valid_task_2_arguments(None, invalid_file.name, 'remove_words.csv', 10)
    assert result is False  # Invalid case: sentences path is invalid

def test_invalid_remove_words_path_task_2_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")

    result = valid_task_2_arguments(None, sentences_csv, 'invalidfile.csv', 10)
    assert result is False  # Invalid case: remove words path is invalid

def test_invalid_maximal_kseq_task_2_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_2_arguments(None, sentences_csv, remove_words_csv, -5)  # Invalid kseq
    assert result is False  # Invalid case: maximal_kseq is not valid


# Test case 5: Missing required paths or invalid maximal_kseq
def test_missing_arguments_task_2_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_2_arguments(None, None, None, 10)  # Missing all paths
    assert result is False  # Invalid case: Missing paths
    result = valid_task_2_arguments(None, sentences_csv, None, 10)  # Missing remove_words_path
    assert result is False  # Invalid case: Missing remove_words_path
    result = valid_task_2_arguments(None, None, remove_words_csv, 10)  # Missing sentences_path
    assert result is False  # Invalid case: Missing sentences_path


# TASK 3 VALID ARGS: 

# Test case 1: Valid preprocessed path
def test_valid_preprocessed_path_task_3_args():
    # Create a valid JSON file for preprocessed_path
    preprocessed_json = create_temp_json('{"key": "value"}')
    
    result = valid_task_3_arguments(preprocessed_json, None, None, None)
    assert result is True  # Valid case: Preprocessed path is valid


# Test case 2: Invalid preprocessed path
def test_invalid_preprocessed_path_task_3_args():
    result = valid_task_3_arguments('invalid_path.txt', None, None, None)
    assert result is False  # Invalid case: Invalid preprocessed_path (not a JSON)


# Test case 3: Valid CSV paths when preprocessed_path is not provided
def test_valid_csv_paths_task_3_args():
    # Create valid temporary CSV files for each path
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_3_arguments(None, sentences_csv, names_csv, remove_words_csv)
    assert result is True  # Valid case: All paths are correct CSVs


# Test case 4: Invalid CSV paths when preprocessed_path is not provided
def test_invalid_sentences_path_task_3_args():
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_3_arguments(None, 'invalidfile.csv', names_csv, remove_words_csv)
    assert result is False  # Invalid case: sentences path is invalid

def test_invalid_names_path_task_3_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_3_arguments(None, sentences_csv, 'invalidfile.csv', remove_words_csv)
    assert result is False  # Invalid case: names path is invalid

def test_invalid_remove_words_path_task_3_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    result = valid_task_3_arguments(None, sentences_csv, names_csv, 'invalidfile.csv')
    assert result is False  # Invalid case: remove words path is invalid


# Test case 5: Missing paths or invalid paths when preprocessed_path is not provided
def test_missing_paths_task_3_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_3_arguments(None, None, None, None)  # Missing all paths
    assert result is False  # Invalid case: Missing paths
    
    result = valid_task_3_arguments(None, sentences_csv, None, None)  # Missing names and remove_words paths
    assert result is False  # Invalid case: Missing names and remove_words paths
    
    result = valid_task_3_arguments(None, None, names_csv, None)  # Missing sentences and remove_words paths
    assert result is False  # Invalid case: Missing sentences and remove_words paths

    result = valid_task_3_arguments(None, None, None, remove_words_csv)  # Missing sentences and remove_words paths
    assert result is False  # Invalid case: Missing sentences and remove_words paths


# Test case 6: Missing one of the CSV paths (when preprocessed_path is not provided)
def test_missing_one_csv_path_task_3_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    
    result = valid_task_3_arguments(None, sentences_csv, names_csv, None)  # Missing remove_words path
    assert result is False  # Invalid case: Missing remove_words path


# TASK 4 VALID ARGS:

# Test case 1: Valid preprocessed_path and kseq_list_path (both JSON)
def test_valid_preprocessed_and_kseq_list_paths_task_4_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    kseq_json = create_temp_json('{"kseq": [1, 2, 3]}')
    
    result = valid_task_4_arguments(preprocessed_json, None, None, kseq_json)
    assert result is True  # Valid case: Preprocessed and kseq_list paths are valid JSON


# Test case 2: Invalid preprocessed_path or kseq_list_path
def test_invalid_preprocessed_path_task_4_args():
    kseq_json = create_temp_json('{"kseq": [1, 2, 3]}')
    
    result = valid_task_4_arguments('invalidfile.txt', None, None, kseq_json)
    assert result is False  # Invalid case: Invalid preprocessed_path (not a JSON)


def test_invalid_kseq_list_path_valid_preprocessed_task_4_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    
    result = valid_task_4_arguments(preprocessed_json, None, None, 'invalidfile.txt')
    assert result is False  # Invalid case: Invalid kseq_list_path (not a JSON)


# Test case 3: Valid CSV paths and kseq_list_path (JSON)
def test_valid_csv_paths_and_kseq_list_path_task_4_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    kseq_json = create_temp_json('{"kseq": [1, 2, 3]}')
    
    result = valid_task_4_arguments(None, sentences_csv, remove_words_csv, kseq_json)
    assert result is True  # Valid case: All paths are correct CSVs and kseq_list_path is valid JSON


# Test case 4: Invalid CSV paths or invalid kseq_list_path (when preprocessed_path is not provided)
def test_invalid_sentences_path_task_4_args():
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    seq_json = create_temp_json('{"kseq": [1, 2, 3]}')
    
    result = valid_task_4_arguments(None, 'invalidname.csv', remove_words_csv, seq_json)
    assert result is False  # Invalid case: sentences path is invalid

def test_invalid_remove_words_path_task_4_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    kseq_json = create_temp_json('{"kseq": [1, 2, 3]}')
    
    result = valid_task_4_arguments(None, sentences_csv, 'invalidfile.csv', kseq_json)
    assert result is False  # Invalid case: remove words path is invalid

def test_invalid_kseq_list_path_task_4_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_4_arguments(None, sentences_csv, remove_words_csv, 'invalidfile.csv')
    assert result is False  # Invalid case: kseq_list_path is invalid


# Test case 5: Missing required paths or invalid paths when preprocessed_path is not provided
def test_missing_paths_task_4_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_4_arguments(None, None, None, None)  # Missing all paths
    assert result is False  # Invalid case: Missing paths

    result = valid_task_4_arguments(None, sentences_csv, None, None)  # Missing remove_words and kseq_list paths
    assert result is False  # Invalid case: Missing remove_words and kseq_list paths

    result = valid_task_4_arguments(None, None, remove_words_csv, None)  # Missing sentences and kseq_list paths
    assert result is False  # Invalid case: Missing sentences and kseq_list paths


# Test case 6: Missing one of the CSV paths or invalid kseq_list_path when preprocessed_path is not provided
def test_missing_one_csv_path_task_4_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_4_arguments(None, sentences_csv, remove_words_csv, None)  # Missing kseq_list path
    assert result is False  # Invalid case: Missing kseq_list_path
    
    result = valid_task_4_arguments(None, sentences_csv, remove_words_csv, 'invalidpath.txt')  # Invalid kseq_list_path
    assert result is False  # Invalid case: Invalid kseq_list_path


# Test case 7: Invalid case with missing kseq_list_path but valid preprocessed_path
def test_missing_kseq_list_path_with_preprocessed_path_task_4_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    
    result = valid_task_4_arguments(preprocessed_json, None, None, None)  # Missing kseq_list_path
    assert result is False  # Invalid case: Missing kseq_list_path


# TASK 5 VALID ARGS:

# Test case 1: Valid preprocessed_path and valid maximal_kseq
def test_valid_preprocessed_and_maximal_kseq_task_5_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    
    result = valid_task_5_arguments(preprocessed_json, None, None, None, 10)
    assert result is True  # Valid case: Preprocessed path is valid, and maximal_kseq is valid


# Test case 2: Invalid preprocessed_path or invalid maximal_kseq
def test_invalid_preprocessed_path_task_5_args():
    result = valid_task_5_arguments('invalidfile.json', None, None, None, 10)
    assert result is False  # Invalid case: Invalid preprocessed_path (not a JSON)


def test_invalid_maximal_kseq_task_valid_preprocessed_5_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    
    result = valid_task_5_arguments(preprocessed_json, None, None, None, -5)  # Invalid maximal_kseq (negative)
    assert result is False  # Invalid case: maximal_kseq is not positive


# Test case 3: Valid CSV paths and valid maximal_kseq
def test_valid_csv_paths_and_maximal_kseq_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_5_arguments(None, sentences_csv, names_csv, remove_words_csv, 10)
    assert result is True  # Valid case: All paths are correct CSVs, and maximal_kseq is valid


# Test case 4: Invalid CSV paths or invalid maximal_kseq when preprocessed_path is not provided
def test_invalid_sentences_path_task_5_args():
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_5_arguments(None, 'invalidfile.csv', names_csv, remove_words_csv, 10)
    assert result is False  # Invalid case: sentences path is invalid


def test_invalid_names_path_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_5_arguments(None, sentences_csv, 'invalidfile.csv', remove_words_csv, 10)
    assert result is False  # Invalid case: names path is invalid


def test_invalid_remove_words_path_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    
    result = valid_task_5_arguments(None, sentences_csv, names_csv, 'invalidfile.csv', 10)
    assert result is False  # Invalid case: remove words path is invalid


def test_invalid_maximal_kseq_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_5_arguments(None, sentences_csv, names_csv, remove_words_csv, -10)  # Invalid maximal_kseq
    assert result is False  # Invalid case: maximal_kseq is negative


# Test case 5: Missing required paths or invalid maximal_kseq
def test_missing_paths_or_invalid_maximal_kseq_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")


    result = valid_task_5_arguments(None, None, None, None, 10)  # Missing all paths
    assert result is False  # Invalid case: Missing all paths

    result = valid_task_5_arguments(None, sentences_csv, None, None, 10)  # Missing names and remove_words paths
    assert result is False  # Invalid case: Missing names and remove_words paths

    result = valid_task_5_arguments(None, None, names_csv, None, 10)  # Missing sentences and remove_words paths
    assert result is False  # Invalid case: Missing sentences and remove_words paths

    result = valid_task_5_arguments(None, None, None, remove_words_csv, 10)  # Missing sentences and remove_words paths
    assert result is False  # Invalid case: Missing sentences and names paths

    result = valid_task_5_arguments(None, sentences_csv, names_csv, remove_words_csv, -5)  # Invalid maximal_kseq
    assert result is False  # Invalid case: maximal_kseq is negative


# Test case 6: Missing one of the CSV paths when preprocessed_path is not provided
def test_missing_one_csv_path_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    
    result = valid_task_5_arguments(None, sentences_csv, names_csv, None, 10)  # Missing remove_words path
    assert result is False  # Invalid case: Missing remove_words path


# Test case 7: Missing maximal_kseq when preprocessed_path is not provided
def test_missing_maximal_kseq_task_5_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_5_arguments(None, sentences_csv, names_csv, remove_words_csv, None)  # Missing maximal_kseq
    assert result is False  # Invalid case: Missing maximal_kseq    


# TEST TASK 6 ARGS

# Test case 1: Valid preprocessed_path, valid window_size, and valid treshold
def test_valid_preprocessed_and_parameters_task_6_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    
    result = valid_task_6_arguments(preprocessed_json, None, None, None, 5, 10)
    assert result is True  # Valid case: Preprocessed path is valid, and window_size and treshold are valid


# Test case 2: Invalid preprocessed_path or invalid window_size/treshold
def test_invalid_preprocessed_path_or_parameters_task_6_args():
    
    result = valid_task_6_arguments('invalidfile.json', None, None, None, 5, 10)
    assert result is False  # Invalid case: Invalid preprocessed_path (not a JSON)
    
    # Invalid window_size (negative)
    preprocessed_json = create_temp_json('{"key": "value"}')
    result = valid_task_6_arguments(preprocessed_json, None, None, None, -1, 10)
    assert result is False  # Invalid case: window_size is negative

    # Invalid treshold (negative)
    result = valid_task_6_arguments(preprocessed_json, None, None, None, 5, -1)
    assert result is False  # Invalid case: treshold is negative


# Test case 3: Valid CSV paths and valid window_size, treshold
def test_valid_csv_paths_and_parameters_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, 10)
    assert result is True  # Valid case: All paths are correct CSVs, and window_size and treshold are valid


# Test case 4: Invalid CSV paths or invalid window_size/treshold when no preprocessed_path
def test_invalid_sentences_path_task_6_args():
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_6_arguments(None, 'invalidfile.csv', names_csv, remove_words_csv, 5, 10)
    assert result is False  # Invalid case: sentences path is invalid


def test_invalid_names_path_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_6_arguments(None, sentences_csv, 'invalidfile.csv', remove_words_csv, 5, 10)
    assert result is False  # Invalid case: names path is invalid


def test_invalid_remove_words_path_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, 'invalidfile.csv', 5, 10)
    assert result is False  # Invalid case: remove words path is invalid


def test_invalid_window_size_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, -1, 10)  # Invalid window_size
    assert result is False  # Invalid case: window_size is negative


def test_invalid_treshol_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, -1)  # Invalid treshold
    assert result is False  # Invalid case: treshold is negative


# Test case 5: Missing required paths or invalid window_size/treshold
def test_missing_paths_or_invalid_parameters_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_6_arguments(None, None, None, None, 5, 10)  # Missing all paths
    assert result is False  # Invalid case: Missing all paths

    result = valid_task_6_arguments(None, sentences_csv, None, None, 5, 10)  # Missing names and remove_words paths
    assert result is False  # Invalid case: Missing names and remove_words paths

    result = valid_task_6_arguments(None, None, names_csv, None, 5, 10)  # Missing sentences and remove_words paths
    assert result is False  # Invalid case: Missing sentences and remove_words paths

    result = valid_task_6_arguments(None, None, None, remove_words_csv, 5, 10)  # Missing sentences and remove_words paths
    assert result is False  # Invalid case: Missing sentences and names paths

    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, -5, 10)  # Invalid window_size
    assert result is False  # Invalid case: window_size is negative

    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, -5)  # Invalid treshold
    assert result is False  # Invalid case: treshold is negative


# Test case 6: Missing one of the CSV paths when no preprocessed_path
def test_missing_one_csv_path_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, None, 5, 10)  # Missing remove_words path
    assert result is False  # Invalid case: Missing remove_words path


# Test case 7: Missing window_size or treshold when no preprocessed_path
def test_missing_window_size_or_treshold_task_6_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, None, 10)  # Missing window_size
    assert result is False  # Invalid case: Missing window_size
    
    result = valid_task_6_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, None)  # Missing treshold
    assert result is False  # Invalid case: Missing treshold


# TEST TASK 7 ARGS

# Test case 1: Valid preprocessed data, people_connections_json_path, and maximal_distance
def test_valid_preprocessed_and_parameters_task_7_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')
    
    result = valid_task_7_arguments(preprocessed_json, None, None, None, 5, 10, people_connections_json, 5)
    assert result is True  # Valid case: Preprocessed data and other parameters are valid


# Test case 2: Invalid preprocessed_path or people_connections_json_path or maximal_distance
def test_invalid_preprocessed_or_connections_or_distance_task_7_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')
    
    # Invalid preprocessed JSON path (non-JSON file)
    result = valid_task_7_arguments('invalidfile.json', None, None, None, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Invalid preprocessed_path

    # Invalid people connections JSON (non-JSON file)
    result = valid_task_7_arguments(preprocessed_json, None, None, None, 5, 10, 'invalidfile.json', 5)
    assert result is False  # Invalid case: Invalid people_connections_json_path
    
    # Invalid maximal_distance (negative value)
    result = valid_task_7_arguments(preprocessed_json, None, None, None, 5, 10, people_connections_json, -1)
    assert result is False  # Invalid case: maximal_distance is negative


# Test case 3: Valid CSV paths and valid window_size, treshold, maximal_distance
def test_valid_csv_paths_and_parameters_task_7_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    result = valid_task_7_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is True  # Valid case: All paths are correct, and parameters are valid


# Test case 4: Invalid CSV paths when no preprocessed data
def test_invalid_csv_paths_task_7_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    # Invalid sentences CSV
    result = valid_task_7_arguments(None, 'invalidfile.csv', names_csv, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: sentences path is invalid

    # Invalid names CSV
    result = valid_task_7_arguments(None, sentences_csv, 'invalidfile.csv', remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: names path is invalid

    # Invalid remove words CSV
    result = valid_task_7_arguments(None, sentences_csv, names_csv, 'invalidfile.csv', 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: remove words path is invalid


# Test case 5: Invalid window_size, treshold, or maximal_distance
def test_invalid_parameters_task_7_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    # Invalid window_size (negative)
    result = valid_task_7_arguments(None, sentences_csv, names_csv, remove_words_csv, -5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: window_size is negative

    # Invalid treshold (negative)
    result = valid_task_7_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, -5, people_connections_json, 5)
    assert result is False  # Invalid case: treshold is negative

    # Invalid maximal_distance (negative)
    result = valid_task_7_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, 10, people_connections_json, -5)
    assert result is False  # Invalid case: maximal_distance is negative


# Test case 6: Missing required arguments (paths or parameters)
def test_missing_arguments_task_7_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    
    result = valid_task_7_arguments(None, None, None, None, 5, 10, None, 5)  # Missing all paths and JSON
    assert result is False  # Invalid case: Missing all paths and people_connections_json

    result = valid_task_7_arguments(None, sentences_csv, None, None, 5, 10, None, 5)  # Missing names, remove_words, and people_connections_json
    assert result is False  # Invalid case: Missing paths and people_connections_json

    result = valid_task_7_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, 10, None, 5)  # Missing people_connections_json
    assert result is False  # Invalid case: Missing people_connections_json


# Test case 7: Missing one or more of the CSV paths when no preprocessed data
def test_missing_csv_paths_when_no_preprocessed_data_task_7_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    # Missing remove_words path
    result = valid_task_7_arguments(None, sentences_csv, names_csv, None, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Missing remove_words path

    # Missing names path
    result = valid_task_7_arguments(None, sentences_csv, None, remove_words_csv , 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Missing names path

    # Missing sentences path
    result = valid_task_7_arguments(None, None, remove_words_csv, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Missing sentences path


# TEST TASK 8 ARGS:

# Test case 1: Valid preprocessed data, people_connections_json_path, and exact_distance
def test_valid_preprocessed_and_parameters_task_8_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')
    
    result = valid_task_8_arguments(preprocessed_json, None, None, None, 5, 10, people_connections_json, 5)
    assert result is True  # Valid case: Preprocessed data and other parameters are valid


# Test case 2: Invalid preprocessed_path or people_connections_json_path or exact_distance
def test_invalid_preprocessed_or_connections_or_distance_task_8_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')
    
    # Invalid preprocessed JSON path (non-JSON file)
    result = valid_task_8_arguments('invalidfile.json', None, None, None, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Invalid preprocessed_path

    # Invalid people connections JSON (non-JSON file)
    result = valid_task_8_arguments(preprocessed_json, None, None, None, 5, 10, 'invalidtest.json', 5)
    assert result is False  # Invalid case: Invalid people_connections_json_path
    
    # Invalid exact_distance (negative value)
    result = valid_task_8_arguments(preprocessed_json, None, None, None, 5, 10, people_connections_json, -1)
    assert result is False  # Invalid case: exact_distance is negative


# Test case 3: Valid CSV paths and valid window_size, treshold, exact_distance
def test_valid_csv_paths_and_parameters_task_8_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    result = valid_task_8_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is True  # Valid case: All paths are correct, and parameters are valid


# Test case 4: Invalid CSV paths when no preprocessed data
def test_invalid_csv_paths_task_8_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    # Invalid sentences CSV
    result = valid_task_8_arguments(None, 'invalidfile.csv', names_csv, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: sentences path is invalid

    # Invalid names CSV
    result = valid_task_8_arguments(None, sentences_csv, 'invalidfile.csv', remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: names path is invalid

    # Invalid remove words CSV
    result = valid_task_8_arguments(None, sentences_csv, names_csv, 'invalidfile.csv', 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: remove words path is invalid


# Test case 5: Invalid window_size, treshold, or exact_distance
def test_invalid_parameters_task_8_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    # Invalid window_size (negative)
    result = valid_task_8_arguments(None, sentences_csv, names_csv, remove_words_csv, -5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: window_size is negative

    # Invalid treshold (negative)
    result = valid_task_8_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, -5, people_connections_json, 5)
    assert result is False  # Invalid case: treshold is negative

    # Invalid exact_distance (negative)
    result = valid_task_8_arguments(None, sentences_csv, names_csv, remove_words_csv, 5, 10, people_connections_json, -5)
    assert result is False  # Invalid case: exact_distance is negative


# Test case 6: Missing required arguments (paths or parameters)
def test_missing_arguments_task_8_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')


    result = valid_task_8_arguments(None, None, None, None, 5, 10, None, 5)  # Missing all paths and JSON
    assert result is False  # Invalid case: Missing all paths and people_connections_json

    result = valid_task_8_arguments(None, sentences_csv, None, None, 5, 10, None, 5)  # Missing names, remove_words, and people_connections_json
    assert result is False  # Invalid case: Missing paths and people_connections_json

    result = valid_task_8_arguments(None, people_connections_json, names_csv, remove_words_csv, 5, 10, None, 5)  # Missing people_connections_json
    assert result is False  # Invalid case: Missing people_connections_json


# Test case 7: Missing one or more of the CSV paths when no preprocessed data
def test_missing_csv_paths_when_no_preprocessed_data_task_8_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    names_csv = create_temp_csv("name1\nname2\nname3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")
    people_connections_json = create_temp_json('{"connections": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}')

    # Missing remove_words path
    result = valid_task_8_arguments(None, sentences_csv, names_csv, None, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Missing remove_words path

    # Missing names path
    result = valid_task_8_arguments(None, sentences_csv, None, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Missing names path

    # Missing sentences path
    result = valid_task_8_arguments(None, None, names_csv, remove_words_csv, 5, 10, people_connections_json, 5)
    assert result is False  # Invalid case: Missing sentences path


# TEST TASK 9 ARGS:

# Test case 1: Valid preprocessed data and treshold
def test_valid_preprocessed_data_and_treshold_task_9_args():
    preprocessed_json = create_temp_json('{"key": "value"}')

    result = valid_task_9_arguments(preprocessed_json, None, None, 10)
    assert result is True  # Valid case: Preprocessed data and treshold are correct


# Test case 2: Invalid preprocessed path or treshold
def test_invalid_preprocessed_path_or_treshold_task_9_args():
    preprocessed_json = create_temp_json('{"key": "value"}')

    # Invalid preprocessed path (non-JSON file)
    result = valid_task_9_arguments('invalid.json', None, None, 10)
    assert result is False  # Invalid case: Preprocessed path is not a JSON

    # Invalid treshold (negative value)
    result = valid_task_9_arguments(preprocessed_json, None, None, -10)
    assert result is False  # Invalid case: treshold is negative


# Test case 3: Valid CSV paths and treshold when no preprocessed data
def test_valid_csv_paths_and_treshold_task_9_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_9_arguments(None, sentences_csv, remove_words_csv, 10)
    assert result is True  # Valid case: All CSV paths are valid and treshold is correct


# Test case 4: Invalid CSV paths or treshold when no preprocessed data
def test_invalid_csv_paths_or_treshold_task_9_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    # Invalid sentences CSV
    result = valid_task_9_arguments(None, 'invalidfile.json', remove_words_csv, 10)
    assert result is False  # Invalid case: sentences path is invalid

    # Invalid remove words CSV
    result = valid_task_9_arguments(None, sentences_csv, 'invalidfile.json', 10)
    assert result is False  # Invalid case: remove words path is invalid

    # Invalid treshold (negative value)
    result = valid_task_9_arguments(None, sentences_csv, remove_words_csv, -10)
    assert result is False  # Invalid case: treshold is negative


# Test case 5: Missing arguments (either preprocessed or CSV paths and treshold)
def test_missing_arguments_task_9_args():
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    # Missing preprocessed path and CSV paths
    result = valid_task_9_arguments(None, None, None, 10)
    assert result is False  # Invalid case: Missing all paths

    # Missing one CSV path and preprocessed path
    result = valid_task_9_arguments(None, sentences_csv, None, 10)
    assert result is False  # Invalid case: Missing remove_words path

    # Missing one CSV path and preprocessed path
    result = valid_task_9_arguments(None, None, remove_words_csv, 10)
    assert result is False  # Invalid case: Missing sentences path

    # Missing treshold
    result = valid_task_9_arguments(None, sentences_csv, remove_words_csv, None)
    assert result is False  # Invalid case: Missing treshold


# Test case 6: Valid preprocessed data with CSV paths and treshold
def test_valid_preprocessed_data_with_csv_paths_and_treshold_task_9_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    result = valid_task_9_arguments(preprocessed_json, sentences_csv, remove_words_csv, 10)
    assert result is True  # Valid case: Preprocessed data is provided with CSV paths and treshold


# Test case 7: Invalid file types for CSV or JSON files
def test_invalid_file_types_task_9_args():
    result = valid_task_9_arguments('invalidfile.json', None, None, 10)
    assert result is False  # Invalid case: Invalid JSON file (should be a JSON)

    result = valid_task_9_arguments(None, 'invalidfile.json', None, 10)
    assert result is False  # Invalid case: Invalid CSV file (should be a CSV)


# Test case 8: Valid and invalid combinations for preprocessed path or CSV paths
def test_combined_valid_and_invalid_inputs_task_9_args():
    preprocessed_json = create_temp_json('{"key": "value"}')
    sentences_csv = create_temp_csv("sentence1\nsentence2\nsentence3\n")
    remove_words_csv = create_temp_csv("word1\nword2\nword3\n")

    # Valid preprocessed path with treshold
    result = valid_task_9_arguments(preprocessed_json, None, None, 5)
    assert result is True  # Valid case: Preprocessed path with treshold

    # Valid CSV paths with treshold when no preprocessed data
    result = valid_task_9_arguments(None, sentences_csv, remove_words_csv, 5)
    assert result is True  # Valid case: CSV paths with treshold

    # Invalid preprocessed path with treshold
    result = valid_task_9_arguments('invalidfile.json', None, None, 5)
    assert result is False  # Invalid case: Invalid preprocessed path

    # Invalid CSV paths with treshold when no preprocessed data
    result = valid_task_9_arguments(None, 'invalidfile.csv', remove_words_csv, 5)
    assert result is False  # Invalid case: Invalid CSV path