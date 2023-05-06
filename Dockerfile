# Use an official Python runtime as a parent image
FROM python

# Install dependencies
RUN pip install certifi==2022.12.7 gevent==22.10.2 greenlet==2.0.2 python-dotenv==1.0.0 slack-bolt==1.18.0 slack-sdk==3.21.3 websocket==0.2.1 websocket-client==1.5.1 zope.event==4.6 zope.interface==6.0 openai==0.27.4 langchain==0.0.150 chromadb==0.3.21 hnswlib==0.7.0 tiktoken==0.3.3 

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "slack-app.py"]
