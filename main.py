import audio_editor
import file_manager


help = """
       Для разреза аудио команда cut. Пример: cut lalal.mp3 from to. 
       From и to указывают, с какого момента по какой сделать разрез. 
       Для ускорения аудио команда speedup. Пример: speedup lala.mp3 k. 
       K -- во сколько раз ускорить аудио. К принимает значения от 1 до 100 
       Для замедления аудио команда slowdown. Пример: slowdown lala.mp3 k. 
       K -- от 0.5 до 1. В дальнейшем планируется, что к будет от 0 до 1. 
       Для склейки нескольких аудиофайлов команда concat. Пример: oncat lala.mp3 la.mp3 la.mp3 
       Файлы для склейки перечислить через пробел. Ограничения на кол-во файлов нет. 
       Для изменения громкости звука команда cv. Пример: cv lala.mp3 r/i k. 
       r -- убавить звук, i -- увеличить звук (подобрать, что нужно). 
       k -- можно указать просто числом, если хочется изменить звук на сколько-то процентов. 
       А если дописать суффикс dB, то звук изменится на к децибелл. 
       Пример1: cv lala.mp3 r 50 -- уменьшит звук на 50%. 
       Пример2: cv lala.mp3 i 10dB -- увелиичит звук на 10 децибелл.
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
        Простой аудиоредактор. При редактировании аудио создается новый аудиофайл.
        Напечатайте help, чтоб увидеть доступные команды. Чтобы завершить работу, напечатайте exit.
        """

goodbye_message = """
        Спасибо, что использовали мой аудиоредактор. До новых встреч!
        """


def main():
    print(greetingMessage)
    input_string = ""
    # input_string = input("#>>> ")
    # process_input(input_string)
    while input_string.strip() != "exit":
        input_string = input("#>>> ")
        process_input(input_string)
    print(goodbye_message)
    file_manager.kill_temp_dir()


def process_input(input_string):
    tmp = input_string.split()
    if len(input_string) == 0:
        print("""
        Неверная команда. Попробуйте снова.
        """)
    else:
        command = tmp[0]
        if command == "help":
            print(help)
        elif command == "cut":
            audio_editor.cut_audio(tmp[1], tmp[2], tmp[3])
        elif command == "slowdown":
            audio_editor.slowdown_audio(tmp[1], tmp[2], tmp[3])
        elif command == "speedup":
            audio_editor.speedup_audio(tmp[1], tmp[2], tmp[3])
        elif command == "concat":
            audio_editor.concat_audio(tmp[1], tmp[2:])
        elif command == "cv":
            audio_editor.change_volume(tmp[1], tmp[2], tmp[3], tmp[3])
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
