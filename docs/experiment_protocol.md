# Experiment Protocol

This document describes the complete experimental setup and procedures used to collect the VertexPursuit-SoftHard-Dataset.

## Overview

Vertex Pursuit is a gamified motor skill assessment task designed to evaluate fundamental skills relevant to surgical training. Participants trace a star pentagon pattern while managing a secondary task, creating a dual-task paradigm that tests multiple cognitive and motor abilities.

## Hardware Setup

- **Computer**: Windows laptop with 15.6-inch screen
- **Input Device**: 3000 DPI gaming mouse
- **Display**: Full-screen mode (1920×1080 resolution)
- **Active Area**: 1000×1000 pixel square centered on screen

## Software Implementation

- **Language**: Python 3.10.14
- **Framework**: Pygame
- **Sampling Rate**: 200ms (5 Hz)
- **Data Format**: CSV files with timestamp, coordinates, and events

## Task Description

### Primary Task: Star Pentagon Tracing
1. Participants start at a designated circle
2. Press 'S' key to begin
3. Follow the star pentagon pattern clockwise
4. Blue arrows indicate direction and proximity to vertices
5. Complete the pattern and return to start

### Secondary Task: Space Bar Management
- Press space bar when within 1cm of corner vertices
- Release after passing the vertex
- Do not press during transitions to/from start circle

### Performance Constraints
- Inward deviations (toward center) penalized more than outward
- No time limit, but completion time recorded
- Participants encouraged to prioritize accuracy over speed

## Participant Information

- **Sample Size**: 24 participants
- **Demographics**: Mixed age groups, genders, and dominant hands
- **Trials**: 5 trials per participant
- **Rest Period**: 30 seconds between trials
- **Training**: Brief familiarization before data collection

## Evaluator Selection and Training

### Selection Criteria
- Consistent performance across trials
- Clear understanding of both tasks
- Good completion times and accuracy

### Training Protocol (10 minutes)
1. Explanation of assessment criteria
2. Demonstration of benchmark performances:
   - Poor performance examples
   - Intermediate performance examples
   - Excellent performance examples
3. Practice evaluation session
4. Discussion of additional performance indicators

## Data Collection Procedure

1. **Setup Phase**
   - Participant seated comfortably
   - Screen positioned at eye level
   - Mouse sensitivity adjusted if needed

2. **Familiarization**
   - Explanation of tasks
   - Practice run (not recorded)
   - Questions answered

3. **Data Collection**
   - 5 consecutive trials
   - 30-second rest between trials
   - Continuous recording of mouse position and events

4. **Quality Assurance**
   - Real-time monitoring for technical issues
   - Post-trial data validation
   - Backup of raw data files

## Segmentation Strategy

Each trial divided into 5 sub-trials based on:
- Geometric segments of the star pattern
- Space bar press/release events
- Natural breakpoints for evaluation

## Assessment Methodology

### Quantitative Metrics
- Completion time
- Path length (absolute and relative)
- Velocity statistics
- Weighted RMSE (inward errors weighted 2x)
- Jerk and smoothness measures

### Qualitative Assessment
- Two independent evaluators per sub-trial
- Third evaluator for disagreements
- Free-text descriptions of performance
- Structured feedback on specific aspects

## Ethical Considerations

- Informed consent obtained from all participants
- No personally identifiable information collected
- Voluntary participation with right to withdraw
- Data anonymized before publication

