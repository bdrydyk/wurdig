import tw.forms as twf
from tw.forms.validators import UnicodeString, Email, URL, Int, Number, Set, String, OneOf
from tw.forms.validators import NotEmpty, MaxLength, MinLength, Regex, PlainText, StringBool
from tw.forms.validators import DateValidator, DateConverter, TimeConverter, Invalid
import wurdig.lib.helpers as h
#from formencode import Schema, NoDefault
from tw.forms.validators import Schema, NoDefault, FancyValidator, ForEach


movie_form = twf.TableForm('movie_form', action='save', children=[
    twf.HiddenField('id'),
    twf.TextField('title'),
    twf.Spacer(),
    twf.TextField('year', size=4, label_text='Year of Fuck'),
    twf.CalendarDatePicker('release_date'),
    twf.SingleSelectField('genera', options=['', 'Action', 'Comedy', 'Other']),
    twf.Label(text='Hello', suppress_label=True),
    twf.TextArea('description'),
])


page_form = twf.TableForm('page_form', action='save', children=[
    twf.HiddenField('id'),
    twf.TextField('title', validator=twf.validators.NotEmpty),
    twf.Spacer(),
    twf.TextField('year', size=4, label_text='Year of Fuck', validator=Int(not_empty=True)),
    twf.CalendarDatePicker('release_date'),
    twf.SingleSelectField('genera', options=['', 'Action', 'Comedy', 'Other']),
    twf.Label(text='Hello', suppress_label=True),
    twf.TextArea('description', validator= UnicodeString(not_empty=True)),

])


post_form = twf.TableForm('page_form', action='save', children=[
    twf.HiddenField('id'),
    twf.TextField('title'),
    twf.Spacer(),
    twf.TextField('year', size=4, label_text='Year of Fuck'),
    twf.CalendarDatePicker('release_date'),
    twf.SingleSelectField('genera', options=['', 'Action', 'Comedy', 'Other']),
    twf.Label(text='Hello', suppress_label=True),
    twf.TextArea('description'),

])

tag_form = twf.TableForm('page_form', action='save', children=[
    twf.HiddenField('id'),
    twf.TextField('name'),
    twf.Spacer(),
    twf.TextField('slug', size=4, label_text='Year of Fuck')
])

comment_form = twf.TableForm('page_form', action='save', children=[
    twf.HiddenField('id'),
    twf.TextField('name'),
    twf.TextField('email'),
    twf.Spacer(),
    twf.TextArea('content'),

])


class UniqueSlug(FancyValidator):
    messages = {
        'invalid': 'Slug must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = UnicodeString(max=30).to_python(value, state)
        # validate that slug only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise Invalid("Slug can only contain letters, numbers, and dashes", value, state)
        
        # Ensure slug is unique
        page_q = Session.query(model.Page).filter_by(slug=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing post.
            page_q = page_q.filter(model.Page.id != int(request.urlvars['id']))
            
        # Check if the slug exists
        slug = page_q.first()
        if slug is not None:
            raise Invalid(
                self.message('invalid', state),
                value, state)
        
        return value


class ValidTags(FancyValidator):
    messages = {
        'invalid': 'One ore more selected tags could not ' +
        'be found in the database'
    }
    def _to_python(self, values, state):
        all_tag_ids = [tag.id for tag in Session.query(model.Tag)]
        for tag_id in values['tags']:
            if tag_id not in all_tag_ids:
                raise Invalid(
                    self.message('invalid', state),
                    values, state
                )
        return values


#TAG##
class ConstructSlug(FancyValidator):
    def _to_python(self, value, state):
        if value['slug'] in ['', u'', None]:
            tag_name = value['name'].lower()
            value['slug'] = re.compile(r'[^\w-]+', re.U).sub('-', tag_name).strip('-')
        return value



class UniqueName(FancyValidator):
    messages = {
        'invalid': 'Tag name must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = UnicodeString(max=30).to_python(value, state)
        # validate that tag only contains letters, numbers, and spaces
        result = re.compile("[^a-zA-Z0-9 ]").search(value)
        if result:
            raise Invalid("Tag name can only contain letters, numbers, and spaces", value, state)
        
        # Ensure tag name is unique
        tag_q = Session.query(model.Tag).filter_by(name=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing tag
            tag_q = tag_q.filter(model.Tag.id != int(request.urlvars['id']))
            
        # Check if the tag name exists
        name = tag_q.first()
        if name is not None:
            raise Invalid(
                self.message('invalid', state),
                value, state)
        
        return value
    
class UniqueSlug(FancyValidator):
    messages = {
        'invalid': 'Tag slug must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = UnicodeString(max=30).to_python(value, state)
        # validate that slug only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise Invalid("Slug can only contain letters, numbers, and dashes", value, state)
        
        # Ensure tag slug is unique
        tag_q = Session.query(model.Tag).filter_by(slug=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing post.
            tag_q = tag_q.filter(model.Tag.id != int(request.urlvars['id']))
            
        # Check if the slug exists
        slug = tag_q.first()
        if slug is not None:
            raise Invalid(
                self.message('invalid', state),
                value, state)
        
        return value


####Comments

class AkismetSpamCheck(FancyValidator):
    messages = {
        'invalid-akismet': 'Your comment has been identified as spam.  Are you a spammer?'
    }
    def _to_python(self, values, state):
        # we're in the administrator
        if request.urlvars['action'] == 'save':
            return values
        
        if h.wurdig_use_akismet():
            from wurdig.lib.akismet import Akismet
            # Thanks for the help from http://soyrex.com/blog/akismet-django-stop-comment-spam/
            a = Akismet(h.wurdig_get_akismet_key(), wurdig_url=request.server_name)
            akismet_data = {}
            akismet_data['user_ip'] = request.remote_addr
            akismet_data['user_agent'] = request.user_agent
            akismet_data['comment_author'] = values['name']
            akismet_data['comment_author_email'] = values['email']
            akismet_data['comment_author_url'] = values['url']
            akismet_data['comment_type'] = 'comment'
            spam = a.comment_check(values['content'], akismet_data)
            if spam:
                raise Invalid(
                    self.message('invalid-akismet', state),
                    values, state
                )
        return values
    
class PrimitiveSpamCheck(FancyValidator):
    def _to_python(self, value, state):        
        # Ensure we have a valid string
        value = UnicodeString(max=10).to_python(value, state)
        eq = h.wurdig_spamword().lower() == value.lower()
        if not eq:
            raise Invalid("Double check your answer to the spam prevention question and resubmit.", value, state)
        return value



class NewPageForm(Schema):
#    pre_validators = [ConstructSlug(), Cleanup()]
    allow_extra_fields = True
    filter_extra_fields = True
    title = UnicodeString(
        not_empty=True,
        max=100, 
        messages={
            'empty':'Enter a page title'
        },
        strip=True
    )
    slug = UniqueSlug(not_empty=True, max=100, strip=True)
    content = UnicodeString(
        not_empty=True,
        messages={
            'empty':'Enter some post content.'
        },
        strip=True
    )

class NewPostForm(Schema):
#    pre_validators = [ConstructSlug(), Cleanup()]
    allow_extra_fields = True
    filter_extra_fields = True
    title = UnicodeString(
        not_empty=True,
        max=100, 
        messages={
            'empty':'Enter a post title'
        },
        strip=True
    )
    slug = UniqueSlug(not_empty=True, max=100, strip=True)
    content = UnicodeString(
        not_empty=True,
        messages={
            'empty':'Enter some post content.'
        },
        strip=True
    )
    draft = StringBool(if_missing=False)
    comments_allowed = StringBool(if_missing=False)
    tags = ForEach(Int())
    chained_validators = [ValidTags()]


class NewTagForm(Schema):
    pre_validators = [ConstructSlug()]
    allow_extra_fields = True
    filter_extra_fields = True
    name = UniqueName(not_empty=True, max=30, strip=True)
    slug = UniqueSlug(not_empty=True, max=30, strip=True)

class NewCommentForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = UnicodeString(not_empty=True, max=100, strip=True)
    email = Email(not_empty=True, max=50, strip=True)
    url = URL(not_empty=False, check_exists=True, max=125, strip=True)
    content = UnicodeString(
        not_empty=True,
        strip=True,
        messages={
            'empty':'Please enter a comment.'
        }
    )
    approved = StringBool(if_missing=False)

    if not h.auth.authorized(h.auth.is_valid_user):
        if h.wurdig_use_akismet():
            chained_validators = [AkismetSpamCheck()]
        else:
            wurdig_comment_question = PrimitiveSpamCheck(not_empty=True, max=10, strip=True)



