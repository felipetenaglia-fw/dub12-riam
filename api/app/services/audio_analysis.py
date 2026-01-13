"""
Audio Analysis Service - Extracts musical features from audio files using Librosa.

This service provides comprehensive audio feature extraction for music coaching,
including tempo, pitch, dynamics, tone quality, articulation, and structure analysis.
"""

import io
import librosa
import numpy as np
from typing import Optional


class AudioAnalysisService:
    """Service for extracting musical features from audio files."""
    
    def extract_features(self, audio_data: bytes, audio_format: str = "mp3") -> dict:
        """
        Extract comprehensive musical features from audio data.
        
        Args:
            audio_data: Raw audio file bytes
            audio_format: Audio file format (mp3, wav, etc.)
            
        Returns:
            dict: Comprehensive audio features for coaching feedback
        """
        print(f"🎵 Analyzing audio ({len(audio_data) / 1024 / 1024:.2f} MB)...")
        
        # Load audio from bytes
        audio_buffer = io.BytesIO(audio_data)
        y, sr = librosa.load(audio_buffer, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        print(f"✅ Audio loaded: {duration:.2f} seconds, sample rate: {sr} Hz")
        
        features = {
            "basic_info": {},
            "tempo_rhythm": {},
            "pitch_intonation": {},
            "dynamics": {},
            "tone_quality": {},
            "articulation": {},
            "musical_structure": {},
            "performance_scores": {}
        }
        
        # ========== BASIC INFO ==========
        features["basic_info"] = {
            "duration_seconds": float(duration),
            "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}",
            "sample_rate": int(sr),
            "file_size_mb": len(audio_data) / 1024 / 1024
        }
        
        # ========== TEMPO & RHYTHM ANALYSIS ==========
        print("  → Analyzing tempo and rhythm...")
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        tempo_value = float(np.atleast_1d(tempo)[0])
        
        # Beat timing analysis for tempo stability
        beat_times = librosa.frames_to_time(beats, sr=sr)
        if len(beat_times) > 1:
            beat_intervals = np.diff(beat_times)
            tempo_stability = 1.0 - (np.std(beat_intervals) / np.mean(beat_intervals)) if np.mean(beat_intervals) > 0 else 0
            tempo_variation_percent = (np.std(beat_intervals) / np.mean(beat_intervals)) * 100 if np.mean(beat_intervals) > 0 else 0
        else:
            tempo_stability = 0.5
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
            rhythm_regularity = 0.5
        
        features["tempo_rhythm"] = {
            "tempo_bpm": tempo_value,
            "tempo_category": self._categorize_tempo(tempo_value),
            "tempo_stability_score": float(max(0, min(1, tempo_stability))),
            "tempo_variation_percent": float(tempo_variation_percent),
            "beat_count": len(beats),
            "onset_count": len(onsets),
            "rhythm_regularity_score": float(max(0, min(1, rhythm_regularity))),
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
            pitch_range_semitones = 12 * np.log2(np.max(pitch_values) / np.min(pitch_values)) if np.min(pitch_values) > 0 else 0
        else:
            pitch_stability = 0.5
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
            "key_confidence": float(key_confidence),
            "pitch_stability_score": float(max(0, min(1, pitch_stability))),
            "pitch_range_semitones": float(pitch_range_semitones),
            "average_pitch_hz": float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0,
            "harmonic_content_ratio": float(harmonic_ratio),
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
            "dynamic_range_category": self._categorize_dynamic_range(dynamic_range_db),
            "average_loudness_db": float(np.mean(rms_db)),
            "loudness_variation": float(np.std(rms_db)),
            "dynamic_contrast_score": float(min(1.0, dynamic_contrast)),
            "crescendo_presence": float(crescendo_frames / len(rms_diff)) if len(rms_diff) > 0 else 0,
            "decrescendo_presence": float(decrescendo_frames / len(rms_diff)) if len(rms_diff) > 0 else 0,
            "dynamic_expressiveness": self._categorize_dynamic_expressiveness(dynamic_range_db, float(dynamic_contrast))
        }
        
        # ========== TONE QUALITY & TIMBRE ==========
        print("  → Analyzing tone quality...")
        
        # Spectral features for timbre
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]
        
        # MFCCs for timbral texture
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        
        brightness_score = float(np.mean(spectral_centroids) / sr)
        
        features["tone_quality"] = {
            "brightness_score": brightness_score,
            "brightness_hz": float(np.mean(spectral_centroids)),
            "brightness_consistency": float(1.0 - min(1.0, np.std(spectral_centroids) / (np.mean(spectral_centroids) + 1))),
            "tone_warmth": float(1.0 - brightness_score),
            "spectral_flatness_avg": float(np.mean(spectral_flatness)),
            "tonal_vs_noisy": "tonal" if np.mean(spectral_flatness) < 0.1 else "mixed" if np.mean(spectral_flatness) < 0.3 else "noisy",
            "zero_crossing_rate": float(np.mean(zcr)),
            "timbre_consistency": float(1.0 - min(1.0, np.mean(np.std(mfccs, axis=1)) / 10))
        }
        
        # ========== ARTICULATION ANALYSIS ==========
        print("  → Analyzing articulation...")
        
        # Onset strength for attack analysis
        onset_strengths = onset_env[onsets] if len(onsets) > 0 else np.array([0])
        attack_sharpness = float(np.mean(onset_strengths)) if len(onset_strengths) > 0 else 0
        
        # Note separation analysis
        if len(onset_times) > 1:
            note_gaps = np.diff(onset_times)
            legato_score = 1.0 - min(1.0, np.std(note_gaps) / (np.mean(note_gaps) + 0.001))
            staccato_tendency = float(np.sum(note_gaps < 0.1) / len(note_gaps))
            legato_tendency = float(np.sum(note_gaps > 0.3) / len(note_gaps))
        else:
            legato_score = 0.5
            staccato_tendency = 0
            legato_tendency = 0
        
        features["articulation"] = {
            "attack_clarity_score": float(min(1.0, attack_sharpness / 10)),
            "note_separation_consistency": float(max(0, min(1, legato_score))),
            "staccato_tendency": staccato_tendency,
            "legato_tendency": legato_tendency,
            "articulation_variety": float(abs(staccato_tendency - legato_tendency)),
            "predominant_articulation": "staccato" if staccato_tendency > legato_tendency else "legato" if legato_tendency > staccato_tendency else "mixed"
        }
        
        # ========== MUSICAL STRUCTURE ==========
        print("  → Analyzing musical structure...")
        
        mfcc_sync = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Self-similarity matrix
        similarity = librosa.segment.recurrence_matrix(mfcc_sync, mode='affinity', sym=True)
        
        # Estimate sections using spectral flux
        spectral_flux = np.sqrt(np.sum(np.diff(mfcc_sync, axis=1)**2, axis=0))
        if len(spectral_flux) > 20:
            spectral_flux_norm = (spectral_flux - np.min(spectral_flux)) / (np.max(spectral_flux) - np.min(spectral_flux) + 0.001)
            peaks = librosa.util.peak_pick(spectral_flux_norm, pre_max=5, post_max=5, pre_avg=5, post_avg=5, delta=0.3, wait=10)
        else:
            peaks = np.array([])
        
        features["musical_structure"] = {
            "estimated_sections": len(peaks) + 1,
            "structural_repetition": float(np.mean(similarity)),
            "musical_development_score": float(1.0 - np.mean(similarity)),
        }
        
        # ========== PERFORMANCE SCORES ==========
        print("  → Computing performance scores...")
        
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
        
        features["performance_scores"] = {
            "technical_proficiency": float(technical_score),
            "expressiveness": float(expressiveness_score),
            "overall_score": float((technical_score + expressiveness_score) / 2),
            "difficulty_estimate": self._estimate_difficulty(features),
            "performance_level": self._categorize_performance_level(float(technical_score), float(expressiveness_score))
        }
        
        print("✅ Audio analysis complete!")
        return features
    
    def _categorize_tempo(self, tempo: float) -> str:
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
    
    def _categorize_dynamic_range(self, dynamic_range_db: float) -> str:
        """Categorize dynamic range."""
        if dynamic_range_db < 10:
            return "Limited (pp-p)"
        elif dynamic_range_db < 20:
            return "Moderate (p-mf)"
        elif dynamic_range_db < 35:
            return "Good (p-f)"
        elif dynamic_range_db < 50:
            return "Excellent (pp-ff)"
        else:
            return "Exceptional (ppp-fff)"
    
    def _categorize_dynamic_expressiveness(self, dynamic_range: float, contrast: float) -> str:
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
    
    def _estimate_difficulty(self, features: dict) -> str:
        """Estimate piece difficulty based on features."""
        tempo = features["tempo_rhythm"]["tempo_bpm"]
        notes_per_sec = features["tempo_rhythm"]["notes_per_second"]
        pitch_range = features["pitch_intonation"]["pitch_range_semitones"]
        
        difficulty_score = 0
        
        if tempo > 140:
            difficulty_score += 2
        elif tempo > 100:
            difficulty_score += 1
        
        if notes_per_sec > 8:
            difficulty_score += 3
        elif notes_per_sec > 5:
            difficulty_score += 2
        elif notes_per_sec > 3:
            difficulty_score += 1
        
        if pitch_range > 36:
            difficulty_score += 2
        elif pitch_range > 24:
            difficulty_score += 1
        
        if difficulty_score <= 2:
            return "Beginner (Grade 1-2)"
        elif difficulty_score <= 4:
            return "Intermediate (Grade 3-5)"
        elif difficulty_score <= 6:
            return "Advanced (Grade 6-8)"
        else:
            return "Professional/Diploma"
    
    def _categorize_performance_level(self, technical: float, expressive: float) -> str:
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


# Singleton instance
audio_analysis_service = AudioAnalysisService()
