gcloud dataproc jobs submit pyspark \
    --cluster cluster-cloudmark --region global \
    gs://ufcloudcomputing/cloudComputingProject/spark_tf_hub_delf.py

gcloud dataproc jobs submit pyspark \
    --cluster cluster-cloudmark --region global \
    gs://ufcloudcomputing/cloudComputingProject/tf_hub_delf_module.py

# Set up Jupiter notebook in local
1. In GOOGLE cloud shell
export PROJECT=bigdataass;export HOSTNAME=cluster-cloudmark-m;export ZONE=us-east1-b
export PORT1=8080;export PORT2=8084;

gcloud compute ssh ${HOSTNAME} \
    --project=${PROJECT} --zone=${ZONE}  -- \
    -4 -N -L ${PORT1}:${HOSTNAME}:${PORT2}

source:
> https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook