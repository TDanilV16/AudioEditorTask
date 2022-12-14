import tempfile

import audio_editor
import file_manager
import chronicler
from command_manager import CommandManager

help = """
       1) Для разреза аудио команда cut. Пример: cut lalal.mp3 from to. 
       From и to указывают, с какого момента по какой сделать разрез. 
       2) Для ускорения аудио команда speedup. Пример: speedup lala.mp3 k. 
       K -- во сколько раз ускорить аудио. К принимает значения от 1 до 100 
       3) Для замедления аудио команда slowdown. Пример: slowdown lala.mp3 k. 
       K -- от 0.5 до 1. В дальнейшем планируется, что к будет от 0 до 1. 
       4) Для склейки нескольких аудиофайлов команда concat. Пример: concat 
       lala.mp3 la.mp3 la.mp3 
       Файлы для склейки перечислить через пробел. Ограничения на кол-во файлов
       нет. 
       5) Для изменения громкости звука команда cv. Пример: cv lala.mp3 r/i k. 
       r -- убавить звук, i -- увеличить звук (подобрать, что нужно). 
       k -- можно указать просто числом, если хочется изменить звук на 
       сколько-то процентов. 
       А если дописать суффикс dB, то звук изменится на к децибелл. 
       Пример1: cv lala.mp3 r 50 -- уменьшит звук на 50%. 
       Пример2: cv lala.mp3 i 10dB -- увелиичит звук на 10 децибелл.
       6) Чтобы узнать глобальную историю изменений, введите history.
       Если хотите узнать историю изменений конкретного файла, введите history 
       и имя файла через пробел.
       Пример: history lala.mp3 выведет историю изменений этого файла. Если же 
       такой файл не существует 
       или не редактировался, то программа не выведет ничего.
       Пример: history выведет глобальную историю изменений файлов (время, 
       название файла, действие).
       7) Команда undo отменяет последнее выполненное действие.
       8) Команда redo отменяет последнее отмененное действие.
       """

# cut lalal.mp3 from to
# speedup lala.mp3 1.5
# slowdown lala.mp3 0.5
# concat lala.mp3 la.mp3 la.mp3
# cv lala.mp3 r/i 50
# cv lala.mp3 r/i 10dB
# set source ///
# set dest ///

temp_dir = file_manager.create_temp_dir()

greetingMessage = """
        Простой аудиоредактор. При редактировании аудио создается новый 
        аудиофайл.
        Напечатайте help, чтоб увидеть доступные команды. Чтобы завершить 
        работу, напечатайте exit.
        """

goodbye_message = """
        Спасибо, что использовали мой аудиоредактор. До новых встреч!
        """


def main():
    print(greetingMessage)
    print(chronicler.get_today_date_and_time())
    input_string = ""
    tmp_dir = tempfile.mkdtemp()
    manager = CommandManager()
    while input_string.strip() != "exit":
        input_string = input("#>>> ")
        process_input(input_string, tmp_dir, manager)
    print(goodbye_message)


def process_input(input_string, tmp_dir, manager):
    tmp = input_string.split()

    if len(input_string) == 0:
        print("""
        Неверная команда. Попробуйте снова.
        """)
    else:
        command = tmp[0]
        if command == "help":
            print(help)
        elif command == "exit":
            pass
        elif command == "redo":
            manager.redo()
        elif command == "undo":
            manager.undo()
        elif command == "history":
            if len(tmp) == 1:
                chronicler.get_all_history()
            elif len(tmp) == 2:
                chronicler.get_history_of_file(tmp[1])
            else:
                print(
                    "Если хотите узнать историю изменений файла, "
                    "введите history и название файла.")
                print(
                    "Если хотите узнать глобальную историю изменений, "
                    "введите history.")
        elif command == "cut":
            if len(tmp) == 5:
                manager.do(
                    audio_editor.CutAudioOperation(tmp[1], tmp[2], tmp[3],
                                                   delete_old=tmp[4],
                                                   tmp_dir=tmp_dir))
            else:
                manager.do(
                    audio_editor.CutAudioOperation(tmp[1], tmp[2], tmp[3],
                                                   tmp_dir=tmp_dir))
        elif command == "slowdown":
            if len(tmp) == 4:
                manager.do(audio_editor.SlowDownAudioOperation(tmp[1], tmp[2],
                                                               tmp_dir,
                                                               tmp[3]))
            elif len(tmp) == 3:
                manager.do(audio_editor.SlowDownAudioOperation(tmp[1], tmp[2],
                                                               tmp_dir))
        elif command == "speedup":
            if len(tmp) == 4:
                manager.do(
                    audio_editor.SpeedUpAudioOperation(tmp[1], tmp[2], tmp_dir,
                                                       tmp[3]))
            elif len(tmp) == 3:
                manager.do(audio_editor.SpeedUpAudioOperation(tmp[1], tmp[2],
                                                              tmp_dir))
        elif command == "concat":
            manager.do(
                audio_editor.ConcatAudioOperation(tmp[1], tmp[2:-1], tmp_dir,
                                                  tmp[-1]))
        elif command == "cv":
            if len(tmp) == 5:
                manager.do(
                    audio_editor.ChangeAudioVolumeOperation(tmp[1], tmp[2],
                                                            tmp[3], tmp_dir,
                                                            tmp[4]))
            elif len(tmp) == 4:
                manager.do(
                    audio_editor.ChangeAudioVolumeOperation(tmp[1], tmp[2],
                                                            tmp[3], tmp_dir))
        elif command == "set":
            if tmp[1] == "source":
                file_manager.set_source_folder(tmp[2])
            elif tmp[1] == "dest":
                file_manager.set_source_folder(tmp[2])
        else:
            print("""
        Команда {} не опознана. Воспользуйтесь help или попробуйте еще раз.
            """.format(command))


if __name__ == '__main__':
    main()
