# tnzapi

## Documentation

The documentation for the TNZ API can be found [here][apidocs].

## Versions

`tnzapi` uses a modified version of [Semantic Versioning](https://semver.org) for all changes. [See this document](VERSIONS.md) for details.

### Supported Python Versions

This library supports the following Python implementations:

* Python 3.8
* Python 3.9

## Installation

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python.

    pip install tnzapi

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

    python setup.py install

You may need to run the above commands with `sudo`.

## Getting Started

Getting started with the TNZ API couldn't be easier. Create a
`Client` and you're ready to go.

### API Credentials

The `TNZAPI` needs your TNZ API credentials. You can either pass these
directly to the constructor (see the code below) or via environment variables.

```python
from tnzapi import TNZAPI

client = TNZAPI()

client.Sender = "user@example.com"
client.APIKey = "ABC123"
```

### Send an SMS

```python
from tnzapi import TNZAPI

client = TNZAPI(
    Sender="user@example.com",
    APIKey="ABC123",
)

request = client.Send.SMS(
    Reference="Test",
    MessageText = "Test SMS Message click [[Reply]] to opt out",
    Recipients = ["+64211231234"],
)

response = request.SendMessage()

print(repr(response))
```

### Send a Fax Document

```python
from tnzapi import TNZAPI

client = TNZAPI(
    Sender="user@example.com",
    APIKey="ABC123",
)

request = client.Send.Fax(
    Recipients = "+6491232345",
    Attachments = ["C:\\Document.pdf"]
)

response = request.SendMessage()

print(repr(response))
```

### Make a Call - Text-to-Speech (TTS)

```python
from tnzapi import TNZAPI

client = TNZAPI(
    Sender="user@example.com",
    APIKey="ABC123",
)

request = client.Send.TTS(
    Recipients = "+64211232345",
    Reference = "Voice Test - 64211232345",
    MessageToPeople = "Hi there!"
)

request.AddKeypad(Tone=1,RouteNumber="+6491232345",Play="You pressed 1")

response = request.SendMessage()

print(repr(response))
```

### Make a Call - Upload MP3 / Wav File

```python
from tnzapi import TNZAPI

client = TNZAPI(
    Sender="user@example.com",
    APIKey="ABC123",
)

request = client.Send.Voice(
    Recipients = "+64211232345",
    Reference = "Voice Test - 64211232345",
)

request.AddMessageData("MessageToPeople","C:\\file1.wav")
request.AddMessageData("MessageToAnswerPhones","C:\\file2.wav")

request.AddKeypad(Tone=1,RouteNumber="+6491232345",PlayFile="C:\\file3.wav")

response = request.SendMessage()

print(repr(response))
```

### Getting help

If you need help installing or using the library, please check the [TNZ Contact](https://www.tnz.co.nz/About/Contact/) if you don't find an answer to your question.

[apidocs]: https://www.tnz.co.nz/Docs/PythonAPI/
