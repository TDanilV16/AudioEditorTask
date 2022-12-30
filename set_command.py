from abc import ABCMeta, abstractmethod


class SetAudioEditorOperation(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self):
        return

    @abstractmethod
    def undo(self):
        return


def main():
    pass


if __name__ == "__main__":
    main()
