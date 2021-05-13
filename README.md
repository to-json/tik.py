# Whassis?

it's a goofy little front end to py-jira that i thought might help others

basically, the library is great! and there are other perfectly good jira 
cli options. but they are varying levels of difficult to use with broswer-cookie
which, in turn, is basically required if you're stuck in certain corporate
configs. and well, if you weren't stuck in a corp setting, you probably wouldn't
be using jira.

## Contributing?

um...prs welcome i guess? but also, it's pretty trash and probably you 
just shouldn't? 

## Usage?
so, `pip install -r requirements.txt`, using whatever pip installs stuff that's
reachable by the `python` or `python3` on your `path`. then just stick tik.py
somewhere on your path and `chmod +x` it. make sure `tik.ini` is in the same
dir. a `tik.ini.example` is provided, you know the drill.

A `jira-todo` is also provided as an example of a one off script using some parts
from here to accomplish something that didn't really fit into `tik` proper. it 
can also just be dropped onto the `PATH` in the same dir as `tik.ini`

## But I'm not on a unix!

condolences

## How do i make a fields section in my `tik.ini`?

this is a special hell

jira calls every displayed field that's not part of the unmodified jira config
`customfield_<int>`. "How to i get a mapping from those to their names?" you ask?

you don't! (I actually did eventually figure this out, but it's absurd)

i sat in ipython for about an hour looking at random fields and setting the visible
fields on my test ticket to different things, in order to pull out the 4 or so fields
that are in my personal fields.ini. i could probably do some sort of nifty list
comprehension to get every one of them that carries a name with it, but, turns out,
most don't!

jira; not even once.

for that reason, ipython is in the requirements, and an 'embed' flag is provided. this
is also how i personally do feature development, i just pop into the repl that way and
play with ideas until they work.

this is a good idea because the jira module has some broken bits (like attach_file*)
so you really need to just...try everything you intend to include

\* this is apparently fixed in 3.o, but 3.0 is not on pypi. i might vendor it at some point.

if you do so, `jira` is the var that contains your jira instance

## Does it just do the things that are in the help, provided by running `tik.py -h`?

mostly! if you pipe stuff to `tik <ticket-id> -c` it will use that as the comment body,
inside a code block, because that's a central usecase for me. i wanted to be able to pipe
in attachments too, but, see above about `attach_file` being Just Broken.

there also an interactive transition mode if you invoke `tik.py <ticket-id> -t` without a 
transition after it, and ... iono honestly you should probably read the argument parsing
stanza, i'm forgetful and almost forgot to write docs at all. in fact this file exists
mostly because git repos look like shit on github if they don't have one.

## Why not an ethical or viral license?

no viral license because if you're using it at all, it's probably for work, because jira.
no 'ethical' license because it's just not that big of a project. also, if
there was a 'do no harm' clause you probably couldn't use it at work, becuase, there
is no ethical (consumption|development) blah blah etc.

but also, please do as little harm as possible? like, not as part of the license, just as
one person asking another.
