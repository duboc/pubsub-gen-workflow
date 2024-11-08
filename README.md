# PubSub Simulator with Gemini 1.5 Flash

A Streamlit application that demonstrates integration between Google Cloud PubSub and Vertex AI's Gemini 1.5 Flash model. This application allows users to publish messages to PubSub, process them with Gemini 1.5 Flash, and view the responses.

## Prerequisites

- Python 3.8+
- Google Cloud Platform account with billing enabled
- Vertex AI API enabled
- PubSub API enabled
- Google Cloud CLI installed

## Setup

1. First, set up your Google Cloud project and create the necessary PubSub resources:

```bash
# Set project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Create topic
gcloud pubsub topics create demo-topic

# Create pull subscription
gcloud pubsub subscriptions create demo-sub \
    --topic=projects/$PROJECT_ID/topics/demo-topic \
    --ack-deadline=60 \
    --message-retention-duration=1d \
    --expiration-period=never

# Verify the linkage
gcloud pubsub topics list-subscriptions demo-topic
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
streamlit
google-cloud-pubsub
google-cloud-aiplatform
vertexai
python-dotenv
```

## Configuration

1. Create a `.env` file in the project root with your Google Cloud credentials:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
```

2. Make sure you have the necessary service account credentials with permissions for:
   - PubSub Publisher/Subscriber
   - Vertex AI Model User

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Features

- **Message Publishing**: Publish messages to a specified PubSub topic
- **Message Processing**: Process received messages using Gemini 1.5 Flash model
- **Response Publishing**: Publish model responses back to PubSub
- **Message History**: View history of published messages and model responses
- **Configuration**: Easy configuration of project ID, topic, and subscription through the sidebar

## Application Structure

- `app.py`: Main Streamlit application file
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not tracked in git)

## Main Functions

- `publish_message()`: Publishes messages to PubSub topic
- `receive_message()`: Receives messages from PubSub subscription
- `process_with_vertex()`: Processes messages using Gemini 1.5 Flash
- `main()`: Main Streamlit application logic

## Configuration Options

In the Streamlit sidebar, you can configure:
- Project ID
- Topic ID
- Subscription ID
- Vertex AI Location

## Error Handling

The application includes error handling for:
- PubSub publishing/receiving errors
- Vertex AI processing errors
- Configuration errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
