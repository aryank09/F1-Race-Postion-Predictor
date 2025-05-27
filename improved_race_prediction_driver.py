#Description: Enhanced driver program with better UI and prediction explanations
#Author: Aryan Khanna  
#Version: Jan 16th, 2025

import race_prediction_calculator as data_collection
from improved_model import ImprovedF1Predictor
import pandas as pd
import sys
import os

def print_banner():
    """Print a nice banner for the application"""
    print("=" * 60)
    print("🏎️  F1 RACE POSITION PREDICTOR 🏁")
    print("   Advanced Machine Learning Race Prediction")
    print("=" * 60)
    print()

def validate_race_input(race_name):
    """Validate user input for race name"""
    valid_races = [
        "bahrain", "saudi-arabia", "australia", "japan", "emilia-romagna", 
        "monaco", "canada", "spain", "great-britain", "hungary", "belgium", 
        "netherlands", "italy", "azerbaijan", "singapore", "mexico", 
        "las-vegas", "abu-dhabi"
    ]
    
    race_normalized = race_name.lower().replace(" ", "-")
    
    if race_normalized not in valid_races:
        print(f"❌ Invalid race name: '{race_name}'")
        print("\n📅 Available races for 2024:")
        for i, race in enumerate(valid_races, 1):
            print(f"   {i:2d}. {race.replace('-', ' ').title()}")
        return False
    
    return race_normalized

def display_prediction_results(top_5_predictions, race_name):
    """Display prediction results in a nice format"""
    print(f"\n🏆 TOP 5 RACE WIN CONTENDERS - {race_name.replace('-', ' ').title()}")
    print("=" * 80)
    
    for i, (idx, row) in enumerate(top_5_predictions.iterrows(), 1):
        driver_name = row['Driver']
        predicted_pos = row['Predicted_Position']
        confidence = row['Confidence']
        constructor = row['Constructor']
        
        # Create confidence indicator
        if confidence > 0.8:
            conf_indicator = "🟢 Very High"
        elif confidence > 0.6:
            conf_indicator = "🟡 High"
        elif confidence > 0.4:
            conf_indicator = "🟠 Medium"
        else:
            conf_indicator = "🔴 Low"
        
        print(f"{i}. {driver_name}")
        print(f"   Team: {constructor}")
        print(f"   Predicted Position: {predicted_pos:.2f}")
        print(f"   Confidence: {conf_indicator} ({confidence:.1%})")
        print()

def display_feature_importance(predictor):
    """Display which features are most important for predictions"""
    try:
        # Get feature importance from Random Forest model
        if hasattr(predictor, 'random_forest') and predictor.random_forest:
            feature_importance = predictor.random_forest.feature_importances_
            feature_names = predictor.feature_columns
            
            # Create feature importance dataframe
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': feature_importance
            }).sort_values('Importance', ascending=False).head(10)
            
            print("📊 TOP 10 MOST IMPORTANT FACTORS:")
            print("-" * 50)
            for idx, row in importance_df.iterrows():
                feature_name = row['Feature'].replace('_', ' ').title()
                importance = row['Importance']
                bar_length = int(importance * 30)  # Scale for visual bar
                bar = "█" * bar_length + "░" * (30 - bar_length)
                print(f"{feature_name:<25} {bar} {importance:.3f}")
            print()
            
    except Exception as e:
        print(f"Could not display feature importance: {e}")

def main():
    try:
        print_banner()
        
        # Get race input with validation
        while True:
            race_name = input("🏁 Enter the race name (e.g., 'Monaco', 'Silverstone'): ").strip()
            
            if not race_name:
                print("❌ Please enter a race name.")
                continue
                
            validated_race = validate_race_input(race_name)
            if validated_race:
                race_name = validated_race
                break
        
        print(f"\n🔄 Loading data for {race_name.replace('-', ' ').title()}...")
        
        # Collect training data
        try:
            training_data = data_collection.data_compiler_new(race_name)
            current_data = data_collection.current_race_data(race_name)
            
            if not training_data:
                print("❌ No training data available for this race.")
                return
                
            print(f"✅ Successfully loaded {len(training_data)} races of training data")
            
        except Exception as e:
            print(f"❌ Error loading race data: {e}")
            return
        
        # Train the improved model
        print("\n🧠 Training advanced machine learning models...")
        print("   - Neural Network with batch normalization")
        print("   - Random Forest with 200 trees")
        print("   - Gradient Boosting")
        print("   - Ensemble combination")
        
        predictor = ImprovedF1Predictor()
        predictor.train_ensemble_model(training_data, race_name)
        
        # Make predictions
        print(f"\n🔮 Generating predictions for {race_name.replace('-', ' ').title()}...")
        top_5_predictions = predictor.predict_top_5_enhanced(current_data, race_name)
        
        # Display results
        display_prediction_results(top_5_predictions, race_name)
        
        # Show feature importance
        display_feature_importance(predictor)
        
        # Offer to save model
        save_model = input("💾 Would you like to save this trained model? (y/n): ").lower().strip()
        if save_model in ['y', 'yes']:
            model_name = f"f1_model_{race_name}"
            predictor.save_model(model_name)
            print(f"✅ Model saved as '{model_name}'")
        
        print("\n🏁 Prediction complete! Good luck with your F1 predictions! 🏎️")
        
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please check your input and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 