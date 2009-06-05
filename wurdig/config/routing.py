"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'], explicit=True)
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/', controller='post', action='home')
    map.connect('/admin/', controller='admin', action='home')
    map.connect('/movie/', controller='movie', action='index')
    
    map.connect('/feeds/', 
                controller='post', 
                action='redirect_wp_feeds')
    
    map.connect('/feeds/blog', 
                controller='post', 
                action='feeds')
    
    map.connect('/feeds/comments', 
                controller='comment', 
                action='feeds')
    
    map.connect('/feeds/comments/{post_id}',
                controller='comment',
                action='post_comment_feed',
                requirements = dict(post_id='\d+')
    )

    map.connect('/feeds/tag/{path}',
                controller='tag',
                action='tag_feed',
                requirements = dict(path='[-\w]+')
    )
    
    map.connect('/post/{post_id}/{controller}/{action}',
                requirements = dict(post_id='\d+')
    ) 
    
    map.connect('/post/{post_id}/{controller}/{action}/{id}',
                requirements = dict(post_id='\d+', id='\d+')
    )
    
    map.connect('/{year}/{month}/{path}', controller='post', 
                action='view', 
                requirements = {'year' : '\d{2,4}', 
                                'month' : '\d{1,2}', 
                                'path' : '[-\w]+'})
    
    map.redirect('/{year}/{month}/{path}/', '/{year}/{month}/{path}', _redirect_code='301 Moved Permanently')
    
    map.connect('/{year}/{month}', controller='post', 
                action='archive', 
                requirements = {'year' : '\d{2,4}', 'month' : '\d{1,2}'})
    
    map.connect('/{year}', controller='post', 
                action='archive', 
                requirements = {'year' : '\d{2,4}'})
    
    map.connect('/category/{path}', controller='tag', 
                action='category', 
                requirements = {'path' : '[-\w]+'})
    
    # Not a big fan of hardcoding in these actions,
    # but I'm unsure how to proceed otherwise in order to get
    # a nice clean url for the tag path
    map.connect('/tag/{action}', controller='tag', 
                requirements = {'action' : 'cloud|new|create|edit|save|list|delete'})
    
    map.connect('/tag/{path}', controller='tag', 
                action='archive', 
                requirements = {'path' : '[-\w]+'})
    
    map.connect('/{path}', controller='page', 
                action='view', 
                requirements = {'path' : '[-\w]+'})
    
    map.redirect('/{path}/', '/{path}', _redirect_code='301 Moved Permanently')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
