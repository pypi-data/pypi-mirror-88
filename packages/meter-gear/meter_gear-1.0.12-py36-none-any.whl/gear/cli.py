from jsonrpcserver import async_dispatch
import json
from aiohttp import web
from .rpc import make_version
from .meter.account import (
    solo,
    keystore as _keystore,
)
from .meter.client import meter
import requests
import click
from datetime import datetime


res_headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Connection": "keep-alive",
}


async def handle(request, logging=False, debug=False):
    jreq = await request.json()
    reqStr = json.dumps(jreq)
    arrayNeeded = True
    if not isinstance(jreq, list):
        jreq = [jreq]
        arrayNeeded = False

    print('*'*40+"\nRaw Req:", reqStr, "\n"+"*"*40)
    responses = []
    for r in jreq:
        method = r['method']
        # request = await request.text()
        response = await async_dispatch(json.dumps(r), basic_logging=logging, debug=debug)
        if response.wanted:
            print(json.dumps(response.deserialized()))
            responses.append(json.loads(json.dumps(response.deserialized())))

    if len(responses):
        print("-"*40+"\nRPC Call:", method, "\nTime: ", datetime.now().timestamp(),
              "\nRequest:", reqStr, "\nResponse:", json.dumps(responses)+"\n"+"-"*40)
        if arrayNeeded:
            return web.json_response(responses, headers=res_headers, status=response.http_status)
        else:
            return web.json_response(responses[0], headers=res_headers, status=response.http_status)
    else:
        return web.Response(headers=res_headers, content_type="text/plain")


@click.command()
@click.option(
    "--host",
    default="127.0.0.1",
)
@click.option(
    "--port",
    default=8545,
    type=int,
)
@click.option(
    "--endpoint",
    default="http://127.0.0.1:8669",
)
@click.option(
    "--keystore",
    default="",
)
@click.option(
    "--passcode",
    default="",
)
@click.option(
    "--log",
    default=False,
    type=bool,
)
@click.option(
    "--debug",
    default=False,
    type=bool,
)
def run_server(host, port, endpoint, keystore, passcode, log, debug):
    print('run server')
    try:
        print(endpoint)
        response = requests.options(endpoint)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Unable to connect to Meter-Restful server.")
        return

    print(make_version())
    print("Listening on %s:%s" % (host, port))

    meter.set_endpoint(endpoint)
    if keystore == "":
        meter.set_accounts(solo())
    else:
        meter.set_accounts(_keystore(keystore, passcode))

    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(headers=res_headers))
    app.router.add_post("/", lambda r: handle(r, log, debug))
    app.router.add_options("/", lambda r: web.Response(headers=res_headers))
    app.router.add_get(
        "/health", lambda r: web.Response(headers=res_headers, body="OK", content_type="text/plain"))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    run_server()
