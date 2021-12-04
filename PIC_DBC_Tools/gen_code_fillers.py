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
RAW_SIGNAL_RECEIVER_NODE_POSITION = 9



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