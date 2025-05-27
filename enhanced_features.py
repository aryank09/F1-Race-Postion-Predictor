import pandas as pd
import numpy as np
from weather_data_scraper import get_weather_data, get_track_characteristics

def calculate_pace_consistency(practice_times):
    """Calculate how consistent a driver's pace is across practice sessions"""
    times = [t for t in practice_times if t and t > 0]
    if len(times) < 2:
        return 0
    return 1 / (np.std(times) + 0.001)  # Higher = more consistent

def calculate_qualifying_improvement(practice_avg, qualifying_time):
    """How much faster qualifying time is compared to practice average"""
    if not practice_avg or not qualifying_time or practice_avg <= 0:
        return 0
    return (practice_avg - qualifying_time) / practice_avg

def get_historical_track_performance(driver_name, track_name, years_back=3):
    """Get driver's historical performance at this specific track"""
    # This would require historical data - simplified for now
    historical_performance = {
        'avg_finish_position': 10.0,
        'podium_rate': 0.1,
        'dnf_rate': 0.1,
        'points_per_race': 5.0
    }
    return historical_performance

def calculate_team_form(constructor_points, recent_races=5):
    """Calculate team's recent form (momentum)"""
    # This would require race-by-race constructor points
    # Simplified for now - higher points = better form
    if constructor_points > 400:
        return 0.9
    elif constructor_points > 200:
        return 0.7
    elif constructor_points > 100:
        return 0.5
    else:
        return 0.3

def add_enhanced_features(df, race_weekend_name):
    """Add advanced features to the existing dataframe"""
    
    # Weather and track data
    weather_data = get_weather_data(race_weekend_name)
    track_data = get_track_characteristics(race_weekend_name)
    
    # Add weather features
    df['is_wet_conditions'] = 1 if weather_data['practice_weather'] == 'wet' else 0
    df['temperature'] = weather_data['temperature_avg']
    
    # Add track characteristics
    for key, value in track_data.items():
        df[f'track_{key}'] = value
    
    # Calculate pace consistency
    df['pace_consistency'] = df.apply(
        lambda row: calculate_pace_consistency([
            row['Practice 1'], row['Practice 2'], row['Practice 3']
        ]), axis=1
    )
    
    # Calculate qualifying improvement
    df['qualifying_improvement'] = df.apply(
        lambda row: calculate_qualifying_improvement(
            np.mean([t for t in [row['Practice 1'], row['Practice 2'], row['Practice 3']] if t and t > 0]),
            row['Qualifying']
        ), axis=1
    )
    
    # Add team form
    df['team_form'] = df['Constructor Points'].apply(
        lambda points: calculate_team_form(points)
    )
    
    # Grid position advantage (lower qualifying position = advantage)
    df['grid_advantage'] = df['Qualifying'].apply(
        lambda pos: 1 / (pos + 1) if pos and pos > 0 else 0
    )
    
    # Driver championship position (based on points)
    df = df.sort_values('Driver Points', ascending=False).reset_index(drop=True)
    df['championship_position'] = range(1, len(df) + 1)
    df['championship_advantage'] = df['championship_position'].apply(
        lambda pos: 1 / pos if pos > 0 else 0
    )
    
    return df

def engineer_interaction_features(df):
    """Create interaction features between existing variables"""
    
    # Qualifying position vs driver points (good drivers starting high)
    df['quali_points_interaction'] = df['grid_advantage'] * df['championship_advantage']
    
    # Team performance vs track characteristics
    df['team_track_fit'] = df['team_form'] * df['track_power_sensitivity']
    
    # Weather vs driver skill (some drivers better in wet)
    df['wet_weather_skill'] = df['is_wet_conditions'] * df['championship_advantage']
    
    return df 