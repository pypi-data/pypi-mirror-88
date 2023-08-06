import datetime
import json
import os
import random
import sys
import time

if sys.version[0] == '2':
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser

import dateutil.parser
import email.utils

from subprocess import Popen, PIPE, CalledProcessError

# Python 2.x compabitlity
if sys.version[0] == '2':
    FileNotFoundError = IOError

class HTMLStripper(HTMLParser):
    """Strips HTML off an string"""
    def __init__(self):
        self.reset()
        self.strict = False
        self.fed = []
        self.convert_charrefs = True
        self.numlinks = 0
        self.links = {}

    def handle_data(self, d):
        self.fed.append(d)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    link = attr[1]
                    break;
            self.fed.append('[Image]: {}\n'.format(link))
        elif tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links[self.numlinks] = attr[1]
        elif tag == 'li':
            self.fed.append('- ')

    def handle_endtag(self, tag):
        if tag == 'a':
            self.fed.append(' [{}]'.format(self.numlinks))
            self.numlinks += 1

    def get_data(self):
        out = ''.join(self.fed)
        if self.numlinks:
            out += '\n'
            for l in range(self.numlinks):
                out += '  [{}]: {}\n'.format(l, self.links[l])
        return out

class ExternalHTMLStripper:
    def __init__(self, strip_program):
        self.strip_program = strip_program
        self.reset()

    def feed(self, data):
        self.raw_data.append(data)

    def close(self):
        input_ = u''.join(self.raw_data).encode('utf-8')
        p = Popen(self.strip_program, stdin=PIPE, stdout=PIPE, shell=True)
        output, err = p.communicate(input_)
        if p.returncode != 0:
           # Note: feed2maildir supports Python 2.7+ and 3.2+ so we have to
           # print the stderr here. In Python 3.5+ we could add it as part
           # of the CalledProcessError exception.
           print(err)
           raise CalledProcessError(p.returncode, self.strip_program)

        self.stripped = output.decode('utf-8')

    def reset(self):
        self.raw_data = []
        self.stripped = u''

    def get_data(self):
        return self.stripped

class Converter:
    """Compares the already parsed feeds and converts new ones to maildir"""

    TEMPLATE = u"""MIME-Version: 1.0
Date: {}
Subject: {}
From: {}
Content-Type: text/plain

[Feed2Maildir] Read the update here:
{}

{}
"""

    def __init__(self, db='~/.f2mdb', maildir='~/mail/feeds', strip=False,
                 strip_program=None, links=False, silent=False):
        self.silent = silent
        self.maildir = os.path.expanduser(maildir)
        self.db = os.path.expanduser(db)
        self.links = links
        self.strip = strip
        if self.strip and strip_program is None:
            self.stripper = HTMLStripper()
        elif self.strip:
            self.stripper = ExternalHTMLStripper(strip_program)

        try: # to read the database
            with open(self.db, 'r') as f:
                self.dbdata = json.loads(f.read())
        except FileNotFoundError:
            self.dbdata = None
        except ValueError:
            self.output('WARNING: database is malformed and will be ignored')
            self.dbdata = None

    def run(self):
        """Do a full run"""
        if self.feeds:
            self.check_maildir(self.maildir)
            self.news = self.find_new(self.feeds, self.dbdata)
            for newfeed, posts in self.news.items():
                for newpost in posts:
                    self.write(self.compose(newfeed, newpost))

    def load(self, feeds):
        """Load a list of feeds in feedparser-dict form"""
        self.feeds = feeds

    def find_new(self, feeds, db, writedb=True, dbfile=None):
        """Find the new posts by comparing them to the db, by default
        refreshing the db"""
        new = {}
        newtimes = {}
        for feed in feeds:
            feedname = feed.feed.title
            feedaliasname = feed.feed_alias_name
            feedup = self.feed_update_time(feed)
            try: # to localize the timezone
                feedup = feedup.astimezone(dateutil.tz.tzutc())
            except: # it is naive, force UTC
                feedup = feedup.replace(tzinfo=dateutil.tz.tzutc())
            try: # to find the old update time in the db
                oldtime = self.mktime(db[feedname]).astimezone(
                            dateutil.tz.tzutc())
            except: # it is not there
                oldtime = None
            if oldtime and not oldtime.tzinfo: # force UTC
                oldtime = oldtime.replace(tzinfo=dateutil.tz.tzutc())
            # print(feedname, feedup.tzinfo)
            if not oldtime or oldtime < feedup:
                for post in feed.entries:
                    feedtime = self.post_update_time(post)
                    try: # to localize the timezone
                        feedtime = feedtime.astimezone(dateutil.tz.tzutc())
                    except: # it is naive
                        feedtime = feedtime.replace(tzinfo=dateutil.tz.tzutc())
                    if not oldtime or oldtime < feedtime:
                        try: # to append the post the the feed-list
                            new[feedaliasname].append(post)
                        except: # it is the first one, make a new list
                            new[feedaliasname] = [post, ]
            if writedb:
                newtimes[feedname] = feedup.strftime('%Y-%m-%d %H:%M:%S %Z')

        if writedb:
            if not dbfile: # use own dbfile as default
                dbfile = self.db
            try: # to write the new database
                with open(dbfile, 'w') as f:
                    f.write(json.dumps(newtimes))
            except:
                self.output('WARNING: failed to write the new database')

        return new

    def post_update_time(self, post):
        """Try to get the post time"""
        try:
            return self.mktime(post.updated)
        except AttributeError:
            try:
                return self.mktime(post.published)
            except AttributeError: # last resort
                return datetime.datetime.now()

    def find_update_time(self, feed):
        """Find the last updated post in a feed"""
        times = []
        for post in feed.entries:
            times.append(self.post_update_time(post))
        return sorted(times)[-1]

    def feed_update_time(self, feed):
        # find the newest post and get its time
        newest_post_time = self.find_update_time(feed)
        try: # to get the update time from the feed itself
            feed_time = self.mktime(feed.feed.updated)
        except:
            return newest_post_time
        # Some feeds like Youtube do not update the feed's update time.
        # The value 'feed_time' is a valid date, but outdated so
        # we have to compare it with the posts' times and get the latest.
        return max(newest_post_time, feed_time)

    def check_maildir(self, maildir):
        """Check access to the maildir and try to create it if not present"""
        mdirs = ('', '/tmp', '/new', '/cur')
        for mdir in mdirs:
            fullname = maildir + mdir
            if not os.access(fullname, os.W_OK):
                try: # to make the maildirs
                    os.mkdir(fullname)
                except:
                    sys.exit('ERROR: accessing "{}" failed'.format(fullname))

    def compose(self, title, post):
        """Compose the mail using the tempate"""
        try: # to get the update/publish time from the post
            updated = post.updated
        except: # the property is not set, use now()
            updated = datetime.datetime.now()

        # convert the time to RFC 2822 format, expected by MUA programs
        d = dateutil.parser.parse(updated)
        updated = email.utils.formatdate(time.mktime(d.timetuple()), usegmt=True)

        desc = ''
        if not self.links:
            if self.strip:
                self.stripper.feed(post.description)
                self.stripper.close()
                desc = self.stripper.get_data()
                self.stripper.reset()
            else:
                desc = post.description
        return self.TEMPLATE.format(updated, post.title, title, post.link,
                                    desc)

    def write(self, message):
        """Take a message and write it to a mail"""
        rand = str(random.randint(10000, 99999))
        dt = str(datetime.datetime.now())
        pid = str(os.getpid())
        host = os.uname()[1]
        name = u'{}/new/{}{}{}{}'.format(self.maildir, rand, dt, pid, host)
        try: # to write out the message
            with open(name, 'w') as f:
                # We can thank the P2/P3 unicode madness for this...
                if sys.version[0] == '2':
                    f.write(str(message.encode('utf8')))
                else:
                    f.write(message)
        except:
            self.output('WARNING: failed to write message to file')

    def mktime(self, arg):
        """Make a datetime object from a time string"""
        return dateutil.parser.parse(arg)

    def output(self, arg):
        if not self.silent:
            print(arg)

