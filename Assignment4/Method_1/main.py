import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from PIL import Image
from sklearn.preprocessing import StandardScaler
from NeuralNetwork_F import NeuralNetwork
import cv2
import os


class ImageColorizer:
    def __init__(self, list_red, list_green, list_blue, image_location):
        self.size_image = (0, 0)
        self.location_image = image_location
        self.image = None
        self.object_pixel = None
        self.values_pixel= None
        self.red_content = list_red
        self.blue_content = list_blue
        self.green_content = list_green

    def gen_colored_image(self):
        # Open the image
        self.image = Image.open(self.location_image)
        # Pixel object is the loaded image
        self.object_pixel = self.image.load()
        # Assigning the size of the image
        self.size_image = self.image.size
        # Starting from the left corner, moving L to R, extracting all pixel values
        self.values_pixel = list(self.image.getdata())
        width, height, list_itr = 100, 100, 0
        # The argument 3 corresponds to three color channels
        data = np.zeros((height, width, 3), dtype = np.uint8)
        for pixel_current_w in range(width):
            for pixel_current_h in range(height):
                data[pixel_current_w, pixel_current_h] = (int(self.red_content[list_itr]),
                                                          int(self.green_content[list_itr]),
                                                          int(self.blue_content[list_itr]))
                list_itr += 1
        # Using the PIL module, generate the coloured image using pixel values og RGB
        output_image = Image.fromarray(data, 'RGB')
        output_image.save('test_image_output.png')
        output_image.show()


class AllImageData:
    def __init__(self, directory):
        self.directory = directory

    def dataset_creation(self, gray, red, green, blue):
        X, y = [], []
        gray_padded = np.pad(array=gray, pad_width=3, mode='constant', constant_values=0)
        red_padded = np.pad(array=red, pad_width=3, mode='constant', constant_values=0)
        blue_padded = np.pad(array=blue, pad_width=3, mode='constant', constant_values=0)
        green_padded = np.pad(array=green, pad_width=3, mode='constant', constant_values=0)

        for i in range(0, len(gray_padded) - 6):
            for j in range(0, len(gray_padded) - 6):
                X.append(list(gray_padded[i:i + 7, j:j + + 7].flatten()))

                y.append([red_padded[i:i + 7, j:j + 7].flatten()[int(7 * 7 / 2)],
                          green_padded[i:i + 7, j:j + 7].flatten()[int(7 * 7 / 2)],
                          blue_padded[i:i + 7, j:j + 7].flatten()[int(7 * 7 / 2)]])
        return X, y

    def obtain_images(self, directory=None, data_type=None):
        if data_type == 'test':
            self.directory = directory

        print("{} Directory accessed!".format(self.directory))
        for root, _, files in os.walk(self.directory):
            if root:
                X, y, file_name = [], [], []
                for f in files:
                    if f.split(".")[1] == 'jpg':
                        print("Accessing ", f)
                        image = cv2.imread(os.path.join(root, f))
                        image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
                        # gray image -- USE FORMULA INSTEAD !!!
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        # red, green, blue components
                        red, green, blue = image[:, :, 2], image[:, :, 1], image[:, :, 0]
                        m_X, m_y = self.dataset_creation(gray, red, green, blue)

                        X.append(m_X)
                        y.append(m_y)
                        file_name.append(f)

        return X, y, file_name

    def data_alignment(self, X, y):
        X_data = []
        for current_sublist in X:
            for current_item in current_sublist:
                X_data.append(current_item)

        y_data_red, y_data_blue, y_data_green = [], [], []

        for current_sublist in y:
            for current_item in current_sublist:
                y_data_red.append(current_item[0])
                y_data_green.append(current_item[1])
                y_data_blue.append(current_item[2])

        return X_data, y_data_red, y_data_green, y_data_blue

    def prediction_for_bounds(self, predictions_r, predictions_b, predictions_g):
        for i in range(len(predictions_g)):
            if predictions_b[i] < 0:
                predictions_b[i] = 0
            if predictions_b[i] > 255:
                predictions_b[i] = 255
            if predictions_g[i] < 0:
                predictions_g[i] = 0
            if predictions_g[i] > 255:
                predictions_g[i] = 255
            if predictions_r[i] < 0:
                predictions_r[i] = 0
            if predictions_r[i] > 255:
                predictions_r[i] = 255

            predictions_b[i], predictions_g[i], predictions_r[i] = \
                int(predictions_b[i]), int(predictions_g[i]), int(predictions_r[i])
        return predictions_r, predictions_g, predictions_b


if __name__== '__main__':
    image_data = AllImageData(directory='./Images')
    X, y, file_name = image_data.obtain_images()
    # X_data, y_data_red, y_data_green, y_data_blue = image_data.data_alignment(X, y)
    X_data = []
    for current_sublist in X:
        for current_item in current_sublist:
            X_data.append(current_item)

    y_data_red, y_data_blue, y_data_green = [], [], []

    for current_sublist in y:
        for current_item in current_sublist:
            y_data_red.append(current_item[0])
            y_data_green.append(current_item[1])
            y_data_blue.append(current_item[2])

    scalar = StandardScaler()
    scalar.fit(X_data)

    train_X = scalar.transform(X_data)

    neural_net_R = NeuralNetwork(epochs=50, batch_size=100, num_hidden_layers=4, num_neurons_each_layer=[10, 30, 20, 10],
                                 learning_rate=0.007)

    neural_net_G = NeuralNetwork(epochs=50, batch_size=100, num_hidden_layers=4, num_neurons_each_layer=[10, 30, 20, 10],
                                 learning_rate=0.007)

    neural_net_B = NeuralNetwork(epochs=50, batch_size=100, num_hidden_layers=4, num_neurons_each_layer=[10, 30, 20, 10],
                                 learning_rate=0.007)

    print("\nTraining Red Model\n = = = = = = = = = = = ")
    neural_net_R.fit(train_X, y_data_red)
    print("\nTraining for Green model\n = = = = = = = = = = = ")
    neural_net_G.fit(train_X, y_data_red)
    print("\nTraining for Blue model\n = = = = = = = = = = = ")
    neural_net_B.fit(train_X, y_data_red)

    directory = "./Images/test"
    X, y, files = image_data.obtain_images(directory, "test")
    print(files)

    # test_X_data = []
    # for current_sublist in X:
    #     for current_item in current_sublist:
    #         X_data.append(current_item)
    #
    # test_y_data_red, test_y_data_green, test_y_data_blue = [], [], []
    #
    # for current_sublist in y:
    #     for current_item in current_sublist:
    #         test_y_data_red.append(current_item[0])
    #         test_y_data_green.append(current_item[1])
    #         test_y_data_blue.append(current_item[2])
    #
    # scalar = StandardScaler()
    # scalar.fit(test_X_data)

    test_X_data, test_y_data_red, test_y_data_green, test_y_data_blue = image_data.data_alignment(X, y)
    # test_X_data.reshape(-1,1)
    test_X_data = scalar.transform(test_X_data)
    test_B_predictions = neural_net_B.predict_values(test_X_data)
    test_G_predictions = neural_net_G.predict_values(test_X_data)
    test_R_predictions = neural_net_R.predict_values(test_X_data)
    print("Prediction for BLUE: {}".format(test_B_predictions))
    print("Prediction for GREEN: {}".format(test_G_predictions))
    print("Prediction for RED: {}".format(test_R_predictions))

    assigned_color = ImageColorizer(list_red=test_R_predictions, list_blue=test_B_predictions,
                                    list_green=test_G_predictions, image_location='./Images/test/test_image.jpg')
    assigned_color.gen_colored_image()
    print(" Finished! The Neural Network just did its job!")





