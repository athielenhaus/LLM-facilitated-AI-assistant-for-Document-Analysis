# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /AccChatBot

# Copy the current directory contents into the container at /AccChatBot
COPY . /AccChatBot

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8501 available to the world outside this container (Streamlit default port)
EXPOSE 8501

# Run the specified command when the container launches
CMD ["python", "-m", "streamlit", "run", "acc_checkerUI.py"]
