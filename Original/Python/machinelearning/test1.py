import tensorflow as tf
import matplotlib.pyplot as plt
import os
import numpy as np
import csv
import string
import requests
import io
from zipfile import ZipFile
from tensorflow.contrib import learn
sess=tf.Session()

save_file_name=os.path.join('temp','temp_spam_data.csv')
if os.path.isfile(save_file_name):
    text_data=[]
    with open(save_file_name,'r') as temp_output_file:
        reader=csv.reader(temp_output_file)
        for row in reader:
            text_data.append(row)
else:
    z=ZipFile('D:/Trade/Original/Files/reading/smsspamcollection.zip')
    file=z.read('SMSSpamCollection')
    text_data=file.decode()
    text_data=text_data.encode('ascii',errors='ignore')
    text_data=text_data.decode().split('\n')
    text_data=[x.split('\t') for x in text_data if len(x)>=1]
    with open(save_file_name,'w') as temp_output_file:
        writer=csv.writer(temp_output_file)
        writer.writerows(text_data)
texts=[x[1] for x in text_data]
target=[x[0] for x in text_data]
target=[1 if x=='spam' else 0 for x in target]

texts=[x.lower() for x in texts]
texts=[''.join(c for c in x if c not in string.punctuation)\
       for x in texts]
texts=[''.join(c for c in x if c not in '0123456789')\
       for x in texts]
texts=[' '.join(x.split()) for x in texts]
text_lengths=[len(x.split()) for x in texts]
text_lengths=[x for x in text_lengths if x<50]
plt.hist(text_lengths,bins=25)
plt.title('Histogram of # of Words in Texts')

sentence_size=25
min_word_freq=3
vocab_processor=learn.preprocessing.VocabularyProcessor(\
sentence_size,min_frequency=min_word_freq)
vocab_processor.fit_transform(texts)
embedding_size=len(vocab_processor.vocabulary_)
train_indices=np.random.choice(len(texts),\
                round(len(texts)*0.8),replace=False)
test_indices=np.array(list(set(range(len(texts)))-set(train_indices)))
target_train=[x for ix,x in enumerate(target) \
              if ix in train_indices]
target_test=[x for ix,x in enumerate(target) if ix in test_indices]

identity_mat=tf.diag(tf.ones(shape=[embedding_size]))
A=tf.Variable(tf.random_normal(shape=[embedding_size,1]))
b=tf.Variable(tf.random_normal(shape=[1,1]))
x_data=tf.placeholder(shape=[sentence_size],dtype=tf.int32)
y_target=tf.placeholder(shape=[1,1],dtype=tf.float32)
x_embed=tf.nn.embedding_lookup(identity_mat,x_data)
x_col_sums=tf.reduce_sum(x_embed,0)

















































