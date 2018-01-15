#!/usr/bin/env python
# coding: utf8
import pimaton

if __name__ == '__main__':
    try:
        pimaton.main()

    except KeyboardInterrupt:
        print("Leaving pimaton, goodbye")

    except Exception as exception:
        print("unexpected error: ", str(exception))

    finally:
        # camera.stop_preview()
        # camera.close()
        # GPIO.cleanup()
        pass
