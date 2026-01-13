#!/usr/bin/env python3
"""
RIAM AI Music Coach - Audio Analysis with AWS Bedrock

This script analyzes music performances by extracting detailed audio features
using Librosa and providing expert coaching feedback via Claude.

Features analyzed:
- Tempo stability and rhythm accuracy
- Pitch/intonation analysis
- Dynamic control and expression
- Tone quality and timbre
- Articulation patterns
- Phrasing and musical structure
"""

import boto3
import json
import librosa
import numpy as np
from pathlib import Path
from scipy import stats
from typing import Optional

# AWS Configuration
AWS_PROFILE = "hackaton"
AWS_REGION = "us-west-2"
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"


def extract_comprehensive_features(audio_file_path: str) -> dict:
    """
    Extract comprehensive musical features for performance analysis.
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        dict: Comprehensive audio features for coaching feedback
    """
    print(f"🎵 Loading audio file: {audio_file_path}")
    
    # Load audio file
    y, sr = librosa.load(audio_file_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    
    print(f"✅ Audio loaded: {duration:.2f} seconds, sample rate: {sr} Hz")
    print("🔍 Extracting comprehensive features...")
    
    features = {
        "basic_info": {},
        "tempo_rhythm": {},
        "pitch_intonation": {},
        "dynamics": {},
        "tone_quality": {},
        "articulation": {},
        "musical_structure": {},
        "advanced_metrics": {}
    }
    
    # ========== BASIC INFO ==========
    features["basic_info"] = {
        "duration_seconds": float(duration),
        "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}",
        "sample_rate": int(sr),
        "total_samples": len(y)
    }
    
    # ========== TEMPO & RHYTHM ANALYSIS ==========
    print("  → Analyzing tempo and rhythm...")
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # Handle different return types from librosa (numpy array, scalar, etc.)
    tempo_value = float(np.atleast_1d(tempo)[0])
    
    # Beat timing analysis for tempo stability
    beat_times = librosa.frames_to_time(beats, sr=sr)
    if len(beat_times) > 1:
        beat_intervals = np.diff(beat_times)
        tempo_stability = 1.0 - (np.std(beat_intervals) / np.mean(beat_intervals)) if np.mean(beat_intervals) > 0 else 0
        tempo_variation_percent = (np.std(beat_intervals) / np.mean(beat_intervals)) * 100 if np.mean(beat_intervals) > 0 else 0
    else:
        tempo_stability = 0
        tempo_variation_percent = 0
    
    # Onset detection for rhythm accuracy
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onsets = librosa.onset.onset_detect(y=y, sr=sr, onset_envelope=onset_env)
    onset_times = librosa.frames_to_time(onsets, sr=sr)
    
    # Rhythm regularity analysis
    if len(onset_times) > 2:
        onset_intervals = np.diff(onset_times)
        rhythm_regularity = 1.0 - min(1.0, np.std(onset_intervals) / (np.mean(onset_intervals) + 0.001))
    else:
        rhythm_regularity = 0
    
    features["tempo_rhythm"] = {
        "tempo_bpm": tempo_value,
        "tempo_category": categorize_tempo(tempo_value),
        "tempo_stability_score": float(tempo_stability),  # 0-1, higher is more stable
        "tempo_variation_percent": float(tempo_variation_percent),
        "beat_count": len(beats),
        "onset_count": len(onsets),
        "rhythm_regularity_score": float(rhythm_regularity),  # 0-1, higher is more regular
        "notes_per_second": len(onsets) / duration if duration > 0 else 0
    }
    
    # ========== PITCH & INTONATION ANALYSIS ==========
    print("  → Analyzing pitch and intonation...")
    
    # Extract pitch using piptrack
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # Get the most prominent pitch at each frame
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    
    pitch_values = np.array(pitch_values)
    
    # Pitch stability analysis
    if len(pitch_values) > 10:
        pitch_stability = 1.0 - min(1.0, np.std(pitch_values) / (np.mean(pitch_values) + 0.001))
        pitch_range_hz = float(np.max(pitch_values) - np.min(pitch_values))
        pitch_range_semitones = 12 * np.log2(np.max(pitch_values) / np.min(pitch_values)) if np.min(pitch_values) > 0 else 0
    else:
        pitch_stability = 0
        pitch_range_hz = 0
        pitch_range_semitones = 0
    
    # Chroma features for key estimation
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    estimated_key = key_names[np.argmax(chroma_mean)]
    key_confidence = float(np.max(chroma_mean) / np.sum(chroma_mean)) if np.sum(chroma_mean) > 0 else 0
    
    # Harmonic content analysis
    harmonic, percussive = librosa.effects.hpss(y)
    harmonic_ratio = np.sum(np.abs(harmonic)) / (np.sum(np.abs(y)) + 0.001)
    
    features["pitch_intonation"] = {
        "estimated_key": estimated_key,
        "key_confidence": key_confidence,
        "pitch_stability_score": float(pitch_stability),
        "pitch_range_semitones": float(pitch_range_semitones),
        "average_pitch_hz": float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0,
        "harmonic_content_ratio": float(harmonic_ratio),
        "chroma_distribution": {key: float(val) for key, val in zip(key_names, chroma_mean)},
    }
    
    # ========== DYNAMICS ANALYSIS ==========
    print("  → Analyzing dynamics...")
    
    # RMS energy for dynamics
    rms = librosa.feature.rms(y=y)[0]
    rms_db = librosa.amplitude_to_db(rms + 0.0001)
    
    # Dynamic range and control
    dynamic_range_db = float(np.max(rms_db) - np.min(rms_db))
    
    # Segment the piece to analyze dynamic variation over time
    num_segments = min(10, len(rms) // 10)
    if num_segments > 1:
        segment_size = len(rms) // num_segments
        segment_dynamics = [np.mean(rms[i*segment_size:(i+1)*segment_size]) for i in range(num_segments)]
        dynamic_contrast = np.std(segment_dynamics) / (np.mean(segment_dynamics) + 0.001)
    else:
        dynamic_contrast = 0
    
    # Crescendo/Decrescendo detection
    rms_diff = np.diff(rms_db)
    crescendo_frames = np.sum(rms_diff > 0.5)
    decrescendo_frames = np.sum(rms_diff < -0.5)
    
    features["dynamics"] = {
        "dynamic_range_db": dynamic_range_db,
        "dynamic_range_category": categorize_dynamic_range(dynamic_range_db),
        "average_loudness_db": float(np.mean(rms_db)),
        "loudness_variation": float(np.std(rms_db)),
        "dynamic_contrast_score": float(min(1.0, dynamic_contrast)),
        "crescendo_presence": float(crescendo_frames / len(rms_diff)) if len(rms_diff) > 0 else 0,
        "decrescendo_presence": float(decrescendo_frames / len(rms_diff)) if len(rms_diff) > 0 else 0,
        "dynamic_expressiveness": categorize_dynamic_expressiveness(dynamic_range_db, float(dynamic_contrast))
    }
    
    # ========== TONE QUALITY & TIMBRE ==========
    print("  → Analyzing tone quality...")
    
    # Spectral features for timbre
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]
    
    # MFCCs for timbral texture
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    # Zero crossing rate (relates to noisiness/brightness)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    
    features["tone_quality"] = {
        "brightness_score": float(np.mean(spectral_centroids) / sr),  # Normalized 0-1
        "brightness_hz": float(np.mean(spectral_centroids)),
        "brightness_consistency": float(1.0 - min(1.0, np.std(spectral_centroids) / (np.mean(spectral_centroids) + 1))),
        "tone_warmth": float(1.0 - np.mean(spectral_centroids) / sr),  # Inverse of brightness
        "spectral_bandwidth_avg": float(np.mean(spectral_bandwidth)),
        "spectral_rolloff_avg": float(np.mean(spectral_rolloff)),
        "spectral_flatness_avg": float(np.mean(spectral_flatness)),
        "tonal_vs_noisy": "tonal" if np.mean(spectral_flatness) < 0.1 else "noisy",
        "zero_crossing_rate": float(np.mean(zcr)),
        "mfcc_means": [float(x) for x in np.mean(mfccs, axis=1)],
        "timbre_consistency": float(1.0 - min(1.0, np.mean(np.std(mfccs, axis=1)) / 10))
    }
    
    # ========== ARTICULATION ANALYSIS ==========
    print("  → Analyzing articulation...")
    
    # Onset strength for attack analysis
    onset_strengths = onset_env[onsets] if len(onsets) > 0 else np.array([0])
    
    # Attack time estimation
    attack_sharpness = float(np.mean(onset_strengths)) if len(onset_strengths) > 0 else 0
    
    # Note separation analysis
    if len(onset_times) > 1:
        note_gaps = np.diff(onset_times)
        legato_score = 1.0 - min(1.0, np.std(note_gaps) / (np.mean(note_gaps) + 0.001))
        staccato_tendency = float(np.sum(note_gaps < 0.1) / len(note_gaps))
        legato_tendency = float(np.sum(note_gaps > 0.3) / len(note_gaps))
    else:
        legato_score = 0
        staccato_tendency = 0
        legato_tendency = 0
    
    features["articulation"] = {
        "attack_clarity_score": float(min(1.0, attack_sharpness / 10)),
        "note_separation_consistency": float(legato_score),
        "staccato_tendency": staccato_tendency,
        "legato_tendency": legato_tendency,
        "articulation_variety": float(abs(staccato_tendency - legato_tendency)),
        "predominant_articulation": "staccato" if staccato_tendency > legato_tendency else "legato" if legato_tendency > staccato_tendency else "mixed"
    }
    
    # ========== MUSICAL STRUCTURE ==========
    print("  → Analyzing musical structure...")
    
    # Segment the piece for structural analysis
    # Use spectral clustering for structure
    mfcc_sync = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    # Self-similarity matrix
    similarity = librosa.segment.recurrence_matrix(mfcc_sync, mode='affinity', sym=True)
    
    # Estimate number of distinct sections using spectral flux as novelty
    spectral_flux = np.sqrt(np.sum(np.diff(mfcc_sync, axis=1)**2, axis=0))
    # Normalize and find peaks
    if len(spectral_flux) > 20:
        spectral_flux_norm = (spectral_flux - np.min(spectral_flux)) / (np.max(spectral_flux) - np.min(spectral_flux) + 0.001)
        peaks = librosa.util.peak_pick(spectral_flux_norm, pre_max=5, post_max=5, pre_avg=5, post_avg=5, delta=0.3, wait=10)
    else:
        peaks = np.array([])
    
    features["musical_structure"] = {
        "estimated_sections": len(peaks) + 1,
        "structural_repetition": float(np.mean(similarity)),
        "musical_development_score": float(1.0 - np.mean(similarity)),  # Higher = more varied
        "section_boundaries_seconds": [float(librosa.frames_to_time(p, sr=sr)) for p in peaks[:10]]  # First 10 boundaries
    }
    
    # ========== ADVANCED METRICS ==========
    print("  → Computing advanced metrics...")
    
    # Overall performance scores
    technical_score = np.mean([
        features["tempo_rhythm"]["tempo_stability_score"],
        features["pitch_intonation"]["pitch_stability_score"],
        features["articulation"]["attack_clarity_score"],
        features["articulation"]["note_separation_consistency"]
    ])
    
    expressiveness_score = np.mean([
        features["dynamics"]["dynamic_contrast_score"],
        min(1.0, features["dynamics"]["dynamic_range_db"] / 40),
        features["tone_quality"]["brightness_consistency"],
        features["musical_structure"]["musical_development_score"]
    ])
    
    features["advanced_metrics"] = {
        "technical_proficiency_score": float(technical_score),
        "expressiveness_score": float(expressiveness_score),
        "overall_performance_score": float((technical_score + expressiveness_score) / 2),
        "difficulty_estimate": estimate_difficulty(features),
        "performance_level": categorize_performance_level(float(technical_score), float(expressiveness_score))
    }
    
    print("✅ Feature extraction complete!")
    return features


def categorize_tempo(tempo: float) -> str:
    """Categorize tempo into musical terms."""
    if tempo < 40:
        return "Grave (very slow)"
    elif tempo < 60:
        return "Largo (slow)"
    elif tempo < 66:
        return "Larghetto (rather slow)"
    elif tempo < 76:
        return "Adagio (slow, expressive)"
    elif tempo < 108:
        return "Andante (walking pace)"
    elif tempo < 120:
        return "Moderato (moderate)"
    elif tempo < 156:
        return "Allegro (fast, bright)"
    elif tempo < 176:
        return "Vivace (lively)"
    elif tempo < 200:
        return "Presto (very fast)"
    else:
        return "Prestissimo (extremely fast)"


def categorize_dynamic_range(dynamic_range_db: float) -> str:
    """Categorize dynamic range."""
    if dynamic_range_db < 10:
        return "Limited (pp-p range)"
    elif dynamic_range_db < 20:
        return "Moderate (p-mf range)"
    elif dynamic_range_db < 35:
        return "Good (p-f range)"
    elif dynamic_range_db < 50:
        return "Excellent (pp-ff range)"
    else:
        return "Exceptional (ppp-fff range)"


def categorize_dynamic_expressiveness(dynamic_range: float, contrast: float) -> str:
    """Categorize dynamic expressiveness."""
    score = (dynamic_range / 50) * 0.5 + contrast * 0.5
    if score < 0.2:
        return "Flat/monotonous"
    elif score < 0.4:
        return "Limited expression"
    elif score < 0.6:
        return "Moderate expression"
    elif score < 0.8:
        return "Good expression"
    else:
        return "Highly expressive"


def estimate_difficulty(features: dict) -> str:
    """Estimate piece difficulty based on features."""
    tempo = features["tempo_rhythm"]["tempo_bpm"]
    notes_per_sec = features["tempo_rhythm"]["notes_per_second"]
    pitch_range = features["pitch_intonation"]["pitch_range_semitones"]
    
    difficulty_score = 0
    
    # Tempo factor
    if tempo > 140:
        difficulty_score += 2
    elif tempo > 100:
        difficulty_score += 1
    
    # Note density factor
    if notes_per_sec > 8:
        difficulty_score += 3
    elif notes_per_sec > 5:
        difficulty_score += 2
    elif notes_per_sec > 3:
        difficulty_score += 1
    
    # Pitch range factor
    if pitch_range > 36:  # 3 octaves
        difficulty_score += 2
    elif pitch_range > 24:  # 2 octaves
        difficulty_score += 1
    
    if difficulty_score <= 2:
        return "Beginner (Grade 1-2)"
    elif difficulty_score <= 4:
        return "Intermediate (Grade 3-5)"
    elif difficulty_score <= 6:
        return "Advanced (Grade 6-8)"
    else:
        return "Professional/Diploma"


def categorize_performance_level(technical: float, expressive: float) -> str:
    """Categorize overall performance level."""
    avg = (technical + expressive) / 2
    if avg < 0.3:
        return "Developing"
    elif avg < 0.5:
        return "Intermediate"
    elif avg < 0.7:
        return "Proficient"
    elif avg < 0.85:
        return "Advanced"
    else:
        return "Expert"


def generate_coaching_feedback(features: dict, audio_file_name: str, profile: str = AWS_PROFILE) -> str:
    """
    Generate comprehensive music coaching feedback using Claude.
    
    Args:
        features: Comprehensive extracted audio features
        audio_file_name: Name of the audio file
        profile: AWS profile name
        
    Returns:
        str: Detailed coaching feedback
    """
    session = boto3.Session(profile_name=profile, region_name=AWS_REGION)
    bedrock = session.client('bedrock-runtime')
    
    # Create detailed coaching prompt
    prompt = f"""You are a master music teacher at the Royal Irish Academy of Music (RIAM) with decades of experience coaching instrumentalists. A student has submitted a practice recording for your expert feedback.

## Audio Analysis Results for "{audio_file_name}"

### Basic Information
- Duration: {features['basic_info']['duration_formatted']} ({features['basic_info']['duration_seconds']:.1f} seconds)

### Tempo & Rhythm Analysis
- Tempo: {features['tempo_rhythm']['tempo_bpm']:.1f} BPM ({features['tempo_rhythm']['tempo_category']})
- Tempo Stability Score: {features['tempo_rhythm']['tempo_stability_score']:.2f}/1.00 (higher = more stable)
- Tempo Variation: {features['tempo_rhythm']['tempo_variation_percent']:.1f}%
- Rhythm Regularity Score: {features['tempo_rhythm']['rhythm_regularity_score']:.2f}/1.00
- Note Density: {features['tempo_rhythm']['notes_per_second']:.1f} notes/second

### Pitch & Intonation Analysis
- Estimated Key: {features['pitch_intonation']['estimated_key']} (confidence: {features['pitch_intonation']['key_confidence']:.1%})
- Pitch Stability Score: {features['pitch_intonation']['pitch_stability_score']:.2f}/1.00
- Pitch Range: {features['pitch_intonation']['pitch_range_semitones']:.1f} semitones
- Harmonic Content: {features['pitch_intonation']['harmonic_content_ratio']:.1%}

### Dynamics Analysis
- Dynamic Range: {features['dynamics']['dynamic_range_db']:.1f} dB ({features['dynamics']['dynamic_range_category']})
- Average Loudness: {features['dynamics']['average_loudness_db']:.1f} dB
- Dynamic Contrast Score: {features['dynamics']['dynamic_contrast_score']:.2f}/1.00
- Expressiveness: {features['dynamics']['dynamic_expressiveness']}
- Crescendo Presence: {features['dynamics']['crescendo_presence']:.1%}
- Decrescendo Presence: {features['dynamics']['decrescendo_presence']:.1%}

### Tone Quality Analysis
- Brightness Score: {features['tone_quality']['brightness_score']:.2f}/1.00
- Tone Warmth: {features['tone_quality']['tone_warmth']:.2f}/1.00
- Brightness Consistency: {features['tone_quality']['brightness_consistency']:.2f}/1.00
- Timbre Consistency: {features['tone_quality']['timbre_consistency']:.2f}/1.00
- Tone Character: {features['tone_quality']['tonal_vs_noisy']}

### Articulation Analysis
- Attack Clarity Score: {features['articulation']['attack_clarity_score']:.2f}/1.00
- Note Separation Consistency: {features['articulation']['note_separation_consistency']:.2f}/1.00
- Predominant Articulation: {features['articulation']['predominant_articulation']}
- Staccato Tendency: {features['articulation']['staccato_tendency']:.1%}
- Legato Tendency: {features['articulation']['legato_tendency']:.1%}

### Musical Structure
- Estimated Sections: {features['musical_structure']['estimated_sections']}
- Musical Development Score: {features['musical_structure']['musical_development_score']:.2f}/1.00

### Overall Performance Metrics
- Technical Proficiency Score: {features['advanced_metrics']['technical_proficiency_score']:.2f}/1.00
- Expressiveness Score: {features['advanced_metrics']['expressiveness_score']:.2f}/1.00
- Overall Performance Score: {features['advanced_metrics']['overall_performance_score']:.2f}/1.00
- Estimated Difficulty Level: {features['advanced_metrics']['difficulty_estimate']}
- Performance Level: {features['advanced_metrics']['performance_level']}

---

Based on these detailed audio analysis metrics, please provide comprehensive coaching feedback as an experienced RIAM music teacher. Your feedback should include:

## 1. Overall Performance Assessment
Provide an honest, constructive assessment of the overall performance based on the metrics. What does the data tell you about this student's playing?

## 2. Technical Analysis & Feedback

### Rhythm & Tempo
- Analyze the tempo stability ({features['tempo_rhythm']['tempo_stability_score']:.2f}) and rhythm regularity ({features['tempo_rhythm']['rhythm_regularity_score']:.2f})
- What do these scores indicate about the student's rhythmic control?
- Specific exercises to improve rhythm if needed

### Intonation & Pitch Control  
- Analyze the pitch stability ({features['pitch_intonation']['pitch_stability_score']:.2f})
- What does the harmonic content ({features['pitch_intonation']['harmonic_content_ratio']:.1%}) suggest about tone production?
- Suggestions for improving intonation

### Tone Quality
- Analyze brightness ({features['tone_quality']['brightness_score']:.2f}) and warmth ({features['tone_quality']['tone_warmth']:.2f})
- Comment on timbre consistency ({features['tone_quality']['timbre_consistency']:.2f})
- Exercises for tone development

### Articulation
- Analyze the articulation patterns (attack clarity: {features['articulation']['attack_clarity_score']:.2f})
- Comment on the {features['articulation']['predominant_articulation']} tendency
- How to develop more varied articulation

## 3. Musical Expression & Interpretation
- Analyze dynamic control (range: {features['dynamics']['dynamic_range_db']:.1f} dB, contrast: {features['dynamics']['dynamic_contrast_score']:.2f})
- Comment on expressiveness: {features['dynamics']['dynamic_expressiveness']}
- How to develop greater musical expression

## 4. Strengths to Build On
List 3-4 specific strengths evident from the analysis metrics that the student should continue to develop.

## 5. Priority Areas for Improvement
List 3-4 specific areas that need the most attention, based on the lowest scores in the analysis.

## 6. Practice Plan (2-4 weeks)
Create a structured practice plan targeting the areas identified for improvement:
- Week 1-2: Focus areas and specific exercises
- Week 3-4: Integration and refinement
- Daily practice routine suggestions (30-60 min breakdown)

## 7. Recommended Repertoire for Development
Based on the performance level ({features['advanced_metrics']['performance_level']}) and the areas needing work, suggest:
- 2-3 études or technical studies that address the weak areas
- 2-3 pieces at an appropriate level that would help develop the skills needed
- For each recommendation, explain WHY it would help this student

## 8. Technical Exercises
Provide 3-5 specific technical exercises with detailed instructions:
- For rhythm improvement (if tempo stability < 0.7)
- For intonation (if pitch stability < 0.7)  
- For dynamics (if dynamic contrast < 0.5)
- For articulation variety
- For tone development

## 9. Encouragement & Next Steps
End with specific, genuine encouragement based on the strengths observed, and clear next steps for the student.

---

Be specific, practical, and reference the actual metrics in your feedback. Adjust your tone and recommendations to match the performance level: {features['advanced_metrics']['performance_level']}.
"""

    messages = [{"role": "user", "content": [{"text": prompt}]}]
    
    try:
        print("🤖 Generating coaching feedback with Claude...")
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": 6000,
                "temperature": 0.7,
            }
        )
        
        return response['output']['message']['content'][0]['text']
        
    except Exception as e:
        print(f"❌ Error calling Bedrock: {e}")
        raise


def main():
    """Main function for music coaching analysis."""
    
    audio_file = "input.mp3"
    
    print("=" * 80)
    print("🎵 RIAM AI MUSIC COACH - Performance Analysis")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Extract comprehensive audio features
        features = extract_comprehensive_features(audio_file)
        
        # Step 2: Display summary
        print("\n" + "=" * 80)
        print("📊 PERFORMANCE METRICS SUMMARY")
        print("=" * 80)
        print(f"\n📁 File: {audio_file}")
        print(f"⏱️  Duration: {features['basic_info']['duration_formatted']}")
        print(f"🎼 Tempo: {features['tempo_rhythm']['tempo_bpm']:.0f} BPM ({features['tempo_rhythm']['tempo_category']})")
        print(f"🎹 Key: {features['pitch_intonation']['estimated_key']}")
        print(f"📈 Dynamic Range: {features['dynamics']['dynamic_range_db']:.1f} dB")
        print()
        print("Performance Scores:")
        print(f"  • Technical Proficiency: {features['advanced_metrics']['technical_proficiency_score']:.0%}")
        print(f"  • Expressiveness: {features['advanced_metrics']['expressiveness_score']:.0%}")
        print(f"  • Overall Score: {features['advanced_metrics']['overall_performance_score']:.0%}")
        print(f"  • Level: {features['advanced_metrics']['performance_level']}")
        print(f"  • Piece Difficulty: {features['advanced_metrics']['difficulty_estimate']}")
        
        # Step 3: Generate coaching feedback
        print("\n" + "=" * 80)
        print("🎓 AI MUSIC COACH FEEDBACK")
        print("=" * 80)
        print()
        
        feedback = generate_coaching_feedback(features, audio_file)
        print(feedback)
        
        # Step 4: Save results
        print("\n" + "=" * 80)
        
        output_file = Path(audio_file).stem + "_coaching_report.json"
        results = {
            "audio_file": audio_file,
            "features": features,
            "coaching_feedback": feedback
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Full report saved to: {output_file}")
        
        # Also save markdown version
        md_output = Path(audio_file).stem + "_coaching_report.md"
        with open(md_output, 'w') as f:
            f.write(f"# RIAM AI Music Coach Report\n\n")
            f.write(f"**Audio File:** {audio_file}\n")
            f.write(f"**Duration:** {features['basic_info']['duration_formatted']}\n")
            f.write(f"**Performance Level:** {features['advanced_metrics']['performance_level']}\n")
            f.write(f"**Overall Score:** {features['advanced_metrics']['overall_performance_score']:.0%}\n\n")
            f.write("---\n\n")
            f.write(feedback)
        
        print(f"📄 Markdown report saved to: {md_output}")
        print("\n" + "=" * 80)
        
    except FileNotFoundError:
        print(f"❌ Error: Audio file '{audio_file}' not found.")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        raise


if __name__ == "__main__":
    main()
