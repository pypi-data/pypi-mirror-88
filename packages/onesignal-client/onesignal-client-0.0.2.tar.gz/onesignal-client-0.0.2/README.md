# OneSignal client

OneSignal client is a wrapper for the OneSignal API which allows you to send notifications to Android, iOS and Web App.

It is based on ![onesignal-notifications](https://github.com/Lanseuo/onesignal-notifications) library.

## Installation

```
pip install onesignal-client
```

## Usage

```python
from onesignal import OneSignalClient, SegmentNotification

client = OneSignal("MY_APP_ID", "MY_REST_API_KEY")
notification_to_all_users = SegmentNotification(
    contents={
        "en": "Hello from OneSignal-Notifications"
    },
    included_segments=[SegmentNotification.ALL]
)
client.send(notification_to_all_users)
```

## Development

> Contributions are welcome

```
pip install --editable .
```

run the tests

```
export ONESIGNAL_API_KEY="..."
export ONESIGNAL_REST_API_KEY="..."

pytest
```

### Docs

To edit the docs, change the folder and spin up the development server.

```
cd docs
npm install -g vuepress
vuepress dev
```

## Meta

Lucas Hild - [https://lucas-hild.de](https://lucas-hild.de)  
This project is licensed under the MIT License - see the LICENSE file for details
