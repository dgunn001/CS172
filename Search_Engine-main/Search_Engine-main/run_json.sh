#!/bin/bash
curl -X POST -u elastic:4E3PF7tX973zTTP9EVlFIPCD "https://cs172fp.es.eastus2.azure.elastic-cloud.com:9243/index/_bulk" -H "Content-Type: application/x-ndjson" --data-binary @data.json