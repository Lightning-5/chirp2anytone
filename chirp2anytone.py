import csv


# Define your expected header row
chirp_header = ["Location", "Name", "Frequency", "Duplex", "Offset", "Tone", "rToneFreq", "cToneFreq", "DtcsCode",
                   "DtcsPolarity", "RxDtcsCode", "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment", "URCALL",
                   "RPT1CALL", "RPT2CALL", "DVCODE"]

anytone_header = ['No.', 'Channel Name', 'Receive Frequency', 'Transmit Frequency', 'Channel Type', 'Transmit Power', 'Band Width', 'CTCSS/DCS Decode', 'CTCSS/DCS Encode', 'Contact', 'Contact Call Type', 'Contact TG/DMR ID', 'Radio ID', 'Busy Lock/TX Permit', 'Squelch Mode', 'Optional Signal', 'DTMF ID', '2Tone ID', '5Tone ID', 'PTT ID', 'Color Code', 'Slot', 'Scan List', 'Receive Group List', 'PTT Prohibit', 'Reverse', 'Simplex TDMA', 'Slot Suit', 'AES Digital Encryption', 'Digital Encryption', 'Call Confirmation', 'Talk Around(Simplex)', 'Work Alone', 'Custom CTCSS', '2TONE Decode', 'Ranging', 'Through Mode', 'APRS RX', 'Analog APRS PTT Mode', 'Digital APRS PTT Mode', 'APRS Report Type', 'Digital APRS Report Channel', 'Correct Frequency[Hz]', 'SMS Confirmation', 'Exclude channel from roaming', 'DMR MODE', 'DataACK Disable', 'R5toneBot', 'R5ToneEot', 'Auto Scan', 'Ana Aprs Mute', 'Send Talker Alias', 'AnaAprsTxPath', 'ARC4', 'ex_emg_kind']

anytone_right_side_of_row = ['"Contact1"', '"Group Call"', '"12345678"', '"My Radio"', '"Off"', '"Carrier"', '"Off"', '"1"', '"1"', '"1"', '"Off"', '"1"', '"1"', '"None"', '"None"', '"Off"', '"Off"', '"Off"', '"Off"', '"Normal Encryption"', '"Off"', '"Off"', '"Off"', '"Off"', '"251.1"', '"0"', '"Off"', '"On"', '"Off"', '"Off"', '"Off"', '"Off"', '"1"', '"0"', '"Off"', '"0"', '"0"', '"0"', '"0"', '"0"', '"0"', '"0"', '"0"', '"0"', '"0"', '"0"']



with open("chirp_full.csv" ,'r', newline='', encoding='utf-8') as chirpCSV:
    chirp = csv.reader(chirpCSV, delimiter=',', quotechar='|')
    actual_header_in_csv = next(chirp)
    # Compare the actual header with the expected header
    if actual_header_in_csv == chirp_header:
        print("The first row is the correct header row.")
    else:
        print("The first row is not the correct header row.")
        print("Exiting...")
        exit()

    print("Creating Anytone csv")
    with open("a.csv" ,'w+', newline='', encoding='utf-8') as anytone_CSV:
        anytone = csv.writer(anytone_CSV, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("Writing header")
        anytone.writerow(anytone_header)
        
        for chirp_row in chirp:
            new_any_row=[""] * len(anytone_header)
            #DEBUG
            #print(chirp_row)

            #copy Channel number
            new_any_row[0] = chirp_row[0]
            #copy channel name
            new_any_row[1] = chirp_row[1]
            #copy receive frequency
            new_any_row[2] = chirp_row[2]
            #copy transmit frequency
            if(chirp_row[3] == "-"):
                transmit_frequency=round(float(new_any_row[2]) - float(chirp_row[4]) , 6 )
                new_any_row[3] = "{:.6f}".format(transmit_frequency)
                print("Calculated frequency", new_any_row[3])   

            elif(chirp_row[3] == "+"):
                transmit_frequency=round(float(new_any_row[2]) + float(chirp_row[4]) , 6 )
                new_any_row[3] = "{:.6f}".format(transmit_frequency)
                print("Calculated frequency", new_any_row[3])

            else:
                transmit_frequency=new_any_row[2]
                new_any_row[3]=transmit_frequency
            
            #copy channel type ANALOG|DIGITAL
            #Channel is always analog (FOR NOW????)
            new_any_row[4] = "A-Analog"

            #copy power level
            #print("chirp_row[15]:", chirp_row[15])
            if(chirp_row[15] == "1.0W"):
                new_any_row[5] = "Low"
            else:
                new_any_row[5] = "Turbo"
            
            #set band width
            if(chirp_row[12] == "FM"):
                new_any_row[6] = "25K"
            elif(chirp_row[12] == "NFM"):
                new_any_row[6] = "12.5K"
            else:
                print("Unknown chirp mode in column 12")
                print("Exiting...")
                exit()

            #setCTCSS            
            ##CTCSS receive
            if(float(chirp_row[7]) == 88.5): #85.5 is the default CHIRP subtone. It just couses problems. 
                new_any_row[7]="Off"
            else:
                new_any_row[7]=chirp_row[7]

            ##CTCSS transmit
            new_any_row[8]=chirp_row[6]

            #Appending non populated right side of the row
            new_any_row = new_any_row[:9] + anytone_right_side_of_row
            print(new_any_row)
            if len(new_any_row) != len(anytone_header):
                print("New anytone row is not the correct length")
                print("Exiting...")
                exit()

            
            anytone.writerow(new_any_row)

            