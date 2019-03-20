# Adaptive System & SocketIO communication protocol
This repository contains both adaptive learning algorithms and SocketIO connection protocol. The structure of the folder is given:
* Folder __Adaptive Learning__ contains the source codes of adaptive alert level generation and apaptive notification time generation.

* Folder __SocketIO__ contains the source code of SocketIO that has been used in Raspberry pi for communicating with the server.

## Adaptive Learning
In this part, we provide 2 different versions of code in both **_Jupyter Notebook_** and **_Python .py_** for you to test the algortithms. For testing, please use the `Jupyter` version to get a better visualisation, but in the actual case, please use the `Python` version. The structure of this part is given:

* `Jupyter Notebook`
    * **_alert level.ipynb_**: it access the database with specific username and get the 1st daily medicine-taken time, and compare it with the current time that the user takes the medicine. The difference will be put into a decision tree model, which is named as `notification_model.sav` and saved in the root folder in **Adaptive Learning**. 
        * The model is trained in the file **_decision_tree_training.ipynb_**, with training data stored in `_./res/notification_lvl.csv_`
        * If you want to change the decision tree model, please change the training data file, and run **_decision_tree_training.ipynb_** it again, the new model wiil be generated and stored in the root folder.
        * After getting the predicted alert level from the decision tree, the predicted level will be passed back to the server using SocketIO files.

    * **_estimate notification time.ipynb_**: it access the database with specific username and get the histories of taking the medicine in morning, afternoon and evening using SQL. Further data and statistical processing will be done in this file. Finally, the predicted time will be generated in terms of `Morning`, `Afternoon` and `Evening`.
        * The time will then be passed back to the server using the SocketIO files.

* `Python Code`
    * **_socket.py_**: this is the main file that the server calls, it will run in the background and listen to the specific topic for generating the alert level and notification time. 
        * This file is also used by the Raspberri Pi to communicate between the Server and Pi. For more information about the modification in the Raspberri Pi version, please refer to [Raspberri Pi Client](https://github.com/elisaherme/CaterPillar/blob/master/pillbox/client.py)
        * `Python-SocketIO` library is used here, please refer to [Python SocketIO](https://python-socketio.readthedocs.io/en/latest/)

    * **_decision_tree.py_**: this is the same as the jupyter version but with more comment and more tidy. The whole file was converted to an object, if you want to test the decision tree, following code would help:

        ``` python
        t = DecisionTree(hour,minute)
        level = t.analysis()
        ```
* `decision_tree_training.ipynb`: this is the file takes the training set in `_./res/notification_lvl.csv_` using sklearn-decision tree classifier. The result model will be saved in the locally called `notification_model.sav`. 
        * If you want to edit the model, please go to this file
        * Source of sklearn SocketIO please refer to [Decision Tree](https://scikit-learn.org/stable/modules/tree.html)

* `res`
    * This folder contains the source file including the training data `_./res/notification_lvl.csv_` and the database for testing `storage.db`

* `Tree Visualisation`: after the training process in the decision tree, the plot of the tree will be generated, and named as `Source.gv.pdf`

## SocketIo
This part contains the source code for communicating between the server and local devices, i.e. Raspberry Pi or PC for testing.

* `socket-io-simulator`: this can simulate the SocketIO sender and receiver, so that the simulation process becomes easier.

* `Jupyter`
    * **_socketio_**: the jupyter version of the SocketIo client.
        * To send the message, `sio.emit(topic, msg)`
        * To receive the message:

            ```
            # client receiver
            @sio.on('topic')
            def on_message(data):
                print('message received with ', data)
            ```

* `Python`
    * **_main_**: it initialises the SocketIO object and use it to send and receive the message to/from Server. This is for testing/demonstration purposes. For details of using SocketIo in this project, please refer to [Raspberri Pi Client](https://github.com/elisaherme/CaterPillar/blob/master/pillbox/client.py) and `socket.py` files.

    * **_client_**: SocketIo object to send and receive the message to/from server.
