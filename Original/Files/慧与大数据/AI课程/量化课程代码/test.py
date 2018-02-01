import tensorflow as tf

with tf.Graph().as_default():
    a=tf.constant(1.0,name='a')
    b=tf.constant(2.0,name='b')
    result=tf.add(a,b,name='result')

    with tf.Session() as sess:
        print(sess.run(result))




















