import tensorflow as tf

a=tf.constant(1.)
print(a.device)

with tf.device("GPU"):
    b=tf.constant(2.0)

print(b.device)

with tf.device("GPU"):
    c=tf.range(4)

cc=c.numpy()
c.shape
c.ndim
tf.rank(c)

tf.is_tensor(a)
a.dtype