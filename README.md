# ApexSports Basketball Shot Analyzer

An advanced AI-powered basketball shot analysis system using computer vision and machine learning to provide real-time feedback on shooting form and technique.

## Features

- **Real-time Pose Detection**: Uses MediaPipe for accurate body pose estimation
- **Comprehensive Shot Analysis**: Analyzes release angle, form, balance, and consistency
- **Performance Tracking**: Stores and tracks shooting performance over time
- **Interactive Visualizations**: Detailed charts and graphs for progress monitoring
- **Session Management**: Organize training sessions and track improvement
- **Coaching Recommendations**: AI-powered tips for form improvement

## Installation

1. Clone or download this repository
2. Install Python 3.8 or higher
3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (usually `http://localhost:8501`)

3. Create a new training session or select an existing one

4. Upload a video file or image of your basketball shot

5. View real-time analysis results and coaching recommendations

## Requirements

- Python 3.8+
- Webcam (for live analysis) or video files
- Minimum 4GB RAM recommended
- Good lighting conditions for optimal pose detection

## Technology Stack

- **Streamlit**: Web application framework
- **MediaPipe**: Pose estimation and hand tracking
- **OpenCV**: Computer vision and video processing
- **TensorFlow**: Machine learning capabilities
- **Plotly**: Interactive visualizations
- **SQLite**: Local database for session storage

## File Structure

```
ApexSports-grok/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .github/
│   └── copilot-instructions.md
└── shot_analysis.db      # SQLite database (created on first run)
```

## Features Overview

### Shot Analysis Metrics
- Release angle and height
- Follow-through analysis
- Elbow alignment
- Knee bend evaluation
- Balance scoring
- Overall form consistency

### Performance Dashboard
- Session statistics
- Progress tracking over time
- Detailed shot breakdowns
- Performance trends

### Data Management
- Session creation and management
- CSV export functionality
- Historical data storage

## Troubleshooting

**Camera not working**: Ensure your webcam is properly connected and not being used by other applications.

**Poor pose detection**: Make sure you have good lighting and the full body is visible in the frame.

**Installation issues**: Try updating pip and installing packages one by one if batch installation fails.

## Support

For technical support or feature requests, please create an issue in this repository.

## License

This project is for educational and personal use. Commercial use requires proper licensing of included libraries.
