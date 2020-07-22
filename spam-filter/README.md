# Spam Filter - Use PAI To Build a Naive Bayes Spam Classifier

- Status: **OK**
- Notes: Code tested and working as of 2020-07-22 (YYYY-MM-DD)

## What

This code demonstrates how to use Platform for AI (PAI)'s [Data Science Workshop (DSW)](https://www.alibabacloud.com/help/doc-detail/126293.htm) to build a simple Naive Bayes spam classifier.

The idea for the spam classifier comes from [this Kaggle page](https://www.kaggle.com/veleon/ham-and-spam-dataset). The idea of using a Naive Bayes classifier in particular is an older idea: you can learn more from [this Wikipedia article](https://en.wikipedia.org/wiki/Naive_Bayes_spam_filtering). 

The code here is in the form of a Jupyter notebook `.ipynb` file. All you need to do is upload this code (along with ham and spam example mail) to PAI-DSW, then run the notebook! This will extract email data (using Python's built-in `email` library), build feature vectors based on word frequency using scikit-learn's `CountVectorizer` (docs [here](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)), and then finally train a Complement Naive Bayes model using scikit-learn's `ComplementNB` (docs [here](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.ComplementNB.html#sklearn.naive_bayes.ComplementNB)).

If you're curious about Naive Bayes in general, the scikit-learn website has a [really great introduction](https://scikit-learn.org/stable/modules/naive_bayes.html#complement-naive-bayes). 

## How

It's pretty straightforward!

### Create a PAI DSW Environment

You can follow [this guide](https://www.alibabacloud.com/help/doc-detail/155151.htm) to set up a new PAI DSW instance.

Once your instance is running you'll see it in the instance list at the bottom of the console, and there will be a `Launch DSW` button you can click to enter the DSW web console. 

A couple notes:

- Choose the lowest specification **CPU** type DSW notebook instance: we won't need a GPU for this experiment
- Users outside Mainland China should deploy their DSW notebook instance in a region outside mainland China, we recommend **Singapore**
- Users inside Mainland China should deploy their DW notebook instance in a region inside mainland China, we recommend **Shanghai**

### Prepare the data and code

To use PAI to train our Naive Bayes model, we need to upload our code, as well as some training and test data (spam and non-spam emails):

1. Get the email data from [here](https://www.kaggle.com/veleon/ham-and-spam-dataset/download)
2. Unpack the zip file
3. Create a new folder called `email_example`: in this new folder, include the `email_model.ipynb` file from this repository and the `hamnspam` folder from the Kaggle zip file
4. Create a new zip file, `email_example.zip` from the `email_example` folder

### Upload the data and code

By default, PAI notebook instances come with 5 GB of storage space. You can store Jupyter notebook files and test and training data there, and you have access to this space via a Linux command line that is built into the DSW web console. 

We'll be using this built-in storage space to upload our code and data. The *upload data* section of [this document](https://www.alibabacloud.com/help/doc-detail/155155.htm) explains how. Essentially you just click the "Upload" button on the left side of the DSW web interface, and select the `email_example.zip` file. A file upload dialog will open up and once it gets to 100% you can close the dialog, that's it! 

### Unpack the data, install extra dependencies

From the DSW web console, scroll down to the bottom of the `DSW Launcher` tab and choose `Terminal` from the `Other` category. This will open up a terminal window.

From this window, you should be able to unzip the `email_example.zip` file that you uploaded, like this:

```
unzip email_example.zip
```

It may take a while to run as there are several thousand emails included in the `hamnspam` directory.

Before we actually load our `.ipynb` file, we need to install some third party Python packages which are not included in the DSW environment out-of-the-box. Specifically, we need scikit-learn BeautifulSoup (an HTML parser), and lxml (needed by BeautifulSoup). We install these from the PAI DSW terminal window with:

```
pip install bs4 lxml sklearn
```

### Training and testing our model

In the file explorer pane on the left side of the DSW web console, double click on the folder `email_examples`. Inside you should see the `hamnspam` directory and the Jupyter notebook file `email_model.ipynb`. Double click on `email_model.ipynb` to open a new Jupyter notebook tab. 

Have a look at the code and make sure you understand what it is doing. There are comments to help you understand, but in general the code is broken into these steps:

- Read in email data
- Convert email data to plain text
- Convert plain text into lists of word counts
- Split this data into training and test datasets
- Train Naive Bayes model based on word counts (probability each word appears in a spam or non-spam email)
- Calculate "accuracy" (precision and recall) of the model, on our test data
- Try out the model on two "fake" emails (one obviously legitimate, one obviously spam)

There is a `Run` button or `>` arrow near the top of the code that will allow you to run it piece-by-piece (you'll notice Jupyter notebooks are broken into sections, which can be run or rerun independently), or you can choose to run the full notebook at once. Feel free to play around with the code and make changes! 

One fun thing to try is to generate your own fake spam and non-spam emails and plug them into the code at the bottom of the notebook. Can you write a spam message that fools the classifier? 

### Cleaning Up

When you're done, return to the PAI console and stop your notebook. You won't be charged for stopped notebooks, but if you're completely done, you can delete the notebook entirely. This will remove the notebook environment and all our data and code. See the section *Manage a DSW instance* at the bottom of [this page](https://www.alibabacloud.com/help/doc-detail/155151.htm) for instructions on stopping and deleting instances.

## Issues

If you are using PAI-DSW outside Mainland China, I recommend choosing a region outside the Mainland for your PAI-DSW instance: I usually use **Singapore**.

If you are inside China, you should choose a Chinese region such as **Shanghai**. Be aware that some regions in China (like Shanghai and Beijing) offer a newer version of PAI-DSW called 'DSW 2.0'. Feel free to try it out, but this code has not been tested under DSW 2.0 yet. 

## Credits

See the "What" section. Big thanks to Wessel van Lit whose [Kaggle project](https://www.kaggle.com/veleon/ham-and-spam-dataset) was the inspiration for this code. 

