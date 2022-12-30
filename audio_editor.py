import os
import subprocess
import file_manager
import tempfile
import shutil
import chronicler
from set_command import SetAudioEditorOperation


class CutAudioOperation(SetAudioEditorOperation):
    def __init__(self, input_file_name, start, stop, tmp_dir, delete_old="f"):
        self.input_file_name = input_file_name
        self.start = start
        self.stop = stop
        self.delete_old = delete_old
        self.tmp_dir = tmp_dir
        self.exit_file_name = ""

    def __call__(self):
        if self.delete_old == "t":
            file_format = get_audio_format(self.input_file_name)
            exit_file_name = "cut_{}.{}".format(self.input_file_name[:-4], file_format)
            self.exit_file_name = exit_file_name
            command = "ffmpeg -i {} -ss {} -to {} {}".format(self.input_file_name, self.start, self.stop,
                                                             exit_file_name)
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.communicate()
            chronicler.write_history_of_file(self.input_file_name, "удален")
            chronicler.write_history_of_file(self.exit_file_name, "создан")
            shutil.copy(self.input_file_name, self.tmp_dir + "/" + self.input_file_name)
            os.remove(self.input_file_name)
        elif self.delete_old == "f":
            file_format = get_audio_format(self.input_file_name)
            exit_file_name = "cut_{}.{}".format(self.input_file_name[:-4], file_format)
            command = "ffmpeg -i {} -ss {} -to {} {}".format(self.input_file_name, self.start, self.stop,
                                                             exit_file_name)
            process = subprocess.Popen(command)
            process.communicate()
            chronicler.write_history_of_file(self.exit_file_name, "обрезаная копия исходного")
        else:
            return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: {self.delete_old}"

    def undo(self):
        if self.delete_old == "f":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)
        elif self.delete_old == "t":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            chronicler.write_history_of_file(self.input_file_name, "восстановлен")
            os.remove(self.exit_file_name)
            shutil.move(self.tmp_dir + "/" + self.input_file_name, os.getcwd())


class ConcatAudioOperation(SetAudioEditorOperation):
    def __init__(self, exit_file_name, audio_files, tmp_dir, delete_old="f"):
        self.exit_file_name = exit_file_name
        self.audio_files = audio_files
        self.tmp_dir = tmp_dir
        self.delete_old = delete_old

    def __call__(self):
        if self.delete_old == "f":
            t = "|".join(self.audio_files)
            command = "ffmpeg -i concat:{} {}".format(str(t), self.exit_file_name)
            process = subprocess.Popen(command)
            process.communicate()
            chronicler.write_history_of_file(self.exit_file_name, "создан в результате конкатенации")
        elif self.delete_old == "t":
            t = "|".join(self.audio_files)
            command = "ffmpeg -i concat:{} {}".format(str(t), self.exit_file_name)
            process = subprocess.Popen(command)
            process.communicate()
            chronicler.write_history_of_file(self.exit_file_name, "создан в результате конкатенации")
            for file in set(self.audio_files):
                shutil.copy(file, self.tmp_dir + "/" + file)
                os.remove(file)
                chronicler.write_history_of_file(file, "удален")
        else:
            return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: {self.delete_old}"

    def undo(self):
        if self.delete_old == "f":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)
        elif self.delete_old == "t":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)
            for file in set(self.audio_files):
                shutil.move(self.tmp_dir + "/" + file, os.getcwd())
                chronicler.write_history_of_file(file, "восстановлен")


class SpeedUpAudioOperation(SetAudioEditorOperation):
    def __init__(self, input_file_name, times, tmp_dir, delete_old="f"):
        self.input_file_name = input_file_name
        self.times = times
        self.tmp_dir = tmp_dir
        self.delete_old = delete_old

    def __call__(self):
        if 1 <= float(self.times) <= 100:
            if self.delete_old == "f":
                file_format = get_audio_format(self.input_file_name)
                self.exit_file_name = "speedup_{}.{}".format(self.input_file_name[:-4], file_format)
                command = "ffmpeg -i {} -af atempo={} {}".format(self.input_file_name, self.times, self.exit_file_name)
                process = subprocess.Popen(command)
                process.communicate()
                chronicler.write_history_of_file(self.exit_file_name, "ускоренная копия исходного")
            elif self.delete_old == "t":
                file_format = get_audio_format(self.input_file_name)
                self.exit_file_name = "speedup_{}.{}".format(self.input_file_name[:-4], file_format)
                command = "ffmpeg -i {} -af atempo={} {}".format(self.input_file_name, self.times, self.exit_file_name)
                process = subprocess.Popen(command)
                process.communicate()
                chronicler.write_history_of_file(self.exit_file_name, "ускоренная копия исходного")
                chronicler.write_history_of_file(self.input_file_name, "удален")
                shutil.copy(self.input_file_name, self.tmp_dir + "/" + self.input_file_name)
                os.remove(self.input_file_name)
            else:
                return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: " \
                       f"{self.delete_old}"
        else:
            return "Параметр изменения звука должен быть в пределах от 1 до 100. Попробуйте еще раз."

    def undo(self):
        if self.delete_old == "f":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)
        elif self.delete_old == "t":
            shutil.copy(self.tmp_dir + "/" + self.input_file_name, os.getcwd())
            chronicler.write_history_of_file(self.input_file_name, "восстановлен")
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)


class SlowDownAudioOperation(SetAudioEditorOperation):
    def __init__(self, input_file_name, times, tmp_dir, delete_old="f"):
        self.input_file_name = input_file_name
        self.times = times
        self.tmp_dir = tmp_dir
        self.delete_old = delete_old

    def __call__(self):
        if 0.5 <= float(self.times) <= 1:
            if self.delete_old == "f":
                file_format = get_audio_format(self.input_file_name)
                self.exit_file_name = "slowdown_{}.{}".format(self.input_file_name[:-4], file_format)
                command = "ffmpeg -i {} -af atempo={} {}".format(self.input_file_name, self.times,
                                                                 self.exit_file_name)
                process = subprocess.Popen(command)
                process.communicate()
                chronicler.write_history_of_file(self.exit_file_name, "замедленная копия исходного")
            elif self.delete_old == "t":
                file_format = get_audio_format(self.input_file_name)
                self.exit_file_name = "slowdown_{}.{}".format(self.input_file_name[:-4], file_format)
                command = "ffmpeg -i {} -af atempo={} {}".format(self.input_file_name, self.times,
                                                                 self.exit_file_name)
                process = subprocess.Popen(command)
                process.communicate()
                chronicler.write_history_of_file(self.exit_file_name, "замедленная копия исходного")
                chronicler.write_history_of_file(self.input_file_name, "удален")
                shutil.copy(self.input_file_name, self.tmp_dir + "/" + self.input_file_name)
                os.remove(self.input_file_name)
            else:
                return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: " \
                       f"{self.delete_old}"
        else:
            return "Параметр изменения звука должен быть в пределах от 1 до 100. Попробуйте еще раз."

    def undo(self):
        if self.delete_old == "f":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)
        elif self.delete_old == "t":
            shutil.copy(self.tmp_dir + "/" + self.input_file_name, os.getcwd())
            chronicler.write_history_of_file(self.input_file_name, "восстановлен")
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)


class ChangeAudioVolumeOperation(SetAudioEditorOperation):
    def __init__(self, input_file_name, action, k, tmp_dir, delete_old="f"):
        self.input_file_name = input_file_name
        self.action = action
        self.k = k
        self.tmp_dir = tmp_dir
        self.delete_old = delete_old

    def __call__(self):
        file_format = get_audio_format(self.input_file_name)
        self.exit_file_name = "{}_volume_{}.{}".format(self.action, self.input_file_name[:-4], file_format)
        if self.action == "i":
            if "dB" in self.k:
                command = 'ffmpeg -i {} -filter:a "volume={}" {}'.format(self.input_file_name, self.k,
                                                                         self.exit_file_name)
            else:
                command = 'ffmpeg -i {} -filter:a "volume={}" {}'.format(self.input_file_name, 1 + float(self.k),
                                                                         self.exit_file_name)
        elif self.action == "r":
            if "dB" in self.k:
                command = 'ffmpeg -i {} -filter:a "volume=-{}" {}'.format(self.input_file_name, self.k,
                                                                          self.exit_file_name)
            else:
                command = 'ffmpeg -i {} -filter:a "volume={}" {}'.format(self.input_file_name, 1 - float(self.k),
                                                                         self.exit_file_name)
        else:
            return "Неверная команда! Попробуй снова"

        if self.delete_old == "f":
            process = subprocess.Popen(command)
            process.communicate()
            chronicler.write_history_of_file(self.exit_file_name, "изменена громкость звука исходного файла")
        elif self.delete_old == "t":
            process = subprocess.Popen(command)
            process.communicate()
            chronicler.write_history_of_file(self.exit_file_name, "изменена громкость звука исходного файла")
            chronicler.write_history_of_file(self.input_file_name, "удален")
            shutil.copy(self.input_file_name, self.tmp_dir + "/" + self.input_file_name)
            os.remove(self.input_file_name)
        else:
            return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: " \
                   f"{self.delete_old}"

    def undo(self):
        if self.delete_old == "f":
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)
        elif self.delete_old == "t":
            shutil.copy(self.tmp_dir + "/" + self.input_file_name, os.getcwd())
            chronicler.write_history_of_file(self.input_file_name, "восстановлен")
            shutil.copy(self.exit_file_name, self.tmp_dir + "/" + self.exit_file_name)
            chronicler.write_history_of_file(self.exit_file_name, "удален")
            os.remove(self.exit_file_name)


def change_volume(input_file_name, action, k, delete_old="f"):
    file_format = get_audio_format(input_file_name)
    exit_file_name = "{}_volume_{}.{}".format(action, input_file_name[:-4], file_format)
    if action == "i":
        if "dB" in k:
            command = 'ffmpeg -i {} -filter:a "volume={}" {}'.format(input_file_name, k, exit_file_name)
        else:
            command = 'ffmpeg -i {} -filter:a "volume={}" {}'.format(input_file_name, 1 + float(k), exit_file_name)
    elif action == "r":
        if "dB" in k:
            command = 'ffmpeg -i {} -filter:a "volume=-{}" {}'.format(input_file_name, k, exit_file_name)
        else:
            command = 'ffmpeg -i {} -filter:a "volume={}" {}'.format(input_file_name, 1 - float(k), exit_file_name)
    else:
        return "Wrong command! Try again!"
    if delete_old == "t":
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate()
        os.remove(input_file_name)
    elif delete_old == "f":
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate()
    else:
        return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: {delete_old}"


def get_audio_format(input_file_name):
    return input_file_name.split('.')[-1]
