"""
Bedrock Service - AWS Bedrock integration for AI music coaching.

This service combines Librosa audio analysis with Claude AI to provide
comprehensive music coaching feedback based on actual performance metrics.
"""

import boto3
import json
from botocore.exceptions import ClientError
from typing import Optional

from ..config import get_settings
from .audio_analysis import audio_analysis_service

settings = get_settings()


class BedrockService:
    """Service for AWS Bedrock operations with Claude."""
    
    def __init__(self):
        """Initialize Bedrock client."""
        # Use profile for local development, credentials for production
        if hasattr(settings, 'aws_profile') and settings.aws_profile:
            session = boto3.Session(profile_name=settings.aws_profile, region_name=settings.aws_region)
            self.bedrock_runtime = session.client('bedrock-runtime')
        elif settings.aws_access_key_id:
            self.bedrock_runtime = boto3.client(
                'bedrock-runtime',
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        else:
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=settings.aws_region)
        
        # Use Claude 3.5 Sonnet v2
        self.model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    def analyze_audio_performance(
        self, 
        audio_data: bytes,
        audio_format: str = "mp3",
        piece_name: Optional[str] = None,
        composer: Optional[str] = None,
        student_notes: Optional[str] = None
    ) -> Optional[dict]:
        """
        Analyze a student's musical performance using Librosa audio analysis
        and Claude AI for comprehensive coaching feedback.
        
        Args:
            audio_data: Raw audio file bytes
            audio_format: Audio file format (mp3, wav, etc.)
            piece_name: Optional name of the piece (helps with context)
            composer: Optional composer name (helps with context)
            student_notes: Optional notes or questions from the student
            
        Returns:
            Dictionary with audio analysis and coaching feedback
        """
        try:
            file_size_mb = len(audio_data) / 1024 / 1024
            print(f"🎵 Processing {file_size_mb:.2f}MB {audio_format} file for AI coaching...")
            
            # Step 1: Extract audio features using Librosa
            try:
                features = audio_analysis_service.extract_features(audio_data, audio_format)
            except Exception as e:
                print(f"⚠️ Audio analysis error: {e}")
                # If audio analysis fails, provide text-based feedback
                return self._provide_text_only_feedback(
                    file_size_mb, audio_format, piece_name, composer, student_notes
                )
            
            # Step 2: Generate coaching feedback with Claude using the extracted features
            feedback = self._generate_coaching_feedback(
                features, piece_name, composer, student_notes
            )
            
            return {
                "success": True,
                "feedback": feedback,
                "audio_analysis": features,
                "model": self.model_id
            }
            
        except ClientError as e:
            print(f"Error calling Bedrock: {e}")
            return {
                "success": False,
                "error": str(e),
                "feedback": None
            }
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e),
                "feedback": None
            }
    
    def _generate_coaching_feedback(
        self,
        features: dict,
        piece_name: Optional[str] = None,
        composer: Optional[str] = None,
        student_notes: Optional[str] = None
    ) -> str:
        """Generate comprehensive coaching feedback using Claude based on audio analysis."""
        
        # Build context section
        context_parts = []
        if piece_name:
            context_parts.append(f"🎵 **Piece:** {piece_name}")
        if composer:
            context_parts.append(f"👤 **Composer:** {composer}")
        if student_notes:
            context_parts.append(f"💭 **Student's Notes:** {student_notes}")
        
        context = "\n".join(context_parts) if context_parts else "No additional context provided."
        
        # Create the coaching prompt with actual metrics
        prompt = f"""You are a master music teacher at the Royal Irish Academy of Music (RIAM) with decades of experience coaching instrumentalists. A student has submitted a practice recording which has been analyzed.

## Student Context
{context}

## Audio Analysis Results

### Basic Information
- **Duration:** {features['basic_info']['duration_formatted']} ({features['basic_info']['duration_seconds']:.1f} seconds)
- **File Size:** {features['basic_info']['file_size_mb']:.2f} MB

### Tempo & Rhythm Analysis
- **Tempo:** {features['tempo_rhythm']['tempo_bpm']:.1f} BPM ({features['tempo_rhythm']['tempo_category']})
- **Tempo Stability:** {features['tempo_rhythm']['tempo_stability_score']:.0%} (higher = more stable)
- **Tempo Variation:** {features['tempo_rhythm']['tempo_variation_percent']:.1f}%
- **Rhythm Regularity:** {features['tempo_rhythm']['rhythm_regularity_score']:.0%}
- **Note Density:** {features['tempo_rhythm']['notes_per_second']:.1f} notes/second

### Pitch & Intonation
- **Estimated Key:** {features['pitch_intonation']['estimated_key']} (confidence: {features['pitch_intonation']['key_confidence']:.0%})
- **Pitch Stability:** {features['pitch_intonation']['pitch_stability_score']:.0%}
- **Pitch Range:** {features['pitch_intonation']['pitch_range_semitones']:.1f} semitones
- **Harmonic Content:** {features['pitch_intonation']['harmonic_content_ratio']:.0%}

### Dynamics
- **Dynamic Range:** {features['dynamics']['dynamic_range_db']:.1f} dB ({features['dynamics']['dynamic_range_category']})
- **Dynamic Contrast:** {features['dynamics']['dynamic_contrast_score']:.0%}
- **Expressiveness:** {features['dynamics']['dynamic_expressiveness']}
- **Crescendo Presence:** {features['dynamics']['crescendo_presence']:.0%}
- **Decrescendo Presence:** {features['dynamics']['decrescendo_presence']:.0%}

### Tone Quality
- **Brightness:** {features['tone_quality']['brightness_score']:.0%}
- **Warmth:** {features['tone_quality']['tone_warmth']:.0%}
- **Brightness Consistency:** {features['tone_quality']['brightness_consistency']:.0%}
- **Timbre Consistency:** {features['tone_quality']['timbre_consistency']:.0%}
- **Tone Character:** {features['tone_quality']['tonal_vs_noisy']}

### Articulation
- **Attack Clarity:** {features['articulation']['attack_clarity_score']:.0%}
- **Note Separation Consistency:** {features['articulation']['note_separation_consistency']:.0%}
- **Predominant Articulation:** {features['articulation']['predominant_articulation']}
- **Staccato Tendency:** {features['articulation']['staccato_tendency']:.0%}
- **Legato Tendency:** {features['articulation']['legato_tendency']:.0%}

### Musical Structure
- **Estimated Sections:** {features['musical_structure']['estimated_sections']}
- **Musical Development:** {features['musical_structure']['musical_development_score']:.0%}

### Overall Performance Scores
- **Technical Proficiency:** {features['performance_scores']['technical_proficiency']:.0%}
- **Expressiveness:** {features['performance_scores']['expressiveness']:.0%}
- **Overall Score:** {features['performance_scores']['overall_score']:.0%}
- **Difficulty Estimate:** {features['performance_scores']['difficulty_estimate']}
- **Performance Level:** {features['performance_scores']['performance_level']}

---

Based on these actual audio analysis metrics, provide comprehensive RIAM-standard coaching feedback. Your feedback should:

## 1. Overall Performance Assessment
Provide an honest, constructive assessment based on the metrics. What does the data reveal about this student's playing?

## 2. Technical Analysis

### Rhythm & Tempo
- Interpret the tempo stability ({features['tempo_rhythm']['tempo_stability_score']:.0%}) and rhythm regularity ({features['tempo_rhythm']['rhythm_regularity_score']:.0%})
- What do these scores indicate about rhythmic control?
- Specific exercises to improve rhythm if scores are below 70%

### Intonation & Pitch Control
- Interpret the pitch stability ({features['pitch_intonation']['pitch_stability_score']:.0%})
- What does the harmonic content ({features['pitch_intonation']['harmonic_content_ratio']:.0%}) suggest about tone production?
- Suggestions for improving intonation if needed

### Tone Quality
- Interpret brightness ({features['tone_quality']['brightness_score']:.0%}) and warmth ({features['tone_quality']['tone_warmth']:.0%})
- Comment on timbre consistency ({features['tone_quality']['timbre_consistency']:.0%})
- Exercises for tone development if scores are below 70%

### Articulation
- Interpret the articulation patterns (attack clarity: {features['articulation']['attack_clarity_score']:.0%})
- Comment on the {features['articulation']['predominant_articulation']} tendency
- How to develop more varied articulation

## 3. Musical Expression
- Interpret dynamic control (range: {features['dynamics']['dynamic_range_db']:.1f} dB, contrast: {features['dynamics']['dynamic_contrast_score']:.0%})
- Comment on expressiveness level: {features['dynamics']['dynamic_expressiveness']}
- Suggestions for developing greater musical expression

## 4. Strengths to Build On
List 3-4 specific strengths evident from the highest scores in the analysis.

## 5. Priority Areas for Improvement
List 3-4 specific areas needing attention based on the lowest scores.

## 6. Practice Plan (2-4 weeks)
Create a structured practice plan targeting the weakest areas:
- **Weeks 1-2:** Focus areas and specific exercises
- **Weeks 3-4:** Integration and refinement
- Include daily practice routine (30-60 min breakdown)

## 7. Recommended Repertoire for Development
Based on performance level ({features['performance_scores']['performance_level']}) and weak areas, suggest:
- 2-3 études or technical studies addressing weak areas
- 2-3 pieces at appropriate level
- Explain WHY each recommendation would help

## 8. Technical Exercises
Provide 3-5 specific exercises with detailed instructions targeting:
- Rhythm (if tempo stability < 70%)
- Intonation (if pitch stability < 70%)
- Dynamics (if dynamic contrast < 50%)
- Articulation variety
- Tone development

## 9. Encouragement & Next Steps
End with specific encouragement based on strengths observed, and clear next steps.

---

**Important:** 
- Reference the actual metrics in your feedback
- Be specific and practical
- Adjust tone to match performance level: {features['performance_scores']['performance_level']}
- If piece/composer provided, incorporate piece-specific advice
"""

        # Call Claude
        print("🤖 Generating coaching feedback with Claude...")
        
        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={
                "maxTokens": 6000,
                "temperature": 0.7,
            }
        )
        
        return response['output']['message']['content'][0]['text']
    
    def _provide_text_only_feedback(
        self,
        file_size_mb: float,
        audio_format: str,
        piece_name: Optional[str],
        composer: Optional[str],
        student_notes: Optional[str]
    ) -> dict:
        """Fallback to text-only feedback if audio analysis fails."""
        
        if not piece_name and not composer:
            return {
                "success": True,
                "feedback": f"""# RIAM AI Music Coach

Thank you for uploading your {file_size_mb:.1f}MB {audio_format} recording!

Unfortunately, I couldn't analyze your audio file. To provide feedback, please include:

## Required Information:
- **Piece Name** - What are you playing?
- **Composer** - Who wrote it?

## Optional:
- **Your Level** - RIAM Grade level
- **Specific Questions** - Techniques you're working on?

Re-submit with this information for comprehensive coaching feedback!
""",
                "model": self.model_id
            }
        
        # Build context and provide text-based feedback
        context = []
        if piece_name:
            context.append(f"Piece: {piece_name}")
        if composer:
            context.append(f"Composer: {composer}")
        if student_notes:
            context.append(f"Student notes: {student_notes}")
        
        prompt = f"""You are a master music teacher at RIAM. A student submitted a recording but audio analysis failed.

Context provided:
{chr(10).join(context)}

Provide comprehensive coaching feedback for this piece including:
1. Historical context and significance
2. Key technical challenges
3. Interpretive guidance
4. Practice plan (2-4 weeks)
5. Recommended recordings
6. Exercises for common challenges
7. Encouragement

Be specific to the piece mentioned."""

        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 4000, "temperature": 0.7}
        )
        
        return {
            "success": True,
            "feedback": response['output']['message']['content'][0]['text'],
            "model": self.model_id,
            "note": "Audio analysis unavailable - feedback based on piece information only"
        }


# Singleton instance
bedrock_service = BedrockService()
