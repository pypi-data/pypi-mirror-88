==================
Configuration File
==================

Path Section
============

Give the data path. 

Data Section
============

Format of data, and train file

Feature Section
===============

Item features. The structure is ``item id, feature name, feature value``

Splitter Section
================

Select amount of data to train and method of splitting data.

Algorithm Section
=================

Select the initial recommendation algorithm. The default setting is biasedmf.
Can be assigned two different Num-factor value for comparing results. 

Metrics Section
===============

Select proper metrics for fairness calculation, such as ``erroe-based fairness metrics`` and ``feature-based diversity metrics``.

Rerank Section
==============

Select different method to rerank the previous result for fairness of recommendation system, including ``far_rerank``, ``pfar_rerank``, ``MMR_rerank``, ``ofar_rerank`` and more.
Control the accuracy and diversity of the recommendation system by hyperparameter lambda. Higher lambda means more accurate, and Lower lambda means higher diversity.


Post-Porcession Section
=======================

Connect your project to your Slack, show the visualized results in your Slack channel or dropbox. Please read ``Slack integration`` and ``Dropbox integration`` for more details