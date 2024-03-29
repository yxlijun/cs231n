import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_classes = W.shape[1]
  for i in xrange(num_train):
      scores = np.dot(X[i],W) #1xc
      scores-=np.max(scores)
      #losstemp = -np.log(np.exp(scores[y[i]])/np.sum(np.exp(scores)))
      losstemp = -scores[y[i]] +np.log(np.sum(np.exp(scores)))
      loss += losstemp
      for j in xrange(num_classes):
          outputs = np.exp(scores[j])/(np.sum(np.exp(scores)))
          if j==y[i]:
              dW[:,j] += (-1+outputs)*X[i]
          else:
              dW[:,j] += outputs*X[i]
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  loss/=num_train
  loss += 0.5 * reg * np.sum(W * W)
  dW/=num_train
  dW+=reg*W

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = np.dot(X,W)
  scores-=np.max(scores,axis=1).reshape(num_train,1)
  scores_acc = scores[np.arange(num_train),y]
  scores_tolexp = np.sum(np.exp(scores),axis=1)
  losstemp = -scores_acc+np.log(scores_tolexp)
  loss += np.sum(losstemp)
  loss/=num_train
  loss += 0.5 * reg * np.sum(W * W)
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  outputs = np.exp(scores)/np.sum(np.exp(scores),axis=1).reshape(num_train,1)
  outputs[np.arange(num_train),y]-=1
  dW = np.dot(X.T,outputs)
  dW/=num_train
  dW+=reg*W

  return loss, dW
