/*
AID 050403020100
j3viton (alto..)

Juan Antonio Hernandez

Estado VIRGIN_   : La tarjeta solo acepta el comando de perso. este comando incluye la informacion de todos los ficheros incluyendo claves.

private: solo por la clase
protected: acceso para la clase y herederas
public: publico

final static : para constantes
Transiet method para crear variables en RAM

++++++++++++++++++++++++++++++++
Creaci�n (carga + perso) del SAM
++++++++++++++++++++++++++++++++
1 cargar el .CAP
2 intalar con el AID 050403020100
    Aplication parameters (las claves y el PSAM)
    20910070206001B975E1F9C07C10714B0AD06B33A5FDC1B975E1F9C07C10714B0AD06B33A5FDC1A886D00ABF8D0F823A1BEF7C22B6ECD2
    bit CarOnReset

*/

package galiciaSAM;

import javacard.framework.*;
import javacard.security.*;
import javacardx.crypto.*;
import javacard.framework.Util.*;
import org.globalplatform.*;
//import javacard.framework.JCSystem.*;


public class galiciaSAM extends Applet
{
    // Constantes
    private static final boolean CHECK_STATE = true;        // Habilita el chequeo de estados
    private static final boolean CHECK_SIGNATURE = true;    // Habilita el chequeo de la firma de saldo
    private static final boolean BLOCK_SAM = false;         // Habilita el bloqueo del SAM 
    
    private static final byte SAMVersion[] = {(byte)0x0A,(byte)0x03};
    private static final byte SAMSerial[]  = {(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00};  
    
    // Semillas para la derivaci�n de las claves de tarjeta
    private static final byte seedBIN_A[] = {(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0xff,(byte)0xff,(byte)0xff,(byte)0xff};
    private static final byte seedBIN_B[] = {(byte)0x00,(byte)0x50,(byte)0x20,(byte)0x00,(byte)0xff,(byte)0x00,(byte)0x00,(byte)0x00};
    private static final byte seedBIN_C[] = {(byte)0x98,(byte)0x70,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00};
    private static final byte seedBIN_D[] = {(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x98,(byte)0x70,(byte)0x00,(byte)0x00};
    private static final byte seedBIN_E[] = {(byte)0x98,(byte)0x70,(byte)0x00,(byte)0x00,(byte)0xA5,(byte)0xA5,(byte)0xA5,(byte)0x00};
    private static final byte seedBIN_F[] = {(byte)0xA5,(byte)0xA5,(byte)0xA5,(byte)0x00,(byte)0x98,(byte)0x70,(byte)0x00,(byte)0x00};
    
    
    // Claves Madre
    //private static final byte MotherConsumoKEYCard_test[] = {                                         
    //                                  (byte)0xB9, (byte)0x75, (byte)0xE1, (byte)0xF9, (byte)0xC0, (byte)0x7C, (byte)0x10, (byte)0x71, 
    //                                  (byte)0x4B, (byte)0x0A, (byte)0xD0, (byte)0x6B, (byte)0x33, (byte)0xA5, (byte)0xFD, (byte)0xC1};
    //private static final byte MotherConsumoKEYPhone_test[] = {                                            
    //                                  (byte)0xB9, (byte)0x75, (byte)0xE1, (byte)0xF9, (byte)0xC0, (byte)0x7C, (byte)0x10, (byte)0x71, 
    //                                  (byte)0x4B, (byte)0x0A, (byte)0xD0, (byte)0x6B, (byte)0x33, (byte)0xA5, (byte)0xFD, (byte)0xC1};
    //private static final byte MotherSignKEY_test[] = {                                            
    //                                  (byte)0xA8, (byte)0x86, (byte)0xD0, (byte)0x0A, (byte)0xBF, (byte)0x8D, (byte)0x0F, (byte)0x82, 
    //                                  (byte)0x3A, (byte)0x1B, (byte)0xEF, (byte)0x7C, (byte)0x22, (byte)0xB6, (byte)0xEC, (byte)0xD2};

    // Claves derivadas por BIN
    // private static final byte MDK_10[] = { (byte)0xE9, (byte)0xE3, (byte)0x3A, (byte)0xFC, (byte)0x4E, (byte)0x4F, (byte)0x30, (byte)0x63,
                                           // (byte)0x4A, (byte)0xB2, (byte)0xE7, (byte)0x7C, (byte)0xEF, (byte)0x4F, (byte)0x88, (byte)0x07 };
    // private static final byte MDK_20[] = { (byte)0xC4, (byte)0xCC, (byte)0xCB, (byte)0x93, (byte)0x49, (byte)0xF1, (byte)0x68, (byte)0xD9,
                                           // (byte)0x29, (byte)0xE5, (byte)0x88, (byte)0x7C, (byte)0xD0, (byte)0x1E, (byte)0x48, (byte)0x26 };
    // private static final byte MDK_30[] = { (byte)0x12, (byte)0x8E, (byte)0xE4, (byte)0xAE, (byte)0xB5, (byte)0xE8, (byte)0xFD, (byte)0x73,
                                           // (byte)0xB4, (byte)0x2D, (byte)0x3A, (byte)0xDA, (byte)0x7F, (byte)0x4D, (byte)0x43, (byte)0xAE };
    
    // private static final byte MSK_10[] = { (byte)0x38, (byte)0x00, (byte)0x15, (byte)0x37, (byte)0xA0, (byte)0x13, (byte)0xDF, (byte)0xAF,
                                           // (byte)0xA5, (byte)0x19, (byte)0xEB, (byte)0x2A, (byte)0x36, (byte)0x86, (byte)0xD5, (byte)0x04 };
    // private static final byte MSK_20[] = { (byte)0x96, (byte)0x5F, (byte)0x20, (byte)0xB0, (byte)0x2E, (byte)0xD0, (byte)0x99, (byte)0xD6,
                                           // (byte)0xED, (byte)0x30, (byte)0x63, (byte)0xA1, (byte)0xF7, (byte)0xB0, (byte)0xA9, (byte)0x30 };
    // private static final byte MSK_30[] = { (byte)0xBA, (byte)0x9B, (byte)0xAB, (byte)0x2D, (byte)0x84, (byte)0x7E, (byte)0xBF, (byte)0x83,
                                           // (byte)0xAC, (byte)0x3A, (byte)0x77, (byte)0xB3, (byte)0x6D, (byte)0x52, (byte)0x45, (byte)0x85 };
    
    private static final byte SIGN_MASK[] = { (byte)0x14, (byte)0x82, (byte)0x21, (byte)0x48 };
                                    
    // Datos devueltos por el SAM en selectTransportNetwork
    private static final byte SAM_data[] = {(byte) 0x98, (byte)0x70,(byte) 0x20, (byte)0x20,(byte) 0x20, (byte)0x20,(byte) 0x20, (byte)0x01, (byte)0x01};
                             
    // APDUs
    private static byte SAM_CLA =(byte)0x80;

    private static final byte INS_UNBLOCK                   =(byte)0x20;
    //private static final byte INS_PERSO                       =(byte)0x23;
    private static final byte INS_SelectNetwork             =(byte)0x26;
    private static final byte INS_ValChallenge              =(byte)0x28;
    private static final byte INS_InitCertific              =(byte)0x2A;        // lento
    private static final byte INS_CertificarDatos           =(byte)0x2C;        // lento
    private static final byte INS_FinCertificacion          =(byte)0x2E;
    private static final byte INS_VerificarCertificado      =(byte)0x30;
    private static final byte INS_ISO_RD_binary             =(byte)0xB0;
    private static final byte INS_ISO_getResponse           =(byte)0xC0;
    private static final byte INS_ISO_SELECT_FILE           =(byte)0xA4;
    
    private static final byte ATR_[] = {(byte) 0x00,(byte) 0x66, (byte)0x4D,(byte) 0x45, (byte)0x31,(byte) 0x53, (byte)0x05,(byte) 0x06, (byte)0x53, (byte)0x03, (byte)0x61, (byte)0x04, (byte)0xF0};
        
    // Maquina Estados
    private static final byte NON_SELECTED_             =(byte)0x82;
    private static final byte RESET_                    =(byte)0x83;
    private static final byte NETWORK_SELECTED_         =(byte)0x84;
    private static final byte CHALLENGED_               =(byte)0x85;
    private static final byte INITCERTIFICATION_        =(byte)0x86;
    private static final byte CERTIFICAR_DATOS_         =(byte)0x87;
    private static final byte FIN_CERTIFICAR_           =(byte)0x88;
    private static final byte VERIFICAR_CERTIFICADO_    =(byte)0x89;
        
    private static final byte VIRGIN_                   =(byte)0x32;
    private static final byte ACTIVE_                   =(byte)0x33;
    private static final byte BLOCKED_                  =(byte)0x34;
    
    private static final byte DEBIT_SESSION_KEY_CARD    = (byte)0x01;
    private static final byte DEBIT_SESSION_KEY_PHONE   = (byte)0x02;
    private static final byte SIGN_SESSION_KEY          = (byte)0x03;
    
    private static final byte SAM_NUM_FILES             = (byte)7;
    private static final byte SAM_MF                    = (byte)0x00;
    private static final byte SAM_DF_4F10               = (byte)0x01;
    private static final byte SAM_DF_4F11               = (byte)0x02;
    private static final byte SAM_DF_4F12               = (byte)0x03;
    private static final byte SAM_VERSION               = (byte)0x04;
    private static final byte SAM_SERIAL                = (byte)0x05;
    //private static final byte SAM_LOG                     = (byte)0x06; /// DEBUG!!!
    
    private static final byte SAM_NUM_KEYS              = (byte)6;
    
    private static final byte MAX_SIGN_ERROR            = (byte)10;
    
    private static final byte EVENT_INDEX               =(byte)0; // Indice del nuevo evento de la tarjeta en la cadena de datos a certificar
    private static final byte CERT_LEN                  =(byte)1; // Longitud de los datos a certificar
    private static final byte SIGN_STATUS               =(byte)2; // Estado de verificaci�n de la firma del saldo
    private static final byte ESTADO                    =(byte)3; // Estado del applet
    private static final byte SELECTED_FILE             =(byte)4; // Fichero seleccionado
    private static final byte IS_PHONE                  =(byte)5; // Flag que indica que se est� hablando con un tel�fono
    
    
    // FICHEROS                             
    private static final byte EF_info_4F11[]   = {(byte)0x20,(byte)0x91,(byte)0x00,(byte)0x70,(byte)0x20,(byte)0x60,(byte)0x01};    // PSAM(3): Identificador del SAM, PPSAM(4): Identificador del proveedeor del SAM                           
    private static final byte EF_info_4F12[]   = {(byte)0x01,(byte)0x02};   // VK: Version de clave, VAlg: Version de algoritmo
    private static final byte EF_info_4F10[]   = {(byte)0x6F,(byte)0x1A,(byte)0x84,(byte)0x07,(byte)0x98,(byte)0x70,(byte)0x00,(byte)0x02,(byte)0x00,(byte)0x00,(byte)0x00,(byte)0x83,(byte)0x02,(byte)0x4F,(byte)0x10,(byte)0x80,(byte)0x02,(byte)0x17,(byte)0x70,(byte)0x85,(byte)0x03,(byte)0x38,(byte)0x33,(byte)0x80,(byte)0x86,(byte)0x02,(byte)0x20,(byte)0x00};
    private static final byte MF_info[]        = {(byte)0x6F,(byte)0x17,(byte)0x84,(byte)0x04,(byte)0x52,(byte)0x4F,(byte)0x4F,(byte)0x54,(byte)0x83,(byte)0x02,(byte)0x3F,(byte)0x00,(byte)0x80,(byte)0x02,(byte)0x3C,(byte)0x00,(byte)0x85,(byte)0x03,(byte)0x38,(byte)0x00,(byte)0x80,(byte)0x86,(byte)0x02,(byte)0x20,(byte)0x00};

    private static Object[] SAM_Files;
    //private static Object[] SAM_Keys;
    
    //private static final byte EF_Kinfo_0012[] ={0x01,0x01};
    
    // Variables y buffers
    // Claves
    private static DESKey MotherConsumoKEYCard;
    private static DESKey MotherConsumoKEYPhone;
    private static DESKey MotherSignKEY; 
    
    private static DESKey Key_A;    // Atributos?? private
    private static DESKey Key_B; 
    private static DESKey Key_C; 
    private static DESKey Key_Debit_M;
    private static Cipher Cipher_A;  
    private static Signature Sign_Saldo;
                                                                            
    private static byte random_SAM_CARD_[]; // Randoms del SAM y la tarjeta
    private static byte PAN_[];             // PAN de la tarjeta
    private static byte MAC_[];             // MAC calculado
    private static byte debit_sesionK_[];   // Clave de d�bito de sesion
    private static byte sign_sesionK_[];    // Clave de firma de sesion
    private static byte cadenaData_[];      // Datos de entrada del c�lculo del certificado
    
    private static byte auxBuf_[];          // Buffer auxiliar de datos
    private static byte auxKeyBuf_[];       // Buffer auxiliar de claves
    private static byte auxBuf2_[];         // Buffer auxiliar de datos
        
    private static RandomData myRandom01;   // Generador de n�meros aleatorios
    
    private static byte vars_[];            // Buffer para guardar las variables globales 
    
    //private static byte log[]; // DEBUG!!!
    //private static short logL; // DEBUG!!!
    
    // Variables persistentes
    private static byte cardStatus = VIRGIN_;   // Estado de personalizaci�n de la tarjeta
    private static byte signErrCount = 0;       // Contador de firmas/certificados erroneos
     
    // Constructor
    private galiciaSAM(byte bArray[], short bOffset, byte bLength)
    {   
        short tmp;
            
        // Inicializamos variables en el constructor
        Cipher_A = Cipher.getInstance(Cipher.ALG_DES_CBC_ISO9797_M1,false);
        
        // Clave Debit es DES.
        Key_Debit_M =   (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES_TRANSIENT_DESELECT, KeyBuilder.LENGTH_DES, false);
        Key_A = (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES_TRANSIENT_DESELECT, KeyBuilder.LENGTH_DES, false);
        Key_B = (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES_TRANSIENT_DESELECT, KeyBuilder.LENGTH_DES, false);
        
        // Clave 3DES
        Key_C = (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES_TRANSIENT_DESELECT, KeyBuilder.LENGTH_DES3_2KEY, false);
        
        if (MotherConsumoKEYCard == null) // Permanentes
            MotherConsumoKEYCard = (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES, KeyBuilder.LENGTH_DES3_2KEY, false);
        if (MotherConsumoKEYPhone == null) // Permanentes
            MotherConsumoKEYPhone = (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES, KeyBuilder.LENGTH_DES3_2KEY, false);
        if (MotherSignKEY == null) // Permanentes
            MotherSignKEY = (DESKey)KeyBuilder.buildKey(KeyBuilder.TYPE_DES, KeyBuilder.LENGTH_DES3_2KEY, false);
        
        vars_ = JCSystem.makeTransientByteArray((short)6, (byte)JCSystem.CLEAR_ON_DESELECT);
            
        myRandom01 = RandomData.getInstance(RandomData.ALG_SECURE_RANDOM);
        vars_[ESTADO] = RESET_;
        
        MAC_ = JCSystem.makeTransientByteArray((short)8, (byte)JCSystem.CLEAR_ON_DESELECT);
        debit_sesionK_ = JCSystem.makeTransientByteArray((short)8, (byte)JCSystem.CLEAR_ON_DESELECT);
        sign_sesionK_ = JCSystem.makeTransientByteArray((short)16, (byte)JCSystem.CLEAR_ON_DESELECT);
        
        cadenaData_ = JCSystem.makeTransientByteArray((short)125, (byte)JCSystem.CLEAR_ON_DESELECT);
    
        auxBuf_ = JCSystem.makeTransientByteArray((short)16, (byte)JCSystem.CLEAR_ON_DESELECT);
        auxKeyBuf_ = JCSystem.makeTransientByteArray((short)16, (byte)JCSystem.CLEAR_ON_DESELECT);
        auxBuf2_ = JCSystem.makeTransientByteArray((short)16, (byte)JCSystem.CLEAR_ON_DESELECT);
        
        PAN_ = JCSystem.makeTransientByteArray((short)8, (byte)JCSystem.CLEAR_ON_DESELECT);
        
        random_SAM_CARD_ = JCSystem.makeTransientByteArray((short)8, (byte)JCSystem.CLEAR_ON_DESELECT);
        
        Sign_Saldo = Signature.getInstance(Signature.ALG_DES_MAC8_NOPAD, false);
        
        vars_[EVENT_INDEX] = 0;
        vars_[CERT_LEN] = 0;
        vars_[SIGN_STATUS] = 0;
        vars_[IS_PHONE] = 0;
        
        //log = new byte[200]; // DEBUG!!!!
        //logL = 0;  // DEBUG!!!!
                
        //80E60C0051 05 0504030201 06 050403020100 -->06 050403020100 0104 39C9 37 20910070206001 B975E1F9C07C10714B0AD06B33A5FDC1 B975E1F9C07C10714B0AD06B33A5FDC1 A886D00ABF8D0F823A1BEF7C22B6ECD2 00
        //80E60C0051 05 0504030201 06 050403020100 -->06 050403020100 0104      37 20910070206001 B975E1F9C07C10714B0AD06B33A5FDC1 B975E1F9C07C10714B0AD06B33A5FDC1 A886D00ABF8D0F823A1BEF7C22B6ECD2
        //                          *                               *                               *
        // OK:        20910070206001B975E1F9C07C10714B0AD06B33A5FDC1B975E1F9C07C10714B0AD06B33A5FDC1A886D00ABF8D0F823A1BEF7C22B6ECD2
        // BAD DEBIT: 20910070206001B975E1F9C07C10714B0AD06B33A5FDC1A975E1F9C07C10714B0AD06B33A5FDC0A886D00ABF8D0F823A1BEF7C22B6ECD2
        // BAD SIGN:  20910070206001B975E1F9C07C10714B0AD06B33A5FDC1B975E1F9C07C10714B0AD06B33A5FDC1B886D00ABF8D0F823A1BEF7C22B6ECD2
        // BAD BOTH:  20910070206001B975E1F9C07C10714B0AD06B33A5FDC1A975E1F9C07C10714B0AD06B33A5FDC1B886D00ABF8D0F823A1BEF7C22B6ECD2

        // Load PSAM:
        tmp = (short)(bLength - 55 - 1);
        // bLength = 65
        // bOffset = 18
        // dataLength = 55
        if (bArray[tmp + bOffset] == 55) //Comprobar longitud
        {
            tmp = (short)(bOffset + tmp + 1);
            // Guardar PSAM
            Util.arrayCopyNonAtomic(bArray, (short)(tmp), EF_info_4F11, (short)0x00, (short)EF_info_4F11.length);
            tmp = (short)(tmp + EF_info_4F11.length);
            // Guardar la clave de consumo de tarjeta
            MotherConsumoKEYCard.setKey(bArray, (short)(tmp));
            tmp = (short)(tmp + MotherConsumoKEYCard.getSize() / 8);
            // Guardar la clave de consumo de tel�fono
            MotherConsumoKEYPhone.setKey(bArray, (short)(tmp));
            tmp = (short)(tmp + MotherConsumoKEYPhone.getSize() / 8);
            // Guardar la clave de firma
            MotherSignKEY.setKey(bArray, (short)(tmp));
            
            cardStatus = ACTIVE_;
        }
            
        SAM_Files = new Object[SAM_NUM_FILES];
        SAM_Files[SAM_MF] =  MF_info;
        SAM_Files[SAM_DF_4F10] =  EF_info_4F10;
        SAM_Files[SAM_DF_4F11] =  EF_info_4F11;
        SAM_Files[SAM_DF_4F12] =  EF_info_4F12;
        SAM_Files[SAM_VERSION] =  SAMVersion;
        SAM_Files[SAM_SERIAL] =  SAMSerial;
        //SAM_Files[SAM_LOG] =  log; // DEBUG!!!!
            
        // SAM_Keys = new Object[SAM_NUM_KEYS];
        // SAM_Keys[0] = MDK_10;
        // SAM_Keys[1] = MDK_20;
        // SAM_Keys[2] = MDK_30;
        // SAM_Keys[3] = MSK_10;
        // SAM_Keys[4] = MSK_20;
        // SAM_Keys[5] = MSK_30;
        
        register();
                
    }//constructor
     
        
    /**
     * Called by the JCRE to inform this applet that it has been 
     * selected. Perform any initialization that may be required to 
     * process APDU commands. This method returns a boolean to   
     * indicate whether it is ready to accept incoming APDU commands 
     * via its process() method.
     * @return If this method returns false, it indicates to the JCRE  
     * that this Applet declines to be selected.
     */
    public boolean select() {
        //  Perform any applet-specific session initialization.
            
        return true;
    }

    public static void install(byte[] bArray, short bOffset, byte bLength) 
    {       
        short tmp = (short)(bLength - 55 - 1);
        
        // Si la longitud no es la esperada retornar error:
        if (bArray[tmp + bOffset] != 55)
            ISOException.throwIt(ISO7816.SW_DATA_INVALID);
            
        new galiciaSAM(bArray, bOffset, bLength);
    }//Install

    public void process(APDU apdu)
    {
        if (selectingApplet())
        {
            return;
        }

        byte[] buf = apdu.getBuffer();
        
        if ((buf[ISO7816.OFFSET_CLA] != SAM_CLA) && 
            (buf[ISO7816.OFFSET_INS]!= INS_ISO_RD_binary)&& 
            (buf[ISO7816.OFFSET_INS]!= INS_ISO_getResponse) &&
            (buf[ISO7816.OFFSET_INS]!= INS_ISO_SELECT_FILE)){
                ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED);         
        }
            
        switch (buf[ISO7816.OFFSET_INS])
        {
            case INS_SelectNetwork:
                selectTransportNetwork(apdu);
                break;
            case INS_ValChallenge:
                valChallenge(apdu);
                break;                  
            case INS_InitCertific:
                initCertification(apdu);
                break;
            case INS_CertificarDatos:
                certificarDatos(apdu);
                break;
            case INS_VerificarCertificado:
                verificarCertificado(apdu);
                break;          
            case INS_FinCertificacion:
                finCertificacion(apdu);
                break;
            case INS_ISO_RD_binary:
                readBinary(apdu);
                break;
            case INS_ISO_getResponse:
                getResponse(apdu);
                break;
            case INS_ISO_SELECT_FILE:
                selectFile(apdu);
                break;
            /*case INS_PERSO:
                funcionPerso(apdu);
                break;*/
            case INS_UNBLOCK:
                unBlock(apdu);
                break;
            default:
                ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
        }
    }  // Process
    
    /*****************************************************
    Funciones de los APDUs
    ******************************************************/
        
    /////// 
    /* 1 */
    ///////
    private static void selectTransportNetwork(APDU apdu){
            
        byte[] buf = apdu.getBuffer();
                 
        vars_[ESTADO] = NETWORK_SELECTED_;  // cambio el estado del SAM
        
        //logL = 0; // DEBUG!!!
        
        // compruebo que el Identificador de Aplicacion es bueno 
        //  
        //   Tabla de conversion: TMG Dual => 4f55; Millenium => 4F11; Lugo => 4F66;  TMG => 4F10; 
        
        if(buf[ISO7816.OFFSET_P1] == 0x4F  &&  
          (buf[ISO7816.OFFSET_P2] == 0x55  ||
           buf[ISO7816.OFFSET_P2] == 0x11  ||
           buf[ISO7816.OFFSET_P2] == 0x66))
        {  
            //log[logL++] = 0x11; // DEBUG!!!
            //log[logL++] = 0x11; // DEBUG!!!
            
            Util.arrayCopyNonAtomic(SAM_data,(short)0x00, auxBuf_, (short)0x00, (short)SAM_data.length);
            
            if (buf[ISO7816.OFFSET_P2] == 0x55)
                auxBuf_[2] = 0x20;
            else if (buf[ISO7816.OFFSET_P2] == 0x11)
                auxBuf_[2] = 0x10;
            else if (buf[ISO7816.OFFSET_P2] == 0x66)
                auxBuf_[2] = 0x30;
            
            //Return data
            short le = apdu.setOutgoing();           
            apdu.setOutgoingLength((byte)9);                 
            apdu.sendBytesLong(auxBuf_, (short)0, (short)SAM_data.length);   
        }
        else{  // AID INcorrecto
            //log[logL++] = 0x22; // DEBUG!!!
            //log[logL++] = 0x22; // DEBUG!!!
                        
            vars_[ESTADO]=RESET_;       // el AID es Incorrecto.
            ISOException.throwIt(ISO7816.SW_FILE_NOT_FOUND);
        }
                
    }//selectTransportNetwork
    
    /////// 
    /* 2 */
    /////// 
    private static void valChallenge(APDU apdu){
        
        byte[] buf = apdu.getBuffer();
        
        if (CHECK_STATE)
        {
            if(vars_[ESTADO] != NETWORK_SELECTED_){
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x6985); // Aplicaci�n de transportes no seleccionada
            }
        }               
        
        Util.arrayFillNonAtomic(PAN_, (short)0, (short)PAN_.length, (byte)0);
        Util.arrayFillNonAtomic(random_SAM_CARD_, (short)0, (short)random_SAM_CARD_.length, (byte)0);
        Util.arrayFillNonAtomic(cadenaData_, (short)0, (short)cadenaData_.length, (byte)0);
        Util.arrayFillNonAtomic(MAC_, (short)0, (short)MAC_.length, (byte)0);
        Util.arrayFillNonAtomic(auxBuf_, (short)0, (short)auxBuf_.length, (byte)0);
        Util.arrayFillNonAtomic(auxBuf2_, (short)0, (short)auxBuf2_.length, (byte)0);
        Util.arrayFillNonAtomic(auxKeyBuf_, (short)0, (short)auxKeyBuf_.length, (byte)0);
        
        short numBytes = (short)buf[ISO7816.OFFSET_LC];
        short byteRead =(short)(apdu.setIncomingAndReceive());
       
        //log[logL++] = 0x33; // DEBUG!!!
        //log[logL++] = 0x33; // DEBUG!!!
            
        if (numBytes != (byte)0x0A)                         // espera: NT[2] || PAN[8]
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        if (numBytes != byteRead)
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        
        // Actualizo Datos internos     
        Util.arrayCopyNonAtomic(buf,(short)(ISO7816.OFFSET_CDATA + (short)2), PAN_,(short)0x00,(short)8);
        /* BIN = PAN_[0]  to  PAN_[2] */
        
        vars_[ESTADO]=CHALLENGED_;   // Avanzo en la Maquina de estados
        vars_[EVENT_INDEX] = 0;
        vars_[CERT_LEN] = 0;
        
        // Calculo el random Data.  
        myRandom01.generateData(random_SAM_CARD_,(short)0x00, (short)0x04);
        // random_SAM_CARD_[0] = (byte)0x4E;
        // random_SAM_CARD_[1] = (byte)0x4C;
        // random_SAM_CARD_[2] = (byte)0xEB;
        // random_SAM_CARD_[3] = (byte)0x44;
        // random_SAM_CARD_[0] = (byte)0x6E;
        // random_SAM_CARD_[1] = (byte)0x44;
        // random_SAM_CARD_[2] = (byte)0x1F;
        // random_SAM_CARD_[3] = (byte)0xF1;
        
        //log[logL++] = 0x44; // DEBUG!!!
        //log[logL++] = 0x44; // DEBUG!!!
                                            
        //Return data
        short le = apdu.setOutgoing();           
        apdu.setOutgoingLength((byte)4);           
        apdu.sendBytesLong(random_SAM_CARD_, (short)0x00, (short)0x04); // Devuelve el random del SAM 
        
    }//valChallenge

    /////// 
    /* 3 */
    ///////         
    private static void initCertification(APDU apdu){
        byte[] buf = apdu.getBuffer();
        
        short numBytes = (short)buf[ISO7816.OFFSET_LC];
        short byteRead =(short)(apdu.setIncomingAndReceive());
        
        //Comprobar maquina estados
        if (CHECK_STATE)
        {
            if(vars_[ESTADO] > CHALLENGED_ || vars_[ESTADO] == NETWORK_SELECTED_){
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x9580); //Comando fuera de secuencia
            }
            else if (vars_[ESTADO] == RESET_)
            {
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x6985);  //Aplicaci�n de transportes no seleccionada
            }   
        }
            
        //log[logL++] = 0x55; // DEBUG!!!
        //log[logL++] = 0x55; // DEBUG!!!
            
        // compruebo que llegan todos los datos 
        if (numBytes != 0x3A ) 
            ISOException.throwIt(ISO7816.SW_WRONG_DATA);
        if (numBytes != byteRead)
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        
        vars_[ESTADO]=INITCERTIFICATION_; 
        
                                        
        ////////////////////////    
        // CALCULO CLAVE SESION:
        ////////////////////////
        
        // Guardo el random de la tarjeta (PurseSignature)
        // Los 4 bytes del random de la tarjeta emulada es la firma del saldo actual
        vars_[CERT_LEN] = (byte)(numBytes - 0x04);
        Util.arrayCopyNonAtomic(buf,(short)(ISO7816.OFFSET_CDATA + vars_[CERT_LEN]), random_SAM_CARD_, (short)(0x04), (short)0x04);
        
        // Guardo los primeros bytes a firmar
        Util.arrayCopyNonAtomic(buf,(short)(ISO7816.OFFSET_CDATA), cadenaData_,(short)0x00, vars_[CERT_LEN]);  // cardRandom[4] no entra en la firma !!!!
         
        //Util.arrayCopyNonAtomic(cadenaData_,(short)0x00, log, logL, vars_[CERT_LEN]); // DEBUG!!! 
        //logL += vars_[CERT_LEN]; // DEBUG!!!
        
        // Si la tarjeta es una tarjeta emulada: Flag 0x40 en env_str[8] (byte 34 de cadenaData_)
        if ((byte)(cadenaData_[34] & 0x0F) == (byte)0x01)
        //if (cadenaData_[37] == (byte)0x5A)
        {
            vars_[IS_PHONE] = 1;
            deriveCardKey(DEBIT_SESSION_KEY_PHONE, debit_sesionK_, auxBuf_ /*dummy*/);
        }
        else
        {
            vars_[IS_PHONE] = 0;
            deriveCardKey(DEBIT_SESSION_KEY_CARD, debit_sesionK_, auxBuf_ /*dummy*/);
        }
        Key_Debit_M.setKey(debit_sesionK_, (short)0x00);    // preparo la clave
                
        // Calcular la clave de firma de saldo con el evento anterior
        if (CHECK_SIGNATURE)
        {   
            if (1 == vars_[IS_PHONE])
            {
                //802A00003A Event(NT(0177) ImpEvent(0082) BalEvent(00E6BF) TransEvent(41) Event(118601142A04B2B31112141100E72C932C9412A035))......
                //Ultimo Evento: NT(2)+ImpEvent(2)+BalEvent(3)+TransEvent(1);
                Util.arrayFillNonAtomic(auxBuf2_, (short)0, (short)auxBuf2_.length, (byte)0);
                Util.arrayCopyNonAtomic(cadenaData_,(short)0x00, auxBuf2_,(short)8, (short)8);
                
                //auxBuf2_[8] = 0x00;
                //auxBuf2_[9] = 0x02;
                //auxBuf2_[10] = 0x02;
                //auxBuf2_[11] = (byte)0xF8;
                //auxBuf2_[12] = 0x00;
                //auxBuf2_[13] = 0x23;
                //auxBuf2_[14] = (byte)0xB4;
                
                deriveCardKey(SIGN_SESSION_KEY, sign_sesionK_, auxBuf2_);

                //log[logL++] = (byte)0x66; // DEBUG!!!
                //log[logL++] = (byte)0x66; // DEBUG!!!
                //Util.arrayCopyNonAtomic(auxBuf2_,(short)8, log, logL, (short)4); // DEBUG!!!
                //logL += 4; // DEBUG!!!
                //Util.arrayCopyNonAtomic(sign_sesionK_,(short)0x00, log, logL, (short)16); // DEBUG!!!
                //logL += 16; // DEBUG!!!           
                //firmaSaldo (sign_sesionK_, auxBuf2_, MAC_); // Test
            }
        }
        //log[logL++] = 0x77; // DEBUG!!!
        //log[logL++] = 0x77; // DEBUG!!!
    }// fin initCert
    
    /////// 
    /* 4 */
    ///////     
    private static void certificarDatos(APDU apdu){ 
    
        int balance = 0, balance_ant = 0, nt = 0;
        int amount_ant = 0;
        
        byte[] buf = apdu.getBuffer();
                
        short j=0;
        
        short numBytes = (short)buf[ISO7816.OFFSET_LC];
        short byteRead =(short)(apdu.setIncomingAndReceive());
        
        //Comprobar maquina estados
        if (CHECK_STATE)
        {
            if(vars_[ESTADO] != INITCERTIFICATION_ && vars_[ESTADO] != RESET_){
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x9580); // Comando fuera de secuencia
            }
            else if (vars_[ESTADO] == RESET_)
            {
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x6985); // Aplicaci�n de transporte no seleccionada
            }
        }
        
        //log[logL++] = (byte)0x88; // DEBUG!!!
        //log[logL++] = (byte)0x88; // DEBUG!!!
            
        if (numBytes != byteRead)
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
            
        vars_[ESTADO]=CERTIFICAR_DATOS_;    
                            
        // Guardo los siguientes bytes a firmar
        vars_[EVENT_INDEX] = (byte)vars_[CERT_LEN];
        Util.arrayCopyNonAtomic(buf,(short)(ISO7816.OFFSET_CDATA), cadenaData_, vars_[EVENT_INDEX], numBytes);      
        
        //Util.arrayCopyNonAtomic(cadenaData_,vars_[EVENT_INDEX], log, logL, numBytes); // DEBUG!!!
        //logL += numBytes; // DEBUG!!!
        
        // Verificar la firma del saldo actual, antes de la transaccion
        if (CHECK_SIGNATURE)
        {   
            if (1 == vars_[IS_PHONE])
            {
                // Comprobar si ha habido una recarga previa!!
                balance_ant = ((auxBuf2_[12]<< 16) & 0x00FF0000) | ((auxBuf2_[13] << 8) & 0x0000FF00) | (auxBuf2_[14] & 0x000000FF);
                amount_ant = ((auxBuf2_[10]<< 8)  & 0x0000FF00) | (auxBuf2_[11] & 0x000000FF);
                if (auxBuf2_[15]!= 0)
                {
                    if ((auxBuf2_[15] & 0x40) == 0x40) // Consumo
                        balance_ant -= amount_ant;
                    else
                        balance_ant += amount_ant; // Anulaci�n
                }
                j = (short)(vars_[EVENT_INDEX] + 4);
                // Saldo actual: �ltimo evento generado por la transacci�n actual
                balance = ((cadenaData_[j]<< 16) & 0x00FF0000) | ((cadenaData_[j+1] << 8) & 0x0000FF00) | (cadenaData_[j+2] & 0x000000FF);
                            
                if (balance > balance_ant) // Ha habido recarga
                {   
                    nt = ((cadenaData_[j-4]<< 8)  & 0x0000FF00) | (cadenaData_[j-3] & 0x000000FF); // NT antes de la operacion
                    nt = nt - 1;
                    amount_ant = balance - balance_ant; // Cantidad recargada
                    // Calcular la nueva clave de firma
                    //Util.arrayFillNonAtomic(auxBuf2_, (short)0, (short)auxBuf2_.length, (byte)0);
                    //Util.arrayFillNonAtomic(sign_sesionK_, (short)0, (short)sign_sesionK_.length, (byte)0);
                    //NT(2)+ImpEvent(2);
                    auxBuf2_[8] = (byte)((nt & 0x0000FF00) >> 8);
                    auxBuf2_[9] = (byte)(nt & 0x000000FF);
                    auxBuf2_[10] = (byte)((amount_ant & 0x0000FF00) >> 8);
                    auxBuf2_[11] = (byte)(amount_ant & 0x000000FF);
                    auxBuf2_[15] = 0x00;
                    
                    deriveCardKey(SIGN_SESSION_KEY, sign_sesionK_, auxBuf2_);
                    //log[logL++] = (byte)0x89; // DEBUG!!!
                    //log[logL++] = (byte)0x98; // DEBUG!!!
                }
                else
                {
                    auxBuf2_[15] = 0x00;
                    //deriveCardKey(SIGN_SESSION_KEY, sign_sesionK_, auxBuf2_);
                }
                
                //Util.arrayCopyNonAtomic(sign_sesionK_, (short)0x00, log, logL, (short)16); // DEBUG!!!
                //logL += 16; // DEBUG!!!
                
                // PAN(8)+NT_ant(2)+ImpEvent_ant(2)+BalEvent_ant(3) 
                Util.arrayCopyNonAtomic(PAN_,(short)0x00, auxBuf2_,(short)0x00, (short)8); // PAN           
                Util.arrayCopyNonAtomic(cadenaData_,(short)j, auxBuf2_,(short)12, (short)3); // BalEvent                
                
                //log[logL++] = (byte)0x99; // DEBUG!!!
                //log[logL++] = (byte)0x99; // DEBUG!!!
                //Util.arrayCopyNonAtomic(auxBuf2_,(short)0x00, log, logL, (short)15); // DEBUG!!!
                //logL += 15; // DEBUG!!!
                    
                vars_[SIGN_STATUS] = verificaSaldo(sign_sesionK_, auxBuf2_, random_SAM_CARD_);
            }
        }
    
        vars_[CERT_LEN] += numBytes;
        
        // 5.- CALCULO EL HASH DE LOS DATOS DE LA TRANSACCION
        funcionCompresion(debit_sesionK_, cadenaData_, auxBuf_);    //semilla,datoIN,datoOUT
        Util.arrayFillNonAtomic(debit_sesionK_, (short)0, (short)debit_sesionK_.length, (byte)0);
        
        // 6.- FIRMO EL HASH PARA HACER EL MAC
        calculateCryptogram(Key_Debit_M, auxBuf_, (short)0x00, (short)0x08, MAC_, (short) 0x00) ;
    
        //log[logL++] = (byte)0xAA; // DEBUG!!!
        //log[logL++] = (byte)0xAA; // DEBUG!!!
    }// Fin certificarDatos


    /////// 
    /* 5 */
    ///////     
    private static void finCertificacion(APDU apdu){
            
        int balance = 0;
        int amount =  0;
        
        //Comprobar maquina estados
        if (CHECK_STATE)
        {
            if(vars_[ESTADO] != CERTIFICAR_DATOS_ && vars_[ESTADO] != RESET_){
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x9580); // Comando fuera de secuencia
            }   
            else if (vars_[ESTADO] == RESET_)
            {
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x6985); // Aplicaci�n de transporte no seleccionada
            }
        }
        
        vars_[ESTADO]=FIN_CERTIFICAR_;  
        
        if (CHECK_SIGNATURE)
        {   
            if (1 == vars_[IS_PHONE])
            {   
                if (0 == vars_[SIGN_STATUS])
                {           
                    // Si la firma del saldo anterior es correcta, se env�a la firma del saldo debitado o cancelado
                    // PAN(8)+NT(2)+ImpEvent(2)+BalEvent(3);
                    Util.arrayCopyNonAtomic(PAN_,(short)0x00, auxBuf2_,(short)0x00, (short)8);
                    Util.arrayCopyNonAtomic(cadenaData_,(short)vars_[EVENT_INDEX], auxBuf2_,(short)8, (short)7);
                    
                    // Calcular el nuevo saldo, si es d�bito o anulaci�n
                    balance = ((auxBuf2_[12]<< 16) & 0x00FF0000) | ((auxBuf2_[13] << 8) & 0x0000FF00) | (auxBuf2_[14] & 0x000000FF);
                    amount = ((auxBuf2_[10]<< 8)  & 0x0000FF00) | (auxBuf2_[11] & 0x000000FF);
                    
                    if ((byte)(cadenaData_[vars_[EVENT_INDEX] + 7] & 0x40) == 0x00) // Anulacion
                        balance = balance + amount;
                    else
                        balance = balance - amount;
                    
                    auxBuf2_[12] = (byte)((balance & 0x00FF0000) >> 16);
                    auxBuf2_[13] = (byte)((balance & 0x0000FF00) >> 8);
                    auxBuf2_[14] = (byte)(balance & 0x000000FF);
                    
                    // Derivar la nueva clave de firma
                    deriveCardKey(SIGN_SESSION_KEY, sign_sesionK_, auxBuf2_);
                    // Firmar el saldo actual
                    firmaSaldo (sign_sesionK_, auxBuf2_, MAC_);
                    
                    /*log[logL++] = (byte)0xBB; // DEBUG!!!
                    log[logL++] = (byte)0xBB; // DEBUG!!!
                    Util.arrayCopyNonAtomic(auxBuf2_,(short)0x00, log, logL, (short)15); // DEBUG!!!
                    logL += 15; // DEBUG!!!
                    Util.arrayCopyNonAtomic(sign_sesionK_,(short)0x00, log, logL, (short)16); // DEBUG!!!
                    logL += 16; // DEBUG!!!
                    Util.arrayCopyNonAtomic(MAC_,(short)0x00, log, logL, (short)8);
                    logL += 8;*/
                    
                    if (signErrCount != 0)
                        signErrCount = 0;   
                }
                else
                {
                    if (true == BLOCK_SAM)
                    {
                        signErrCount++;
                        if (MAX_SIGN_ERROR == signErrCount)
                            cardStatus = BLOCKED_;
                    }
                    
                    //log[logL++] = (byte)0xCC; // DEBUG!!!
                    //log[logL++] = (byte)0xCC; // DEBUG!!!
                    ISOException.throwIt((short)0x9302); // Certificado incorrecto
                }
            }
        }
        
        //log[logL++] = (byte)0xDD; // DEBUG!!!
        //log[logL++] = (byte)0xDD; // DEBUG!!!
                                        
        //Return data
        short le = apdu.setOutgoing();           
        apdu.setOutgoingLength((byte)0x04);    
        apdu.sendBytesLong(MAC_, (short)0x00, (short)0x04);   // Devuelve los cuatro bytes MAS significativos del MAC

    }// Fin certificarDatos

    /////// 
    /* 6 */
    ///////     
    private static void verificarCertificado(APDU apdu){    
        byte[] buf = apdu.getBuffer();
        
        short numBytes = (short)buf[ISO7816.OFFSET_LC];  
        short byteRead =(short)(apdu.setIncomingAndReceive());
        
        //Comprobar maquina estados
        if (CHECK_STATE)
        {
            if(vars_[ESTADO] != FIN_CERTIFICAR_){
                vars_[ESTADO]=RESET_;       
                ISOException.throwIt((short)0x9580); // Comando fuera de secuencia
            }
        }   
        
        //log[logL++] = (byte)0xEE; // DEBUG!!!
        //log[logL++] = (byte)0xEE; // DEBUG!!!
            
        if (numBytes != (byte)0x04)
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        if (numBytes != byteRead)
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
           
        vars_[ESTADO] = RESET_;     // cierra sesion
                
        byte igual = Util.arrayCompare(buf, (short)ISO7816.OFFSET_CDATA, MAC_,(short)0x04, (short)0x04); // Comprueba los cuatro bytes MENOS significativos del MAC
        
        if( igual != 0 || (true == CHECK_SIGNATURE && (vars_[SIGN_STATUS] != 0) && (1 == vars_[IS_PHONE])))
        {
            if (true == BLOCK_SAM)
            {
                signErrCount++;
                if (MAX_SIGN_ERROR == signErrCount)
                    cardStatus = BLOCKED_;
            }

            //log[logL++] = (byte)0xFF; // DEBUG!!!
            //log[logL++] = (byte)0xFF; // DEBUG!!!
            ISOException.throwIt((short)0x9302); // Certificado incorrecto              
        }
        else
        {
            if (signErrCount != 0)
                signErrCount = 0;
        }

    }// Fin verificarCertificado


    /*****************************************************************
        FUNCION DE COMPRESION DE TRANSACCION DEBITO DE TRANSPORTE
    ******************************************************************/
     private static void funcionCompresion(byte[] semilla, byte[] datoIN, byte[] datoOUT_8){

        byte i=0,j=0;
        
        Util.arrayCopyNonAtomic(semilla,(short)0, datoOUT_8,(short)0,(short)8);
            
        do
        {   // j recorre la cadena de entrada byte a byte.          
            datoOUT_8[7]= (byte)(datoOUT_8[7] ^ datoIN[j]);
            
            datoOUT_8[6]= (byte)(datoOUT_8[6] ^ datoOUT_8[7]);  
            datoOUT_8[5]= (byte)(datoOUT_8[5] ^ datoOUT_8[6]);  
            datoOUT_8[4]= (byte)(datoOUT_8[4] ^ datoOUT_8[5]);  
            datoOUT_8[3]= (byte)(datoOUT_8[3] ^ datoOUT_8[4]);  
            datoOUT_8[2]= (byte)(datoOUT_8[2] ^ datoOUT_8[3]);  
            datoOUT_8[1]= (byte)(datoOUT_8[1] ^ datoOUT_8[2]);
            datoOUT_8[0]= (byte)(datoOUT_8[0] ^ datoOUT_8[1]);                      
            j++;
            
        }while(j<vars_[CERT_LEN]);
    
        return;
        
    }//fin Funcion Compresion.

    //////////////////////////////////////////////
    /// Funci�n que calcula la firma del saldo de la tarjeta
    /// 
    //////////////////////////////////////////////
    private static void firmaSaldo (byte[] key, byte[] datoIN, byte[] datoOUT){     

        Key_C.setKey(key, (short)0x00);   //DES
        Sign_Saldo.init(Key_C, Signature.MODE_SIGN);
        // datoIN: PAN(8)+NT(2)+ImpEvent(2)+BalEvent(3);
        Sign_Saldo.sign(datoIN, (short)0, (short)16, auxBuf_, (short)0x00); 

        int nt = ((datoIN[8]<< 8)  & 0x0000FF00) | (datoIN[9] & 0x000000FF);    
        byte i = (byte)(nt % 2);
        
        // Coger los 4 bytes (pares o impares) indicados por NT y Enmascarar
        // datoOUT(MAC 4 +significativos) = Firma[0],Firma[1],Certificado[2],Certificado[3]
        myRandom01.generateData(datoIN,(short)0x04, (short)0x04);
        datoOUT[0] = (byte)(auxBuf_[i] ^ (datoIN[4] & SIGN_MASK[0]));
        datoOUT[1] = (byte)(auxBuf_[i + 2] ^ (datoIN[5] & SIGN_MASK[1]));
        //datoOUT[2] = (byte)(auxBuf_[i + 4] ^ (datoIN[6] & SIGN_MASK[2]));
        //datoOUT[3] = (byte)(auxBuf_[i + 6] ^ (datoIN[7] & SIGN_MASK[3]));
        
    }// fin firmaSaldo

    //////////////////////////////////////////////
    /// Funci�n que verifica la firma del saldo de la tarjeta
    /// 
    //////////////////////////////////////////////
    private static byte verificaSaldo (byte[] key, byte[] datoIN, byte[] firmaIN){      
        // datoIN: &cadenaData[0]: PAN(8) + NT(2) + ImpEvent(2) + BalEvent(3);
        // firmaIN: &random_SAM_CARD_[4]: 4 bytes (s�lo los 2 primeros son la firma de saldo)

        firmaSaldo(key, datoIN, auxBuf_);
        // Desenmascarar para comparar
        auxBuf_[0] = (byte)(auxBuf_[0] & ~SIGN_MASK[0]);
        auxBuf_[1] = (byte)(auxBuf_[1] & ~SIGN_MASK[1]);
        //auxBuf_[2] = (byte)(auxBuf_[2] & ~SIGN_MASK[2]);
        //auxBuf_[3] = (byte)(auxBuf_[3] & ~SIGN_MASK[3]);
        firmaIN[4] = (byte)(firmaIN[4] & ~SIGN_MASK[0]);
        firmaIN[5] = (byte)(firmaIN[5] & ~SIGN_MASK[1]);
        //firmaIN[6] = (byte)(firmaIN[6] & ~SIGN_MASK[2]);
        //firmaIN[7] = (byte)(firmaIN[7] & ~SIGN_MASK[3]);
        
        if ((auxBuf_[0] == firmaIN[4]) && (auxBuf_[1] == firmaIN[5]))
            return 0;
        else
            return 1;
        //return Util.arrayCompare(auxBuf_, (short)0, firmaIN, (short)0x04, (short)0x04); 
                
    }// fin verificaSaldo

    //////////////////////////////////////////////
    ///  
    /// 
    //////////////////////////////////////////////
    private static short calculateCryptogram(DESKey key, byte[] input, short sin, short inLen, byte[] output, short sou) 
    { 
         short ouLen; 
         Cipher_A.init(key, Cipher.MODE_ENCRYPT);
         ouLen = Cipher_A.doFinal(input, (short)0x00, (short)8, output, (short)0x00); 
         return 8;
         
    }//calculateCrytogram  

    //////////////////////////////////////////////
    /// Funci�n que calcula la clave de sesi�n de tarjeta
    /// 
    //////////////////////////////////////////////
    private static void deriveCardKey(byte keyType, byte[] outKey, byte[] auxData_) 
    {               
        //  1.- Diversifico Clave Consumo de aplicacicon Monedero por BIN       
        Util.arrayCopyNonAtomic(seedBIN_A, (short)0x00, auxKeyBuf_,(short)0x00, (short)8);
        Util.arrayCopyNonAtomic(seedBIN_B, (short)0x00, auxKeyBuf_,(short)0x08, (short)8);
        
        auxKeyBuf_[0] = PAN_[0];
        auxKeyBuf_[1] = PAN_[1];
        auxKeyBuf_[2] = PAN_[2];
        
        auxKeyBuf_[13] = PAN_[0];
        auxKeyBuf_[14] = PAN_[1];
        auxKeyBuf_[15] = PAN_[2];
        
        if (DEBIT_SESSION_KEY_CARD == keyType)
        {
            MotherConsumoKEYCard.getKey(auxBuf_, (short)(0));
            //Key_A.setKey(MotherConsumoKEYCard_test, (short)0x00);  //DES
            //Key_B.setKey(MotherConsumoKEYCard_test, (short)0x08);  //DES
        }
        else if (DEBIT_SESSION_KEY_PHONE == keyType)
        {
            MotherConsumoKEYPhone.getKey(auxBuf_, (short)(0));
            //Key_A.setKey(MotherConsumoKEYPhone_test, (short)0x00);  //DES
            //Key_B.setKey(MotherConsumoKEYPhone_test, (short)0x08);  //DES
        }
        else if (SIGN_SESSION_KEY == keyType)
        {
            MotherSignKEY.getKey(auxBuf_, (short)(0));
            //Key_A.setKey(MotherSignKEY_test, (short)0x00);  //DES
            //Key_B.setKey(MotherSignKEY_test, (short)0x08);  //DES
        }
        
        Key_A.setKey(auxBuf_, (short)0x00);  //DES
        Key_B.setKey(auxBuf_, (short)0x08);  //DES
        
        calculaDiversificarClave(Key_A, auxKeyBuf_, (short) 0x00, (short) 8, auxBuf_, (short) 0x00);
        calculaDiversificarClave(Key_B, auxKeyBuf_, (short) 0x08, (short) 8, auxBuf_, (short) 0x08);
            
        Key_C.setKey(auxBuf_, (short)0x00);   // 3DES
        
        //  2.- DIVERSIFICO CLAVE MAESTRA CONSUMO transporte POR PAN
        if (DEBIT_SESSION_KEY_CARD == keyType || DEBIT_SESSION_KEY_PHONE == keyType)
        {
            Util.arrayCopyNonAtomic(seedBIN_C, (short)0x00, auxKeyBuf_,(short)0x00, (short)8);
            Util.arrayCopyNonAtomic(seedBIN_D, (short)0x00, auxKeyBuf_,(short)0x08, (short)8);  
        }
        else
        {
            Util.arrayCopyNonAtomic(seedBIN_E, (short)0x00, auxKeyBuf_,(short)0x00, (short)8);
            Util.arrayCopyNonAtomic(seedBIN_F, (short)0x00, auxKeyBuf_,(short)0x08, (short)8);
        }
                            
        switch(PAN_[2])
        {
            case 0x10:
                auxKeyBuf_[3] = 0x01;
                auxKeyBuf_[15] = 0x01;
                break;
            case 0x20:
                auxKeyBuf_[3] = 0x04;
                auxKeyBuf_[15] = 0x04;
                break;
            case 0x30:
                auxKeyBuf_[3] = 0x05;
                auxKeyBuf_[15] = 0x05;
                break;
            default:
                auxKeyBuf_[0] = 0x00;
                auxKeyBuf_[1] = 0x00;
                auxKeyBuf_[12] = 0x00;
                auxKeyBuf_[13] = 0x00;
                break;
        }
        
        calculaDiversificarClave(Key_C, auxKeyBuf_, (short) 0x00, (short) 8, auxBuf_, (short)0x00);
        calculaDiversificarClave(Key_C, auxKeyBuf_, (short) 0x08, (short) 8, auxBuf_, (short)0x08);
        
        // Clave diversificada por BIN: Precalculadas
        //Util.arrayCopyNonAtomic((byte [])SAM_Keys[keyType - 1 + (PAN_[2] / 0x10)], (short)0, auxBuf_,(short)0, (short)16);
                     
        //  3.- DIVERSIFICO CLAVE POR TARJETA 
        //  PAN actua como clave. Dato es la clave del paso anterior   
        Key_A.setKey(PAN_, (short)0x00);   //DES
        calculaDiversificarClave(Key_A, auxBuf_, (short)0x00, (short) 8, auxBuf_, (short)0x00);
        calculaDiversificarClave(Key_A, auxBuf_, (short)0x08, (short) 8, auxBuf_, (short)0x08); 
            
        //  4.- CLAVE DE SESION (DES)
        if (DEBIT_SESSION_KEY_CARD == keyType || DEBIT_SESSION_KEY_PHONE == keyType)
        {       
            Key_A.setKey(auxBuf_, (short)0x00);
            calculaDiversificarClave(Key_A, random_SAM_CARD_, (short) 0x00, (short) 8, outKey, (short) 0x00);  //DES
        }
        else if (SIGN_SESSION_KEY == keyType)
        {
            Key_C.setKey(auxBuf_, (short)0x00);   // 3DES
            //NT(2)+ ImpEvent(2) iniciales
            Util.arrayFillNonAtomic(auxBuf_, (short)0, (short)auxBuf_.length, (byte)0);
            Util.arrayCopyNonAtomic(auxData_,(short)8, auxBuf_,(short)0, (short)2); // NT
            Util.arrayCopyNonAtomic(auxData_,(short)10, auxBuf_,(short)2, (short)2); // ImpEvent
            calculaDiversificarClave(Key_C, auxBuf_, (short) 0x00, (short) 8, outKey, (short) 0x00);  //3DES
            calculaDiversificarClave(Key_C, auxBuf_, (short) 0x08, (short) 8, outKey, (short) 0x08);  //3DES
        }
        
    } // deriveCardKey
    
    //////////////////////////////////////////////
    /// Funci�n que diversifica una clave 
    /// hace DES o 3DES segun el tipo de clave que reciba
    //////////////////////////////////////////////
                    
    private static short calculaDiversificarClave(DESKey key, byte[] DataInput, short sin, short inLen, byte[] DataOutput, short sou) 
    { 
         short ouLen; 
         Cipher_A.init(key, Cipher.MODE_ENCRYPT);
         ouLen = Cipher_A.doFinal(DataInput, (short)sin, inLen, DataOutput, (short)sou); 
             
         //ouLen = Cipher_A.doFinal(DataInput, (short)0x00, (short)8, DataOutput, (short)0x08); 
         return ouLen;
         
    }//calculate
    
    /////////   
    /* ISO */
    /////////       
    private static void readBinary(APDU apdu){          
        
        byte[] buf = apdu.getBuffer();
        
        if(buf[ISO7816.OFFSET_P1] == (byte)0x91){ // Read fichero 'info = 0011
            //Return data
            short le = apdu.setOutgoing();           
            apdu.setOutgoingLength((byte)EF_info_4F11.length);    
            apdu.sendBytesLong(EF_info_4F11, (short)0, (short)EF_info_4F11.length);   // Devuelve los bytes del fichero.
            //Return data
        }
    } //readBinary.ok

    private static void getResponse(APDU apdu){     
        
        //Return data
        short le = apdu.setOutgoing();     
        apdu.setOutgoingLength((short)((byte [])SAM_Files[vars_[SELECTED_FILE]]).length);
        apdu.sendBytesLong(((byte [])SAM_Files[vars_[SELECTED_FILE]]), (short)0, 
                            (short)((byte [])SAM_Files[vars_[SELECTED_FILE]]).length);   // Devuelve los bytes del fichero.  
        //Return data
    }// getResponse
    
    private static void selectFile(APDU apdu){          
                
        byte[] buf = apdu.getBuffer();
        
        short byteRead =(short)(apdu.setIncomingAndReceive());
        
        
        if (buf[ISO7816.OFFSET_P1] == (byte)0x00 && buf[ISO7816.OFFSET_P2] == (byte)0x00)  //Read fichero MF
        {
            vars_[SELECTED_FILE] = SAM_MF;
            ISOException.throwIt((short)(0x6100 | MF_info.length)); // Imitando al SAM original
        }
        else if(buf[ISO7816.OFFSET_CDATA] == (byte)0x4F)
        {
            switch (buf[ISO7816.OFFSET_CDATA + 1])
            {
                case (byte)0x10:
                    vars_[SELECTED_FILE] = SAM_DF_4F10;
                    ISOException.throwIt((short)(0x6100 | EF_info_4F10.length)); // Imitando al SAM original
                    break;
                case (byte)0x11:
                    vars_[SELECTED_FILE] = SAM_DF_4F11;
                    ISOException.throwIt((short)(0x6100 | EF_info_4F11.length));
                    break;
                case (byte)0x12:
                    vars_[SELECTED_FILE] = SAM_DF_4F12;
                    ISOException.throwIt((short)(0x6100 | EF_info_4F12.length));
                    break;
                case (byte)0x5A:
                    vars_[SELECTED_FILE] = SAM_VERSION;
                    ISOException.throwIt((short)(0x6100 | SAMVersion.length));
                    break;
                case (byte)0x5B:
                    vars_[SELECTED_FILE] = SAM_SERIAL;
                    ISOException.throwIt((short)(0x6100 | SAMSerial.length));
                    break;
                /*case (byte)0xA5: // DEBUG!!
                    vars_[SELECTED_FILE] = SAM_LOG;
                    ISOException.throwIt((short)(0x6100 | log.length));
                    break;*/
                default:
                    ISOException.throwIt(ISO7816.SW_FILE_NOT_FOUND);
                    break;          
            }
        }
        else
            ISOException.throwIt(ISO7816.SW_FILE_NOT_FOUND);    
    } //selectFile.ok
    
    
    /*
    APDU que personaliza la tarjeta
        Acciones:
            .- Estado inicial
            .- Set ATR
            .- PSAM: Identificador del SAM
            .- PPSAM: Identificador del proveedeor del SAM
            .- MK:  Clave maestra de transporte
            .- MSK: Clave maestra de firma de saldo
    */
    /*private static void funcionPerso(APDU apdu){
        //////////////////
        byte[] buf = apdu.getBuffer();
        
        short numBytes = (short)buf[ISO7816.OFFSET_LC];
        short byteRead =(short)(apdu.setIncomingAndReceive());
        
        if (buf[ISO7816.OFFSET_P1] == (byte)0xA5 && buf[ISO7816.OFFSET_P2] == (byte)0x5A) // TODO
        {
            //GPSystem.setATRHistBytes(ATR_, (short) 0x00, (byte) 0x0D);
            if (cardStatus == VIRGIN_)
            {
                if (numBytes != (byte)0x27)
                    ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
                if (numBytes != byteRead)
                    ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
                        
                cardStatus = ACTIVE_;
                signErrCount = 0;
                
                //Util.arrayCopyNonAtomic(buf, (short)ISO7816.OFFSET_CDATA, EF_info_4F11, (short)0x00, (short)EF_info_4F11.length);
                //Util.arrayCopyNonAtomic(buf, (short)(ISO7816.OFFSET_CDATA + 7), auxBuf_, (short)0x00, (short)16);
                //MotherConsumoKEY.setKey(auxBuf_, (short)0);
                //Util.arrayCopyNonAtomic(buf, (short)(ISO7816.OFFSET_CDATA + 23), auxBuf_, (short)0x00, (short)16);
                //MotherSignKEY.setKey(auxBuf_, (short)0);
            }
            else
                ISOException.throwIt(ISO7816.SW_COMMAND_NOT_ALLOWED);
        }
        //else if (buf[ISO7816.OFFSET_P1] == (byte)0xFF && buf[ISO7816.OFFSET_P2] == (byte)0xFF) // Test!!!
        //{
        //  //cardStatus = VIRGIN_;
        //  short le = apdu.setOutgoing();       
        //  
        //  apdu.setOutgoingLength((byte)(EF_info_4F11.length +  MotherConsumoKEYCard.getSize() / 8 + MotherConsumoKEYPhone.getSize() / 8 + MotherSignKEY.getSize() / 8));  
        //  Util.arrayCopyNonAtomic(EF_info_4F11, (short)0x00, auxBuf_, (short)0x00, (short)EF_info_4F11.length);
        //  apdu.sendBytesLong(auxBuf_, (short)0, (short)EF_info_4F11.length);
        //  MotherConsumoKEYCard.getKey(auxBuf_ ,(short)0x00);              
        //  apdu.sendBytesLong(auxBuf_, (short)0, (short)(MotherConsumoKEYCard.getSize() / 8));
        //  MotherConsumoKEYPhone.getKey(auxBuf_ ,(short)0x00);             
        //  apdu.sendBytesLong(auxBuf_, (short)0, (short)(MotherConsumoKEYPhone.getSize() / 8));
        //  MotherSignKEY.getKey(auxBuf_ ,(short)0x00);             
        //  apdu.sendBytesLong(auxBuf_, (short)0, (short)(MotherSignKEY.getSize() / 8));
        //}
        else
            ISOException.throwIt(ISO7816.SW_COMMAND_NOT_ALLOWED);
        /////////////////////////////
        return;
        
    }*/

    private static void unBlock(APDU apdu){
        byte[] buf = apdu.getBuffer();
        
        short numBytes = (short)buf[ISO7816.OFFSET_LC];
        short byteRead =(short)(apdu.setIncomingAndReceive());
        
        if (buf[ISO7816.OFFSET_P1] == (byte)0x12 && buf[ISO7816.OFFSET_P2] == (byte)0x34) // TODO
        {
            if (cardStatus == BLOCKED_)
            {
                cardStatus = ACTIVE_;
                signErrCount = 0;
            }
            else
                ISOException.throwIt(ISO7816.SW_COMMAND_NOT_ALLOWED);
        }
        else
            ISOException.throwIt(ISO7816.SW_COMMAND_NOT_ALLOWED);
    }
}// class











/*****************************************************************************************************
Septiembre 2017
Estamos a dias del referendum de independencia de Catalu�a �al final se separar�n?
Y tristemente hace unos dias fue el atentado terrorista con una furgoneta en las Rambas.
*/