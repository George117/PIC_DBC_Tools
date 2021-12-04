import gen_code_fillers as FILLER

tx_node = "PSU_Controller"

def print_frames(dbc_frames):
    """
    Print found frames
    :param dbc_frames:
    :return: None
    """
    for individual_frame in dbc_frames:
        print("Frame: " + individual_frame[1])
        print("ID: " + individual_frame[2])
        print("DLC: " + individual_frame[3])
        print("TX Node: " + individual_frame[0])
        print("Signals: ")
        for index in range(len(individual_frame[4])):
            print("\t" + individual_frame[4][index][0])
        print("\n\n")


def get_network_nodes(dbc_file):
    """
    Get a list of network nodes
    Get the index where messages are starting
    :param dbc_file:
    :return: network_nodes, start_index_of_messages
    """
    list_of_network_nodes = []
    start_index_of_messages = 0
    for dbc_file_index, dbc_line in enumerate(dbc_file):
        # find all the network nodes
        if FILLER.NETWORK_NODES in dbc_line:
            list_of_network_nodes = dbc_line.strip(FILLER.NETWORK_NODES)
            list_of_network_nodes = list_of_network_nodes.strip(FILLER.NEW_LINE)
            list_of_network_nodes = list_of_network_nodes.split(" ")
            # store start index
            start_index_of_messages = dbc_file_index
    # get back to start of file
    dbc.seek(0)
    return list_of_network_nodes, start_index_of_messages


def get_frames_and_signals(dbc_file, start_index_of_messages):
    """
    Create list of frames with their respective signals 
    :param dbc_file:
    :param start_index_of_messages:
    :return: list of frames with signals
    """
    frame_list = []
    frames = []
    for file_index, line in enumerate(dbc_file):
        if file_index > start_index_of_messages:
            # find messages
            if FILLER.MESSAGE in line:
                if "3221225472" not in line:
                    signal = []
                    raw_frame = line.strip(FILLER.MESSAGE)
                    raw_frame = raw_frame.strip(FILLER.NEW_LINE)
                    raw_frame = raw_frame.split(" ")

                    frame_name = raw_frame[FILLER.RAW_FRAME_NAME_POSITION]
                    frame_name = frame_name.strip(":")

                    frame_id = raw_frame[FILLER.RAW_FRAME_ID_POSITION]
                    frame_dlc = raw_frame[FILLER.RAW_FRAME_DLC_POSITION]
                    frame_transmitter = raw_frame[FILLER.RAW_FRAME_TRANSMITTER_POSITION]

                    frame_list = [frame_transmitter, frame_name, frame_id, frame_dlc, signal]
                    frames.append(frame_list)

            if FILLER.SIGNAL in line:
                try:
                    signal = None
                    signal = line.strip(FILLER.NEW_LINE)
                    signal = signal.split(" ")

                    signal_name = signal[FILLER.RAW_SIGNAL_NAME_POSITION]

                    signal_receiver_node =signal[FILLER.RAW_SIGNAL_RECEIVER_NODE_POSITION]

                    signal_size = signal[FILLER.RAW_SIGNAL_SIZE_POSITION]
                    signal_size_start = signal_size.find("|")
                    signal_size_stop = signal_size.find("@")
                    signal_size = signal_size[signal_size_start + 1: signal_size_stop]

                    signal_start = signal[FILLER.RAW_SIGNAL_SIZE_POSITION]
                    signal_start_start = signal_start.find(":")
                    signal_start_stop = signal_start.find("|")
                    signal_start = signal_start[signal_start_start + 1: signal_start_stop]

                    signal = [signal_name, signal_size, signal_start, signal_receiver_node]

                    frames[-1][4].append(signal[:])

                except:
                    pass
    return frames


def generate_header_file(found_frames):
    generated_file = open("can_app.h", "w")
    generated_file.write(FILLER.FILE_HEADER)

    # define id's
    for frame in found_frames:
        id_define = "#define " + frame[1] + "_ID \t\t" + frame[2] + "\n"
        generated_file.write(id_define)

    generated_file.write("\n\n")

    # compose structs
    for frame in found_frames:
        gen_frame = "struct Frame_" + frame[1] + "{\n"
        for i in range(len(frame[4])):
            gen_frame = gen_frame + "\t"
            if int(frame[4][i][1]) > 8:
                gen_frame = gen_frame + "uint16_t " + frame[4][i][0]
            else:
                gen_frame = gen_frame + "uint8_t " + frame[4][i][0]
            gen_frame = gen_frame + ";\n"
        gen_frame = gen_frame + "};\n\n"
        generated_file.write(gen_frame)

    generated_file.write("\n")

    gen_tx = "struct TX{\n"
    generated_file.write(gen_tx)
    for frame in found_frames:
        if frame[0] == tx_node:
            gen_tx = "\t struct Frame_" + frame[1] + "\t" + frame[1] + ";\n"
            generated_file.write(gen_tx)
        else:
            pass
        gen_tx = "}TX_Frames;\n"
    generated_file.write(gen_tx)

    generated_file.write("\n")

    gen_rx = "struct RX{\n"
    generated_file.write(gen_rx)
    for frame in found_frames:
        if frame[0] != tx_node:
            if frame[4][0][3] == tx_node:
                print(frame[4][0][3])
                gen_tx = "\t struct Frame_" + frame[1] + "\t" + frame[1] + ";\n"
                generated_file.write(gen_tx)
        else:
            pass
        gen_rx = "}RX_Frames;\n"
    generated_file.write(gen_rx)

    generated_file.write(FILLER.FILE_FOOTER)
    generated_file.close()


if __name__ == '__main__':
    dbc = open("dbc\\Tank.dbc")
    network_nodes, start_index = get_network_nodes(dbc)
    dbc_list_of_frames = get_frames_and_signals(dbc, start_index)
    generate_header_file(dbc_list_of_frames)
    #print_frames(dbc_list_of_frames)
    dbc.close()
