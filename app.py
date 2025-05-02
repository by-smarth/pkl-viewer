import dash
from dash import dcc, html, Input, Output, State
import dash_renderjson
import pickle
import json
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout
app.layout = html.Div(
    style={
        'backgroundColor': '#f0f0f0',
        'minHeight': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'flex-start',
        'paddingTop': '50px',
        'fontFamily': 'monospace',
        'color': '#003300',
    },
    children=[
        # Header
        html.H1('🥒 Pickle Viewer', style={'color': '#4CBB17'}),

        # File upload widget
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a .pkl File', style={'color': '#003300', 'textDecoration': 'underline'})
            ]),
            style={
                'width': '400px',
                'height': '100px',
                'lineHeight': '100px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '20px',
                'backgroundColor': '#ffffff',
                'color': '#003300',
                'borderColor': '#4CBB17',
                'fontSize': '16px',
            },
            multiple=False
        ),

        # Container where the Download button will appear
        html.Div(id='button-container', children=[], style={'marginBottom': '20px'}),

        # Collapsible JSON viewer (wrapped in a styled Div)
        html.Div(
            dash_renderjson.DashRenderjson(
                id='json-viewer',
                data={},            # initial empty dict
                max_depth=-1,       # no depth limit
                invert_theme=True   # light theme
            ),
            style={
                'width': '80%',
                'maxWidth': '800px',
                'padding': '20px',
                'backgroundColor': '#ffffff',
                'color': '#222222',
                'border': '1px solid #cccccc',
                'borderRadius': '5px',
                'fontSize': '14px',
                'fontFamily': 'monospace',
                'marginBottom': '50px',
                'overflowX': 'auto'
            }
        ),

        # Hidden download component
        dcc.Download(id="download-json")
    ]
)

# Store the last uploaded JSON to serve for download
uploaded_data = {}

# Callback: handle file upload, parse .pkl, update viewer & show download button
@app.callback(
    Output('json-viewer', 'data'),
    Output('button-container', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if not contents:
        # No file uploaded yet
        return {}, []

    # Decode the uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        # Load the pickle
        data = pickle.load(io.BytesIO(decoded))
        # Store pretty JSON string for download
        uploaded_data['json'] = json.dumps(data, indent=2)

        # Create the Download JSON button
        download_button = html.Button(
            'Download JSON',
            id='download-button',
            n_clicks=0,
            style={
                'backgroundColor': '#4CBB17',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'borderRadius': '5px',
                'fontFamily': 'monospace',
                'fontSize': '16px',
                'cursor': 'pointer'
            }
        )

        # Return the Python object for collapsible viewer, plus the download button
        return data, [download_button]

    except Exception as e:
        # If there's an error loading the pickle
        return {"error": str(e)}, []

# Callback: handle download button click
@app.callback(
    Output('download-json', 'data'),
    Input('download-button', 'n_clicks')
)
def download_json(n_clicks):
    if n_clicks and uploaded_data.get('json'):
        return dict(content=uploaded_data['json'], filename="data.json")
    return dash.no_update

# Run the app
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=True, host='0.0.0.0', port=port)
