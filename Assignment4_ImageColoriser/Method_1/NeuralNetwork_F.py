import numpy as np
import math
from copy import deepcopy
from datetime import datetime

np.seterr(all='raise')


class NeuralNetwork():

    SigmoidActivation = "sigmoid"
    LinearActivation = "linear"

    def __init__(self,
                 num_hidden_layers=3, learning_rate=0.05, num_neurons_each_layer=None, batch_size=32,
                 epochs=30, weights=None):
        self.weights = weights
        self.count_hidden_layers = num_hidden_layers
        self.total_layers = self.count_hidden_layers + 1
        self.layers = range(self.total_layers)
        self.count_neurons_each_layer = num_neurons_each_layer
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size

        # Sigmoid activation for other layers. Linear activation for last layer
        self.activations = [self.SigmoidActivation] * self.count_hidden_layers + [self.LinearActivation]
        # Mapping between the Activation Name and the corresponding function
        self.activations_functions = {
            self.SigmoidActivation: self.sigmoid,
            self.LinearActivation: self.linear
        }
        # Mapping between the Action Name and the corresponding derivative
        self.activation_function_derivatives = {
            self.SigmoidActivation: self.sigmoid_derivative,
            self.LinearActivation: self.linear_derivative
        }

    # Initially set it to "return return 1.0 / (1 + np.exp(-x))"
    # However, this couldn't handle all cases.
    def sigmoid(self, x):
        def sigfunc(x):
            if x < 0:
                return 1 - 1 / (1 + math.exp(x))
            else:
                return 1 / (1 + math.exp(-x))
        x_val = np.array([sigfunc(i) for i in x])
        return x_val

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def linear(self, x):
        return x

    def linear_derivative(self, x):
        return np.ones_like(x)

    def mse(self, pred, y):
        return np.mean((pred - y) ** 2)

    def fetch_activation_function(self, current_layer):
        # Fetching the activation type and function for the current layer
        activation_current_layer = self.activations[current_layer]
        activation_func_current_layer = self.activations_functions[activation_current_layer]
        return activation_func_current_layer

    def fetch_activation_function_derivatives(self, current_layer):
        # Fetching the activation function and its corresponding derivative
        activation_func_current_layer = self.activations[current_layer]
        activation_func_derivative_current_layer = self.activation_function_derivatives[activation_func_current_layer]
        return activation_func_derivative_current_layer

    def initialise_weights(self, input_shape):
        # Taking the extra external bias into account
        self.count_neurons_each_layer.append(1)
        # Initialising a numpy array
        self.weights = []
        # Iterate through all the layers
        for current_layer in self.layers:
            self.weights.append([])
            count_neurons_in_present_layer = self.count_neurons_each_layer[current_layer]
            # np.random.seed(datetime.now())
            if current_layer != 0:
                # Adding 1 for the bias neuron
                self.weights[current_layer] = np.random.randn(count_neurons_in_present_layer,
                                                              1 + self.count_neurons_each_layer[current_layer - 1])
            else:
                # Choosing random numbers for the given size using 'randn' i.e. loc = 0 and scale = 1
                self.weights[current_layer] = np.random.randn(count_neurons_in_present_layer, input_shape)

        self.weights = np.array(self.weights)
        self.old_weights = deepcopy(self.weights)

    # Using the mathematical formula to obtain the new weight using previous weights and learning rate
    def update_weights(self):
        avg_batch_weight_derivatives = np.mean(self.weight_derivatives_batch, axis = 0)
        self.weights = self.old_weights - self.learning_rate * avg_batch_weight_derivatives
        self.old_weights = deepcopy(self.weights)
        self.weight_derivatives_batch = []

    # Reference for this has been taken from GitHub
    def bwd_propagation(self, x, y, out):

        # The derivatives array will have the same shape as weights array. - one derivative for each
        # weight
        derivatives_output, derivatives_weight = deepcopy(out), deepcopy(self.weights)

        # Computing the output derivatives || COMPUTE
        # We traverse from the end to the start i.e. Reversed order
        reversed_layers = self.layers[::-1]
        for current_layer in reversed_layers:
            next_layer = current_layer + 1

            # print("Current Layer : {} and Total Layer: {}".format(curr_layer, self.total_layers-1))

            # For the last layer simply use the formula -- COMPUTE
            if current_layer == self.total_layers - 1:
                derivatives_output[current_layer] = 2*(out[current_layer] - y)
                continue

            # Fetching the activation function derivatives || FETCH
            # Both 'activation_function' and 'activation_function_derivatives' have dict structure --
            # -- from where corresponding functions and their derivatives can be computed
            activation_func_for_next_layer = self.activations[next_layer]
            activation_func_derivative_current_layer = self.activation_function_derivatives[activation_func_for_next_layer]

            # Fetching next layer output derivatives || FETCH
            next_layer_output_derivatives = derivatives_output[next_layer]

            # Computing the activation derivatives || COMPUTE
            output_current_layer = out[current_layer].copy()
            output_current_layer = np.insert(output_current_layer, obj = 0, values = 1)
            activation_func_derivative_next_layer = activation_func_derivative_current_layer(
                self.old_weights[next_layer] @ output_current_layer)
            activation_func_derivative_next_layer = activation_func_derivative_next_layer.reshape(-1, 1)

            # print(self.old_weights[next_layer])

            # Removing the bias from the weights data
            # The first col entry is the external bias
            weights_next_layer_bereft_bias = self.old_weights[next_layer][:, 1:]

            # Computing Hadmard product - multiply each neuron's activation derivative with its weights || COMPUTE
            hadmard_product = activation_func_derivative_next_layer * weights_next_layer_bereft_bias

            # Since each neuron contributes to all the neurons in the next layer
            # Matrix multiplication of the output derivatives and the Hadamard product
            derivatives_output[current_layer] = next_layer_output_derivatives @ hadmard_product

        # Using the above calculated output derivatives, updating the weight
        for current_layer in reversed_layers:
            activation_func_derivative_current_layer = self.fetch_activation_function_derivatives(current_layer)
            # If the layer is first, then use the data from the previous layer
            if current_layer == 0:
                output_previous_layer = x
            else:
                previous_layer = current_layer - 1
                output_previous_layer = out[previous_layer].copy()
                output_previous_layer = np.insert(output_previous_layer, obj=0, values=1)

            # Current layer output derivatives
            current_layer_output_derivatives = derivatives_output[current_layer].reshape(-1, 1)

            # Fetch the current layer activation derivatives for the current layer || FETCH
            current_layer_activation_derivatives = activation_func_derivative_current_layer(
                self.old_weights[current_layer] @ output_previous_layer)
            current_layer_activation_derivatives = current_layer_activation_derivatives.reshape(-1, 1)

            # Multiplying each neuron's activation function derivatives with all the previous layer's outputs
            current_layer_weight_derivatives = current_layer_output_derivatives * current_layer_activation_derivatives * output_previous_layer
            derivatives_weight[current_layer] = current_layer_weight_derivatives

        # Append the current data point's weight derivatives in the batch derivatives array
        self.weight_derivatives_batch.append(derivatives_weight)

    def batch_gradient_descent(self, X_with_bias, X, y):
        for current_epoch in range(self.epochs):
            # Initialise arrays to store all weight derivatives of the batch
            self.weight_derivatives_batch = []

            # Updating weights via mini batch gradient descent
            for current_index in range(X_with_bias.shape[0]):  # rows
                out = self.feed_forward(X_with_bias[current_index])
                self.bwd_propagation(X_with_bias[current_index], y[current_index], out)

                if (current_index + 1) % self.batch_size == 0:
                    self.update_weights()

            predictions = self.predict_values(X)
            loss = self.mse(predictions, y)
            print("Epoch =  {} \t & \t MSE = {}".format(str(current_epoch + 1), str(loss)))

    def feed_forward(self, x):
        out = []
        for current_layer in self.layers:
            out.append([])
            # Fetching the activation type and function for the current layer
            activation_func_current_layer = self.fetch_activation_function(current_layer)

            if current_layer == 0:
                output_previous_layer = x
            else:
                output_previous_layer = out[current_layer - 1].copy()
                output_previous_layer = np.insert(output_previous_layer, obj=0, values=1)

            out[current_layer] = activation_func_current_layer(self.weights[current_layer] @ output_previous_layer)
        out = np.array(out)
        return out

    def fit(self, X, y):

        # Adding bias column to the input X
        X_with_bias = np.column_stack((np.ones(len(X)), X))     # bias

        # Initializing the weights of the network
        self.initialise_weights(X_with_bias.shape[1])   # columns
        self.batch_gradient_descent(X_with_bias, X, y)

    def predict_values(self, X):

        # Adding bias column to the input X
        X_with_bias = np.column_stack((np.ones(len(X)), X))

        prediction = []
        for current_x in X_with_bias:
            pred = self.feed_forward(current_x)[-1][-1]
            prediction.append(pred)

        prediction = np.array(prediction)
        return prediction
