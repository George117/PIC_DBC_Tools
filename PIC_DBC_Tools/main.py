import time


FILE_HEADER = """/* Microchip Technology Inc. and its subsidiaries.  You may use this software
 * and any derivatives exclusively with Microchip products.
 *
 * THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS".  NO WARRANTIES, WHETHER
 * EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
 * WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
 * PARTICULAR PURPOSE, OR ITS INTERACTION WITH MICROCHIP PRODUCTS, COMBINATION
 * WITH ANY OTHER PRODUCTS, OR USE IN ANY APPLICATION.
 *
 * IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
 * INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
 * WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
 * BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE.  TO THE
 * FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS
 * IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF
 * ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *
 * MICROCHIP PROVIDES THIS SOFTWARE CONDITIONALLY UPON YOUR ACCEPTANCE OF THESE
 * TERMS.
 */

/*
 * File:
 * Author: John117
 * Comments:
 * Revision history:
 */

// This is a guard condition so that contents of this file are not included
// more than once.
#ifndef XC_CAN_APP_H
#define	XC_CAN_APP_H

#include <xc.h> // include processor files - each processor file is guarded.
#include "can1.h"

/*TX*/
CAN_MSG_OBJ TX_Frame_Low;

/*RX*/
CAN_MSG_OBJ RX_Frame_Low;\n\n"""


FILE_FOOTER = """

void Main_TX(struct TX *TX_Frames, uint8_t Frame_ID);
void Main_RX(struct RX *RX_Frames);

#ifdef	__cplusplus
extern "C" {
#endif /* __cplusplus */

    // TODO If C++ is being used, regular C code needs function names to have C 
    // linkage so the functions can be used by the c code. 

#ifdef	__cplusplus
}
#endif /* __cplusplus */

#endif	/* XC_CAN_APP_H */"""

NETWORK_NODES = "BU_: "
MESSAGE = "BO_"
SIGNAL = "SG_"
NEW_LINE = "\n"

START_INDEX_OF_MESSAGE = 0


# Frame data in raw frame
RAW_FRAME_ID_POSITION = 1
RAW_FRAME_NAME_POSITION = 2
RAW_FRAME_DLC_POSITION = 3
RAW_FRAME_TRANSMITTER_POSITION = 4

# Signal data in raw signal
RAW_SIGNAL_NAME_POSITION = 2
RAW_SIGNAL_SIZE_POSITION = 4

frames = []
frame = []
frame_list = []
signal = []


tx_node = "PSU_Controller"


if __name__ == '__main__':
    dbc = open("dbc\\Tank.dbc")

    for file_index, line in enumerate(dbc):
        # find all the network nodes
        if NETWORK_NODES in line:
            network_nodes = line.strip(NETWORK_NODES)
            network_nodes = network_nodes.strip(NEW_LINE)
            network_nodes = network_nodes.split(" ")
            START_INDEX_OF_MESSAGE = file_index

    # get back to start of file
    dbc.seek(0)

    for file_index, line in enumerate(dbc):
        if file_index > START_INDEX_OF_MESSAGE:
            # find messages
            if MESSAGE in line:
                if "3221225472" not in line:
                    signal = []
                    raw_frame = line.strip(MESSAGE)
                    raw_frame = raw_frame.strip(NEW_LINE)
                    raw_frame = raw_frame.split(" ")

                    frame_name = raw_frame[RAW_FRAME_NAME_POSITION]
                    frame_name = frame_name.strip(":")

                    frame_id = raw_frame[RAW_FRAME_ID_POSITION]
                    frame_dlc = raw_frame[RAW_FRAME_DLC_POSITION]
                    frame_transmitter = raw_frame[RAW_FRAME_TRANSMITTER_POSITION]

                    frame_list = [frame_transmitter, frame_name, frame_id, frame_dlc, signal]
                    frames.append(frame_list)

            if SIGNAL in line:
                try:
                    signal = None
                    signal = line.strip(NEW_LINE)
                    signal = signal.split(" ")

                    signal_name = signal[RAW_SIGNAL_NAME_POSITION]

                    signal_size = signal[RAW_SIGNAL_SIZE_POSITION]
                    signal_size_start = signal_size.find("|")
                    signal_size_stop  = signal_size.find("@")
                    signal_size = signal_size[signal_size_start + 1: signal_size_stop]

                    signal_start = signal[RAW_SIGNAL_SIZE_POSITION]
                    signal_start_start = signal_start.find(":")
                    signal_start_stop = signal_start.find("|")
                    signal_start = signal_start[signal_start_start + 1: signal_start_stop]

                    signal = [signal_name, signal_size, signal_start]

                    frames[-1][4].append(signal[:])

                except:
                    pass


    # for frame in frames:
    #     print("Frame: " + frame[1])
    #     print("ID: " + frame[2])
    #     print("DLC: " + frame[3])
    #     print("TX Node: " + frame[0])
    #     print("Signals: ")
    #     for i in range(len(frame[4])):
    #         print("\t" + frame[4][i][0])
    #     print("\n\n")

    generated_file = open("can_app.h", "w")
    generated_file.write(FILE_HEADER)

    # define id's
    for frame in frames:
        id_define = "#define " + frame[1] + "_ID \t\t" + frame[2] + "\n"
        generated_file.write(id_define)

    generated_file.write("\n\n")

    # compose structs
    for frame in frames:
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
    for frame in frames:
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
    for frame in frames:
        if frame[0] != tx_node:
            gen_tx = "\t struct Frame_" + frame[1] + "\t" + frame[1] + ";\n"
            generated_file.write(gen_tx)
        else:
            pass
        gen_rx = "}RX_Frames;\n"
    generated_file.write(gen_rx)

    generated_file.write(FILE_FOOTER)
    generated_file.close()
    dbc.close()
