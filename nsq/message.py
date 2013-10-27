TOUCH = '_touch'
FIN = '_fin'
REQ = '_req'


class Message(object):
    """
    A class representing a message received from ``nsqd``.

    If you want to perform asynchronous message processing use the
    :meth:`nsq.Message.enable_async` method, pass the message around,
    and respond using the appropriate instance method.

    NOTE: A calling a message's .finish() and .requeue() methods positively and
    negatively impact the backoff state, respectively.  However, sending the
    backoff=False keyword argument to .requeue() is considered neutral and
    will not impact backoff state.

    :param id: the ID of the message
    :type id: string

    :param body: the raw message body
    :type body: string

    :param timestamp: the timestamp the message was produced
    :type timestamp: int

    :param attempts: the number of times this message was attempted
    :type attempts: int
    """
    def __init__(self, id, body, timestamp, attempts):
        self._async_enabled = False
        self._has_responded = False
        self.id = id
        self.body = body
        self.timestamp = timestamp
        self.attempts = attempts

    def enable_async(self):
        """
        Enables asynchronous processing for this message.

        :class:`nsq.Reader` will not automatically respond to the message upon return of ``message_handler``.
        """
        self._async_enabled = True

    def is_async(self):
        """
        Returns whether or not asynchronous processing has been enabled.
        """
        return self._async_enabled

    def has_responded(self):
        """
        Returns whether or not this message has been responded to.
        """
        return self._has_responded

    def finish(self):
        """
        Respond to ``nsqd`` that you've processed this message successfully (or would like
        to silently discard it).
        """
        assert not self._has_responded
        self._has_responded = True
        self.respond(FIN)

    def requeue(self, **kwargs):
        """
        Respond to ``nsqd`` that you've failed to process this message successfully (and would
        like it to be requeued).

        :param backoff: whether or not :class:`nsq.Reader` should apply backoff handling
        :type backoff: bool

        :param delay: the amount of time (in seconds) that this message should be delayed
        :type delay: int
        """
        assert not self._has_responded
        self._has_responded = True
        self.respond(REQ, **kwargs)

    def touch(self):
        """
        Respond to ``nsqd`` that you need more time to process the message.
        """
        assert not self._has_responded
        self.respond(TOUCH)
