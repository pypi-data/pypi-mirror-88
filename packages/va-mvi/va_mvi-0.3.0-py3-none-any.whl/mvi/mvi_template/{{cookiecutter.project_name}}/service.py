import logging
from mvi.mvi import MviService, notify, Severity

# First of all, we need to create a multiviz integrator service.
mvi = MviService()

# We need a logger. Logging is good.
# When this service is deployed, all logs will be reachable on the mvi dashboard.
logger = logging.getLogger(__name__)

# The mvi service stores parameters which are readable and changeable from outside
# the service, while it is running
mvi.add_parameter("greeting_phrase", "Hello")


# The '@mvi.entrypoint' decorater is used to make the function
# available via an API entrypoint. By using typed arguments in the
# function signature, you make sure that the function won't be reachable
# with wrong argument types. Convenient!
@mvi.entrypoint
def hello(name: str) -> str:
    # Let's get the latests greeting phrase.
    # It could have been changed to "Hola" or something else.
    greeting_phrase = mvi.get_parameter("greeting_phrase")
    # We want to get notified if someone is trying to greet the world.
    # Notifications shows up on the dashboard, there is also an option of receving
    # the notifications as emails, if wanted.
    if name == "World":
        notify(
            msg="Someone is trying to greet the World, too time consuming. Skipping!",
            severity=Severity.WARNING,
            emails=None,
        )
        return "Greeting failed"
    # Let's make sure that we log what we are doing!
    logger.info(f"Greeting someone with the name: {name}")
    return f"{greeting_phrase} {name}"


# Lastly, we need to make sure that our service runs when it is deployed.
mvi.run()
