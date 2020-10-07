"""Plotly Dash HTML layout override edilecek dosya."""

html_layout = '''
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
              <link rel="shortcut icon" href="/static/img/favicon.ico" type="image/x-icon" />
            {%css%}
        </head>
        <body class="dash-template">
            <header>
            </header>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
'''
