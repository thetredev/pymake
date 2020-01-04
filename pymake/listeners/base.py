

# =============================================================================
# >> LISTENER BASE TYPE DEFINITION
# =============================================================================
class ListenerBase(object):
    """Class used as a base for listener decorator classes."""

    # A list of listener decorator instances
    manager = None

    def __init__(self):
        """C'tor."""
        # Register the instance
        self.manager.append(self)

        # Store the callback later
        self.callback = None

    def __call__(self, callback):
        """Store the callback so it can be called later."""
        self.callback = callback
