import pathlib
import json
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from constants import ASSETS_PATH

app = dash.Dash(
    name = __name__,
    assets_folder="assets",
    meta_tags= [{"name": "viewport", "content": "width=device-width"}],
)
server = app.server

predicted_dict_dir = str(ASSETS_PATH.joinpath('predict_data.json'))
actual_dict_dir = str(ASSETS_PATH.joinpath('actual_data.json'))

with open(predicted_dict_dir) as file:
    predicted_dict = json.load(file)

with open(actual_dict_dir) as file:
    actual_dict = json.load(file)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H4(
                    "Number of Hate Crimes againt Racial Minorities in U.S. by States",
                    style={"marginBottom": "10px","textAlign" : "center"}
                ),
                html.P(
                    "HackIllinois 2021",
                    style={"marginBottom": "10px","textAlign" : "center"},
                    id="description"
                )
            ],
            id="header"
        ),
    ],
    className='App'
)

if __name__ == "__main__":
    app.run_server(debug=True)