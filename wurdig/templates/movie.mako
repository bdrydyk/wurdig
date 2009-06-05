<%! from wurdig.controllers.movie import movie_form %>

<html>
    <head><title>ToscaWidgets Tutorial</title></head>
    <body>
        <h1>Welcome to the ToscaWidgets tutorial!</h1>
        ${movie_form(movie)|n}
    </body>
</html>