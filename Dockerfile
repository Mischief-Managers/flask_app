FROM python:3.10

# # Set the working directory within the container
# WORKDIR /api-flask

# # Copy the necessary files and directories into the container
# COPY resources/ static/ util/ .env application.py requirements.txt /api-flask/
# COPY resources/ /api-flask/resources/
# COPY static/ /api-flask/static/
# COPY util/ /api-flask/util/
# COPY .env application.py requirements.txt  /api-flask/

# # Upgrade pip and install Python dependencies
# RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# # Expose port 5000 for the Flask application
# EXPOSE 5000

# # Define the command to run the Flask application using Gunicorn
# CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]

WORKDIR /python-docker

COPY app.py app.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 4500

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]