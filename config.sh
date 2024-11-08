# Set project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Create topic
gcloud pubsub topics create demo-topic

# Create pull subscription with explicit topic path
gcloud pubsub subscriptions create demo-sub \
    --topic=projects/conventodapenha/topics/demo-topic \
    --ack-deadline=60 \
    --message-retention-duration=1d \
    --expiration-period=never

# Verify the linkage
echo "Verifying topic-subscription linkage..."
gcloud pubsub topics list-subscriptions demo-topic