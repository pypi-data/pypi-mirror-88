import asyncio
import datetime
import functools
import inspect
from inspect import Parameter
import logging
import os
import time
import warnings
from enum import Enum
from typing import Any, Callable, List
import json
import uvicorn
from fastapi import Body, Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.concurrency import run_in_threadpool
from pydantic import create_model, validate_arguments

from mvi.logger import setup_logging
from mvi.db import initialize_db, remove_db, write_to_ts
from mvi import session
from mvi.monitoring_api import (
    get_monitored_data_json,
    get_monitored_data_db,
    get_monitored_data_csv,
)

setup_logging(logging.DEBUG)

logger = logging.getLogger(__name__)

MVI_MANAGER_URL = os.environ.get("MVI_MANAGER_URL", "http://host.docker.internal")
MVI_MANAGER_HOSTNAME = os.environ.get("MVI_MANAGER_HOSTNAME", "localhost")

MVI_SERVICE_NAME = os.environ.get("mvi.name", "unknown")
MVI_SERVICE_VERSION = os.environ.get("mvi.version", "0.0.0")
MVI_SERVICE_TOKEN = os.environ.get("mvi.auth", "unknown")


def get_headers() -> dict:
    """Generating headers for API calls

    Returns:
        dict: Assembled header
    """
    return {
        "Authorization": f"Bearer {MVI_SERVICE_TOKEN}",
        "Content-Type": "application/json",
        "Host": MVI_MANAGER_HOSTNAME,
    }


def get_authorized_domains() -> list:
    """Returns list of autorized domains for auth header

    Returns:
        list: List of authorized domains
    """
    return [MVI_MANAGER_HOSTNAME]


class Severity(Enum):
    INFO = 0
    WARNING = 1
    CRITICAL = 2


class MviService:
    def __init__(self):
        self.app = FastAPI(
            root_path=f"/services/{MVI_SERVICE_NAME}_{MVI_SERVICE_VERSION}",
            title=f"{MVI_SERVICE_NAME} {MVI_SERVICE_VERSION}",
            description="Automatically generated, interactive API documentation",
        )
        self.parameters_endpoints = {}
        self.app.get("/~parameters")(self.get_all_parameters)
        self.app.on_event("startup")(initialize_db)
        self.app.on_event("shutdown")(remove_db)

        self.app.get("/~monitor")(get_monitored_data_json)
        self.app.get("/~monitor/csv")(get_monitored_data_csv)
        self.app.get("/~monitor/db")(get_monitored_data_db)

    def get_all_parameters(self) -> dict:
        """Get all registered parameter endpoints

        \f
        Returns:
            dict: The registered parameters and their current value
        """
        return self.parameters_endpoints

    def get_parameter(self, parameter: str) -> Any:
        """Get specific parameter

        Args:
            parameter (str): The name of the parameter

        Returns:
            Any: The value of the parameter
        """
        return self.parameters_endpoints[parameter]

    def add_parameter(self, parameter: str, value: Any, monitor: bool = False):
        """Adds a parameter to the parameter endpoints.

        Args:
            parameter (str): The name of the parameter
            value: (Any): The value of the parameter
            monitor (bool): Whether or not to track this parameter for monitoring.
                If true, the value of this parameter will be saved when changed.
                Defaults to False.

        Returns:
            dict: The parameter and its value
        """
        path = f"/~parameters/{parameter}"

        update_request = create_model(
            f"{parameter}_schema", value=(value.__class__, ...)
        )

        def update_parameter(update_request: update_request):
            logger.info(
                f"Parameter changed from: {self.parameters_endpoints[parameter]}"
                f" to {update_request.value}"
            )
            self.parameters_endpoints[parameter] = update_request.value
            if monitor:
                store(**{parameter: update_request.value})
            return {parameter: update_request.value}

        def get_parameter():
            return self.parameters_endpoints[parameter]

        self.parameters_endpoints[parameter] = value

        # Monitor initial value
        if monitor:
            store(**{parameter: value})

        # Register GET and POST endpoints for the new parameter
        self.app.get(path)(get_parameter)
        self.app.post(path)(update_parameter)
        return {parameter: value}

    def run(self):
        """Runs the service

        This method is usually called at the end of the module when all
        entrypoints etc for the service has been specified
        """
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    def call_every(
        self,
        seconds: float,
        wait_first: bool = False,
    ):
        """Returns a decorator that converts a function to an awaitable that runs
        every `seconds`.

        Decorate a function with this method to make it run repeatedly::

            @mvi.call_every(seconds=60)
            def my_function():
                ....

        Args:
            seconds (float): Interval between calls in seconds
            wait_first (bool): If we should skip the first execution. Defaults to False.

        Returns:
            Callable: The decorator
        """

        def timed_task_decorator(func: Callable) -> Callable:
            """Puts the decorated `func` in a timed asynchronous loop and
            returns the unwrapped `func` again.

            Args:
                func (Callable): The function to be called repeatedly

            Returns:
                Callable: The same function that was inputted
            """
            is_coroutine = asyncio.iscoroutinefunction(func)

            async def timer():

                # Sleep before first call if required
                if wait_first:
                    await asyncio.sleep(seconds)

                # Run forever
                while True:
                    # For timing purposes
                    t_0 = time.time()

                    # Await `func` and log any exceptions
                    try:
                        if is_coroutine:
                            # Non-blocking code, defined by `async def`
                            await func()
                        else:
                            # Blocking code, defined by `def`
                            await run_in_threadpool(func)
                    except Exception:  # pylint: disable=broad-except
                        logger.exception(f"Exception in {func}")

                    # Timing check
                    remainder = seconds - (time.time() - t_0)
                    if remainder < 0:
                        warnings.warn(
                            f"Function {func} has an execution time the exceeds"
                            f" the requested execution interval of {seconds}s!",
                            UserWarning,
                        )

                    # Sleep until next time
                    await asyncio.sleep(max(remainder, 0))

            # Put `timer` on the event loop on service startup
            @self.app.on_event("startup")
            async def _starter():
                asyncio.ensure_future(timer())

            return func

        return timed_task_decorator

    def entrypoint(
        self, func: Callable = None, monitor: bool = False, **fastapi_kwargs
    ) -> Callable:
        """Registers a function as an entrypoint, which will make it reachable
        as an HTTP method on your host machine.

        Decorate a function with this method to create an entrypoint for it::

            @mvi.entrypoint
            def my_function(arg1:type1) -> type2:
                ....

        It is strongly recommended to include types of the arguments and return
        objects for the decorated function.

        Args:
            func (Callable): The decorated function to make an entrypoint for.
            monitor (bool): Set if the input and output to this entrypoint should
                be saved to the service's monitoring database.
            **fastapi_kwargs: Keyword arguments for the resulting API endpoint.
                See FastAPI for keyword arguments of the ``FastAPI.post()`` function.

        Raises:
            TypeError: If :obj:`func` is not callable.

        Returns:
            Callable: The decorated function: :obj:`func`.
        """
        # pylint: disable=protected-access
        def entrypoint_decorator(deco_func):
            funcname = deco_func.__name__
            path = f"/{funcname}"
            signature = inspect.signature(deco_func)

            # Update default values to fastapi Body parameters to force all parameters
            # in a json body for the resulting HTTP method
            new_params = []
            request_sig = inspect.Parameter(
                "request", Parameter.POSITIONAL_OR_KEYWORD, annotation=Request
            )
            new_params.append(request_sig)
            for parameter in signature.parameters.values():
                if parameter.default == inspect._empty:
                    default = Ellipsis
                else:
                    default = parameter.default
                new_params.append(parameter.replace(default=Body(default, embed=True)))

            @functools.wraps(deco_func)
            # async is required for the request.body() method.
            async def wrapper(request: Request, *args, **kwargs):
                result = await run_in_threadpool(deco_func, *args, **kwargs)

                if monitor:
                    request_body = await request.body()
                    json_response = json.dumps(jsonable_encoder(result))
                    store(
                        **{
                            f"{funcname}_request": request_body.decode("utf-8"),
                            f"{funcname}_response": json_response,
                        }
                    )
                return result

            # Update the signature
            signature = signature.replace(parameters=new_params)
            wrapper.__signature__ = signature

            # Get response_model from return type hint
            return_type = signature.return_annotation
            if return_type == inspect._empty:
                return_type = None

            # Give priority to explicitly given response_model
            kwargs = dict(response_model=return_type)
            kwargs.update(fastapi_kwargs)

            # Create API endpoint
            self.app.post(path, **kwargs)(wrapper)

            # Wrap the original func in a pydantic validation wrapper and return that
            return validate_arguments(deco_func)

        # This ensures that we can use the decorator with or without arguments
        if not (callable(func) or func is None):
            raise TypeError(f"{func} is not callable.")
        return entrypoint_decorator(func) if callable(func) else entrypoint_decorator


def store(**variables):
    """Saves variables to the service's monitoring database. Supports
    integers, floats and strings.

    Args:
        **variables: Variables to save to the database.
    """
    timestamp = datetime.datetime.utcnow()
    for variable, value in variables.items():
        write_to_ts(name=variable, value=value, timestamp=timestamp)


def call_service(
    service_name: str,
    entrypoint_name: str,
    arguments: dict = None,
    service_version: str = None,
) -> Any:
    """Call an entrypoint in a different service.

    Example usage::

        data = call_service(
            service_name="data_connector",
            entrypoint_name= "get_data",
        )

    Args:
        service_name (str): The service which contains the entrypoint to call.
        entrypoint_name (str): The name of the entrypoint to call.
            The return object(s) of this entrypoint must be jsonable, i.e pass FastAPI's
            jsonable_encoder, otherwise it won't be reachable.
        arguments (dict): Arguments to the entrypoint.
            In the form: {"argument_name": value, ...}. Default None.
        service_version (str): The specific version of the service to call.
            Default None, the main version and the shadows versions will be called.

    Returns:
        Any: The output from the entrypoint in the other service.
    """
    if service_version:
        url = (
            f"{MVI_MANAGER_URL}/services/"
            + f"{service_name}_{service_version}/{entrypoint_name}"
        )
    else:
        url = f"{MVI_MANAGER_URL}/services/{service_name}/{entrypoint_name}"

    arguments = arguments if arguments else {}

    if service_version:
        logger.info(
            f"Calling entrypoint: {entrypoint_name} in service: "
            f"{service_name} ({service_version}) with: {arguments}"
        )
    else:
        logger.info(
            f"Calling entrypoint: {entrypoint_name} in service: "
            f"{service_name} with: {arguments}"
        )
    logger.info(f"Sending POST request to: {url}")

    response = session.request(
        "POST",
        url=url,
        auth_domains=get_authorized_domains(),
        headers=get_headers(),
        json=arguments,
    )

    logger.info(
        f"Response from entrypoint: {response.text}, code: {response.status_code}"
    )
    return response.json()


def notify(
    msg: str,
    severity: Severity,
    dashboard: bool = True,
    emails: List[str] = None,
    timer: int = 0,
):
    """Generates and sends a notification

    Args:
        msg (str): The message to include for the recipient of the notification.
        severity (Severity): The severity of the notification.
        dashboard (bool): If this is True, the notification will be shown
            on the mvi dashboard. Defaults to True.
        emails (List[str]): List of emails to send the notifications to.
            Defaults to None, in which case no emails are sent
        timer (int): The amount of time (in seconds) that has to pass
            before the same notification can be send again. Defaults to 0.
    """
    url = f"{MVI_MANAGER_URL}/notifications/"

    timer = 0 if timer < 0 else timer

    payload = {
        "service_name": MVI_SERVICE_NAME,
        "service_version": MVI_SERVICE_VERSION,
        "msg": msg,
        "severity": severity.value,
        "dashboard": dashboard,
        "emails": emails,
        "timer": timer,
        "timestamp": str(datetime.datetime.utcnow()),
    }

    logger.info(f"Notification was posted: {payload} to url: {url}")
    session.request(
        "POST",
        url,
        auth_domains=get_authorized_domains(),
        headers=get_headers(),
        json=payload,
    )
