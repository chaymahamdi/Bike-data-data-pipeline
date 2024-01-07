# Streaming-bike_stations-project

Welcome to our Big Data Streaming project! In this project, we utilize various technologies like Kafka, Spark, Elasticsearch, Hive, and Kibana to build a real-time streaming pipeline for bike stations data using the JCDecaux streaming API. Follow the steps below to set up and run the workflow.

## Prerequisites

Before getting started, make sure you have the following technologies installed in the specified order:

1. **Kafka 3.6.0:** Kafka is a distributed, scalable, and fault-tolerant Publish-Subscribe messaging system.

2. **Spark 3.2.4:** Spark provides tools like Kafka Streams, Spark Streaming, or Apache Flink, specializing in the processing of streaming data.

3. **Elasticsearch 8.8.2:** Elasticsearch is used as a NoSQL database to store streaming data.

4. **Kibana 8.2.2:** Kibana is employed for visualizing the data stored in Elasticsearch.

## Steps

### First Workflow: Kafka - Producer and Consumer

1. Start the ZooKeeper service:

   ```bash
   $ bin/zookeeper-server-start.sh config/zookeeper.properties
2. Start the Kafka broker service:
   
   ```bash
   $ bin/kafka-server-start.sh config/server.properties
3. Restart Elasticsearch and check status:
   ```bash
   $ sudo systemctl restart elasticsearch
   $ sudo systemctl status elasticsearch
4. Restart Kibana and check status:
   ```bash
   $ sudo systemctl restart kibana
   $ sudo systemctl status kibana:
6. Start the Kafka producer and consumer:
   ```bash
   $ python3 producer.py   # Start the Kafka producer
   $ python3 consumer_elastic_kibana.py   # Start the consumer for Elasticsearch and Kibana
   $ ./command.sh   # Start the Kafka consumer
8. Check if data is storing in the Elasticsearch index "stations":
   Go to the Kibana sidebar.
   Click on "Index Management" to check if data is storing in the Elasticsearch index "stations".



