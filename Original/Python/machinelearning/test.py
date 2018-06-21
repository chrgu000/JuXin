import tensorflow as tf     
BATCH_SIZE=5    
label=tf.expand_dims(tf.constant([1,3,5,7,9]),1)#真实标签  shape==>[5,1]  
index=tf.expand_dims(tf.range(0, BATCH_SIZE),1)#真实标签的索引  shape==>[5,1]  
concated = tf.concat([index, label],1)   #将标签和索引tensor在第二个维度上连接起来，新的concated的shape==>[5,2]  
onehot_labels = tf.sparse_to_dense(concated, [BATCH_SIZE,10], 1.0, 0.0) # onehot_labels的shape==>[5,10]  
with tf.Session() as sess:    
    onehot1=sess.run(onehot_labels)      
    print (onehot1)  






































































