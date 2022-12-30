class CommandManager(object):
    def __init__(self):
        self.undo_commands = []
        self.redo_commands = []

    def push_undo_command(self, command):
        """Push the given command to the undo command stack."""
        self.undo_commands.append(command)

    def pop_undo_command(self):
        """Remove the last command from the undo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.

        """
        try:
            last_undo_command = self.undo_commands.pop()
        except IndexError:
            print("Пока никаких изменений не было. Отменять нечего :)")
            return
        return last_undo_command

    def push_redo_command(self, command):
        """Push the given command to the redo command stack."""
        self.redo_commands.append(command)

    def pop_redo_command(self):
        """Remove the last command from the redo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.

        """
        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            print("Пока вы не отменили какие-либо изменения, откатывать нечего :)")
            return
        return last_redo_command

    def do(self, command):
        """Execute the given command. Exceptions raised from the command are
        not catched.

        """
        command()
        self.push_undo_command(command)
        # clear the redo stack when a new command was executed
        self.redo_commands[:] = []

    def undo(self, n=1):
        """Undo the last n commands. The default is to undo only the last
        command. If there is no command that can be undone because n is too big
        or because no command has been emitted yet, EmptyCommandStackError is
        raised.

        """
        for _ in range(n):
            command = self.pop_undo_command()
            if command is not None:
                command.undo()
                self.push_redo_command(command)
            else:
                return "Пока никаких изменений не было, откатывать нечего"

    def redo(self, n=1):
        """Redo the last n commands which have been undone using the undo
        method. The default is to redo only the last command which has been
        undone using the undo method. If there is no command that can be redone
        because n is too big or because no command has been undone yet,
        EmptyCommandStackError is raised.

        """
        for _ in range(n):
            command = self.pop_redo_command()
            if command is not None:
                command()
                self.push_undo_command(command)
            else:
                return "Пока никаких изменений не было, откатывать нечего"


def main():
    pass


if __name__ == "__main__":
    main()
