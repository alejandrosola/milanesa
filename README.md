# Milanesas como provincias argentinas

En ese mini proyecto estoy intentando crear y entrenar una **convolutional neural network** que reciba una imágen del usuario y devuelva a qué provincia argentina se le parece más.

## Librerías usadas
Se utilizó el lenguaje **Python**, con ayuda de las siguientes librerías
- **[Tensorflow](https://www.tensorflow.org/api_docs/python/tf)** para la red neuronal
- **[Scikit learn](https://scikit-learn.org/stable/)** para manejar los conjuntos de datos y de prueba
- **[opencv](https://pypi.org/project/opencv-python/)** para el procesamiento de las imágenes

## Funcionamiento
Para entrenar a la red neuronal para que reconozca a las provincias, armé un set de datos artificial (se puede ver el script en **deformar.py**) en el cual uso cada una de las imágenes de las provincias y las deformo ligeramente para que la red neuronal se entrene.
Cuando ya se tiene el **set de entrenamiento**, en el script **entrenar_red.py** se separa el mismo set en dos (train y test) para entrenar la red utilizando funciones de tensorflow
