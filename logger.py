from paho import Mqtt


class Logger:

    __queue = 0
    __topic = 'picar/log'

    def __init__(self, queue, publishTopic):
        self.__queue = queue
        self.__topic = publishTopic
        Mqtt()
        pass

