"""Message packet."""

import re
from collections import namedtuple

from .packet import Packet


class MessageComponent(namedtuple("Component", ("type", "data", "text"))):
    """:obj:`MessagePacket` component.

    Valid Types:

    =========   =====================================   ===================
    Type        Description                             Sample Data
    =========   =====================================   ===================
    text        Plaintext of any length.                Hello, world.
    emoji       Single emoji.                           🌵
    tag         Single user tag or mention.             Username
    url         URL.                                    https://google.com
    variable    Key to be replaced with live values.    %ARGS%
    =========   =====================================   ===================

    Parameters
    ----------
    type : :obj:`str`
        Component type.
    data : :obj:`str`
        Component data.
    text : :obj:`str`
        Text representation of the component.
    """


class MessagePacket(Packet):
    """Packet to store messages.

    Parameters
    ----------
    message : :obj:`dict`, :obj:`tuple`, :obj:`str`, or :obj:`MessageComponent`
        Message content components.

        :obj:`dict` should contain ``"type"``, ``"data"``, and ``"text"`` keys.

        :obj:`tuple` will be interpreted as ``(type, data, text)``. If not
        supplied, ``text`` will be equivalent to ``data``.

        :obj:`str` will be interpreted as a component with ``type`` text.
    user : :obj:`str`
        The sender of the MessagePacket.
    role : :obj:`int`
        The role ID of the sender.
    action : :obj:`bool`
        Whether or not the message was sent in action form.
    target : :obj:`str` or :obj:`None`
        The single user target of the message.
    """

    def __init__(self, *message, user="", role=1, action=False, target=None):
        super().__init__()

        message = list(message)
        for index, chunk in enumerate(message):
            if isinstance(chunk, dict):
                message[index] = MessageComponent(**chunk)
            elif isinstance(chunk, tuple):
                if len(chunk) == 2:
                    chunk = chunk + (chunk[1],)
                message[index] = MessageComponent(*chunk)
            elif isinstance(chunk, str):
                message[index] = MessageComponent("text", chunk, chunk)

        self.message = message
        self._condense()

        self.user = user
        self.role = role
        self.action = action
        self.target = target

    def __str__(self):
        return "<Message: {} - \"{}\">".format(self.user, self.text)

    def __len__(self):
        return len(''.join(
            chunk.text for chunk in self.message
            if chunk.type == "text"
        ))

    def __getitem__(self, key):

        if isinstance(key, int):
            return ''.join(
                chunk.text for chunk in self.message
                if chunk.type == "text"
            )[key]

        elif isinstance(key, slice):

            if key.stop is not None or key.step is not None:
                raise NotImplementedError  # TODO

            count = key.start or 0
            message = self.message.copy()

            for index, component in enumerate(message.copy()):
                if component.type == "text":
                    if len(component.text) <= count:
                        count -= len(component.text)
                        message.pop(0)
                    else:
                        while count > 0:
                            new_text = component.text[1:]
                            component = message[index] = component._replace(
                                text=new_text, data=new_text)
                            count -= 1
                else:
                    message.pop(0)
                if count == 0:
                    return self.copy(*message)
            return self.copy(*message)

        raise TypeError

    def __contains__(self, item):
        for chunk in self.message:
            if chunk.type == "text" and item in chunk.text:
                return True
        return False

    def __iter__(self):
        return self.message.__iter__()

    def __add__(self, other):

        return MessagePacket(
            *(self.message + other.message),
            user=self.user or other.user,
            role=self.role or other.role,
            action=self.action or other.action,
            target=self.target or other.target
        )

    def _condense(self):

        message = [self.message[0]]

        for component in self.message[1:]:

            if message[-1].type == component.type == "text":
                new_text = message[-1].text + component.text
                message[-1] = message[-1]._replace(
                    data=new_text, text=new_text)
            else:
                message.append(component)

        self.message = message

        return self

    @property
    def text(self):
        """Pure text representation of the packet.

        Returns
        -------
        :obj:`str`
            Joined ``text`` of every component.

        Examples
        --------
        >>> MessagePacket("Hello, world! ", ("emoji", "😃")).text
        'Hello, world! 😃'
        """
        return ''.join(chunk.text for chunk in self.message)

    @property
    def json(self):
        """JSON representation of the packet.

        Returns
        -------
        :obj:`dict`
            Object attributes, in a JSON-compatible format.

        Examples
        --------
        >>> import pprint
        >>> pprint.pprint(MessagePacket("Hello, world! ", ("emoji", "😃")).json)
        {'action': False,
         'message': [{'data': 'Hello, world! ',
                      'text': 'Hello, world! ',
                      'type': 'text'},
                     {'data': '😃', 'text': '😃', 'type': 'emoji'}],
         'role': 1,
         'target': None,
         'user': ''}
        """
        return {
            "message": [
                dict(component._asdict()) for component in self.message
            ],
            "user": self.user,
            "role": self.role,
            "action": self.action,
            "target": self.target
        }

    @classmethod
    def from_json(cls, json):
        """Convert :obj:`MessagePacket` JSON into an object.

        Parameters
        ----------
        json : :obj:`dict`
            The JSON dictionary to convert.

        Returns
        -------
        :obj:`MessagePacket`

        Examples
        --------
        >>> MessagePacket.from_json({
        ...     'action': False,
        ...     'message': [{'type': 'text',
        ...                  'data': 'Hello, world! ',
        ...                  'text': 'Hello, world! '},
        ...                 {'data': '😃', 'text': '😃', 'type': 'emoji'}],
        ...     'role': 1,
        ...     'target': None,
        ...     'user': ''
        ... }).text
        'Hello, world! 😃'
        """
        return cls(*json.pop("message"), **json)

    def copy(self, *args, **kwargs):
        """Return a copy of :obj:`self`.

        Parameters
        ----------
        *args
            If any are provided, will entirely override :attr:`self.message`.
        **kwargs
            Each will override class attributes provided in :func:`__init__`.

        Returns
        -------
        :obj:`MessagePacket`
            Copy of :obj:`self`, with replaced attributes as specified in
            ``args`` and ``kwargs``.
        """

        _args = args or self.message

        _kwargs = {
            "user": self.user,
            "role": self.role,
            "action": self.action,
            "target": self.target
        }
        _kwargs.update(kwargs)

        return MessagePacket(*_args, **_kwargs)

    def replace(self, **values):
        """Replace text in packet.

        Parameters
        ----------
        values : :obj:`dict`
            The text to replace.

        Returns
        -------
        :obj:`MessagePacket`
            :obj:`self`, with replaced text.

        Note
        ----
        Modifies the object itself. Does *not* return a copy.

        Examples
        --------
        >>> packet = MessagePacket("Hello, world!")
        >>> packet.replace(world="universe").text
        'Hello, universe!'

        >>> packet = MessagePacket("Hello, world!")
        >>> packet.replace(**{
        ...     "Hello": "Goodbye",
        ...     "world": "Python 2"
        ... }).text
        'Goodbye, Python 2!'
        """
        for index, chunk in enumerate(self.message):
            for old, new in values.items():
                if new is not None:
                    new_text = chunk.text.replace(old, new)
                    new_data = new_text if chunk.type == "text" else chunk.data
                    self.message[index] = self.message[index]._replace(
                        data=new_data, text=new_text)
                    chunk = self.message[index]
        return self

    def sub(self, pattern, repl):
        """Perform regex substitution on packet.

        Parameters
        ----------
        pattern : :obj:`str`
            Regular expression to match.
        repl
            The replacement for the `pattern`.

            Accepts the same argument types as :func:`re.sub`.

        Returns
        -------
        :obj:`MessagePacket`
            :obj:`self`, with replaced patterns.

        Note
        ----
        Modifies the object itself. Does *not* return a copy.

        Examples
        --------
        >>> packet = MessagePacket("I would like 3 ", ("emoji", "😃"), "s.")
        >>> packet.sub(r"\\d+", "<number>").text
        'I would like <number> 😃s.'
        """
        for index, chunk in enumerate(self.message):
            if chunk.type in ("text", "url"):
                self.message[index] = self.message[index]._replace(
                    text=re.sub(pattern, repl, chunk.text))
        return self

    def split(self, separator=' ', maximum=None):
        """Split into multiple MessagePackets, based on a separator.

        Parameters
        ----------
        separator : :obj:`str`, default `' '`
            The characters to split the string with.
        maximum : :obj:`int` or :obj:`None`
            The maximum number of splits to perform.

            If less than the total number of potential splits, will result in a
            list of length `maximum + 1`.
            Otherwise, will perform all splits.

            If :obj:`None`, will perform all splits.

        Returns
        -------
        :obj:`list` of :obj:`MessagePacket`s

        Examples
        --------
        >>> packet = MessagePacket("0 1 2 3 4 5 6 7")
        >>> [component.text for component in packet.split()]
        ['0', '1', '2', '3', '4', '5', '6', '7']

        >>> packet = MessagePacket("0 1 2 3 4 5 6 7")
        >>> [component.text for component in packet.split("2")]
        ['0 1 ', ' 3 4 5 6 7']

        >>> packet = MessagePacket("0 1 2 3 4 5 6 7")
        >>> [component.text for component in packet.split(maximum=3)]
        ['0', '1', '2', '3 4 5 6 7']
        """

        result = []
        components = []

        if maximum is None:
            maximum = float('inf')

        for component in self:

            if len(result) == maximum:
                components.append(component)
                continue

            is_text = component.type == "text"
            if not is_text or separator not in component.text:
                components.append(component)
                continue

            new = MessageComponent("text", "", "")

            for index, character in enumerate(component.text):
                if len(result) == maximum:
                    new_text = new.text + component.text[index:]
                    new = new._replace(data=new_text, text=new_text)
                    break

                if character == separator:
                    components.append(new._replace())
                    result.append(components.copy())
                    components.clear()
                    new = new._replace(data="", text="")
                else:
                    new_text = new.text + character
                    new = new._replace(data=new_text, text=new_text)

            components.append(new)

        result.append(components)

        result = [
            filter(lambda component: component.text, message)
            for message in result
            if any(component.text for component in message)
        ]

        return [self.copy(*message) for message in result]

    @classmethod
    def join(cls, *packets, separator=''):
        """Join multiple message packets together.

        Parameters
        ----------
        *packets : :obj:`MessagePacket`
            The packets to join.
        separator : str
            The string to place between every packet.

        Returns
        -------
        :obj:`MessagePacket`
            Packet containing joined contents.

        Examples
        --------
        >>> MessagePacket.join(MessagePacket("a"), MessagePacket("b"), Message\
Packet("c")).text
        'abc'

        >>> MessagePacket.join(MessagePacket("a"), MessagePacket("b"), Message\
Packet("c"), separator='-').text
        'a-b-c'
        """

        if not packets:
            return MessagePacket("")

        result = packets[0]

        for packet in packets[1:]:

            result += MessagePacket(separator)
            result += packet

        return result
