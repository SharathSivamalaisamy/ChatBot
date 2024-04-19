# Use the official Python base image
FROM python:3.9
 
ENV HTTP_PROXY=http://proxy-in.its.hpecorp.net:443
ENV HTTPS_PROXY=http://proxy-in.its.hpecorp.net:443
ENV http_proxy=http://proxy-in.its.hpecorp.net:443
ENV https_proxy=http://proxy-in.its.hpecorp.net:443
# Set the working directory in the container
WORKDIR /app
 
# Copy the current directory contents into the container at /app
COPY . /app
 
# Install Flask and other dependencies
RUN pip install flask requests beautifulsoup4 scikit-learn numpy flask-cors
 
# Expose the port the app runs on
EXPOSE 8080
 
# Command to run the Flask app
CMD ["python3", "try.py"]