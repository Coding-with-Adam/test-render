import time
import dash
from dash import DiskcacheManager, CeleryManager, Input, Output, html
import os

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)
else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

app = dash.Dash(__name__, background_callback_manager=background_callback_manager)

app.layout = html.Div([
    html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
     html.Button(id="button_id", children="Run Job!"),
])

@dash.callback(
    output=Output("paragraph_id", "children"),
    inputs=Input("button_id", "n_clicks"),
    background=True,
)
def update_clicks(n_clicks):
    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    app.run_server(debug=True)
