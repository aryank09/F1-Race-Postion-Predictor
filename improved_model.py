import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Dropout, BatchNormalization
from tf_keras.optimizers import Adam
from tf_keras.callbacks import EarlyStopping, ReduceLROnPlateau
import joblib
from enhanced_features import add_enhanced_features, engineer_interaction_features

class ImprovedF1Predictor:
    def __init__(self):
        self.neural_network = None
        self.random_forest = None
        self.gradient_boost = None
        self.scaler = None
        self.feature_columns = None
        
    def prepare_features(self, data_list, race_weekend_name=None):
        """Enhanced feature preparation with new engineered features"""
        
        # Combine all race data
        all_race_data = pd.concat(data_list, ignore_index=True)
        
        # Add enhanced features if race weekend is provided
        if race_weekend_name:
            all_race_data = add_enhanced_features(all_race_data, race_weekend_name)
            all_race_data = engineer_interaction_features(all_race_data)
        
        # Enhanced feature set
        feature_columns = [
            'Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 
            'Driver Points', 'Constructor Points',
            'pace_consistency', 'qualifying_improvement', 'team_form',
            'grid_advantage', 'championship_advantage',
            'is_wet_conditions', 'temperature',
            'track_overtaking_difficulty', 'track_power_sensitivity',
            'track_downforce_sensitivity', 'track_tire_degradation_level',
            'quali_points_interaction', 'team_track_fit', 'wet_weather_skill'
        ]
        
        # Filter to available columns
        available_columns = [col for col in feature_columns if col in all_race_data.columns]
        self.feature_columns = available_columns
        
        return all_race_data, available_columns
    
    def build_neural_network(self, input_dim):
        """Build an improved neural network architecture"""
        model = Sequential([
            Dense(128, input_dim=input_dim, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.4),
            
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            Dropout(0.2),
            
            Dense(32, activation='relu'),
            Dense(1, activation='linear')
        ])
        
        # Use adaptive learning rate
        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        return model
    
    def train_ensemble_model(self, data_list, race_weekend_name=None):
        """Train an ensemble of models for better predictions"""
        
        all_race_data, feature_columns = self.prepare_features(data_list, race_weekend_name)
        
        # Prepare features and target
        X = all_race_data[feature_columns]
        y = all_race_data['Race Finish Position']
        
        # Handle missing values more robustly
        X = X.fillna(X.median())
        
        # Use RobustScaler for better handling of outliers
        self.scaler = RobustScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=None
        )
        
        # Train Neural Network
        self.neural_network = self.build_neural_network(X_train.shape[1])
        
        # Callbacks for better training
        early_stopping = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=0.0001)
        
        history = self.neural_network.fit(
            X_train, y_train,
            epochs=200,
            batch_size=16,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping, reduce_lr],
            verbose=0
        )
        
        # Train Random Forest
        self.random_forest = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.random_forest.fit(X_train, y_train)
        
        # Train Gradient Boosting
        self.gradient_boost = GradientBoostingRegressor(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
        self.gradient_boost.fit(X_train, y_train)
        
        # Evaluate models
        self.evaluate_models(X_test, y_test)
        
        return self
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all models and print metrics"""
        
        # Neural Network predictions
        nn_pred = self.neural_network.predict(X_test, verbose=0).flatten()
        
        # Random Forest predictions
        rf_pred = self.random_forest.predict(X_test)
        
        # Gradient Boosting predictions
        gb_pred = self.gradient_boost.predict(X_test)
        
        # Ensemble prediction (weighted average)
        ensemble_pred = (0.4 * nn_pred + 0.3 * rf_pred + 0.3 * gb_pred)
        
        print("Model Evaluation Results:")
        print("-" * 50)
        
        for name, predictions in [
            ("Neural Network", nn_pred),
            ("Random Forest", rf_pred),
            ("Gradient Boosting", gb_pred),
            ("Ensemble", ensemble_pred)
        ]:
            mae = mean_absolute_error(y_test, predictions)
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            
            print(f"{name}:")
            print(f"  MAE: {mae:.3f}")
            print(f"  MSE: {mse:.3f}")
            print(f"  R²:  {r2:.3f}")
            print()
    
    def predict_top_5_enhanced(self, current_race_data, race_weekend_name):
        """Enhanced prediction with ensemble and confidence scores"""
        
        # Add enhanced features
        enhanced_data = add_enhanced_features(current_race_data.copy(), race_weekend_name)
        enhanced_data = engineer_interaction_features(enhanced_data)
        
        # Prepare features
        X = enhanced_data[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from all models
        nn_pred = self.neural_network.predict(X_scaled, verbose=0).flatten()
        rf_pred = self.random_forest.predict(X_scaled)
        gb_pred = self.gradient_boost.predict(X_scaled)
        
        # Ensemble prediction with confidence
        ensemble_pred = (0.4 * nn_pred + 0.3 * rf_pred + 0.3 * gb_pred)
        
        # Calculate prediction variance as confidence measure
        pred_variance = np.var([nn_pred, rf_pred, gb_pred], axis=0)
        confidence = 1 / (1 + pred_variance)  # Higher variance = lower confidence
        
        # Create results dataframe
        results_df = pd.DataFrame({
            'Driver': enhanced_data.index,
            'Predicted_Position': ensemble_pred,
            'Confidence': confidence,
            'Constructor': enhanced_data['Constructor']
        })
        
        # Sort by predicted position and get top 5
        top_5 = results_df.nsmallest(5, 'Predicted_Position')
        
        return top_5
    
    def save_model(self, filepath):
        """Save the trained ensemble model"""
        model_data = {
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'random_forest': self.random_forest,
            'gradient_boost': self.gradient_boost
        }
        
        # Save sklearn models and scaler
        joblib.dump(model_data, f"{filepath}_ensemble.pkl")
        
        # Save neural network separately
        self.neural_network.save(f"{filepath}_neural_network.h5")
        
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a pre-trained ensemble model"""
        # Load sklearn models and scaler
        model_data = joblib.load(f"{filepath}_ensemble.pkl")
        
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.random_forest = model_data['random_forest']
        self.gradient_boost = model_data['gradient_boost']
        
        # Load neural network
        self.neural_network = tf.keras.models.load_model(f"{filepath}_neural_network.h5")
        
        print(f"Model loaded from {filepath}")
        return self 