from flask import Flask, request
from nameko.standalone.rpc import ServiceRpcProxy

app = Flask(__name__)


RABBIT_HOST_NAME = "rabbit"


@app.route('/')
def take_taxi():
    return """
        <html>
            <body>
                <h1>Take Taxi</h1>
                <h2>Select Destination</h2>
                <form action="/assign_driver" method="post">
                    From:
                    <input type="text" name="from">
                    To:
                    <input type="text" name="to">
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    """


@app.route('/assign_driver', methods=['POST'])
def assign_driver():
    with driver_rpc_proxy() as task_proxy:
        driver_id = task_proxy.create("ashkan")

    with passenger_rpc_proxy() as task_proxy:
        passenger_id = task_proxy.create("akbar")

    from_loc = request.form['from']
    to_loc = request.form['to']

    with trip_rpc_proxy() as task_proxy:
        trip_id = task_proxy.create(passenger_id, driver_id, from_loc, to_loc)

    return """
        <html>
            <body>
                <p>
                    Your trip is set.
                    <a href="/trip/{trip_id}">Result</a>
                </p>
            </body>
        </html>
    """.format(trip_id=trip_id)


@app.route('/trip/<string:trip_id>')
def trip_result(trip_id):
    with trip_rpc_proxy() as task_proxy:
        result = task_proxy.get(trip_id)

    return """
        <html>
            <body>
                <p>The result of trip {trip_id} is {result}.</p>
            </body>
        </html>
    """.format(trip_id=trip_id, result=result)


def trip_rpc_proxy():
    config = {'AMQP_URI': f'amqp://guest:guest@{RABBIT_HOST_NAME}/'}
    return ServiceRpcProxy('trip_service', config)


def passenger_rpc_proxy():
    config = {'AMQP_URI': f'amqp://guest:guest@{RABBIT_HOST_NAME}/'}
    return ServiceRpcProxy('passenger_service', config)


def driver_rpc_proxy():
    config = {'AMQP_URI': f'amqp://guest:guest@{RABBIT_HOST_NAME}/'}
    return ServiceRpcProxy('driver_service', config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
