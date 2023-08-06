

def use_image_form(app, routes):
    for route in routes:
        @app.get(route + '/form')
        def _form_route():
            image_form = ((
                '<form method="POST" action="' + route + '" enctype="multipart/form-data"'
                ' style="max-width: 400px; margin: 40px auto; border: 1px solid rgba(0,0,0,0.1); border-radius: 4px; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column;">'
                '<label style="margin-bottom: 20px;">'
                'Select an image to upload'
                '<input type="file" name="image" id="image" />'
                '</label>'
                '<button type="submit">Submit</button>'
                '</form>'
            ))
            return image_form
