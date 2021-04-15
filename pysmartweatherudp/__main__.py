from .receiver import SWReceiver

def main():
    print ('Starting interactive test')
    receiver = SWReceiver()
    receiver.registerCallback(_obs_callback)
    receiver.registerEventCallback(_evt_callback)
    receiver.run()
    print ('Done')

def _obs_callback(data):
    print ('Observation: %s' % data)

def _evt_callback(data):
    print ('Event: %s' % data)

if __name__ == "__main__":
    main()
