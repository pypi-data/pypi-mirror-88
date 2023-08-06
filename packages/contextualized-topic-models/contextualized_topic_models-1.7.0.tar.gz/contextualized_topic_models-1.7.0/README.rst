===========================
Contextualized Topic Models
===========================

.. image:: https://img.shields.io/pypi/v/contextualized_topic_models.svg
        :target: https://pypi.python.org/pypi/contextualized_topic_models

.. image:: https://travis-ci.com/MilaNLProc/contextualized-topic-models.svg
        :target: https://travis-ci.com/MilaNLProc/contextualized-topic-models

.. image:: https://readthedocs.org/projects/contextualized-topic-models/badge/?version=latest
        :target: https://contextualized-topic-models.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/github/contributors/MilaNLProc/contextualized-topic-models
        :target: https://github.com/MilaNLProc/contextualized-topic-modelsgraphs/contributors/
        :alt: Contributors

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
        :target: https://lbesson.mit-license.org/
        :alt: License

.. image:: https://pepy.tech/badge/contextualized-topic-models
        :target: https://pepy.tech/project/contextualized-topic-models
        :alt: Downloads

.. image:: https://colab.research.google.com/assets/colab-badge.svg
    :target: https://colab.research.google.com/drive/1V0tkpJL1yhiHZUJ_vwQRu6I7_svjw1wb?usp=sharing
    :alt: Open In Colab


Contextualized Topic Models (CTM) are a family of topic models that use pre-trained representations of language (e.g., BERT) to
support topic modeling. See the papers for details:

* `Cross-lingual Contextualized Topic Models with Zero-shot Learning` https://arxiv.org/pdf/2004.07737v1.pdf
* `Pre-training is a Hot Topic: Contextualized Document Embeddings Improve Topic Coherence` https://arxiv.org/pdf/2004.03974.pdf


.. image:: https://raw.githubusercontent.com/MilaNLProc/contextualized-topic-models/master/img/logo.png
   :align: center
   :width: 200px

README
------

Make **sure** you read the doc a bit.
The cross-lingual topic modeling requires to use a ZeroShot model and it is trained only on **ONE** language;
with the power of multilingual BERT it can then be used to predict the topics of documents in unseen languages.
For more details you can read the two papers mentioned above.


Jump start Tutorial
-------------------

.. |colab1| image:: https://colab.research.google.com/assets/colab-badge.svg
    :target: https://colab.research.google.com/drive/1V0tkpJL1yhiHZUJ_vwQRu6I7_svjw1wb?usp=sharing
    :alt: Open In Colab

.. |colab2| image:: https://colab.research.google.com/assets/colab-badge.svg
    :target: https://colab.research.google.com/drive/1quD11TMy-1D-GxPUj_Dea4iRYmOO8C2C?usp=sharing
    :alt: Open In Colab

+----------------------------------------------------------------+--------------------+
| Name                                                           | Link               |
+================================================================+====================+
| CombinedTM for Wikipedia Documents                             | |colab1|           |
+----------------------------------------------------------------+--------------------+
| CombinedTM with Preprocessing                                  | |colab2|           |
+----------------------------------------------------------------+--------------------+

TL;DR
-----

+ In CTMs we have two models. CombinedTM and ZeroShotTM, they have different use cases.
+ CTMs work better when the size of the bag of words **has been restricted to a number of terms** that does not go over **2000 elements** (this is because we have a neural model that reconstructs the input bag of word). We have a preprocessing_ pipeline that can help you in dealing with this.
+ Check the BERT model you are using, the **multilingual BERT model one used on English data might not give results that are as good** as the pure English trained one.
+ **Preprocessing is key**. If you give BERT preprocessed text, it might be difficult to get out a good representation. What we usually do is use the preprocessed text for the bag of word creating and use the NOT preprocessed text for BERT embeddings. Our preprocessing_ class can take care of this for you.

ZeroShot Topic Model
--------------------

.. image:: https://raw.githubusercontent.com/MilaNLProc/contextualized-topic-models/master/img/lm_topic_model_multilingual.png
   :target: https://raw.githubusercontent.com/MilaNLProc/contextualized-topic-models/master/img/lm_topic_model_multilingual.png
   :align: center
   :width: 400px

Combined Topic Model
--------------------

.. image:: https://raw.githubusercontent.com/MilaNLProc/contextualized-topic-models/master/img/lm_topic_model.png
   :target: https://raw.githubusercontent.com/MilaNLProc/contextualized-topic-models/master/img/lm_topic_model.png
   :align: center
   :width: 400px



Software details:

* Free software: MIT license
* Documentation: https://contextualized-topic-models.readthedocs.io.
* Super big shout-out to `Stephen Carrow`_ for creating the awesome https://github.com/estebandito22/PyTorchAVITM package from which we constructed the foundations of this package. We are happy to redistribute again this software under the MIT License.


Features
--------

* Combines BERT and Neural Variational Topic Models
* Two different methodologies: Combined, where we combine BoW and BERT embeddings and ZeroShot, that uses only BERT embeddings
* Includes methods to create embedded representations and BoW
* Includes evaluation metrics


Overview
--------

**Important**: If you want to use CUDA you need to install the correct version of
the CUDA systems that matches your distribution, see pytorch_.

Install the package using pip

.. code-block:: bash

    pip install -U contextualized_topic_models

Contextual neural topic models can be easily instantiated using few parameters (although there is a wide range of
parameters you can use to change the behaviour of the neural topic model). When you generate
embeddings with BERT remember that there is a maximum length and for documents that are too long some words will be ignored.

An important aspect to take into account is which network you want to use: the one that combines BERT and the BoW or the one that just uses BERT.
It's easy to swap from one to the other:

ZeroShotTM:

.. code-block:: python

    ZeroShotTM(input_size=len(qt.vocab), bert_input_size=512, n_components=50)

CombinedTM:

.. code-block:: python

    CombinedTM(input_size=len(qt.vocab), bert_input_size=512,  n_components=50)


But remember that you can do zero-shot cross-lingual topic modeling only with the :code:`ZeroShotTM` model. See cross-lingual-topic-modeling_

Mono vs Multi-lingual Embeddings
--------------------------------

All the examples below use a multilingual embedding model :code:`distiluse-base-multilingual-cased`.
If you are doing topic modeling in English, **you can use the English sentence-bert model**, `bert-base-nli-mean-tokens`. In that case,
it's really easy to update the code to support mono-lingual English topic modeling.

.. code-block:: python

    qt = QuickText("bert-base-nli-mean-tokens",
                text_for_bert=list_of_unpreprocessed_documents,
                text_for_bow=list_of_preprocessed_documents)

In general, our package should be able to support all the models described in the `sentence transformer package <https://github.com/UKPLab/sentence-transformers>`_.
and in HuggingFace.

Zero-Shot Cross-Lingual Topic Modeling
--------------------------------------

Our ZeroShotTM can be used for zero-shot topic modeling. It can handle words that are not used during the training phase.
More interestingly, this model can be used for cross-lingual topic modeling! See the paper (https://arxiv.org/pdf/2004.07737v1.pdf)

The high level API to handle the text is pretty easy to use; `text_for_bert` should be used to pass to the model
a list of documents that are not preprocessed. In this way, SBERT can use all the information in the text to generate the representations.
Instead, to `text_for_bow` you should pass the pre-processed text used to build the BoW.

.. code-block:: python

    from contextualized_topic_models.models.ctm import ZeroShotTM
    from contextualized_topic_models.utils.data_preparation import QuickText
    from contextualized_topic_models.utils.data_preparation import bert_embeddings_from_file
    from contextualized_topic_models.datasets.dataset import CTMDataset

    qt = QuickText("distiluse-base-multilingual-cased",
                    text_for_bert=list_of_ENGLISH_unpreprocessed_documents,
                    text_for_bow=list_of_ENGLISH_preprocessed_documents)

    training_dataset = qt.load_dataset()

    ctm = ZeroShotTM(input_size=len(qt.vocab), bert_input_size=512, n_components=50)

    ctm.fit(training_dataset) # run the model

    ctm.get_topics()


Predict Topics for Unseen Documents
-----------------------------------
Once you have trained the cross-lingual topic model, you can use this simple pipeline to predict the topics for documents in a different language.

**Note** that the bag of words of the two languages will not be comparable!

.. code-block:: python


    qt = QuickText("distiluse-base-multilingual-cased",
                    text_for_bert=list_of_SPANISH_unpreprocessed_documents,
                    text_for_bow=list_of_SPANISH_preprocessed_documents)

    testing_dataset = qt.load_dataset()

    # n_sample how many times to sample the distribution (see the doc)
    ctm.get_thetas(testing_dataset, n_samples=20)

Combined Topic Modeling
-----------------------

Here is how you can use the CombinedTM. Combined TM combines the BoW with SBERT, a process that seems to increase
the coherence (https://arxiv.org/pdf/2004.03974.pdf).

.. code-block:: python

    from contextualized_topic_models.models.ctm import CombinedTM
    from contextualized_topic_models.utils.data_preparation import QuickText
    from contextualized_topic_models.utils.data_preparation import bert_embeddings_from_file
    from contextualized_topic_models.datasets.dataset import CTMDataset

    qt = QuickText("distiluse-base-multilingual-cased",
                    text_for_bert=list_of_unpreprocessed_documents,
                    text_for_bow=list_of_preprocessed_documents)

    training_dataset = qt.load_dataset()

    ctm = CombinedTM(input_size=len(qt.vocab), bert_input_size=512, n_components=50)

    ctm.fit(training_dataset) # run the model

See the example notebook in the `contextualized_topic_models/examples` folder.
We have also included some of the metrics normally used in the evaluation of topic models, for example you can compute the coherence of your
topics using NPMI using our simple and high-level API.

.. code-block:: python

    from contextualized_topic_models.evaluation.measures import CoherenceNPMI

    with open('preprocessed_documents.txt',"r") as fr:
        texts = [doc.split() for doc in fr.read().splitlines()] # load text for NPMI

    npmi = CoherenceNPMI(texts=texts, topics=ctm.get_topic_lists(10))
    npmi.score()






Preprocessing
-------------

Do you need a quick script to run the preprocessing pipeline? we got you covered! Load your documents
and then use our SimplePreprocessing class. It will automatically filter infrequent words and remove documents
that are empty after training. The preprocess method will return the preprocessed and the unpreprocessed documents.
We generally use the unpreprocessed for BERT and the preprocessed for the Bag Of Word.

.. code-block:: python

    from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessing

    documents = [line.strip() for line in open("unpreprocessed_documents.txt").readlines()]
    sp = WhiteSpacePreprocessing(documents)
    preprocessed_documents, unpreprocessed_documents, vocab = sp.preprocess()


Development Team
----------------

* `Federico Bianchi`_ <f.bianchi@unibocconi.it> Bocconi University
* `Silvia Terragni`_ <s.terragni4@campus.unimib.it> University of Milan-Bicocca
* `Dirk Hovy`_ <dirk.hovy@unibocconi.it> Bocconi University

References
----------

If you use this in a research work please cite these papers:

CombinedTM

::

    @article{bianchi2020pretraining,
        title={Pre-training is a Hot Topic: Contextualized Document Embeddings Improve Topic Coherence},
        author={Federico Bianchi and Silvia Terragni and Dirk Hovy},
        year={2020},
       journal={arXiv preprint arXiv:2004.03974},
    }


ZeroShotTM

::

    @article{bianchi2020crosslingual,
        title={Cross-lingual Contextualized Topic Models with Zero-shot Learning},
        author={Federico Bianchi and Silvia Terragni and Dirk Hovy and Debora Nozza and Elisabetta Fersini},
        year={2020},
       journal={arXiv preprint arXiv:2004.07737},
    }



Credits
-------


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
To ease the use of the library we have also included the `rbo`_ package, all the rights reserved to the author of that package.

Note
----

Remember that this is a research tool :)

.. _pytorch: https://pytorch.org/get-started/locally/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _preprocessing: https://github.com/MilaNLProc/contextualized-topic-models#preprocessing
.. _cross-lingual-topic-modeling: https://github.com/MilaNLProc/contextualized-topic-models#cross-lingual-topic-modeling
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Stephen Carrow` : https://github.com/estebandito22
.. _`rbo` : https://github.com/dlukes/rbo
.. _Federico Bianchi: https://federicobianchi.io
.. _Silvia Terragni: https://silviatti.github.io/
.. _Dirk Hovy: https://dirkhovy.com/
