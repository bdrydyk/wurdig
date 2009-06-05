"""Setup the Wurdig application"""
import logging
import os.path
import datetime

from wurdig.config.environment import load_environment
import wurdig.config as config
from authkit.users.sqlalchemy_driver import UsersFromDatabase
from authkit.users import md5

from sqlalchemy import engine_from_config

from wurdig import model as model



log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup wurdig here"""
    load_environment(conf.global_conf, conf.local_conf)

    #model.metadata.bind = meta.engine
    # model.setup_all()
    # model.create_all()
    
    model.metadata.drop_all(checkfirst=True)
    #model.metadata.setup_all()
    model.metadata.create_all(checkfirst=True)
    
    
    # log.info("Adding the AuthKit model...")
    # users = UsersFromDatabase(model)
    
    # filename = os.path.split(conf.filename)[-1]
    # if filename == 'test.ini':
    #     # Permanently drop any existing tables
    #     log.info("Dropping existing tables...")
    #     model.metadata.drop_all(checkfirst=True)
        
    # Create the tables if they aren't there already

    # log.info("Adding roles and uses...")
    # users.role_create("admin")
    # users.user_create("admin", password=md5("admin"))
    # users.user_add_role("admin", role="admin")
    
    
    log.info("Adding tags...")

    pyylons = model.Tag(name=u"Pylons", slug='pylons')
    science = model.Tag(name=u"Science", slug='science')
    arduino = model.Tag(name=u"Arduino", slug='adruino')
    maxmsp = model.Tag(name=u"Max/MSP", slug='max')
    movement = model.Tag(name=u"Movement", slug='movement')
    godel = model.Tag(name=u"godel", slug='godel')
    
    
    log.info("Adding about page...")
    page1 = model.Page()
    page1.title = u'About me and this site'
    page1.slug = u'about'
    page1.content = u"""
    <p>Welcome.  My name is Jason Leveille.  I currently live (with my beautiful wife and two daughters) and attend <a href="http://www.hood.edu">graduate school (<abbr title="Master of Science in Computer Science">MSCS</abbr>)</a> in Frederick, Maryland.  June 16th, 2007 I ended my <del>6</del> <ins>8</ins> year career as a <a href="http://www.qohs.org">High School</a> <abbr title="Computer Science">CS</abbr> teacher, and June 18th, 2007 I started my new career as a web software developer with <a href="http://www.blueatlas.com">Blue Atlas Interactive</a> in Germantown, Maryland.  I had been developing web applications since 2002, and finally decided that it was something I needed to be doing full time.  While developing I mostly work with PHP and JavaScript, though I have been paid to develop web applications in .net (C#), Python (Plone), classic asp, and I have dabbled in Ruby/Rails, Django, and Pylons.  I also work closely with designers to take their PSD goodies and turn them into CSS works of art.  I have also been known to focus on issues in <a href="http://www.webstandards.org/action/edutf/examples/">web standards</a> and <a href="http://www.adainfo.org/accessible/it/events.asp">accessibility</a>.</p>
    <p>If you have any questions for me about any of my posts, feel free to leave a comment.  If that is not sufficient, my email address is leveillej [at] gmail [dot] com.</p>
    <h3>ElseWhere</h3>
    <ul>
        <li><a href="http://twitter.com/jleveille">Twitter</a></li>
        <li><a href="http://del.icio.us/leveille">Del.icio.us</a></li>
    </ul>
    <h3>Disclaimer</h3>
    <p>Views and opinions expressed on this site are mine and do not necessarily reflect the views of my fantastic employer, <a href="http://www.blueatlas.com">Blue Atlas Interactive</a>.</p>
    <h3>My Office</h3>
    <div class="wurdig-caption aligncenter" style="width: 440px;"><a href="http://www.flickr.com/photos/leveilles/3273777769/"><img title="My Office" src="http://farm4.static.flickr.com/3368/3273777769_be393f175a_b.jpg" alt="Office Image 1" width="430" height="287"></a><p class="wurdig-caption-text">Office Image 1</p></div>
    <div class="wurdig-caption aligncenter" style="width: 440px;"><a href="http://www.flickr.com/photos/leveilles/3274596830/in/photostream/"><img title="Office Image 2" src="http://farm4.static.flickr.com/3300/3274596830_ac344872d7_b.jpg" alt="Office Image 2" width="430" height="287"></a><p class="wurdig-caption-text">Office Image 2</p></div>
    """
    
    
    log.info("Adding teach page...")
    page2 = model.Page()
    page2.title = u'My life as a teacher'
    page2.slug = u'teaching'
    page2.content = u'<p>I am often asked about my old teaching material (which used to be housed at http://www.my-classes.org - <a href="http://web.archive.org/web/20071216031655/http://www.my-classes.org/">wayback</a>).  <a href="http://jasonleveille.com/teacher/">My old lessons</a> are still available (I can\'t say how relevant they still are though!).  Let me know if you have any questions.</p>'
    #model.Session.add(page2)
    #model.Session.flush()
    
    log.info("Adding comment styleguide page...")
    styleguide = model.Page()
    styleguide.title = u'Comment Styleguide'
    styleguide.slug = u'comment-styleguide'
    styleguide.content = u"""
    <h5>Supported Comment HTML</h5>
    <p>In addition to line breaks being converted to paragraphs:</p>
    <ul>
        <li>Links will automatically be linked for you if not wrapped in anchor tag.</li><li>&lt;a href=&quot;&quot title=&quot;&quot&gt;link&lt;/a&gt;</li>
    </ul>
    """
    #model.Session.add(styleguide)
    #model.Session.flush()
    
    log.info("Adding search page...")
    search = model.Page()
    search.title = u'Search'
    search.slug = u'search'
    search.content = u"""
    <div id="cse-search-results"></div>
        <script type="text/javascript">
            var googleSearchIframeName = "cse-search-results";
            var googleSearchFormName = "cse-search-box";
            var googleSearchFrameWidth = 600;
            var googleSearchDomain = "www.google.com";
            var googleSearchPath = "/cse";
        </script>
        <script type="text/javascript" src="http://www.google.com/afsonline/show_afs_search.js">
    </script>
    """
    #model.Session.add(search)
    #model.Session.flush()
    
    log.info("Adding first post...")
    post1 = model.Post()
    post1.title = u'First test post'
    post1.slug = u'first-test-post'
    post1.tags = [pyylons, science, godel]
    post1.content = u'<p>This is the first test post</p>'
    post1.created_on = datetime.datetime(2008, 3, 17, 12, 30, 45)
    #model.Session.add(post1)
    #model.Session.flush()
    
    log.info("Adding fifth post...")
    post5 = model.Post()
    post5.title = u'Fifth test post'
    post5.slug = u'fifth-test-post'
    post5.content = u'<p>This is the fifth test post</p>'
    post5.tags = [pyylons, science, godel]
    post5.created_on = datetime.datetime(2008, 3, 17, 12, 30, 45)
    post5.draft = False
    post5.posted_on = datetime.datetime(2008, 3, 18, 12, 30, 45)
    #model.Session.add(post5)
    #model.Session.flush()
    
    log.info("Adding second post...")
    post2 = model.Post()
    post2.title = u'Second test post'
    post2.slug = u'second-test-post'
    post2.content = u'<p>This is the second test post</p>'
    post2.tags = [pyylons, science, godel]
    post2.created_on = datetime.datetime(2009, 3, 24, 12, 30, 45)
    post2.draft = False
    post2.posted_on = datetime.datetime(2009, 3, 24, 12, 30, 45)
    #model.Session.add(post2)
    #model.Session.flush()
    
    log.info("Adding third post...")
    post3 = model.Post()
    post3.title = u'Third test post'
    post3.slug = u'third-test-post'
    post3.content = u'<p>This is the third test post</p>'
    post3.tags = [pyylons, science, godel]
    post3.created_on = datetime.datetime(2009, 3, 25, 12, 30, 45)
    post3.draft = False
    post3.posted_on = datetime.datetime(2009, 3, 25, 12, 30, 45)
    #model.Session.add(post3)
    #model.Session.flush()
    
    log.info("Adding fourth post...")
    post4 = model.Post()
    post4.title = u'Fourth test post'
    post4.slug = u'fourth-test-post'
    post4.content = u'<p>This is the fourth test post</p>'
    post4.created_on = datetime.datetime(2009, 4, 5, 12, 30, 45)
    post4.draft = False
    post4.posted_on = datetime.datetime(2009, 4, 5, 12, 30, 45)
    #model.Session.add(post4)
    #model.Session.flush()
    
    log.info("Adding second post comment...")
    comment1 = model.Comment()
    comment1.post_id = int(2)
    comment1.content = u'This is my comment content'
    comment1.name = u'Responsible Web'
    comment1.email = u'nomail@gmail.com'
    comment1.url = u'http://responsibleweb.com'
    #model.Session.add(comment1)
    #model.Session.flush()
    
    log.info("Adding second post comment...")
    comment2 = model.Comment()
    comment2.post_id = int(2)
    comment2.content = u'This is my second comment content'
    comment2.name = u'Responsible Web'
    comment2.email = u'nomail@gmail.com'
    comment2.url = u'http://responsibleweb.com'
    comment2.approved = True
    #model.Session.add(comment2)
    #model.Session.flush()
    

    
    model.Session.commit()
    log.info('Successfully set up.')
