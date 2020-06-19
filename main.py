from threading import *
from tkinter.filedialog import *
from tkinter.messagebox import *

from pytube import *

file_size = 0


def completeDownload(stream=None, file_path=None):
    print("download Completed")
    showinfo("Message", "File Downloaded!")


def downloadProgress(stream=None, chunk=None, bytes_remaining=None):
    # get % downloaded
    file_downloaded = (file_size - bytes_remaining)
    percent = float(file_downloaded / file_size) * 100
    dBtn['text'] = "{:00.0f} % Downloaded".format(percent)


def startDownload():
    global file_size
    try:
        url = urlField.get()
        print(url)
        dBtn.config(text='Please Wait...')
        dBtn.config(state=DISABLED)
        path_to_save_video = askdirectory()
        print(path_to_save_video)
        if path_to_save_video is None:
            return

        # creating obj of youtube

        obj = YouTube(url, on_progress_callback=downloadProgress)

        # strms = obj.streams.all()
        # for s in strms:

        strm = obj.streams.first()  # get YTLoader stream 360p
        obj.register_on_complete_callback(completeDownload)
        obj.register_on_progress_callback(downloadProgress)
        file_size = strm.filesize
        print(file_size)
        strm.download(path_to_save_video)
        print("Done!")
        dBtn.config(text="Start Download")
        dBtn.config(state=NORMAL)

    except Exception as e:
        print(e)
        print("error !!")


def startDownloadThread():
    thread = Thread(target=startDownload)
    thread.start()


# GUI Code Section

main = Tk()
main.title("YTDLoader")
main.iconbitmap('icon.ico')
main.geometry("600x600")
main.config(bg='#2C3335')

file = PhotoImage(file='download_icon.png')
headingIcon = Label(main, image=file)
headingIcon.pack(side=TOP, padx=10, pady=10)

urlField = Entry(main, font=("verdena", 18), justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10, pady=10)

dBtn = Button(main, text="Start Download", font=("verdana", 18), relief='ridge', command=startDownloadThread)
dBtn.pack(side=TOP, pady=10)

#main object called infinitely
main.mainloop()
