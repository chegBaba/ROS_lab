import rospy
from sound_play.libsoundplay import SoundClient

if __name__ == '__main__':
    rospy.init_node('say', anonymous = True)
    soundhandle = SoundClient()
    rospy.sleep(1)

    voice = 'voice_kal_diphone'
    volume = 1.0
    s = 'Hello world'
    print 'Saying: %s' % s
    print 'Voice: %s' % voice
    print 'Volume: %s' % volume

    soundhandle.say(s, voice, volume)
    rospy.sleep(1)
