# base image
FROM amazonlinux:1

# Set the working directory to /news-crawler
WORKDIR /news-crawler

# Copy the current directory contents into the container at /news-crawler
COPY . /news-crawler

# Install any needed packages specified in requirements.txt
RUN yum install -y python36 python36-pip python36-devel.x86_64 mysql mysql-devel mysql-libs glibc-devel gcc gcc-c++ nano postgresql-devel git screen && \
    pip-3.6 install --upgrade pip && \
    pip install  -r requirements.txt && \
    pip install --upgrade awscli

# Define environment variable
ENV PYTHONPATH "${PYTHONPATH}:/news_crawler"

# Run run.sh when the container launches
ENTRYPOINT ["/run.sh"]

