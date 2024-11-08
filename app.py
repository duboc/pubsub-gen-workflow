import streamlit as st
from google.cloud import pubsub_v1
from google.cloud import aiplatform
import json
import time
from datetime import datetime
from vertexai.generative_models import GenerationConfig, GenerativeModel
import vertexai

# Initialize Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'vertex_responses' not in st.session_state:
    st.session_state.vertex_responses = []

def publish_message(project_id, topic_id, message):
    """Publishes a message to PubSub topic"""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    message_json = json.dumps({
        'message': message,
        'timestamp': datetime.now().isoformat()
    })
    
    future = publisher.publish(topic_path, message_json.encode('utf-8'))
    message_id = future.result()
    return message_id

def receive_message(project_id, subscription_id):
    """Receives a message from PubSub subscription"""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )
    
    if len(response.received_messages) > 0:
        message = response.received_messages[0]
        # Acknowledge the message
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [message.ack_id],
            }
        )
        return json.loads(message.message.data.decode('utf-8'))
    return None

def process_with_vertex(project_id, location, message):
    """Processes message with Gemini 1.5 Flash"""
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    
    # Load Gemini model
    model = GenerativeModel("gemini-1.5-flash-002")
    
    # Generate response
    response = model.generate_content(
        message,
        generation_config=GenerationConfig(
            temperature=0.7,
            max_output_tokens=256,
            top_p=0.8,
            top_k=40
        )
    )
    
    return response.text

def main():
    st.title("PubSub Simulator with Gemini 1.5 Flash")
    
    # Configuration section
    st.sidebar.header("Configuration")
    project_id = st.sidebar.text_input("Project ID", "your-project-id")
    topic_id = st.sidebar.text_input("Topic ID", "your-topic-id")
    subscription_id = st.sidebar.text_input("Subscription ID", "your-subscription-id")
    vertex_location = st.sidebar.text_input("Vertex AI Location", "us-central1")
    
    # Publisher section
    st.header("Message Publisher")
    message_input = st.text_input("Enter message to publish:")
    if st.button("Publish Message"):
        try:
            message_id = publish_message(project_id, topic_id, message_input)
            st.session_state.messages.append({
                'message': message_input,
                'id': message_id,
                'timestamp': datetime.now().isoformat()
            })
            st.success(f"Message published successfully! ID: {message_id}")
        except Exception as e:
            st.error(f"Error publishing message: {str(e)}")
    
    # Subscriber section
    st.header("Message Subscriber")
    if st.button("Receive and Process with Flash-002"):
        try:
            received_message = receive_message(project_id, subscription_id)
            if received_message:
                # Process with Vertex AI
                vertex_response = process_with_vertex(
                    project_id, 
                    vertex_location,
                    received_message['message']
                )
                st.session_state.vertex_responses.append({
                    'input': received_message,
                    'response': vertex_response,
                    'timestamp': datetime.now().isoformat()
                })
                st.success("Message processed with Flash-002!")
            else:
                st.warning("No messages available to receive")
        except Exception as e:
            st.error(f"Error processing message: {str(e)}")
    
    # Publish back to PubSub
    if st.button("Publish Flash-002 Response to PubSub"):
        try:
            if st.session_state.vertex_responses:
                latest_response = st.session_state.vertex_responses[-1]
                response_message = json.dumps(latest_response)
                message_id = publish_message(project_id, topic_id, response_message)
                st.success(f"Flash-002 response published to PubSub! ID: {message_id}")
            else:
                st.warning("No Flash-002 responses available to publish")
        except Exception as e:
            st.error(f"Error publishing Flash-002 response: {str(e)}")
    
    # Display message history
    st.header("Message History")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Published Messages")
        for msg in st.session_state.messages:
            st.text_area(
                f"Message ID: {msg['id'][:8]}...",
                msg['message'],
                height=100,
                key=f"pub_{msg['id']}"
            )
    
    with col2:
        st.subheader("Flash-002 Responses")
        for resp in st.session_state.vertex_responses:
            st.text_area(
                f"Processed at {resp['timestamp']}",
                f"Input: {resp['input']['message']}\nResponse: {resp['response']}",
                height=100,
                key=f"vertex_{resp['timestamp']}"
            )

if __name__ == "__main__":
    main()