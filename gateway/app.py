from flask import Flask, request
from nameko.standalone.rpc import ServiceRpcProxy

app = Flask(__name__)


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
    from_loc = request.form['from']
    to_loc = request.form['to']
    with trip_rpc_proxy() as task_proxy:
        task_id = task_proxy.create("fibonacci", n)

    return """
        <html>
            <body>
                <p>
                    Your task is running.
                    <a href="/task/{task_id}">Result</a>
                </p>
            </body>
        </html>
    """.format(task_id=task_id)


@app.route('/task/<string:task_id>')
def task_result(task_id):
    with trip_rpc_proxy() as task_proxy:
        result = task_proxy.get_result(task_id)

    return """
        <html>
            <body>
                <p>The result of task {task_id} is {result}.</p>
            </body>
        </html>
    """.format(task_id=task_id, result=result)


def trip_rpc_proxy():
    config = {'AMQP_URI': 'amqp://guest:guest@localhost/'}
    return ServiceRpcProxy('trip_service', config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
