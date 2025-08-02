# Data Format Documentation

This document describes the structure and format of all data files in the VertexPursuit-SoftHard-Dataset.

## File Types Overview

### 1. Raw Trajectory Files (`SHSA_X_Y.csv`)

Located in `data/raw/trajectories/`, these files contain the raw mouse tracking data.

**Naming Convention**: `SHSA_[participant_id]_[trial_number].csv`
- `participant_id`: 1-24
- `trial_number`: 1-5

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| Timestamp | float | Time in seconds since trial start |
| X | int | Mouse X coordinate (0-1000 pixels) |
| Y | int | Mouse Y coordinate (0-1000 pixels) |
| Event | int | Space bar state (0=not pressed, 1=pressed) |

**Example**:
```csv
Timestamp,X,Y,Event
0.0,885,394,0
0.2,883,398,0
0.4,880,405,0
```

### 2. Soft Data File (`softData-v02.csv`)

Located in `data/raw/evaluations/`, contains human evaluator assessments.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| id | string | Sub-trial identifier (format: `P[participant]-T[trial]-S[subtrial]`) |
| text | string | Free-text evaluation from human assessor |
| label | int | Skill level classification (1=poor, 2=intermediate, 3=excellent) |

**Example**:
```csv
id,text,label
P1-T1-S1,"The participant shows smooth movement with minimal deviation...",3
P1-T1-S2,"Some hesitation observed near the vertex, trajectory slightly...",2
```

### 3. Master Dataset (`master_dataset.csv`)

Located in `data/processed/`, this is the primary file for analysis.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| id | string | Sub-trial identifier |
| text | string | Evaluator assessment |
| label | int | Skill classification |
| Subtrial | string (dict) | Serialized trajectory data |
| feature_vector | string (dict) | Pre-computed features (if available) |

**Subtrial Dictionary Structure**:
```python
{
    "Timestamp": {"0": 71.487, "1": 71.687, ...},
    "X": {"0": 521, "1": 520, ...},
    "Y": {"0": 187, "1": 189, ...},
    "Event": {"0": 0, "1": 0, ...}
}
```

## Coordinate System

- **Origin**: Top-left corner of the screen
- **Range**: 1000×1000 pixel area centered on screen
- **Reference trajectory**: Star pentagon with vertices at predefined coordinates

## Sub-trial Segmentation

Each trial is divided into 5 sub-trials based on the star pentagon geometry:
- **Sub-trial 1**: Start → Vertex 1
- **Sub-trial 2**: Vertex 1 → Vertex 2
- **Sub-trial 3**: Vertex 2 → Vertex 3
- **Sub-trial 4**: Vertex 3 → Vertex 4
- **Sub-trial 5**: Vertex 4 → Return to start

## Label Definitions

The skill level labels represent:
- **1 (Poor)**: Significant deviations, poor timing, inconsistent movement
- **2 (Intermediate)**: Some deviations, generally good timing, mostly smooth movement
- **3 (Excellent)**: Minimal deviations, precise timing, smooth and controlled movement

## Notes

- All timestamps are in seconds with 0.2-second sampling interval
- Evaluator text may contain subjective observations about movement quality, timing, and task understanding
- The space bar should be pressed near vertices (within ~1cm before/after)

