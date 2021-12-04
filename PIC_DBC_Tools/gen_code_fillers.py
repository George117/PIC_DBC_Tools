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


HEADER_FILE_HEADER = """/* Microchip Technology Inc. and its subsidiaries.  You may use this software
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
#include "bit_settings.h"

/*TX*/
CAN_MSG_OBJ TX_Frame_Low;

/*RX*/
CAN_MSG_OBJ RX_Frame_Low;\n\n"""


HEADER_FILE_FOOTER = """

void Main_TX(struct TX *TX_Frames, uint8_t Frame_ID);
void Main_RX(struct RX *RX_Frames);
void Main_CAN_Loop(int64_t timebase);

#ifdef	__cplusplus
extern "C" {
#endif /* __cplusplus */

    // TODO If C++ is being used, regular C code needs function names to have C 
    // linkage so the functions can be used by the c code. 

#ifdef	__cplusplus
}
#endif /* __cplusplus */

#endif	/* XC_CAN_APP_H */"""


SOURCE_FILE_HEADER = """
/*
 * File:   can_app.c
 * Author: 117
 *
 */
 

#include <xc.h>
#include "config.h"
#include "can_app.h"

"""
SOURCE_FILE_FOOTER = """

"""

MAIN_TX_HEADER = """
void Main_TX(struct TX *TX_Frames, uint8_t Frame_ID)
{       
    uint8_t CAN_Transmit_Data[8]={0,0,0,0,0,0,0,0};
    
    switch(Frame_ID){
"""

MAIN_TX_FOOTER = """
  }

    TX_Frame_Low.field.brs=CAN_NON_BRS_MODE;
    TX_Frame_Low.field.dlc=DLC_8;
    TX_Frame_Low.field.formatType=CAN_2_0_FORMAT;
    TX_Frame_Low.field.frameType=CAN_FRAME_DATA;
    TX_Frame_Low.field.idType=CAN_FRAME_STD;
    TX_Frame_Low.msgId=Frame_ID;
    TX_Frame_Low.data=CAN_Transmit_Data;

    if(CAN_TX_FIFO_AVAILABLE == (CAN1_TransmitFIFOStatusGet(TXQ) & CAN_TX_FIFO_AVAILABLE)){
        CAN1_Transmit(TXQ, &TX_Frame_Low);
    }
}
"""

MAIN_RX_HEADER = """
void Main_RX(struct RX *RX_Frames)
{
    if(CAN1_ReceivedMessageCountGet() > 0){
        if(true == CAN1_Receive(&RX_Frame_Low)){
            switch(RX_Frame_Low.msgId){
"""

MAIN_RX_FOOTER = """}
        }
    }
    else{
    
    }

}
"""

MAIN_CAN_HEADER = """
void Main_CAN_Loop(int64_t timebase)
{
"""

MAIN_CAN_FOOTER = """
    Main_RX(&RX_Frames);
     __delay_us(1);
}
"""