import csv
import tkinter
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt


def reading_csv(file_name):
    with open(file_name, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        row_data = list(reader)
        row_data = [[float(j) for j in i] for i in row_data]
        return row_data


def plot_file(signal_data, title, convolution_plot=False, signal_2_number_of_channels=1):
    time_list = [i for i in range(1, len(signal_data) + 1)]
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.figure(figsize=(6.40, 4.80), dpi=100)

    for channel_number in range(len(signal_data[0])):
        legend_string = 'channel ' + str(channel_number+1)
        if convolution_plot:
            legend_string = 'channel ' + str(channel_number//signal_2_number_of_channels+1) + ' ' + \
                            str(channel_number % signal_2_number_of_channels+1)
        plt.plot(time_list,
                 [channel[channel_number] for channel in signal_data], label=legend_string)

    plt.legend()
    title = '_'.join(title.split())
    title = title + ".png"
    plt.savefig(title, dpi=100)
    plt.clf()


def convolution(signal_1_data, signal_2_data):
    signal_1_length = len(signal_1_data)
    signal_2_length = len(signal_2_data)
    convolution_length = signal_1_length + signal_2_length - 1

    convolution_result = []
    for i in range(convolution_length):
        convolution_result.append([])
    for signal_1_channel_number in range(len(signal_1_data[0])):
        for signal_2_channel_number in range(len(signal_2_data[0])):
            for time in range(convolution_length):
                convolution_at_time_point = 0
                for it in range(max(time-signal_2_length+1, 0), min(signal_1_length, time+1)):
                    convolution_at_time_point = convolution_at_time_point + \
                                                signal_1_data[it][signal_1_channel_number] * \
                                                signal_2_data[time-it][signal_2_channel_number]

                convolution_result[time].append(convolution_at_time_point)

    return convolution_result, len(signal_2_data[0])


files_count = 0
file1 = ''
file2 = ''

window = tkinter.Tk()
window.geometry('1650x1000')
window.title('Convolution')
window.config(bg='black')

font_standard = ('Times New Roman', 32, 'bold')

file_1_upload_status = tkinter.Label(
    window, text='Not submitted yet', font=font_standard, bg='red')
file_2_upload_status = tkinter.Label(
    window, text='Not submitted yet', font=font_standard, bg='red')


def upload1():
    global files_count
    global file1

    format_files = [('Csv files', '*.csv')]
    file1 = tkinter.filedialog.askopenfilename(filetypes=format_files)
    if file1 != "":
        file_1_upload_status.configure(text='Submitted', bg='green')
        files_count = files_count + 1


def upload2():
    global files_count
    global file2

    format_files = [('Csv files', '*.csv')]
    file2 = tkinter.filedialog.askopenfilename(filetypes=format_files)
    if file2 != "":
        file_2_upload_status.configure(text='Submitted', bg='green')
        files_count = files_count + 1


upload_button_1 = tkinter.Button(window, text='Upload file of first signal', font=font_standard, command=upload1)
upload_button_2 = tkinter.Button(window, text='Upload file of second signal', font=font_standard, command=upload2)
upload_button_1.place(x=100, y=100)
upload_button_2.place(x=100, y=300)

file_1_upload_status.place(x=1200, y=115)
file_2_upload_status.place(x=1200, y=315)


def end_button_operations():
    quit()


def submit_button_operations():
    global files_count

    try:
        if files_count < 2:
            files_count = 1 // 0

        submit_button.place_forget()
        file_1_upload_status.place_forget()
        file_2_upload_status.place_forget()
        upload_button_1.place_forget()
        upload_button_2.place_forget()

        first_signal = reading_csv(file1)
        plot_file(first_signal, 'First signal')
        plot1_image = tkinter.PhotoImage(file="First_signal.png")
        plot1_label = tkinter.Label(window, image=plot1_image)
        plot1_label.anchor = plot1_image
        plot1_label.place(x=10, y=10)

        second_signal = reading_csv(file2)
        plot_file(second_signal, 'Second signal')
        plot2_image = tkinter.PhotoImage(file="Second_signal.png")
        plot2_label = tkinter.Label(window, image=plot2_image)
        plot2_label.anchor = plot2_image
        plot2_label.place(x=10, y=510)

        convolution_of_signals, signal_2_number_of_channels = convolution(first_signal, second_signal)
        plot_file(convolution_of_signals, 'Convolution of signals', True, signal_2_number_of_channels)
        plot3_image = tkinter.PhotoImage(file="Convolution_of_signals.png")
        plot3_label = tkinter.Label(window, image=plot3_image)
        plot3_label.anchor = plot3_image
        plot3_label.place(x=990, y=220)

        with open('convolution.csv', 'w', newline='\n') as csv_out_file:
            write = csv.writer(csv_out_file, delimiter=';')
            write.writerows(convolution_of_signals)

        desc_1 = tkinter.Label(window, text='1. signal', font=font_standard, bg='black', fg='white')
        desc_1.place(x=654, y=210)

        desc_2 = tkinter.Label(window, text='2. signal', font=font_standard, bg='black', fg='white')
        desc_2.place(x=654, y=705)

        desc_conv = tkinter.Label(window, text='Convolution of signals', font=font_standard, bg='black', fg='white')
        desc_conv.place(x=1105, y=725)

        end_button = tkinter.Button(window, text='End', font=font_standard, command=end_button_operations,
                                       bg='Green')
        end_button.place(x=1470, y=870)

    except ZeroDivisionError:
        messagebox.showerror('Error', 'Submit both files!')


submit_button = tkinter.Button(window, text='Run', font=font_standard, command=submit_button_operations, bg='green')
submit_button.place(x=750, y=500)


def main():
    window.mainloop()


if __name__ == '__main__':
    main()
