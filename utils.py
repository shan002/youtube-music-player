import shutil
import vlc
import time


def play_stream(selected_stream):
    Instance = vlc.Instance('--no-video --verbose -1')
    player = Instance.media_player_new()
    Media = Instance.media_new(selected_stream.url)
    Media.get_mrl()
    player.set_media(Media)
    player.play()

    while True:
        player_state = player.get_state()
        # print(player_state)
        if player_state == vlc.State.Playing:
            time.sleep(1)
            if player.get_state() == vlc.State.Playing:
                break
            else:
                return -1
        elif player_state == vlc.State.Ended:
            return -1

    while True:
        time.sleep(2)
        if not player.get_time():
            return -1
        else:
            break
    
    print("\nPlaying ", selected_stream.title, "...")
    while player.is_playing():
        printProgressBar(player.get_position()*100, 100, prefix = 'Progress:', suffix = 'Complete')
        time.sleep(0.5)

    printProgressBar(100, 100, prefix = 'Progress:', suffix = 'Complete')

    return 0


def printProgressBar (iteration, total, prefix = '', suffix = '', usepercent = True, decimals = 1, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        usepercent  - Optoinal  : display percentage (Bool)
        decimals    - Optional  : positive number of decimals in percent complete (Int), ignored if usepercent = False
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    # length is calculated by terminal width
    twx, twy = shutil.get_terminal_size()
    length = twx - 1 - len(prefix) - len(suffix) -4
    if usepercent:
        length = length - 6
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    # process percent
    if usepercent:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='', flush=True)
    else:
        print('\r%s |%s| %s' % (prefix, bar, suffix), end='', flush=True)
    # Print New Line on Complete
    if iteration == total:
        print(flush=True)