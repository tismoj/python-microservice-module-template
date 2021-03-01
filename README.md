# python-microservice-module-template

This project serves as the main template for the creation of python modules composed of several related microservices, with the intent to work in conjunction with my other project the microservice-event-receiver (https://github.com/tismoj/microservice-event-receiver).

## HOW TO USE:

### Install Procedure for microservice-event-receiver
- Clone microservice-event-receiver from GitHub
```bash
$ git clone https://github.com/tismoj/microservice-event-receiver && cd microservice-event-receiver
```

### Startup Procedure for microservice-event-receiver
- Startup all microservices and support apps for microservice-event-receiver
```bash
$ docker-compose up -d --build
```

### Logs Monitoring for microservice-event-receiver
- To view logs from microservice-event-receiver
```bash
$ docker-compose logs -f
```

### Install Procedure for python-microservice-module-template
- Clone python-microservice-module-template from GitHub
```bash
$ git clone https://github.com/tismoj/python-microservice-module-template && cd python-microservice-module-template
```

### Startup Procedure for python-microservice-module-template
- Startup all microservices and support apps for python-microservice-module-template
```bash
$ docker-compose up -d --build
```

### Logs Monitoring for python-microservice-module-template
- To view logs from python-microservice-module-template
```bash
$ docker-compose logs -f
```

### Typical / Normal RESTapi Request via Curl
- To send a Request directly to the sample microservice hello_microservice
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/hello/ -d '{"name": "tismoj"}'
{"hello":{"response":"Hello, tismoj!"}}
```

### Sending of a similar Request through the event_receiver, without any microservice, registered to receive it
- To send a similar Request through the event_receiver, but prior to registering hello_microservice to any events
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/receive_event/request_from_human -d '{"name": "tismoj while unregistered"}'
{"event_received":{"data":{"name":"tismoj while unregistered","transaction_id":"20201228220527.235058"},"event":"request_from_human:20201228220527.235058"}}
```

### Sending of another similar Request through the event_receiver, with a microservice, registered to receive it
- To register hello_microservice to the event request_from_human
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/register_for_events/ -d '{"events_to_register": [{"event": "request_from_human", "urls_to_register": [{"url": "http://<ip of your machine>:8800/hello/"}]}]}'
{"registered_for_events": {"request_from_human": {"http://<ip of your machine>:8800/hello/": {}}}}
```

- To send a similar Request through the event_receiver, but this time hello_microservice is registered to receive all events of the event request_from_human
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/receive_event/request_from_human -d '{"name": "tismoj now registered"}'
{"event_received":{"data":{"name":"tismoj now registered","transaction_id":"20201228220741.306084"},"event":"request_from_human:20201228220741.306084"}}
```

- To check if the event is actually received by the hello_microservice, we could only check through the api_1 app, as I still couldn't figure out how to log prints from any microservice started via nameko
```bash
$ docker-compose logs api
...
api_1                                    | In RegisterForEvents: Listen for Events with JSON data: {'events_to_register': [{'event': 'request_from_human', 'urls_to_register': [{'url': 'http://<ip of your machine>:8800/hello/'}]}]}
api_1                                    | Micro-service returned with a response: {"registered_for_events": {"request_from_human": {"http://<ip of your machine>:8800/hello/": {}}}}
api_1                                    | 172.27.0.1 - - [28/Dec/2020 22:07:24] "POST /register_for_events/ HTTP/1.1" 200 -
api_1                                    | In ReceiveEvent: Received event: request_from_human, with JSON data: {'name': 'tismoj now registered'}
api_1                                    | Micro-service returned with a response: {"event_received": {"event": "request_from_human:20201228220741.306084", "data": {"name": "tismoj now registered", "transaction_id": "20201228220741.306084"}}}
api_1                                    | 172.27.0.1 - - [28/Dec/2020 22:07:41] "POST /receive_event/request_from_human HTTP/1.1" 200 -
api_1                                    | In Hello: Received Event with JSON data: {'name': 'tismoj now registered', 'transaction_id': '20201228220741.306084'}
api_1                                    | Microservice returned with a response: {"hello": {"response": "Hello, tismoj now registered!"}}
api_1                                    | 172.27.0.9 - - [28/Dec/2020 22:07:41] "POST /hello/ HTTP/1.1" 200 -
...
```
### Sending a new event without again any registered microservice to receive
- Send a request with a new event name request_from_animal
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/receive_event/request_from_animal -d '{"name": "cat"}'
{"event_received":{"data":{"name":"cat","transaction_id":"20201228230007.695724"},"event":"request_from_animal:20201228230007.695724"}}
```

### Registering hello_microservice for the new Event, but triggering to send all prior events starting from a given "datetime_start"
- To also register hello_microservice to the event request_from_animal, with a datetime_start requirement
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/register_for_events/ -d '{"events_to_register": [{"event": "request_from_animal", "urls_to_register": [{"url": "http://<ip of your machine>:8800/hello/", "datetime_start": "20201228230007.0"}]}]}'
{"registered_for_retro_event_retrieval": {"request_from_animal": {"http://<ip of your machine>:8800/hello/": {"datetime_start": "20201228230007.0"}}}}
```
```bash
$ docker-compose logs api
...
In RegisterForEvents: Listen for Events with JSON data: {'events_to_register': [{'event': 'request_from_animal', 'urls_to_register': [{'url': 'http://<ip of your machine>:8800/hello/', 'datetime_start': '20201228230007.0'}]}]}
Micro-service returned with a response: {"registered_for_retro_event_retrieval": {"request_from_animal": {"http://<ip of your machine>:8800/hello/": {"datetime_start": "20201228230007.0"}}}}
172.27.0.1 - - [28/Dec/2020 23:21:12] "POST /register_for_events/ HTTP/1.1" 200 -
In Hello: Received Event with JSON data: {'name': 'cat', 'transaction_id': '20201228230007.695724'}
Microservice returned with a response: {"hello": {"response": "Hello, cat!"}}
172.27.0.10 - - [28/Dec/2020 23:21:12] "POST /hello/ HTTP/1.1" 200 -
...
```


- To send another request with the new event request_from_animal, but this time hello_microservice is registered to receive all events of the event request_from_animal as well
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/receive_event/request_from_animal -d '{"name": "dog"}'
{"event_received":{"data":{"name":"dog","transaction_id":"20201228232305.280595"},"event":"request_from_animal:20201228232305.280595"}}
```
```bash
$ docker-compose logs api
...
Micro-service returned with a response: {"event_received": {"event": "request_from_animal:20201228232305.280595", "data": {"name": "dog", "transaction_id": "20201228232305.280595"}}}
172.27.0.1 - - [28/Dec/2020 23:23:05] "POST /receive_event/request_from_animal HTTP/1.1" 200 -
In Hello: Received Event with JSON data: {'name': 'dog', 'transaction_id': '20201228232305.280595'}
Microservice returned with a response: {"hello": {"response": "Hello, dog!"}}
172.27.0.9 - - [28/Dec/2020 23:23:05] "POST /hello/ HTTP/1.1" 200 -
...
```

### Registering to retrieve past events given a "count"
- To register and retrieve past events, with a count requirement
```bash
$ curl -X POST -H 'Content-Type: application/json' localhost:8880/register_for_events/ -d '{"events_to_register": [{"event": "request_from_human", "urls_to_register": [{"url": "http://<ip of your machine>:8800/hello/", "datetime_start": "20200101000000.0", "count": 1}]}]}'
{"registered_for_retro_event_retrieval": {"request_from_human": {"http://<ip of your machine>:8800/hello/": {"datetime_start": "20200101000000.0", "count": 1}}}}
```
```bash
$ docker-compose logs api
...
In RegisterForEvents: Listen for Events with JSON data: {'events_to_register': [{'event': 'request_from_human', 'urls_to_register': [{'url': 'http://<ip of your machine>:8800/hello/', 'datetime_start': '20200101000000.0', 'count': 1}]}]}
Micro-service returned with a response: {"registered_for_retro_event_retrieval": {"request_from_human": {"http://<ip of your machine>:8800/hello/": {"datetime_start": "20200101000000.0", "count": 1}}}}
172.27.0.1 - - [28/Dec/2020 23:44:38] "POST /register_for_events/ HTTP/1.1" 200 -
In Hello: Received Event with JSON data: {'name': 'tismoj while unregistered', 'transaction_id': '20201228220527.235058'}
Microservice returned with a response: {"hello": {"response": "Hello, tismoj while unregistered!"}}
172.27.0.10 - - [28/Dec/2020 23:44:38] "POST /hello/ HTTP/1.1" 200 -
...
```

## TODO:
- Create additional sample microservices to properly show the other already implemented features (transaction_id, datetime_end, required_data, listener_data)
