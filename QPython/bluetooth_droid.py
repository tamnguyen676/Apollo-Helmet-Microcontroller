import androidhelper
import time

droid = androidhelper.Android()
droid.toggleBluetoothState(True)
is_server = True

if is_server:
    droid.bluetoothMakeDiscoverable()
    print("Made bluetooth discoverable")
    droid.bluetoothAccept()
    print("Accepted bluetooth")
# else:
#     droid.bluetoothConnect()

# if is_server:
#     result = droid.dialogGetInput('Chat', 'Enter a message').result
#     if result is None:
#         droid.exit()
#     droid.bluetoothWrite(result + '\n')

while True:
    print('Waiting on message...')
    message = droid.bluetoothReadLine().result
    #droid.dialogCreateAlert('Chat Received', message)
    print("Received message: %s" % message)
    # droid.dialogSetPositiveButtonText('Ok')
    # droid.dialogShow()
    # droid.dialogGetResponse()
    # result = droid.dialogGetInput('Chat', 'Enter a message').result
    # if result is None:
    #     break
    # droid.bluetoothWrite(result + '\n')

droid.exit()