import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

class TaskAllocationModel:
    def __init__(self, csv_path, checkpoint_dir):
        self.csv_path = csv_path
        self.checkpoint_dir = checkpoint_dir
        self.model = None
        self.scaler = StandardScaler()

    def load_dataset(self):
        return pd.read_csv(self.csv_path)

    def prepare_data(self, df):
        X = df[['Task', 'Cognitive_Score', 'Time_Completion_Minutes']]
        y = df['Assignment']
        X_scaled = self.scaler.fit_transform(X)
        y_categorical = to_categorical(y)
        return train_test_split(X_scaled, y_categorical, test_size=0.2, random_state=42)

    def build_model(self, input_shape, num_classes):
        model = Sequential([
            Dense(256, input_shape=(input_shape,), activation='relu'),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(num_classes, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train_and_evaluate(self):
        dataset = self.load_dataset()
        X_train, X_test, y_train, y_test = self.prepare_data(dataset)

        self.model = self.build_model(X_train.shape[1], y_train.shape[1])

        checkpoint_path = os.path.join(self.checkpoint_dir, "checkpoint-{epoch:04d}.ckpt")
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        cp_callback = ModelCheckpoint(
            filepath=checkpoint_path,
            save_weights_only=True,
            verbose=1,
            save_best_only=True,
            monitor='val_loss',
            mode='min'
        )

        history = self.model.fit(
            X_train, y_train, epochs=100, batch_size=32,
            validation_split=0.2, verbose=2, callbacks=[cp_callback]
        )

        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

        final_weights_path = os.path.join(self.checkpoint_dir, "final_model_weights.h5")
        self.model.save_weights(final_weights_path)
        print("Final model weights saved.")

# Example usage
if __name__ == "__main__":
    csv_path = "/DynamicTaskAlocationModule/Data/generated_dataset_dyna_2.csv"
    checkpoint_dir = "/DynamicTaskAlocationModule/weights/"
    task_allocation_model = TaskAllocationModel(csv_path, checkpoint_dir)
    task_allocation_model.train_and_evaluate()
