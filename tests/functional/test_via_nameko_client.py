from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


def test_hello_microservice():
    """
    GIVEN a Nameko client
    WHEN the 'hello_microservice.hello({"name": <name>})' is invoked and given a dictionary argument having a name member
    THEN that name's value should appear in the returned formatted string
    """
    with ClusterRpcProxy(CONFIG) as rpc:
        result = rpc.hello_microservice.hello({"name": "Nameko Client"})
        assert result == {"hello": {"response": "Hello, Nameko Client!"}}


def test_hello2_microservice():
    """
    GIVEN a Nameko client
    WHEN the 'hello2_microservice.hello2(name)' is invoked and given a name argument
    THEN that name argument should appear in the returned formatted string
    """
    with ClusterRpcProxy(CONFIG) as rpc:
        result = rpc.hello2_microservice.hello2("Nameko Client")
        assert result == "Hello, Nameko Client!"

