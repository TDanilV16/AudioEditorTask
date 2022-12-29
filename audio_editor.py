import os
import subprocess
import file_manager
import tempfile


def cut_audio(input_file_name, start, stop, delete_old="f"):
    if delete_old == "t":
        file_format = get_audio_format(input_file_name)
        exit_file_name = "cut_{}.{}".format(input_file_name[:-4], file_format)
        command = "ffmpeg -i {} -ss {} -to {} {}".format(input_file_name, start, stop, exit_file_name)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate()
        os.remove(input_file_name)
    elif delete_old == "f":
        file_format = get_audio_format(input_file_name)
        exit_file_name = "cut_{}.{}".format(input_file_name[:-4], file_format)
        command = "ffmpeg -i {} -ss {} -to {} {}".format(input_file_name, start, stop, exit_file_name)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate()
    else:
        return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: {delete_old}"
    # if change_orig == "t":
    #     temp_file = tempfile.NamedTemporaryFile()
    #     temp_file_name = str(temp_file.name).split("/")[-1] + file_format
    #     command = "ffmpeg -i {} -ss {} -to {} {}".format(input_file_name, start, stop, temp_file_name)
    #     subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #     os.remove(input_file_name)
    #     command = "ffmpeg -i {} {}".format(temp_file_name, input_file_name)
    #     subprocess.Popen(command)


def concat_audio(exit_file_name, audio_files):
    t = "|".join(audio_files)
    command = "ffmpeg -i concat:{} {}".format(str(t), exit_file_name)
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()


def speedup_audio(input_file_name, times, delete_old="f"):
    if 1 <= int(times) <= 100:
        if delete_old == "t":
            file_format = get_audio_format(input_file_name)
            exit_file_name = "speedup_{}.{}".format(input_file_name[:-4], file_format)
            command = "ffmpeg -i {} -af atempo={} {}".format(input_file_name, times, exit_file_name)
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.communicate()
            os.remove(input_file_name)
        elif delete_old == "f":
            file_format = get_audio_format(input_file_name)
            exit_file_name = "speedup_{}.{}".format(input_file_name[:-4], file_format)
            command = "ffmpeg -i {} -af atempo={} {}".format(input_file_name, times, exit_file_name)
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.communicate()
        else:
            return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: {delete_old}"
    else:
        return "Неправильно указан параметр изменения звука. Попробуйте еще раз."


def slowdown_audio(input_file_name, times, delete_old="f"):
    if delete_old == "t":
        file_format = get_audio_format(input_file_name)
        exit_file_name = "slowdown_{}.{}".format(input_file_name[:-4], file_format)
        command = "ffmpeg -i {} -af atempo={} {}".format(input_file_name, times, exit_file_name)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate()
        os.remove(input_file_name)
    elif delete_old == "f":
        file_format = get_audio_format(input_file_name)
        exit_file_name = "slowdown_{}.{}".format(input_file_name[:-4], file_format)
        command = "ffmpeg -i {} -af atempo={} {}".format(input_file_name, times, exit_file_name)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.communicate()
    else:
        return f"Неправильно указан параметр модификации исходного аудио. Ожидали: f/t, получили: {delete_old}"


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


def redo():
    pass


def undo():
    pass


def get_audio_format(input_file_name):
    return input_file_name.split('.')[-1]


